#!/usr/bin/env python3
"""Hand the finished front page to the runner.

The picture itself is drawn by render.py and stored in this folder as
entry.png. This file only moves that image into the directory the
grader names, so the run stays byte-identical and free of clocks,
network calls and chance.
"""

from pathlib import Path

FOLDER = Path(__file__).resolve().parent
PICTURE = FOLDER / "entry.png"


def place_picture() -> int:
    """Copy entry.png into the grader's output folder and report it."""
    import os

    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    target = target_dir / "entry.png"
    if not PICTURE.is_file():
        raise SystemExit(f"missing picture: {PICTURE}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(PICTURE.read_bytes())
    print(f"placed {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(place_picture())
