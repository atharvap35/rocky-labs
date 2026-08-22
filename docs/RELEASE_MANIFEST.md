Release manifest
================

File: release.zip
Generated: 2026-08-23

SHA256: 305A278042DB871D70311B4A062A6EF7127F8704BE82B73059A560A04C8CE792
Size (bytes): 40405

Included: repository files minus local VM state and secrets.
Excludes: `.vagrant`, `.env`, `.venv`, `node_modules` (if present), and other local artifacts.

Notes
-----
- Use `scripts/package_release.ps1` to reproduce the package locally.
- The package is intended for distribution and does not include Vagrant boxes or VM disk images.
- See `docs/RELEASE_NOTES.md` for changelog and release highlights.
