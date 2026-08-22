# Rocky Labs

Rocky Labs is an interactive Linux learning platform for RHCSA EX200 and Linux DevOps/SRE practice. The current release is a Windows-hosted MVP for a filesystem lab running inside a Rocky Linux virtual machine.

The lab VM is isolated from the Windows host. Learner commands run inside the Rocky Linux guest through Vagrant SSH or the browser terminal. Do not run untrusted or destructive commands in a host PowerShell window.

## What is included

- Rocky Linux 8 lab VM managed by Vagrant and VirtualBox
- Filesystem lab provisioner with a learner account and intentionally broken lab state
- FastAPI backend for VM status, startup, validation, snapshots, and terminal proxying
- Browser UI with an embedded xterm.js terminal
- SSH-based validator for README ownership and permissions, fstab persistence, mount state, SELinux, and recursive ownership
- Remediation hints for failed checks
- Pytest unit tests and GitHub Actions CI
- Windows PowerShell setup and run scripts

## Current MVP workflow

1. Install the Windows prerequisites.
2. Install Python dependencies.
3. Start the FastAPI backend.
4. Start the filesystem VM with Vagrant.
5. Open the browser UI.
6. Use the embedded terminal or `vagrant ssh` to complete the task.
7. Run the validator and use its hints to fix failed checks.
8. Save or restore a VirtualBox snapshot while experimenting.

## Requirements

- Windows 10 or 11
- Hardware virtualization enabled in BIOS/UEFI
- VirtualBox 6.x or 7.x
- Vagrant
- Git
- Python 3.8 or newer
- Network access on the first run so Vagrant can download the `rockylinux/8` box

Install VirtualBox from https://www.virtualbox.org/ and Vagrant from https://www.vagrantup.com/.

## Setup

From PowerShell:

```powershell
cd D:\RHCSA
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
.\scripts\install.ps1
```

If PowerShell blocks activation for the current process, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Copy the optional local configuration file before starting the backend:

```powershell
Copy-Item .env.example .env
```

The default VM uses host `192.168.56.101`, user `learner`, and password `learner`. Keep `.env` private. SSH key authentication is supported through `LAB_FILESYSTEM_SSH_KEY_PATH`; see `.env.example` for the setting.

## Run the lab

Start the backend in one PowerShell window:

```powershell
cd D:\RHCSA
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Start the VM in a second PowerShell window:

```powershell
cd D:\RHCSA\labs\filesystem
vagrant up
```

Open the UI at http://127.0.0.1:8000/static/index.html.

You can also connect directly to the guest:

```powershell
cd D:\RHCSA\labs\filesystem
vagrant ssh
```

The backend exposes these main operations:

- `GET /api/status` checks Vagrant status.
- `POST /api/start` starts the lab VM in the background.
- `POST /api/validate` runs the filesystem validator.
- `GET /api/lab/info` returns lab metadata.
- `GET /api/snapshot/list` lists snapshots.
- `POST /api/snapshot/save` saves a named snapshot.
- `POST /api/snapshot/restore` restores a named snapshot.
- `POST /api/snapshot/delete` deletes a named snapshot.
- WebSocket `/ws/terminal` proxies the learner shell using server-side configuration.

## Validate changes

Run the tests with the same Python interpreter used for the environment:

```powershell
cd D:\RHCSA
C:\Users\Hp\AppData\Local\Programs\Python\Python314\python.exe -m pytest -q backend/tests
```

For a real VM validation after `vagrant up`:

```powershell
python backend\validator\validate_filesystem.py
```

The validator returns structured JSON and exits with code `0` when all required checks pass, or code `2` when a check fails.

## Package a release

Create a distributable archive from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package_release.ps1 -Out .\release.zip
Get-FileHash .\release.zip -Algorithm SHA256
```

The package excludes VM state, virtual environments, Git metadata, caches, secrets, and other local-only content. See `docs/RELEASE_MANIFEST.md` and `docs/RELEASE_NOTES.md` for the current release details.

## Safety and credentials

- The platform is intended for local development on a Windows host.
- Run learner commands inside the Rocky Linux VM, not on Windows.
- Never commit `.env`, private keys, passwords, VM state, or box files.
- The browser does not receive SSH credentials; the backend reads them from environment variables or lab configuration.
- Use snapshots before experiments that may leave the guest in a difficult state.

## Project layout

```text
backend/                 FastAPI app and SSH validator
curriculum/              RHCSA and filesystem lesson material
docs/                    Architecture, setup, release, and integration notes
frontend/                Browser UI and embedded terminal
labs/filesystem/         Vagrant lab and Rocky Linux provisioner
scripts/                 Windows setup, startup, and packaging scripts
Vagrantfile              Root VM definition
requirements.txt         Python dependencies
```

## Troubleshooting

- `vagrant` or `VBoxManage` not found: install VirtualBox and Vagrant, then reopen PowerShell so PATH changes are loaded.
- `vagrant up` fails: confirm VirtualBox can start a 2 GB, 2 CPU VM and try `vagrant box add rockylinux/8` first.
- The UI cannot validate: confirm the VM is running and that `192.168.56.101` is reachable from Windows.
- SSH authentication fails: check `.env`, the learner credentials, and the optional SSH key path.
- `pytest` is not recognized: use `python -m pytest` after activating `.venv`.

## Documentation

- [Windows installation guide](docs/INSTALL-WINDOWS.md)
- [Integration checklist](docs/INTEGRATION_CHECKLIST.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Filesystem lesson](curriculum/filesystem/lesson.md)
- [Roadmap](docs/ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Release notes](docs/RELEASE_NOTES.md)

## License

See [LICENSE](LICENSE).
