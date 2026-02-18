#!/usr/bin/env python3
import json
import os

from gradio_client import handle_file
from app.models import DEFAULT_VOICE_SAMPLE, DEFAULT_VOICE_TRANSCRIPT, DEFAULT_VOICE_PROMPT

# OVERRIDE_INPUTS data from models.py
hf_space_inputs = {
 
}

# Create files
output_dir = 'app/inputs'
os.makedirs(output_dir, exist_ok=True)

for key, value in hf_space_inputs.items():
    # Create safe filename from key
    filename = key.replace('/', '__') + '.json'
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
    
    print(f"Created: {filepath}")

print(f"\nTotal files created: {len(hf_space_inputs)}")
