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
