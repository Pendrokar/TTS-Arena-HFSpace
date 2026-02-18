#!/usr/bin/env python3
import json
import os

# HF_SPACES data from models.py
hf_spaces = {

}

# Create files
output_dir = 'app/tts_spaces'
os.makedirs(output_dir, exist_ok=True)

for key, value in hf_spaces.items():
    # Create safe filename from key
    filename = key.replace('/', '__') + '.json'
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({key: key} ... value, f, indent=2, ensure_ascii=False)
    
    print(f"Created: {filepath}")

print(f"\nTotal files created: {len(hf_spaces)}")
