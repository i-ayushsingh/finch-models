# Model Reference

Detailed reference for every AI model distributed through `finch-models`.

All binaries are distributed as GitHub Release assets. SHA-256 hashes and exact byte sizes are recorded in [`models.json`](../models.json) and [`checksums.txt`](../checksums.txt) and are verified by Finch before a model is used.

---

## Contents

- [Speech Recognition](#speech-recognition)
  - [Whisper Large v3 Turbo Q5](#whisper-large-v3-turbo-q5)
  - [Whisper Medium](#whisper-medium)
  - [Whisper Small](#whisper-small)
  - [Whisper Base](#whisper-base)
- [Voice Activity Detection](#voice-activity-detection)
  - [Silero VAD](#silero-vad)
- [Translation](#translation)
  - [IndicTrans2 Distilled 200M](#indictrans2-distilled-200m)
- [Maintenance](#maintenance)
  - [Adding a New Model](#adding-a-new-model)
  - [Regenerating Checksums](#regenerating-checksums)
  - [Updating models.json](#updating-modelsjson)

---

## Speech Recognition

Finch uses OpenAI Whisper models in their GGML quantized form via [whisper.cpp](https://github.com/ggerganov/whisper.cpp) for fast, CPU-friendly offline transcription.

---

### Whisper Large v3 Turbo Q5

| Field | Value |
|---|---|
| **ID** | `whisper-large-v3-turbo-q5_0` |
| **Filename** | `ggml-large-v3-turbo-q5_0.bin` |
| **Category** | Speech Recognition |
| **License** | MIT |
| **Source** | [openai/whisper](https://github.com/openai/whisper) |
| **Download** | [ggerganov/whisper.cpp](https://huggingface.co/ggerganov/whisper.cpp) |
| **Download size** | ~548 MB (574,041,195 bytes) |
| **SHA-256** | `394221709cd5ad1f40c46e6031ca61bce88931e6e088c188294c6d5a55ffa7e2` |
| **Recommended hardware** | Recent CPU with AVX2 support or GPU; 8 GB RAM |
| **Working memory** | ~3 GB |

**Purpose.** High-quality speech-to-text transcription at a substantially reduced model size compared to the full Large v3. The Q5_0 quantization preserves most of the accuracy of the full-precision model while cutting the download size by more than half.

**Accuracy notes.** Excellent accuracy across a wide range of accents and recording conditions. The best choice when transcription quality is the priority and the full Medium model is not sufficient.

**Why Finch includes this model.** Provides a quality ceiling for users who need the highest accuracy available without the full unquantized Large model footprint.

---

### Whisper Medium

| Field | Value |
|---|---|
| **ID** | `whisper-medium` |
| **Filename** | `ggml-medium.bin` |
| **Category** | Speech Recognition |
| **License** | MIT |
| **Source** | [openai/whisper](https://github.com/openai/whisper) |
| **Download** | [ggerganov/whisper.cpp](https://huggingface.co/ggerganov/whisper.cpp) |
| **Download size** | ~1.43 GB (1,533,763,059 bytes) |
| **SHA-256** | `6c14d5adee5f86394037b4e4e8b59f1673b6cee10e3cf0b11bbdbee79c156208` |
| **Recommended hardware** | Fast multi-core CPU or GPU; 16 GB RAM |
| **Working memory** | ~5 GB |

**Purpose.** Full-precision medium model for users who want maximum accuracy without quantization artifacts and have the RAM to support it.

**Accuracy notes.** Higher accuracy than Small on heavily accented speech and noisy recordings. Noticeably slower than Small on low-core-count machines.

**Why Finch includes this model.** Covers users who need higher accuracy than Small and have sufficient hardware, but prefer full-precision weights over a quantized Large variant.

---

### Whisper Small

| Field | Value |
|---|---|
| **ID** | `whisper-small` |
| **Filename** | `ggml-small.bin` |
| **Category** | Speech Recognition |
| **License** | MIT |
| **Source** | [openai/whisper](https://github.com/openai/whisper) |
| **Download** | [ggerganov/whisper.cpp](https://huggingface.co/ggerganov/whisper.cpp) |
| **Download size** | ~465 MB (487,601,967 bytes) |
| **SHA-256** | `1be3a9b2063867b937e64e2ec7483364a79917e157fa98c5d94b5c1fffea987b` |
| **Recommended hardware** | Modern multi-core CPU; 8 GB RAM |
| **Working memory** | ~2 GB |

**Purpose.** The best balance of accuracy and speed for general use. Handles clear recordings and standard accents reliably on any modern laptop.

**Accuracy notes.** Good accuracy for everyday transcription. Performance degrades in very noisy environments or with heavy accents; in those cases Whisper Medium or Large v3 Turbo Q5 is preferable.

**Why Finch includes this model.** The default and recommended transcription model. Covers the broadest range of hardware while still delivering practical accuracy.

---

### Whisper Base

| Field | Value |
|---|---|
| **ID** | `whisper-base` |
| **Filename** | `ggml-base.bin` |
| **Category** | Speech Recognition |
| **License** | MIT |
| **Source** | [openai/whisper](https://github.com/openai/whisper) |
| **Download** | [ggerganov/whisper.cpp](https://huggingface.co/ggerganov/whisper.cpp) |
| **Download size** | ~141 MB (147,951,465 bytes) |
| **SHA-256** | `60ed5bc3dd14eea856493d334349b405782ddcaf0028d4b5df4088345fba2efe` |
| **Recommended hardware** | Any modern CPU; 4 GB RAM |
| **Working memory** | ~1 GB |

**Purpose.** The smallest and fastest Whisper variant. Suitable for machines with limited RAM or when low latency matters more than accuracy.

**Accuracy notes.** Noticeably less accurate than Small, especially on accented or overlapping speech. Best for quick drafts, keyword spotting, or resource-constrained environments.

**Why Finch includes this model.** Provides a low-resource option for users on older hardware or for scenarios where speed is paramount.

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
