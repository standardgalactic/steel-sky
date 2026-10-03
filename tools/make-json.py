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
