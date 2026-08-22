try:
    import paramiko
except ImportError:
    paramiko = None
import time
import json
import os


def load_config():
    # prefer env overrides
    host = os.getenv('LAB_FILESYSTEM_HOST')
    user = os.getenv('LAB_FILESYSTEM_USER')
    password = os.getenv('LAB_FILESYSTEM_PASSWORD')
    ssh_key = os.getenv('LAB_FILESYSTEM_SSH_KEY_PATH')
    if host or user or password:
        return { 'host': host or '192.168.56.101', 'user': user or 'learner', 'password': password or 'learner', 'ssh_key_path': ssh_key }

    root = os.path.dirname(os.path.dirname(__file__))
    cfg_path = os.path.join(root, 'labs', 'filesystem', 'config.json')
    if not os.path.exists(cfg_path):
        return {"host": "192.168.56.101", "user": "learner", "password": "learner"}
    with open(cfg_path, 'r') as f:
        return json.load(f)


def run_cmd(cmd):
    cfg = load_config()
    HOST = cfg.get('host')
    USER = cfg.get('user')
    PASS = cfg.get('password')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # prefer key-based auth if provided
    key_path = cfg.get('ssh_key_path')
    try:
        if key_path and os.path.exists(key_path):
            pkey = paramiko.RSAKey.from_private_key_file(key_path)
            ssh.connect(HOST, username=USER, pkey=pkey)
        elif PASS:
            ssh.connect(HOST, username=USER, password=PASS)
        else:
            # fallback to attempt without auth (rare)
            ssh.connect(HOST, username=USER)
    except Exception:
        # rethrow to caller
        raise
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    ssh.close()
    return out, err


def check_readme():
    out, err = run_cmd('test -f /opt/rlp-labs/filesystem/README.txt && echo OK || echo MISSING')
    return out.strip() == 'OK'


def check_readme_owner():
    out, err = run_cmd("stat -c '%U %a' /opt/rlp-labs/filesystem/README.txt")
    if err:
        raise Exception(err)
    parts = out.strip().split()
    if len(parts) != 2:
        return False
    owner, perms = parts
    return owner == 'learner' and perms.startswith('6')


def check_readme_perms():
    out, err = run_cmd("stat -c '%a' /opt/rlp-labs/filesystem/README.txt")
    if err:
        raise Exception(err)
    perms = out.strip()
    return perms == '644'


def check_broken_fstab():
    out, err = run_cmd("grep -q 'UUID=0000-0000' /etc/fstab && echo FOUND || echo MISSING")
    return out.strip() == 'FOUND'


def check_fstab_contains_broken_mount():
    out, err = run_cmd("grep -q '/mnt/broken' /etc/fstab && echo FOUND || echo MISSING")
    return out.strip() == 'FOUND'


def check_broken_mount_unmounted():
    out, err = run_cmd("mountpoint -q /mnt/broken && echo MOUNTED || echo UNMOUNTED")
    return out.strip() == 'UNMOUNTED'


def check_selinux_enforcing():
    out, err = run_cmd('getenforce')
    if err:
        raise Exception(err)
    state = out.strip()
    return state in ('Enforcing', 'Permissive')


def check_selinux_context_for_readme():
    out, err = run_cmd('ls -Z /opt/rlp-labs/filesystem/README.txt')
    if err:
        raise Exception(err)
    parts = out.strip().split()
    return len(parts) >= 2 and ':' in parts[0]



def check_recursive_owner():
    # ensure no files under the lab dir are owned by other users
    out, err = run_cmd("find /opt/rlp-labs/filesystem ! -user learner -print -quit || true")
    if err:
        # some systems may print warnings; ignore unless command failed
        pass
    return out.strip() == ''


def run_all_checks():
    results = {}
    # remediation hints for common failures
    hints = {
        'readme_present': "Create the README and set ownership: sudo mkdir -p /opt/rlp-labs/filesystem && sudo touch /opt/rlp-labs/filesystem/README.txt && sudo chown learner:learner /opt/rlp-labs/filesystem/README.txt",
        'readme_owner_ok': "Set owner to learner: sudo chown learner:learner /opt/rlp-labs/filesystem/README.txt",
        'readme_perms_ok': "Set permissions to 644: sudo chmod 644 /opt/rlp-labs/filesystem/README.txt",
        'broken_fstab_present': "Restore /etc/fstab to a valid state or remove the invalid UUID line: edit /etc/fstab as root and remove the UUID=0000-0000 line",
        'fstab_broken_entry': "Remove or fix the /mnt/broken entry in /etc/fstab so it does not reference a non-existent device",
        'broken_mount_unmounted': "If /mnt/broken is mounted, unmount it: sudo umount /mnt/broken",
        'selinux_enforcing_or_permissive': "Enable or set SELinux to Enforcing/Permissive: sudo setenforce 1 (temporary) and update /etc/selinux/config for persistence",
        'readme_selinux_context': "Restore SELinux context for the README: sudo restorecon -v /opt/rlp-labs/filesystem/README.txt",
        'recursive_owner_ok': "Recursively set ownership to learner: sudo chown -R learner:learner /opt/rlp-labs/filesystem",
    }

    try:
        results['readme_present'] = check_readme()
    except Exception as e:
        results['readme_present'] = False
        results['readme_error'] = str(e)

    try:
        results['readme_owner_ok'] = check_readme_owner()
    except Exception as e:
        results['readme_owner_ok'] = False
        results['readme_owner_error'] = str(e)

    try:
        results['readme_perms_ok'] = check_readme_perms()
    except Exception as e:
        results['readme_perms_ok'] = False
        results['readme_perms_error'] = str(e)

    try:
        results['broken_fstab_present'] = check_broken_fstab()
    except Exception as e:
        results['broken_fstab_present'] = False
        results['fstab_error'] = str(e)

    try:
        results['fstab_broken_entry'] = check_fstab_contains_broken_mount()
    except Exception as e:
        results['fstab_broken_entry'] = False
        results['fstab_broken_entry_error'] = str(e)

    try:
        results['broken_mount_unmounted'] = check_broken_mount_unmounted()
    except Exception as e:
        results['broken_mount_unmounted'] = False
        results['broken_mount_unmounted_error'] = str(e)

    try:
        results['selinux_enforcing_or_permissive'] = check_selinux_enforcing()
    except Exception as e:
        results['selinux_enforcing_or_permissive'] = False
        results['selinux_error'] = str(e)

    try:
        results['readme_selinux_context'] = check_selinux_context_for_readme()
    except Exception as e:
        results['readme_selinux_context'] = False
        results['readme_selinux_error'] = str(e)

    try:
        results['recursive_owner_ok'] = check_recursive_owner()
    except Exception as e:
        results['recursive_owner_ok'] = False
        results['recursive_owner_error'] = str(e)

    # attach hints for any failing checks
    results['hints'] = {}
    for k, hint in hints.items():
        if k in results and not results.get(k):
            results['hints'][k] = hint

    # all_pass indicates all validator expectations for the lab are satisfied
    results['all_pass'] = all([
        results.get('readme_present', False),
        results.get('broken_fstab_present', False),
        results.get('readme_owner_ok', False),
        results.get('readme_perms_ok', False),
        results.get('selinux_enforcing_or_permissive', False),
        results.get('readme_selinux_context', False),
        results.get('recursive_owner_ok', False),
    ])
    return results


if __name__ == '__main__':
    res = run_all_checks()
    print(json.dumps(res))
    if res.get('all_pass'):
        exit(0)
    else:
        exit(2)
