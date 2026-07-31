# Model Reference

Detailed reference for every AI model distributed through `finch-models`.

All binaries are distributed as GitHub Release assets. SHA-256 hashes and exact byte sizes are recorded in [`models.json`](../models.json) and [`checksums.txt`](../checksums.txt) and are verified by Finch before a model is used.

---

## Contents

- [Speech Recognition](#speech-recognition)
  - [Parakeet V3 (Fast CPU)](#parakeet-v3-fast-cpu)
- [Voice Activity Detection](#voice-activity-detection)
  - [Silero VAD](#silero-vad)
- [Translation](#translation)
  - [IndicTrans2 (Hindi → English)](#indictrans2-hindi--english)
- [Maintenance](#maintenance)
  - [Adding a New Model](#adding-a-new-model)
  - [Regenerating Checksums](#regenerating-checksums)
  - [Updating models.json](#updating-modelsjson)

---

## Speech Recognition

Finch uses Parakeet models for fast, CPU-friendly offline transcription with automatic language detection.

---

### Parakeet V3 (Fast CPU)

| Field | Value |
|---|---|
| **ID** | `parakeet-v3` |
| **Filename** | `parakeet-v3-int8.tar.gz` |
| **Category** | Speech Recognition |
| **License** | MIT |
| **Download size** | ~478 MB (478,517,071 bytes) |
| **SHA-256** | `43d37191602727524a7d8c6da0eef11c4ba24320f5b4730f1a2497befc2efa77` |
| **Recommended hardware** | Modern CPU; 4 GB RAM |

**Purpose.** CPU-optimized speech-to-text transcription with auto-detection for Hindi, English, and Hinglish. Delivers ~5x realtime performance.

**Why Finch includes this model.** The default recommended speech recognition model for Finch. Provides high speed and accuracy for Indian multi-lingual speech.

---

## Voice Activity Detection

---

### Silero VAD

| Field | Value |
|---|---|
| **ID** | `silero-vad` |
| **Filename** | `silero_vad.onnx` |
| **Category** | Voice Activity Detection |
| **License** | MIT |
| **Source** | [snakers4/silero-vad](https://github.com/snakers4/silero-vad) |
| **Download size** | ~2.2 MB (2,327,524 bytes) |
| **SHA-256** | `1a153a22f4509e292a94e67d6f9b85e8deb25b4988682b7e174c65279d8788e3` |
| **Recommended hardware** | Any modern CPU; 1 GB RAM |
| **Working memory** | Well under 100 MB |

**Purpose.** Detects whether a given audio segment contains speech or silence. Finch uses Silero VAD to gate transcription — only segments identified as speech are passed to Whisper, which reduces unnecessary inference and improves overall responsiveness.

**Accuracy notes.** Excellent precision on typical microphone recordings. The ONNX export runs efficiently on CPU with no GPU requirement.

**Why Finch includes this model.** A tiny, efficient gating layer that dramatically reduces wasted transcription calls. At ~2.2 MB it has essentially no download cost.

---

## Translation

---

### IndicTrans2 Distilled 200M

| Field | Value |
|---|---|
| **ID** | `indictrans2-indic-en-dist-200M` |
| **Filename** | `indictrans2-indic-en-dist-200M.safetensors` |
| **Category** | Translation |
| **Direction** | Indic languages → English |
| **Version** | 2025-05-02 |
| **License** | MIT |
| **Homepage** | [AI4Bharat/IndicTrans2](https://github.com/AI4Bharat/IndicTrans2) |
| **HuggingFace** | [ai4bharat/indictrans2-indic-en-dist-200M](https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M) |
| **Download size** | ~871 MB (913,353,672 bytes) |
| **SHA-256** | `a9bff20ae94712db41c8dc99d2e381eb456ddccbcd48cb2c7cf077ccc5bc58d8` |
| **Recommended hardware** | Modern CPU with 8 GB RAM; GPU optional |
| **Working memory** | 1.5–2.5 GB during CPU inference |

**Purpose.** Offline machine translation from Indian languages into English. Finch uses this model to translate transcribed speech in Indic languages so that the output is available in English without a network call.

**Language support.** Covers all Indic languages supported by AI4Bharat's IndicTrans2 family, including Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia, Assamese, and more.

**Accuracy notes.** The 200M distilled variant is significantly smaller than the full 1B model while retaining strong translation quality for common Indic languages. It is the recommended checkpoint for CPU-only deployments.

**Why Finch includes this model.** Finch operates entirely offline. IndicTrans2 is one of the few high-quality, MIT-licensed Indic translation models available in a size that is practical for end-user deployment.

> **Note:** This model is hosted on HuggingFace and requires an account token to download. Set `HF_TOKEN` or `HUGGING_FACE_HUB_TOKEN` in your environment before running `scripts/download_models.py`.

---

## Maintenance

### Adding a New Model

1. Add the model's download URL to `MODELS` in `scripts/download_models.py`.
2. Add the model's metadata tuple to `SPECS` (or `TRANSLATION_SPECS`) in `scripts/generate_manifest.py`.
3. Run the full pipeline:
   ```powershell
   python scripts/download_models.py
   python scripts/generate_checksums.py
   python scripts/generate_manifest.py
   python scripts/verify_models.py
   ```
4. Add a section to this file (`docs/models.md`) with full model details.
5. Update the model table in `README.md`.
6. Commit only the metadata and documentation changes — never the binary.

---

### Regenerating Checksums

If you need to rehash all downloaded files (e.g., after redownloading or replacing a binary):

```powershell
python scripts/generate_checksums.py
```

This overwrites `checksums.txt` in place. The resulting file should be committed along with an updated `models.json`.

---

### Updating models.json

`models.json` should never be edited by hand for the `sha256` and `size` fields — those are always generated from the actual downloaded binary:

```powershell
python scripts/generate_manifest.py
```

Other fields such as `recommended`, `releaseAsset`, `homepage`, and `license` can be edited directly in `generate_manifest.py` inside the `SPECS` / `TRANSLATION_SPECS` tuples, then regenerated.
