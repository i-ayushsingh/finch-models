"""Generate models.json from downloaded files and the official model catalog."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "downloads"
OUTPUT = ROOT / "models.json"

SPECS = [
    ("whisper-base", "Whisper Base", "speech-recognition", "ggml-base.bin", False),
    ("whisper-small", "Whisper Small", "speech-recognition", "ggml-small.bin", True),
    ("whisper-medium", "Whisper Medium", "speech-recognition", "ggml-medium.bin", False),
    ("whisper-large-v3-turbo-q5_0", "Whisper Large v3 Turbo Q5_0", "speech-recognition", "ggml-large-v3-turbo-q5_0.bin", False),
    ("silero-vad", "Silero VAD", "voice-activity-detection", "silero_vad.onnx", True),
]

TRANSLATION_SPECS = [
    ("indictrans2-indic-en-dist-200M", "IndicTrans2 Distilled 200M (Indic → English)", "indictrans2-indic-en-dist-200M.safetensors", "Indic languages → English"),
]


def file_info(name: str) -> tuple[str, int]:
    path = DOWNLOADS / name
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest(), path.stat().st_size


def main() -> int:
    models = []
    for model_id, name, category, filename, recommended in SPECS:
        digest, size = file_info(filename)
        models.append({"id": model_id, "name": name, "category": category, "filename": filename, "sha256": digest, "size": size, "recommended": recommended, "releaseAsset": ""})
    for model_id, name, filename, direction in TRANSLATION_SPECS:
        digest, size = file_info(filename)
        models.append({"id": model_id, "name": name, "category": "translation", "filename": filename, "version": "2025-05-02", "sha256": digest, "size": size, "recommended": True, "default": True, "license": "MIT", "homepage": "https://github.com/AI4Bharat/IndicTrans2", "releaseAsset": "", "direction": direction})
    manifest = {"version": "1.0.0-alpha", "updatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "models": models}
    OUTPUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote manifest to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
