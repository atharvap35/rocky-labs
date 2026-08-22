Release manifest
================

File: release.zip
Generated: 2026-08-23

SHA256: 4F88EF2625EC443E66BA35DFAAD7150A28C8631C21166B609B570362D1A3EF87
Size (bytes): 23210493

Included: repository files minus local VM state and secrets.
Excludes: `.vagrant`, `.env`, `.venv`, `node_modules` (if present), and other local artifacts.

Notes
-----
- Use `scripts/package_release.ps1` to reproduce the package locally.
- The package is intended for distribution and does not include Vagrant boxes or VM disk images.
- See `docs/RELEASE_NOTES.md` for changelog and release highlights.
