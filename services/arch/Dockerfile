# Steel Sky tooling container on Arch Linux.
# Holds the Python tools (generate_collection.py, make_thumbs.py, monotonic_commit.py).
# ComfyUI keeps running in its own container (profile "comfy").
# Any Arch-based image works.

ARG BASE=flyxion/arch-minimal:v1
FROM ${BASE}

RUN pacman -Syu --noconfirm --needed \
      python python-pillow python-requests git openssh less nano vim jq rsync \
    && pacman -Scc --noconfirm

ARG PUID=1000
ARG PGID=1000
