#!/usr/bin/env python3
"""
Local Stable Diffusion image curator.

Usage:
    python curator.py /path/to/stable-diffusion/output
    python curator.py /path/to/output --port 8000

Then open http://127.0.0.1:8000
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import threading
import time
from collections import Counter
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlparse

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
PREFIX_RE = re.compile(r"^(.*)_\d+_\.[^.]+$", re.IGNORECASE)


def infer_album(filename: str) -> str:
    m = PREFIX_RE.match(filename)
    return m.group(1) if m else "Other"


class CuratorState:
    def __init__(self, image_dir: Path, app_dir: Path):
        self.image_dir = image_dir.resolve()
        self.app_dir = app_dir.resolve()
        self.state_path = self.image_dir / "curation.json"
        self.lock = threading.Lock()

        self.images = sorted(
            p.name for p in self.image_dir.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        )
        self.albums = Counter(infer_album(name) for name in self.images)
        self.data = {
            "version": 1,
            "image_dir": str(self.image_dir),
            "updated_at": None,
            "ratings": {},
            "reviewed_pages": {},
            "analysis": {},
        }
        self.load()

    def load(self):
        if self.state_path.exists():
            try:
                saved = json.loads(self.state_path.read_text(encoding="utf-8"))
                if isinstance(saved, dict):
                    for key in ("ratings", "reviewed_pages", "analysis"):
                        if isinstance(saved.get(key), dict):
                            self.data[key] = saved[key]
                    self.data["version"] = saved.get("version", 1)
                    self.data["updated_at"] = saved.get("updated_at")
            except Exception as exc:
                print(f"Warning: could not read {self.state_path}: {exc}")

    def save(self):
        with self.lock:
            self.data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            temp = self.state_path.with_suffix(".json.tmp")
            temp.write_text(
                json.dumps(self.data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            temp.replace(self.state_path)

    def manifest(self):
        return {
            "images": [
                {"filename": name, "album": infer_album(name)}
                for name in self.images
            ],
            "albums": [
                {"name": name, "count": count}
                for name, count in sorted(self.albums.items(), key=lambda x: (-x[1], x[0].lower()))
            ],
            "ratings": self.data["ratings"],
            "reviewed_pages": self.data["reviewed_pages"],
            "analysis": self.data["analysis"],
            "updated_at": self.data["updated_at"],
        }


class Handler(SimpleHTTPRequestHandler):
    state: CuratorState

    def log_message(self, fmt, *args):
        print(fmt % args)

    def send_json(self, obj, status=200):
        payload = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/manifest":
            return self.send_json(self.state.manifest())

        if parsed.path.startswith("/images/"):
            rel = unquote(parsed.path[len("/images/"):])
            candidate = (self.state.image_dir / rel).resolve()
            if candidate.parent != self.state.image_dir or not candidate.is_file():
                return self.send_error(404)
            ctype = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
            try:
                size = candidate.stat().st_size
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(size))
                self.send_header("Cache-Control", "public, max-age=86400")
                self.end_headers()
                with candidate.open("rb") as f:
                    while chunk := f.read(1024 * 1024):
                        self.wfile.write(chunk)
            except BrokenPipeError:
                pass
            return

        if parsed.path in ("/", "/index.html"):
            candidate = self.state.app_dir / "index.html"
        else:
            candidate = (self.state.app_dir / parsed.path.lstrip("/")).resolve()
            if candidate.parent != self.state.app_dir:
                return self.send_error(404)

        if not candidate.exists():
            return self.send_error(404)

        content = candidate.read_bytes()
        ctype = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return self.send_json({"ok": False, "error": "Invalid JSON"}, 400)

        if parsed.path == "/api/rate":
            filename = body.get("filename")
            rating = body.get("rating")
            reasons = body.get("reasons", [])
            note = body.get("note", "")

            if filename not in self.state.images:
                return self.send_json({"ok": False, "error": "Unknown filename"}, 404)

            if rating in (None, "", "normal"):
                self.state.data["ratings"].pop(filename, None)
            elif rating in ("favorite", "awesome", "problem", "reject"):
                self.state.data["ratings"][filename] = {
                    "rating": rating,
                    "reasons": reasons if isinstance(reasons, list) else [],
                    "note": str(note or ""),
                }
            else:
                return self.send_json({"ok": False, "error": "Invalid rating"}, 400)

            self.state.save()
            return self.send_json({"ok": True})

        if parsed.path == "/api/review-page":
            album = str(body.get("album", "All"))
            page = int(body.get("page", 1))
            reviewed = bool(body.get("reviewed", True))
            key = f"{album}:{page}"
            if reviewed:
                self.state.data["reviewed_pages"][key] = True
            else:
                self.state.data["reviewed_pages"].pop(key, None)
            self.state.save()
            return self.send_json({"ok": True})

        return self.send_json({"ok": False, "error": "Unknown endpoint"}, 404)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    image_dir = args.image_dir.expanduser().resolve()
    if not image_dir.is_dir():
        raise SystemExit(f"Not a directory: {image_dir}")

    app_dir = Path(__file__).resolve().parent
    state = CuratorState(image_dir, app_dir)
    Handler.state = state

    print(f"Found {len(state.images):,} images in {image_dir}")
    print("Albums:")
    for name, count in sorted(state.albums.items(), key=lambda x: (-x[1], x[0].lower())):
        print(f"  {count:6,d}  {name}")
    print(f"\nState: {state.state_path}")
    print(f"Open: http://{args.host}:{args.port}")

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
