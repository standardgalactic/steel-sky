# Image Curator

A local, no-database visual curator for large Stable Diffusion output directories.

## Run

```bash
python curator.py /mnt/c/Users/nateg/OneDrive/Documentos/GitHub/stable-diffusion/output
```

Then open:

```text
http://127.0.0.1:8000
```

The server detects albums from ComfyUI-style names such as:

```text
aniara_00044_.png
Steel-sky_00123_.png
```

and displays 100 images per page.

## Ratings

Normal is the implicit default and means "probably keep." You only need to touch exceptions:

- Favorite
- Awesome
- Problem
- Reject

Problem/reject records can also carry reasons such as `frame`, `distorted`, `garbled`, `bad-anatomy`, `text`, `composition`, `duplicate`, and `other`.

The curator continuously writes `curation.json` into the image directory. It also tracks reviewed pages so a page with no flagged images can still be known to have been inspected.

## Keyboard

While an image dialog is open:

```text
A  awesome
F  favorite
P  problem
X  reject
0  normal / reset
←  previous image
→  next image
```

## Exports

The browser can export a JSON snapshot and a `publish.txt`. `publish.txt` contains every image in the current album except explicit rejects.

## CLIP / interrogator analysis

Not included in the first pass on purpose. The state format already has an `analysis` section reserved for it.

A next stage can add a separate worker that computes, for each image:

```json
{
  "clip_caption": "...",
  "aesthetic_score": 0.0,
  "frame_score": 0.0,
  "distortion_score": 0.0,
  "embedding": "optional external file/key"
}
```

I would keep analysis offline and optional so the curator stays fast even with 11k+ images.
