# Cleanup steps for steel-sky

Run from the repo root. Review each step before you commit.

## 1. Move files into folders

```
mkdir -p catalogue projects/03.01/assets projects/01.01/assets manifests tools
git mv 03.01-*.md projects/03.01/
git mv 03.01-reconstruction-marker.svg projects/03.01/assets/
git mv 01.01-*.md projects/01.01/
git mv 01.01-register-overlay.svg projects/01.01/assets/
git mv framework-family-* graphic-treatment-* catalogue/
git mv slate-samples*.json collection.json manifests/
git mv make-json.py check-image.py test-check-image.py test-grok.sh test-samples.sh tools/
```

Move `catalogue.md` into `catalogue/` too (it was never in the tree you sent, so it may be outside the repo).
Delete `README.txt` after its content is merged into `README.md`.
The `*.progress.json` files are run state. Add them to `.gitignore` instead of committing them.

## 2. Stop tracking raw output

Your current rules only cover PNGs directly inside the two folders:

```
/output/comfy/*.png
/output/comfy/cache/
/output/old/*.png
/output/old/*.png        (duplicate line)
```

They do not match the run subfolders (`output/comfy/slate-samples-v4/03-01/...`), so `git add -A` would commit those images. Replace the output rules with:

```
# raw generator output stays local; thumbs/ and samples/ are committed
/output/
*.progress.json
```
