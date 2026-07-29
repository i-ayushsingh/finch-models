"""Verify downloaded files against checksums.txt and models.json."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "downloads"
CHECKSUMS = ROOT / "checksums.txt"
MANIFEST = ROOT / "models.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-only", action="store_true", help="Validate metadata without requiring local downloads")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {}
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            digest, filename = line.split(maxsplit=1)
            expected[filename] = digest
    errors = []
    for model in manifest["models"]:
        filename = model["filename"]
        if not filename:
            continue
        if model.get("category") == "translation":
            for field in ("version", "license", "homepage", "default"):
                if field not in model:
                    errors.append(f"translation metadata missing {field}: {filename}")
        path = DOWNLOADS / filename
        if expected.get(filename) != model["sha256"]:
            errors.append(f"checksum metadata mismatch: {filename}")
        if not path.exists():
            if not args.metadata_only:
                errors.append(f"missing file: {filename}")
            continue
        actual_hash = sha256(path)
        actual_size = path.stat().st_size
        if actual_hash != model["sha256"]:
            errors.append(f"manifest SHA256 mismatch: {filename}")
        if actual_size != model["size"]:
            errors.append(f"manifest size mismatch: {filename}")
        if actual_hash != expected.get(filename):
            errors.append(f"checksum mismatch: {filename}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Model verification passed" if not args.metadata_only else "Metadata verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
