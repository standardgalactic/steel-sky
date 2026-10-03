#!/usr/bin/env python3
"""Collection runner for the generate.py supplied earlier. Standard library only."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def slug(value):
    value = re.sub(r'[^a-zA-Z0-9_-]+', '-', str(value)).strip('-').lower()
    if not value:
        raise ValueError('Names must contain at least one ASCII letter or number')
    return value


def save(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
    temporary.replace(path)


def plan(config, selected):
    root = slug(config['name'])
    shared = config['shared_prompt'].strip()
    defaults = config.get('defaults', {})
    seen = set()
    for category, group in config['categories'].items():
        if selected and category not in selected:
            continue
        for entry in group['items']:
            settings = {**defaults, **group.get('settings', {}), **entry.get('settings', {})}
            variations = int(settings.get('variations', 1))
