#!/usr/bin/python3

import os
from openai import OpenAI
import os
import base64

XAI_API_KEY = os.getenv("XAI_API_KEY")
image_path = "ComfyUI_04099_.png"

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# Getting the base64 string
