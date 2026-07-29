# Changelog

All notable changes are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0-alpha] — 2026-07-29

### Added

- `models.json` — machine-readable model catalog
- `checksums.txt` — SHA-256 hashes for all release assets
- `scripts/download_models.py` — downloads model binaries; supports `HF_TOKEN` for gated models
- `scripts/generate_checksums.py` — hashes `downloads/` and writes `checksums.txt`
- `scripts/generate_manifest.py` — builds `models.json` from downloaded files
- `scripts/verify_models.py` — cross-validates manifest, checksums, and local files
- `.github/workflows/validate.yml` — CI: JSON validation, metadata checks, binary rejection guard
- Whisper Base, Small, Medium, Large v3 Turbo Q5 (speech recognition)
- Silero VAD (voice activity detection)
- IndicTrans2 Distilled 200M — Indic → English (translation)

---

[1.0.0-alpha]: https://github.com/i-ayushsingh/finch-models/releases/tag/v1.0.0-alpha
