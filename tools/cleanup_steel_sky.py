#!/usr/bin/env python3
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

THINK = re.compile(r'<think>.*?</think>', re.DOTALL)
MOVES = [
 ('03.01-*.md', 'projects/03.01'),
 ('03.01-reconstruction-marker.svg', 'projects/03.01/assets'),
 ('01.01-*.md', 'projects/01.01'),
 ('01.01-register-overlay.svg', 'projects/01.01/assets'),
 ('framework-family-*', 'catalogue'), ('graphic-treatment-*', 'catalogue'),
 ('catalogue.md', 'catalogue'), ('slate-samples*.json', 'manifests'),
 ('collection.json', 'manifests'),
 ('make-json.py', 'tools'), ('check-image.py', 'tools'),
 ('test-check-image.py', 'tools'), ('test-grok.sh', 'tools'),
 ('test-samples.sh', 'tools'), ('make_thumbs.py', 'tools'),
]
