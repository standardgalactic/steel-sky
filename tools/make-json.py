#!/usr/bin/python3

import json
import re

input_path = "output/comfy/steel-sky.txt"
output_path = "image_descriptions.json"

def is_separator(line):
    return set(line.strip()) == {"-"} and len(line.strip()) >= 2

def is_stop_line(line):
    # Add more stop triggers here as needed
    return (line.strip().startswith("Total Token Usage Across All Files:") or
            line.strip().startswith('{') or
            line.strip().startswith('}'))

def is_list_line(line):
    stripped = line.lstrip()
    return (
        stripped.startswith("- ") or
        stripped.startswith("* ") or
        bool(re.match(r"^\d+\.\s", stripped))
    )

def join_summary_lines(lines):
    result = []
    for i, line in enumerate(lines):
        result.append(line)
        if i < len(lines) - 1:
            current_is_list = is_list_line(line)
            next_is_list = is_list_line(lines[i+1])
            if current_is_list and not next_is_list and lines[i+1].strip():
                result.append("")  # add blank line to break list in markdown
    return "\n".join(result)

with open(input_path, "r", encoding="utf-8") as f:
    lines = [line.rstrip() for line in f if line.strip()]
