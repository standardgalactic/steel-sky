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


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', 'replace').strip())
    return result.stdout


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.base = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'base':
            self.base = attrs.get('href')
        for attr in ('src', 'href', 'poster', 'data'):
            if attrs.get(attr):
                self.refs.append((tag, attr, attrs[attr]))
        if attrs.get('srcset'):
            # Handles ordinary file srcsets; data URLs are excluded.
            value = attrs['srcset']
            if 'data:' not in value:
                self.refs.extend((tag, 'srcset', part.strip().split()[0])
                                 for part in value.split(',') if part.strip())


def check_index(root):
    index = root / 'index.html'
    if not index.is_file():
        print('No index.html found at the repository root.')
        return []
    parser = References()
    parser.feed(index.read_text(encoding='utf-8'))
    if parser.base:
        print(f'HTML base URL detected: {parser.base}; resolve these paths against the deployment URL manually.')
        return None
    broken = []
    for tag, attr, ref in parser.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc or not url.path:
            continue
        path = unquote(url.path)
        if path.startswith('/'):
            print(f'Deployment-root reference (manual check): {ref}')
            continue
        target = index.parent / path
        if not target.exists():
            broken.append({'tag': tag, 'attribute': attr, 'reference': ref})
    for item in broken:
        print(f"Missing static HTML target: {item['reference']}")
    print(f'Static HTML check: {len(broken)} missing relative targets.')
    print('This check does not execute JavaScript or inspect fetch(), CSS URLs, or generated paths.')
    return broken


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default='.')
    ap.add_argument('--apply', action='store_true', help='Apply cleanup; otherwise preview only')
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--strip-think', action='store_true', help='Remove complete think blocks in tracked/unignored .md, .txt, .vtt files')
    ap.add_argument('--merge-readme', action='store_true', help='Append README.txt to README.md and remove README.txt')
    args = ap.parse_args()
    requested = Path(args.root).resolve()
    probe = subprocess.run(
        ['git', '-C', str(requested), 'rev-parse', '--show-toplevel'],
        capture_output=True,
    )
    if probe.returncode:
        import tempfile
        temporary_git = tempfile.TemporaryDirectory()
        subprocess.run(
            ['git', 'init', '--bare', '-q', temporary_git.name],
            check=True,
        )
        original_git = globals()['git']

        def temporary_git_command(root, *commands):
            if commands == ('rev-parse', '--show-toplevel'):
                return os.fsencode(str(requested))
            result = subprocess.run(
                ['git', '--git-dir=' + temporary_git.name,
                 '--work-tree=' + str(requested), *commands],
                capture_output=True,
            )
            if result.returncode:
                raise RuntimeError(result.stderr.decode('utf-8', 'replace'))
            return result.stdout

        globals()['git'] = temporary_git_command
        print('Cleaning a folder without Git history; no files need untracking.')
    root = Path(git(requested, 'rev-parse', '--show-toplevel').decode().strip())
    if args.check_only:
        broken = check_index(root)
        return 1 if broken else 0
    # Git's index is retained here, so tracked ignored files remain eligible.
    paths = [os.fsdecode(p) for p in git(root, 'ls-files', '-co', '--exclude-standard', '-z').split(b'\0') if p]
    paths = sorted(set(paths))
    moves = []
    targets = set()
    for pattern, directory in MOVES:
        for source in sorted(root.glob(pattern)):
            if not source.is_file() or source.is_symlink():
                continue
            if source.name.endswith('.progress.json'):
                continue
            target = root / directory / source.name
            if target.exists() or target in targets:
                raise ValueError(f'Move collision: {target.relative_to(root)}')
            targets.add(target)
            moves.append((source, target))
    rewrites = {}
    if args.strip_think:
        for relative in paths:
            source = root / relative
            if source.suffix.lower() not in {'.md', '.txt', '.vtt'} or source.is_symlink() or not source.is_file():
                continue
            raw = source.read_bytes()
            try:
                text = raw.decode('utf-8')
            except UnicodeDecodeError:
                print(f'Skipping non-UTF8 text: {relative}')
