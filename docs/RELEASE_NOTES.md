Release v0.1.0 - MVP
=====================

Summary
-------

This release delivers the MVP vertical slice for the interactive Linux learning platform focused on RHCSA/EX200 topics. It includes a filesystem lab backed by a Rocky Linux VM (Vagrant + VirtualBox), automatic validation, snapshot controls, and an embedded SSH terminal.

Highlights
----------

- Lab: `labs/filesystem` — Rocky Linux VM provisioner and broken fstab exercise.
- Backend: `backend/app.py` — FastAPI orchestration, snapshot APIs, validator invocation, and SSH-to-WebSocket terminal proxy.
- Validator: `backend/validator/validate_filesystem.py` — SSH-based checks for README and fstab entries (env-driven config).
- Frontend: `frontend/index.html` — SPA with xterm.js terminal, snapshot UI, and validation controls.
- Security: Credentials are now loaded server-side via env vars (`LAB_FILESYSTEM_*`) or `labs/<lab>/config.json`. Frontend no longer sends credentials.
- CI: Basic unit-tests run by GitHub Actions to validate config-loading logic.

Known limitations
-----------------

- CI does not run Vagrant/VirtualBox steps — VM integration tests must be run locally.
- Curriculum content beyond the filesystem lesson is a work in progress.

Upgrade / Run
-------------

See `backend/README.md` for run instructions and `.env.example` for env var names.

Release artifacts
-----------------

- `release.zip`: packaged repository suitable for distribution (excludes local VM state and `.env`).

Changelog
---------

- 2026-08-22: Added structured validator JSON response and frontend rendering; expanded validator checks (ownership, perms, fstab/mount); added deterministic unit tests and test-run fixes.
 - 2026-08-22: Added remediation hints for failing validator checks (README, SELinux context, recursive ownership) surfaced to frontend; added SELinux and recursive ownership checks and associated unit tests.
