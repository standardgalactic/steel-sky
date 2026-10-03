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
