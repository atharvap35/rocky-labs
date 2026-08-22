# Architecture — Linux Learning Platform (MVP)

This document describes the MVP architecture for the filesystem vertical slice.

Components:
- Frontend: Static browser UI with `xterm.js` for the embedded web terminal and controls for status, validation, and snapshots.
- Backend: Python FastAPI app that orchestrates Vagrant/VirtualBox, exposes VM lifecycle, SSH proxy, lab info, snapshot, and validation endpoints.
- Labs: `labs/filesystem` contains a `Vagrantfile` and `provision.sh` for a Rocky Linux VM.
- Validators: Python scripts under `backend/validator` perform SSH-based checks to validate learner tasks.
- Scripts: PowerShell scripts under `scripts/` simplify install/start on Windows hosts.

Lab lifecycle:
1. `vagrant up` boots the Rocky Linux VM.
2. Provisioning script sets up lab files and a broken fstab for troubleshooting.
3. Learner connects via `vagrant ssh` or the embedded web terminal to perform tasks.
4. Validator scripts SSH into the VM and run checks to determine task completion.
5. Snapshot API controls save, restore, list, and delete operations for reset workflows.
