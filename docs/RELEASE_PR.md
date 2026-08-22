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

Release steps (local)
---------------------
Run these locally, then create the GitHub release and attach `release.zip`.

```powershell
# create a branch
git checkout -b release/v0.1.0
# commit prepared changes
git add .
git commit -m "chore(release): v0.1.0 filesystem lab MVP"
# push branch
git push origin release/v0.1.0
# (optional) create tag locally
git tag -a v0.1.0 -m "v0.1.0 filesystem lab MVP"
git push origin --tags
```

Then create a release on GitHub using the draft notes in `docs/RELEASE_NOTES.md` and attach `release.zip` (sha256 in `docs/RELEASE_MANIFEST.md`).

Notes for reviewer
------------------
- CI runs unit tests only; VM integration must be validated locally.
- See `docs/INTEGRATION_CHECKLIST.md` for manual integration steps (vagrant, VirtualBox).
