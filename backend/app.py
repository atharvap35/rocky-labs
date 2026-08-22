from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Body
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import threading
import os
import asyncio
import threading
import time
import paramiko
import json

app = FastAPI()

ROOT = os.path.dirname(os.path.dirname(__file__))
LAB_DIR = os.path.join(ROOT, 'labs', 'filesystem')

app.mount("/static", StaticFiles(directory=os.path.join(ROOT, 'frontend')), name="static")

# load .env from repo root if present
load_dotenv(os.path.join(ROOT, '.env'))


def load_lab_config(lab='filesystem'):
    # precedence: env vars LAB_<LAB>_HOST/USER/PASSWORD > labs/<lab>/config.json > defaults
    env_host = os.getenv(f'LAB_{lab.upper()}_HOST')
    env_user = os.getenv(f'LAB_{lab.upper()}_USER')
    env_pass = os.getenv(f'LAB_{lab.upper()}_PASSWORD')
    env_key = os.getenv(f'LAB_{lab.upper()}_SSH_KEY_PATH')
    if env_host or env_user or env_pass:
        return {
            'host': env_host or '192.168.56.101',
            'user': env_user or 'learner',
            'password': env_pass or 'learner',
            'ssh_key_path': env_key
        }

    cfg_path = os.path.join(ROOT, 'labs', lab, 'config.json')
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r') as f:
                return json.load(f)
        except Exception:
            pass

    return {'host': '192.168.56.101', 'user': 'learner', 'password': 'learner'}


class CmdResult(BaseModel):
    stdout: str
    stderr: str


def run_cmd(cmd, cwd=None):
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    return out.decode(), err.decode(), proc.returncode


@app.get("/api/status")
def status():
    out, err, code = run_cmd('vagrant status --machine-readable', cwd=LAB_DIR)
    if code != 0:
        raise HTTPException(status_code=500, detail=f"vagrant status failed: {err}")
    return {"status_raw": out}


@app.get('/api/lab/info')
def lab_info():
    cfg = load_lab_config('filesystem')
    # do not expose secrets; return non-sensitive info
    info = {
        'host': cfg.get('host'),
        'user': cfg.get('user'),
        'keyAuthConfigured': bool(cfg.get('ssh_key_path'))
    }
    return info


@app.post("/api/start")
def start():
    def background_up():
        run_cmd('vagrant up', cwd=LAB_DIR)

    thread = threading.Thread(target=background_up, daemon=True)
    thread.start()
    return {"started": True}


@app.post("/api/validate")
def validate():
    # Call the validator module directly so we return structured JSON
    try:
        from backend.validator import validate_filesystem as vf
        res = vf.run_all_checks()
        return res
    except Exception:
        # fallback to running as a subprocess for isolation
        validator = os.path.join(ROOT, 'backend', 'validator', 'validate_filesystem.py')
        out, err, code = run_cmd(f'python "{validator}"')
        # try to parse stdout as JSON
        try:
            parsed = json.loads(out) if out else {}
            return parsed
        except Exception:
            return CmdResult(stdout=out, stderr=err)


@app.websocket("/ws/terminal")
async def terminal_ws(websocket: WebSocket):
    await websocket.accept()
    # Do not accept credentials from the client. Use server-side lab config.
    cfg = load_lab_config('filesystem')
    host = cfg.get('host')
    user = cfg.get('user')
    password = cfg.get('password')

    loop = asyncio.get_running_loop()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Prefer key-based auth if configured
        ssh_key = cfg.get('ssh_key_path')
        if ssh_key and os.path.exists(ssh_key):
            pkey = paramiko.RSAKey.from_private_key_file(ssh_key)
            await asyncio.to_thread(ssh.connect, hostname=host, port=22, username=user, pkey=pkey, look_for_keys=False, allow_agent=False)
        else:
            await asyncio.to_thread(ssh.connect, hostname=host, port=22, username=user, password=password, look_for_keys=False, allow_agent=False)
        chan = await asyncio.to_thread(ssh.invoke_shell)
    except Exception as e:
        await websocket.send_text(f"ERROR: {e}")
        await websocket.close()
        return

    stop_event = threading.Event()

    def reader():
        try:
            while not stop_event.is_set():
                if chan.recv_ready():
                    data = chan.recv(1024)
                    if not data:
                        break
                    asyncio.run_coroutine_threadsafe(websocket.send_text(data.decode(errors='ignore')), loop)
                else:
                    time.sleep(0.05)
        except Exception as e:
            asyncio.run_coroutine_threadsafe(websocket.send_text(f"\n[reader error] {e}\n"), loop)
        finally:
            try:
                asyncio.run_coroutine_threadsafe(websocket.close(), loop)
            except Exception:
                pass

    reader_thread = threading.Thread(target=reader, daemon=True)
    reader_thread.start()

    try:
        while True:
            msg = await websocket.receive_text()
            if msg is None:
                break
            # write to remote shell
            await asyncio.to_thread(chan.send, msg)
    except WebSocketDisconnect:
        pass
    finally:
        stop_event.set()
        try:
            chan.close()
            ssh.close()
        except Exception:
            pass


def vagrant_snapshot_list():
    out, err, code = run_cmd('vagrant snapshot list', cwd=LAB_DIR)
    if code != 0:
        return None, err
    # vagrant prints 'Saved snapshots:
    #   name'
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    return lines, None


@app.post('/api/snapshot/save')
def snapshot_save(payload: dict = Body(...)):
    name = payload.get('name') if isinstance(payload, dict) else str(payload)
    out, err, code = run_cmd(f'vagrant snapshot save "{name}"', cwd=LAB_DIR)
    if code != 0:
        raise HTTPException(status_code=500, detail=err)
    return {"saved": True, "output": out}


@app.post('/api/snapshot/restore')
def snapshot_restore(payload: dict = Body(...)):
    name = payload.get('name') if isinstance(payload, dict) else str(payload)
    out, err, code = run_cmd(f'vagrant snapshot restore "{name}"', cwd=LAB_DIR)
    if code != 0:
        raise HTTPException(status_code=500, detail=err)
    return {"restored": True, "output": out}


@app.get('/api/snapshot/list')
def snapshot_list():
    snaps, err = vagrant_snapshot_list()
    if snaps is None:
        raise HTTPException(status_code=500, detail=err)
    return {"snapshots": snaps}


@app.post('/api/snapshot/delete')
def snapshot_delete(payload: dict = Body(...)):
    name = payload.get('name') if isinstance(payload, dict) else str(payload)
    out, err, code = run_cmd(f'vagrant snapshot delete "{name}"', cwd=LAB_DIR)
    if code != 0:
        raise HTTPException(status_code=500, detail=err)
    return {"deleted": True, "output": out}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
