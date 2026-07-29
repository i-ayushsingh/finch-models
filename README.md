<div align="center">
  <img src="Horizontal-logo.png" alt="Finch" width="280" />

  <h3>finch-models</h3>

  <p>Official downloadable AI models for Finch.</p>

  <p>
    <img src="https://img.shields.io/github/v/release/i-ayushsingh/finch-models?label=release&color=4f8ef7" alt="GitHub Release" />
    <img src="https://img.shields.io/badge/license-MIT-22c55e" alt="License: MIT" />
    <img src="https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white" alt="Platform: Windows" />
    <img src="https://img.shields.io/badge/status-alpha-f59e0b" alt="Status: Alpha" />
    <img src="https://img.shields.io/badge/binaries-GitHub_Releases-8b5cf6" alt="Distributed via GitHub Releases" />
  </p>
</div>

---

## Overview

This repository is the **official model registry** for [Finch](https://github.com/i-ayushsingh/finch). It does not ship code — it ships the metadata, checksums, and manifest that Finch uses to discover, download, and verify AI models at runtime.

**Key principles:**

- Model binaries are **never committed to Git** and are never stored in Git LFS.
- All binaries are distributed exclusively as **GitHub Release assets**.
- `models.json` is the machine-readable catalog Finch reads at startup.
- `checksums.txt` contains the SHA-256 hashes Finch uses to verify every downloaded file.
- Every field in `models.json` — including `sha256` and `size` — is generated from the actual downloaded binary, not filled in by hand.

---

## Supported Models

| Category | Model | Purpose | Recommended | Approx. Size |
|---|---|---|:---:|---:|
| Speech Recognition | Whisper Large v3 Turbo Q5 | High-quality, quantized transcription | | ~548 MB |
| Speech Recognition | Whisper Medium | High-accuracy transcription | | ~1.43 GB |
| Speech Recognition | Whisper Small | Balanced accuracy and speed | ✓ | ~465 MB |
| Speech Recognition | Whisper Base | Fast, lightweight transcription | | ~141 MB |
| Voice Activity Detection | Silero VAD | Detects speech vs. silence | ✓ | ~2.2 MB |
| Translation | IndicTrans2 Distilled 200M | Indic languages → English | ✓ | ~871 MB |

> Finch automatically selects the recommended model for each category on first launch. The user can switch models in settings.

---

## Repository Structure

```
finch-models/
├── models.json          # Machine-readable model catalog (SHA-256, size, metadata)
├── checksums.txt        # SHA-256 hashes for all release assets
├── Horizontal-logo.png  # Finch brand asset
├── LICENSE              # MIT License
├── CHANGELOG.md         # Version history
│
├── docs/
│   ├── models.md        # Detailed per-model documentation
│   └── releases.md      # Release process and checklist
│
├── scripts/
│   ├── download_models.py     # Downloads all model binaries from upstream sources
│   ├── generate_checksums.py  # Hashes downloaded files → checksums.txt
│   ├── generate_manifest.py   # Builds models.json from downloaded files
│   └── verify_models.py       # Cross-validates models.json, checksums.txt, and downloads/
│
└── downloads/           # Local staging area (git-ignored). Files here are uploaded
                         # to GitHub Releases manually — never committed to Git.
```

---

## How Finch Downloads Models

When Finch starts, it runs the following sequence for each required model:

1. **Manifest fetch** — Finch reads `models.json` from the GitHub Release to get the list of available models, their filenames, and expected SHA-256 hashes.
2. **Skip if cached** — If a local copy already exists and its SHA-256 matches, the model is used immediately without re-downloading.
3. **Download** — If the model is missing or its hash does not match, Finch downloads the binary from the corresponding GitHub Release asset.
4. **Verification** — The downloaded file is hashed and compared against both `models.json` and `checksums.txt`. A mismatch aborts the download and surfaces an error.
5. **Activation** — Once verified, the model file is moved into the application's model cache and made available to the inference engine.

> Models are never loaded from unverified paths. Every binary must pass SHA-256 verification before Finch will use it.

---

## Integrity Verification

All model files are verified using **SHA-256** checksums.

`checksums.txt` contains one entry per file:

```
# SHA256 filename
a9bff20ae94712db41c8dc99d2e381eb456ddccbcd48cb2c7cf077ccc5bc58d8 indictrans2-indic-en-dist-200M.safetensors
1be3a9b2063867b937e64e2ec7483364a79917e157fa98c5d94b5c1fffea987b ggml-small.bin
...
```

The same hashes are embedded in `models.json` alongside file sizes, giving Finch two independent sources to validate against. If either source disagrees with the actual file, the download is rejected.

To manually verify a file:

```powershell
# PowerShell
(Get-FileHash -Algorithm SHA256 .\downloads\ggml-small.bin).Hash.ToLower()
```

---

## Release Workflow

> See [`docs/releases.md`](docs/releases.md) for the full step-by-step checklist.

At a high level, every release follows this sequence:

```
Download binaries  →  Generate checksums  →  Update manifest  →  Verify
→  Create GitHub Release  →  Upload assets  →  Publish
```

Scripts handle every step up to and including verification. The GitHub Release is created manually.

```powershell
python scripts/download_models.py
python scripts/generate_checksums.py
python scripts/generate_manifest.py
python scripts/verify_models.py
```

---

## Licenses

| Model | License | Source |
|---|---|---|
| Whisper Base / Small / Medium | MIT | [openai/whisper](https://github.com/openai/whisper) · [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) |
| Whisper Large v3 Turbo Q5 | MIT | [openai/whisper](https://github.com/openai/whisper) · [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) |
| Silero VAD | MIT | [snakers4/silero-vad](https://github.com/snakers4/silero-vad) |
| IndicTrans2 Distilled 200M | MIT | [AI4Bharat/IndicTrans2](https://github.com/AI4Bharat/IndicTrans2) · [HuggingFace](https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M) |

The repository metadata (JSON, scripts, documentation) is also released under the [MIT License](LICENSE). Upstream model licenses apply to the binaries themselves — review each source before redistribution.

---

## Contributing

This repository contains **metadata and tooling only**. Contributions that add or change model definitions are welcome.

**Please do not:**

- Commit model binaries (`.bin`, `.onnx`, `.safetensors`, `.gguf`, `.pt`, `.pth`, `.ckpt`)
- Use Git LFS
- Open pull requests that add large files of any kind

**CI will automatically reject any pull request that includes a committed binary.**

If you would like to propose a new model for inclusion, open an issue describing the model, its license, its upstream source, and why it should be part of Finch's default catalog.

---

<div align="center">
  <sub>Part of the <a href="https://github.com/i-ayushsingh/finch">Finch</a> project &nbsp;·&nbsp; MIT License &nbsp;·&nbsp; Copyright © 2026 Finch</sub>
</div>
