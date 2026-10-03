#!/usr/bin/env python3
"""Build small WebP thumbnails, a prompt index and contact sheets from ComfyUI output.

Standard library plus Pillow. Run from the repo root:

    python tools/make_thumbs.py output/comfy output/old --dst thumbs

For every PNG under each source folder it writes:
  thumbs/<source-name>/<relative path>.webp      small preview (default 192 px, quality 60)
  thumbs/<source-name>/index.jsonl               one line per image: path, size, seed, prompt, negative
  thumbs/<source-name>/sheets/sheet-NN.webp      contact sheets, 400 images each (20 x 20)

Existing thumbnails are skipped, so the script can be re-run after new generations.
The index keeps the prompt that ComfyUI embeds in each PNG, so the thumbnail
copy of the project does not lose how an image was made.
"""
import argparse
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

from PIL import Image


def read_prompt(img):
    """Return (positive, negative, seed) from the ComfyUI 'prompt' chunk, or blanks."""
    raw = img.info.get("prompt")
    if not raw:
