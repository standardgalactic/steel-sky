#!/usr/bin/bash

(
  set -e
  count=0
  while IFS= read -r prompt || [[ -n "$prompt" ]]; do
    [[ "$prompt" =~ ^[[:space:]]*$ ]] && continue
    [[ "$prompt" =~ ^[[:space:]]*# ]] && continue

    count=$((count + 1))
