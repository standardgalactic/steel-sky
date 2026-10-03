#!/usr/bin/env python3
"""Rebuild a repository's history as many small, cumulative commits.

The history has two parts.

1. Upstream base. The upstream project is cloned and its real commits are kept
   exactly as they are (authors, dates, messages). Upstream files that you did
   not touch are never re-committed, so their credit stays with the real authors.
2. Reconstruction. Every other file in your finished working tree is added on top
   with `git fast-import`. Text files grow line by line (or N lines at a time),
   binary files and very large files go in whole. Commit times are the real
   times at which the script runs. Nothing is back-dated. The intermediate states
   are reconstructions of the finished files, and PROVENANCE.md says so.

Every file is classified before anything is written:

    upstream            identical to the upstream file (ignoring line endings): no commit
    upstream-modified   started from an upstream file and differs from it
    steel-sky           not in upstream
    upstream-removed    in upstream, absent from your folder (deleted, or kept with --removed keep)

Commits that touch an upstream-modified file carry trailers. The authors named are
those whose upstream lines are still present in the final file, found by matching
the final file against `git blame` of the upstream version. It is a count of
surviving lines, not a statement about who wrote the changes:

    Upstream-Origin: https://github.com/AbdBarho/stable-diffusion-webui-docker
    Upstream-Path: docker-compose.yml
    Upstream-Authors: AbdBarho (40 lines retained), PassiveLemon (14 lines retained)
    Upstream-Lines-Retained: 55 of 63
    Provenance: upstream-modified

Emails are never written. Authors are named, not impersonated: the commit author
is you.

Bytes are preserved, with two exceptions that are reported. Files are read and
written as raw bytes (no decoding, no line-ending changes) unless you pass `--eol lf`.

  1. A file whose only difference from upstream is CRLF versus LF counts as identical
     to upstream, so the repository keeps upstream's LF bytes and your CRLF copy is
     not re-committed. The dry run lists these files.
  2. Symbolic links are not imported. They are listed as skipped.

Binary files get no line matching. Their trailers name the authors of the upstream
version ("not line-matched"), which is not a statement about what survives.

File modes: a path that exists upstream keeps its upstream mode. A new file is
100755 only when it starts with a `#!` line, otherwise 100644. The source folder's
own permission bits are not used, so the result is the same on Windows and Linux.

Verification: after the import the script reads every file back out of the new
repository's object database (not the working tree, so autocrlf cannot disturb the
check) and compares its SHA-256 and its mode with the plan. It also checks that the
set of tracked files is exactly the planned set. It refuses to push on any mismatch.

Branch: the whole history, upstream commits included, lives on one branch,
`archdaemon` by default (`--branch NAME` to change it). After the first push, set
that branch as the default branch in the GitHub repository settings.

Typical use, from the finished project folder (needs a .gitignore beside it):

    python tools/monotonic_commit.py --source . --dest ../steel-sky-new --dry-run
    python tools/monotonic_commit.py --source . --dest ../steel-sky-new
    python tools/monotonic_commit.py --source . --dest ../steel-sky-new \\
        --remote https://github.com/standardgalactic/steel-sky --push

Requires git and Python 3.8 or newer. Standard library only.
"""
import argparse
import collections
import csv
import difflib
import fnmatch
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

UPSTREAM_URL = "https://github.com/AbdBarho/stable-diffusion-webui-docker"
ALIASES = {"abdullah barhoum": "AbdBarho", "abdullah": "AbdBarho", "abdbarho": "AbdBarho"}
WHOLE_EXT = (".webp", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".mp3", ".mp4", ".zip", ".woff", ".woff2")

# Phase order matters. First matching rule wins.
RULES = [
    ("pipeline", ["generate.py", "workflow.json", "generate_collection.py", "tools/*", "check-image.py",
                  "make-json.py", "test-*", "docker-compose.yml"]),
    ("catalogue", ["catalogue/*", "catalogue.md", "framework-family-*", "graphic-treatment-*"]),
    ("manifests", ["manifests/*", "slate-samples*.json", "collection.json"]),
    ("samples", ["samples/*", "thumbs/*", "assets/*", "*.webp"]),
    ("site", ["index.html", "image-rater.html", "image_descriptions.json"]),
    ("docs", ["README*", "CONTRIBUTORS.md", "TODO.md", "CLEANUP.md", "LICENSE", ".gitignore"]),
]
PROJECT_RE = re.compile(r"^(?:projects/)?(\d\d\.\d\d)[-/]")


def run(args, cwd=None, inp=None, check=True):
    r = subprocess.run(args, cwd=cwd, input=inp, capture_output=True)
    if check and r.returncode:
        sys.exit("git error: %s\n%s" % (" ".join(args), r.stderr.decode("utf-8", "replace")))
    return r.stdout


def git(dest, *a, **k):
    return run(["git"] + list(a), cwd=dest, **k)


def norm_author(name):
    name = name.strip()
    return ALIASES.get(name.lower(), name)


def is_binary(b):
    return b"\0" in b[:8192]


def to_lf(b):
    return b if is_binary(b) else b.replace(b"\r\n", b"\n")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def hash_object(dest, data):
    return git(dest, "hash-object", "--stdin", inp=data).decode().strip()


def fi_path(p):
    """Path bytes as fast-import wants them (C-quoted only when it has to be)."""
    b = os.fsencode(p)
    if b.startswith(b'"') or b"\n" in b:
        b = b'"' + b.replace(b"\\", b"\\\\").replace(b'"', b'\\"').replace(b"\n", b"\\n") + b'"'
    return b


def list_source_files(source):
    """Files git would track, honouring the source .gitignore, without touching the source."""
    tmp = tempfile.mkdtemp()
    try:
        run(["git", "init", "--bare", "-q", tmp])
        out = run(["git", "-c", "core.excludesFile=", "--git-dir=" + tmp, "--work-tree=" + source,
                   "ls-files", "-co", "--exclude-standard", "-z"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    files, skipped = [], []
    for raw in out.split(b"\0"):
        if not raw:
            continue
        p = os.fsdecode(raw)
        full = os.path.join(source, p)
        if p.startswith(".git/"):
            continue
        if os.path.islink(full):
            skipped.append((p, "symlink"))
        elif os.path.isfile(full):
            files.append(p)
    return sorted(files), skipped


def phase_of(path, cls):
    if cls in ("upstream-modified", "upstream-removed"):
        return "upstream-changes"
    m = PROJECT_RE.match(path)
    if m:
        return "project-" + m.group(1)
