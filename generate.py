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
