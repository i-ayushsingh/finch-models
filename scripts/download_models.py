"""Download the official Finch model inputs into the ignored downloads directory."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "downloads"
HF_TOKEN = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")

MODELS = [
    ("parakeet-v3-int8.tar.gz", "https://github.com/i-ayushsingh/finch-models/releases/download/v1.0.0-alpha/parakeet-v3-int8.tar.gz"),
    ("silero_vad.onnx", "https://raw.githubusercontent.com/snakers4/silero-vad/master/src/silero_vad/data/silero_vad.onnx"),
    ("indictrans2-indic-en-dist-200M.safetensors", "https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M/resolve/main/model.safetensors?download=true"),
]


def download(name: str, url: str) -> None:
    destination = DOWNLOADS / name
    partial = destination.with_suffix(destination.suffix + ".part")
    if destination.exists():
        print(f"Skipping {name}: already downloaded ({destination.stat().st_size:,} bytes)")
        return

    offset = partial.stat().st_size if partial.exists() else 0
    headers = {"User-Agent": "finch-models-downloader/1.0"}
    if HF_TOKEN and "huggingface.co" in url:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"
    if offset:
        headers["Range"] = f"bytes={offset}-"
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=60) as response:
            if offset and response.status != 206:
                print(f"Server did not resume {name}; restarting download")
                offset = 0
                partial.unlink(missing_ok=True)
                return download(name, url)
            total = response.headers.get("Content-Length")
            total_bytes = offset + int(total) if total and total.isdigit() else None
            mode = "ab" if offset else "wb"
            downloaded = offset
            started = time.monotonic()
            with partial.open(mode) as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    output.write(chunk)
                    downloaded += len(chunk)
                    if total_bytes:
                        percent = downloaded * 100 / total_bytes
                        bar = "=" * int(percent // 2) + " " * (50 - int(percent // 2))
                        print(f"\r{name}: [{bar}] {percent:6.2f}%", end="", flush=True)
                    else:
                        elapsed = max(time.monotonic() - started, 0.001)
                        print(f"\r{name}: {downloaded:,} bytes ({downloaded / elapsed / 1024 / 1024:.1f} MiB/s)", end="", flush=True)
            print()
            if total_bytes is not None and downloaded != total_bytes:
                raise OSError(f"incomplete download for {name}: expected {total_bytes} bytes, received {downloaded}")
        partial.replace(destination)
        print(f"Downloaded {name} ({destination.stat().st_size:,} bytes)")
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
        print(f"Failed to download {name}: {error}", file=sys.stderr)
        print(f"Partial data, if any, remains at {partial}", file=sys.stderr)
        raise


def main() -> int:
    DOWNLOADS.mkdir(exist_ok=True)
    try:
        for name, url in MODELS:
            download(name, url)
    except Exception:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
