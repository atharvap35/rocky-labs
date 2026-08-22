# Architecture — Linux Learning Platform (MVP)

This document describes the MVP architecture for the filesystem vertical slice.

Components:
- Frontend: React SPA (not yet implemented) with `xterm.js` for web terminal and interactive diagrams.
- Backend: Python FastAPI (future) that orchestrates Vagrant/VirtualBox, exposes SSH proxy and validation endpoints.
- Labs: `labs/filesystem` contains a `Vagrantfile` and `provision.sh` for a Rocky Linux VM.
- Validators: Python scripts under `backend/validator` perform SSH-based checks to validate learner tasks.
- Scripts: PowerShell scripts under `scripts/` simplify install/start on Windows hosts.

Lab lifecycle:
1. `vagrant up` boots the Rocky Linux VM.
2. Provisioning script sets up lab files and a broken fstab for troubleshooting.
3. Learner connects via SSH (or future web terminal) to perform tasks.
4. Validator scripts SSH into the VM and run checks to determine task completion.
5. `vagrant snapshot` and `vagrant snapshot restore` will be used to reset labs.
