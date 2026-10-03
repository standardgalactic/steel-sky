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
