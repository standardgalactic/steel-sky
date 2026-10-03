#!/usr/bin/bash

curl https://api.x.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <api-key>" \
  -d '{
    "messages": [
      { "role": "system", "content": "You are a test assistant." },
