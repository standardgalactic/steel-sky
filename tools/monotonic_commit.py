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
    for name, pats in RULES:
        for p in pats:
            if fnmatch.fnmatch(path, p):
                return name
    return "misc"


def split_lines(data):
    out = data.split(b"\n")
    if out and out[-1] == b"":
        out.pop()
    return out


def blame_lines(dest, path):
    out = git(dest, "blame", "--line-porcelain", "-w", "HEAD", "--", path)
    return [norm_author(l[7:].decode("utf-8", "replace")) for l in out.split(b"\n") if l.startswith(b"author ")]


def retained_authors(dest, path, new_data):
    """Authors of upstream lines still present in new_data. Returns (Counter, retained, total)."""
    up = git(dest, "cat-file", "blob", "HEAD:" + path)
    names = blame_lines(dest, path)
    if is_binary(up) or is_binary(new_data):
        c = collections.Counter(names)  # upstream version only: no line matching was done
        return c, None, sum(c.values())
    up_l, new_l = split_lines(up), split_lines(new_data)
    c = collections.Counter()
    sm = difflib.SequenceMatcher(None, up_l, new_l, autojunk=False)
    for i, _j, n in sm.get_matching_blocks():
        for k in range(n):
            if i + k < len(names):
                c[names[i + k]] += 1
    return c, sum(c.values()), len(up_l)


def describe(line, n, ext):
    s = line.decode("utf-8", "replace").strip()
    short = (s[:60] + "...") if len(s) > 60 else s
    if ext == ".md":
        if s.startswith("#"):
            return "Add heading: " + s.lstrip("# ").strip()[:60]
        if s.startswith("|"):
            cell = s.strip("| ").split("|")[0].strip()
            return "Add table row: " + (cell[:50] or "row")
        if s[:2] in ("- ", "* ") or re.match(r"^\d+\. ", s):
            return "Add list item: " + re.sub(r"^([-*]|\d+\.)\s+", "", s)[:50]
        if s.startswith("```"):
            return "Add code block"
        return "Add text: " + short
    if ext == ".py":
        m = re.match(r"\s*(def|class)\s+(\w+)", s)
        if m:
            return "Add %s %s" % (m.group(1), m.group(2))
        if s.startswith(("import ", "from ")):
            return "Add import: " + short
        if s.startswith("#"):
            return "Add comment: " + short
        return "Add code line %d" % n
    if ext in (".json", ".csv", ".jsonl"):
        return "Add data entry %d" % n
    if ext in (".html", ".svg", ".xml", ".css"):
        return "Add markup line %d" % n
    return "Add line %d" % n


def group_lines(data):
    """Raw-byte lines; blank lines are attached to the next non-blank line."""
    groups, cur = [], []
    for ln in data.splitlines(keepends=True):  # bytes: splits on \n, \r\n, \r only
        cur.append(ln)
        if ln.strip():
            groups.append(cur)
            cur = []
    if cur:
        if groups:
            groups[-1].extend(cur)
        else:
            groups.append(cur)
    return groups


class Plan:
    def __init__(self):
        self.items = []

    def add(self, **k):
        k.setdefault("data", None)
        self.items.append(k)


def load(it, source, args):
    """The bytes this file should have in the new repository."""
    if it.get("data") is not None:
        return it["data"]
    raw = open(os.path.join(source, it["path"]), "rb").read()
    return to_lf(raw) if args.eol == "lf" else raw


def per_commit(groups, args):
    return max(args.lines, -(-groups // args.max_commits_per_file))


def commit_count(it, args):
    if it["cls"] == "upstream-removed" or it["whole"] or it["groups"] == 0:
        return 1
    return -(-it["groups"] // per_commit(it["groups"], args))


def build_plan(source, dest, args):
    files, skipped = list_source_files(source)
    base = {}
    for e in git(dest, "ls-tree", "-r", "-z", "HEAD").split(b"\0"):
        if e:
            meta, p = e.split(b"\t", 1)
            mode, _t, blob = meta.decode().split()
            base[os.fsdecode(p)] = (mode, blob)
    plan = Plan()
    plan.skipped = skipped
    seen = set()
    for p in files:
        seen.add(p)
        full = os.path.join(source, p)
        raw = open(full, "rb").read()
        data = to_lf(raw) if args.eol == "lf" else raw
        item = dict(path=p, size=len(data), sha=sha(data), phase=None, authors=None, retained=None,
                    total=None, whole=True, groups=0, eol_only=False)
