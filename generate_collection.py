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
