Release manifest
================

File: release.zip
Generated: 2026-08-23

SHA256: A2C8C23D43DA619871DF9D424A3838EC0EBE296225721EED12355A45F67919FB
Size (bytes): 45909577

Included: repository files minus local VM state and secrets.
Excludes: `.vagrant`, `.env`, `.venv`, `node_modules` (if present), and other local artifacts.

Notes
-----
- Use `scripts/package_release.ps1` to reproduce the package locally.
- The package is intended for distribution and does not include Vagrant boxes or VM disk images.
- See `docs/RELEASE_NOTES.md` for changelog and release highlights.
