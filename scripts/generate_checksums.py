"""Generate SHA-256 checksums for downloaded model files."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "downloads"
OUTPUT = ROOT / "checksums.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    files = sorted(path for path in DOWNLOADS.iterdir() if path.is_file() and path.name != ".gitkeep" and not path.name.endswith(".part"))
    lines = ["# SHA256 filename"]
    for path in files:
        lines.append(f"{sha256(path)} {path.name}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(files)} checksum(s) to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
