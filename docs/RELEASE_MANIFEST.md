Release manifest
================

File: release.zip
Generated: 2026-08-23

SHA256: 2EBAE6EEC2D2DF2248632384E4F21C8351203C94D424F2FD35C242777EAE5A91
Size (bytes): 46702

Included: repository files minus local VM state and secrets.
Excludes: `.vagrant`, `.env`, `.venv`, `node_modules` (if present), and other local artifacts.

Notes
-----
- Use `scripts/package_release.ps1` to reproduce the package locally.
- The package is intended for distribution and does not include Vagrant boxes or VM disk images.
- See `docs/RELEASE_NOTES.md` for changelog and release highlights.
