#!/usr/bin/env python3
"""Entrypoint for news-image-20261122 V1 (ATM).

Copies the pre-rendered entry.png (drawn by render.py in this session)
to the output directory the grader provides. Standard library only, no
network, no clock, no randomness: the output is byte-identical every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
