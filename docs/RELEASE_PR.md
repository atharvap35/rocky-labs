Release PR Draft — v0.1.0
=========================

Title: v0.1.0 — Filesystem lab MVP

Description
-----------
This PR packages the MVP vertical slice of the RHCSA learning platform.

Key changes:
- Filesystem lab provisioning and broken fstab exercise
- FastAPI backend orchestration and SSH→WebSocket terminal proxy
- Validator improvements: ownership, permissions, fstab checks, SELinux context, recursive ownership
- Remediation hints surfaced in validator JSON and frontend UI
- Deterministic unit tests and CI workflow for unit tests
- Packaging script `scripts/package_release.ps1` and `docs/RELEASE_MANIFEST.md`

Release status
--------------
The release is published at https://github.com/atharvap35/rocky-labs/releases/tag/v0.1.0.
The public repository is https://github.com/atharvap35/rocky-labs.

The release asset is `release.zip`; its checksum and size are recorded in `docs/RELEASE_MANIFEST.md`.

Reproduction steps (local)
--------------------------
Run these commands when preparing a future release:

```powershell
# build the package from the repository root
powershell -ExecutionPolicy Bypass -File .\scripts\package_release.ps1 -Out .\release.zip
# inspect the package checksum
Get-FileHash .\release.zip -Algorithm SHA256
```

Create a new tag and release only after running the tests and the VM integration checklist.

Notes for reviewer
------------------
- CI runs unit tests only; VM integration must be validated locally.
- See `docs/INTEGRATION_CHECKLIST.md` for manual integration steps (vagrant, VirtualBox).
