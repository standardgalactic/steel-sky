#!/usr/bin/python3

import os
import base64
from openai import OpenAI
import subprocess
import time
import random
import json
import sys

# Retrieve the API key from environment variable
XAI_API_KEY = os.getenv("XAI_API_KEY")
if not XAI_API_KEY:
    raise ValueError("XAI_API_KEY environment variable not set")

# Initialize the OpenAI client
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
