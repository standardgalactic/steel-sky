#!/usr/bin/env python3
import argparse
import json
import secrets
import sys
import time
from pathlib import Path
from urllib import request, error

parser = argparse.ArgumentParser(description="Generate images through local ComfyUI.")
parser.add_argument("prompt", nargs="?", help="Defaults to the workflow's prompt")
parser.add_argument("--workflow", default="workflow.json")
parser.add_argument("--url", default="http://127.0.0.1:7860")
parser.add_argument("--negative")
parser.add_argument("--seed", type=int)
parser.add_argument("--batch", type=int)
parser.add_argument("--prefix")
parser.add_argument("--timeout", type=float, default=1800)
args = parser.parse_args()

# Widget order for the specific node types in your supplied workflow.
widget_names = {
    "CheckpointLoaderSimple": ["ckpt_name"],
    "EmptyLatentImage": ["width", "height", "batch_size"],
    "CLIPTextEncode": ["text"],
    "KSampler": [
        "seed", "_seed_control", "steps", "cfg",
        "sampler_name", "scheduler", "denoise",
    ],
    "SaveImage": ["filename_prefix"],
    "VAEDecode": [],
}

def api(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(
        args.url.rstrip("/") + path,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc

def main():
    workflow = json.loads(Path(args.workflow).read_text(encoding="utf-8"))
    links = {link[0]: link for link in workflow["links"]}
    graph = {}

    for node in workflow["nodes"]:
        kind = node["type"]
        if kind not in widget_names:
            raise ValueError(f"Unsupported node type: {kind}")
        inputs = {}
        for name, value in zip(widget_names[kind], node.get("widgets_values", [])):
            if not name.startswith("_"):
