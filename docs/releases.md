# Release Process

This document describes the end-to-end procedure for creating a `finch-models` release. A release packages the current set of verified model binaries as GitHub Release assets and updates the metadata that Finch reads at runtime.

> **Rule:** Model binaries are never committed to Git and never stored in Git LFS. The `downloads/` directory is git-ignored. The only artifacts that enter Git are metadata files: `models.json`, `checksums.txt`, and documentation.

---

## Contents

- [Prerequisites](#prerequisites)
- [Step-by-Step Release Checklist](#step-by-step-release-checklist)
- [Versioning Policy](#versioning-policy)
- [Asset Naming Convention](#asset-naming-convention)
- [Rollback Procedure](#rollback-procedure)

---

## Prerequisites

- Python 3.9 or later
- Access to the GitHub repository with permission to create releases
- `HF_TOKEN` or `HUGGING_FACE_HUB_TOKEN` environment variable set to a valid [Hugging Face access token](https://huggingface.co/settings/tokens) with **Read** scope (required for gated models such as IndicTrans2)

Verify your token is set:

```powershell
echo $env:HF_TOKEN
```

---

## Step-by-Step Release Checklist

### 1 — Download model binaries

Pull all model binaries from their upstream sources into the local `downloads/` staging directory. Files that are already present and complete are skipped.

```powershell
python scripts/download_models.py
```

Expected output: one `Downloaded …` or `Skipping …` line per model. Any failure aborts the script with exit code 1 — resolve the error before continuing.

---

### 2 — Verify downloads are complete

Confirm that every expected file is present and has a non-zero size before computing hashes.

```powershell
Get-ChildItem downloads -File | Select-Object Name, Length | Format-Table -AutoSize
```

All six files should appear:

| Filename | Expected size |
|---|---:|
| `ggml-base.bin` | 147,951,465 |
| `ggml-small.bin` | 487,601,967 |
| `ggml-medium.bin` | 1,533,763,059 |
| `ggml-large-v3-turbo-q5_0.bin` | 574,041,195 |
| `silero_vad.onnx` | 2,327,524 |
| `indictrans2-indic-en-dist-200M.safetensors` | 913,353,672 |

---

### 3 — Generate SHA-256 checksums

Hash every file in `downloads/` and write `checksums.txt`.

```powershell
python scripts/generate_checksums.py
```

This overwrites `checksums.txt` with one `<sha256> <filename>` line per file.

---

### 4 — Regenerate the manifest

Build `models.json` from the downloaded files. This reads the actual SHA-256 and byte size from disk — the fields are never filled in by hand.

```powershell
python scripts/generate_manifest.py
```

Inspect the output to confirm `sha256` and `size` fields are populated for all models.

---

### 5 — Run full verification

Cross-validate `models.json`, `checksums.txt`, and the files in `downloads/` against each other.

```powershell
python scripts/verify_models.py
```

Expected output: `Model verification passed`. Any `ERROR:` line indicates a mismatch — do not proceed to the next step until all errors are resolved.

---

### 6 — Commit metadata changes

Commit only the updated metadata and documentation. Never include binaries.

```powershell
git add models.json checksums.txt
# If documentation was updated:
git add README.md CHANGELOG.md docs/
git commit -m "release: v<version>"
git push origin main
```

---

### 7 — Create the GitHub Release

1. Go to the repository on GitHub → **Releases** → **Draft a new release**.
2. Set the tag to `v<version>` (e.g., `v1.0.0-alpha`). Create the tag from `main`.
3. Set the release title to `v<version>`.
4. Copy the relevant section from `CHANGELOG.md` into the release notes.
5. Keep the release as a **draft** until all assets have been uploaded (next step).

---

### 8 — Upload release assets

Upload each file from `downloads/` as a release asset, preserving the exact filename. Do not rename, compress, or repackage the files — Finch downloads them by the filename recorded in `models.json`.

Files to upload:

```
ggml-base.bin
ggml-small.bin
ggml-medium.bin
ggml-large-v3-turbo-q5_0.bin
silero_vad.onnx
indictrans2-indic-en-dist-200M.safetensors
```

Also upload `models.json` and `checksums.txt` as release assets so Finch can fetch the manifest and checksums directly from the release.

---

### 9 — Publish and verify

1. Click **Publish release** on GitHub.
2. Download one or two assets from the published release via a browser to confirm the URLs are accessible.
3. Verify the SHA-256 of a downloaded asset matches `checksums.txt`:

```powershell
(Get-FileHash -Algorithm SHA256 .\ggml-small.bin).Hash.ToLower()
# Should match: 1be3a9b2063867b937e64e2ec7483364a79917e157fa98c5d94b5c1fffea987b
```

---

## Versioning Policy

`finch-models` release tags are aligned to Finch application releases. The tag format is:

```
v<major>.<minor>.<patch>[-<pre-release>]
```

Examples: `v1.0.0-alpha`, `v1.0.0`, `v1.1.0`.

- A new `finch-models` release is required whenever a model is added, removed, or replaced.
- If only metadata or documentation changes (no model binary changes), a patch version bump is sufficient and no new release assets need to be uploaded — update the `releaseAsset` pointer in `models.json` to the existing release.
- Model binaries that have not changed between releases do not need to be re-uploaded. The `releaseAsset` field in `models.json` can point to an older release tag for unchanged models.

---

## Asset Naming Convention

Release asset filenames must exactly match the `filename` field in `models.json`. Finch constructs the download URL as:

```
https://github.com/<owner>/<repo>/releases/download/<tag>/<filename>
```

Do not add version suffixes, date stamps, or extra extensions to asset filenames.

---

## Rollback Procedure

If a release is found to ship a broken or incorrect binary:

1. **Yank the release** — on GitHub, convert the release back to a draft to prevent new downloads.
2. **Identify the issue** — determine whether the problem is with the binary itself, the checksum, or the manifest.
3. **Re-download the affected model** from its upstream source and delete the partial or corrupted file from `downloads/`:
   ```powershell
   Remove-Item downloads\<affected-filename>
   python scripts/download_models.py
   ```
4. **Regenerate checksums and manifest:**
   ```powershell
   python scripts/generate_checksums.py
   python scripts/generate_manifest.py
   python scripts/verify_models.py
   ```
5. **Create a patch release** (e.g., `v1.0.1`) — commit the updated metadata, upload the corrected assets, and publish.
6. **Do not delete the broken release** — instead, edit its description to add a prominent notice directing users to the patch release.
