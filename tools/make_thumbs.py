#!/usr/bin/env python3
"""Build small WebP thumbnails, a prompt index and contact sheets from ComfyUI output.

Standard library plus Pillow. Run from the repo root:

    python tools/make_thumbs.py output/comfy output/old --dst thumbs

For every PNG under each source folder it writes:
  thumbs/<source-name>/<relative path>.webp      small preview (default 192 px, quality 60)
  thumbs/<source-name>/index.jsonl               one line per image: path, size, seed, prompt, negative
  thumbs/<source-name>/sheets/sheet-NN.webp      contact sheets, 400 images each (20 x 20)
