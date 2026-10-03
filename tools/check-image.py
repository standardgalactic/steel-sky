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
)

def encode_image(image_path):
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def get_image_summary(image_path):
    """Get a summary of the image content and token usage using the xAI API."""
    try:
        base64_image = encode_image(image_path)
        messages = [
            {
                "role": "user",
