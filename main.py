#!/usr/bin/env python3
"""Entrypoint for news-image-20261120.

Copies the pre-rendered entry.png shipped in this repo to the output
directory (MAKEFUN_OUTPUT_DIR, default /output) and verifies the copy
with sha256. Standard library only, no network, no image processing.

It never deletes the output directory. Two runs write identical bytes.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not os.path.isfile(SRC):
        print("error: entry.png missing next to main.py", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)

    src_hash = sha256(SRC)
    dst_hash = sha256(dst)
    if src_hash != dst_hash:
        print("error: sha256 mismatch after copy", file=sys.stderr)
        return 1

    size = os.path.getsize(dst)
    print("wrote %s (%d bytes, sha256 %s)" % (dst, size, dst_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
