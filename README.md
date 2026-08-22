# Linux Learning Platform — MVP

This repository is a work-in-progress interactive Linux learning platform focused on RHCSA EX200 and DevOps/SRE Linux fundamentals.

This MVP implements a vertical slice for the "Filesystem" module using a local VirtualBox VM managed by Vagrant (Rocky Linux).

Quick start (Windows + PowerShell):

1. Install prerequisites (VirtualBox, Vagrant, Git).

2. From PowerShell run:

```powershell
.\scripts\install.ps1
.\scripts\start.ps1
```

Run the backend API (to control the lab from the web UI):

```powershell
.\scripts\run_backend.ps1
```

3. The `vagrant up` command will provision a Rocky Linux VM located in `labs/filesystem`.

4. To run the validator for the filesystem lesson:

```powershell
python .\backend\validator\validate_filesystem.py
```

See `docs/ARCHITECTURE.md` and `curriculum/` for design notes and next steps.

Release
-------

See `docs/RELEASE_NOTES.md` for the v0.1.0 MVP summary. Use `scripts\package_release.ps1` to create a zip of the repository for distribution (it excludes local VM state and `.env`).
