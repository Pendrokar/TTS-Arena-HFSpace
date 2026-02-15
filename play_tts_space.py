#!/usr/bin/env python3
"""
Command-line tool to synthesize and play TTS audio from a Hugging Face Space.

Usage:
    python play_tts_space.py <space_url> [text]

Arguments:
    space_url   The Hugging Face Space URL (e.g., srinivasbilla/llasa-3b-tts)
    text        Optional text to synthesize (default: "Hello world!")

Example:
    python play_tts_space.py srinivasbilla/llasa-3b-tts "Hello world!"
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

from gradio_client import Client, file

from test_overrides import _get_param_examples, _override_params, HF_SPACES


def play_audio(audio_path: str):
    """Play audio file on Linux using available audio players."""
    audio_path = Path(audio_path)
    
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        return False
    
    # Try different audio players in order of preference
    players = ['aplay', 'paplay', 'ogg123', 'ffplay', 'mpg123']
    
    for player in players:
        try:
            result = subprocess.run(
                ['which', player],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"Playing audio using {player}...")
                
                if player == 'ffplay':
                    # ffplay requires -autoexit and -nodisp for non-interactive use
                    subprocess.run([player, '-autoexit', '-nodisp', str(audio_path)])
                else:
                    subprocess.run([player, str(audio_path)])
                return True
        except Exception:
            continue
    
    print("Error: No suitable audio player found.")
    print("Please install one of: aplay, paplay, ogg123, ffplay, mpg123")
    return False


def synthesize_and_play(space_url: str, text: str = "Hello world!"):
    """
    Synthesize text using a Hugging Face Space and play the audio.
    
    Args:
        space_url: The Hugging Face Space URL (e.g., username/space-name)
        text: The text to synthesize
    """
    print(f"Connecting to Space: {space_url}")
    print(f"Text to synthesize: '{text}'")
    
    # Initialize client
    client = Client(space_url, token=os.getenv('HF_TOKEN'))
    
    # Get API endpoints
    endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
    
    api_name = None
    fn_index = None
    
    # Try to find a suitable endpoint
    if endpoints.get('named_endpoints'):
        # Use the first named endpoint that looks like an inference endpoint
        for endpoint_name, endpoint_info in endpoints['named_endpoints'].items():
            if 'infer' in endpoint_name.lower() or 'predict' in endpoint_name.lower():
                api_name = endpoint_name
                break
        # Fallback to first available endpoint
        if api_name is None:
            api_name = list(endpoints['named_endpoints'].keys())[0]
    elif endpoints.get('unnamed_endpoints'):
        # Use the first unnamed endpoint
        fn_index = int(list(endpoints['unnamed_endpoints'].keys())[0])
    
    # Get endpoint parameters
    if api_name:
        parameters = endpoints['named_endpoints'][api_name]['parameters']
    elif fn_index is not None:
        parameters = endpoints['unnamed_endpoints'][str(fn_index)]['parameters']
    else:
        print("Error: Could not find a suitable API endpoint")
        return False
    
    # Get parameter examples
    end_parameters = _get_param_examples(parameters)
    print(f"Endpoint parameters: {end_parameters}")
    
    # Apply any overrides
    space_inputs = _override_params(end_parameters, space_url)
    
    # Set the text input - try common parameter names
    text_set = False
    if isinstance(space_inputs, dict):
        # Try common text parameter names
        for key in ['text', 'target_text', 'input_text', 'prompt', 'sentence', 'input']:
            if key in space_inputs:
                space_inputs[key] = text
                text_set = True
                break
        # If no known key found, set the first string parameter
        if not text_set:
            for key, value in space_inputs.items():
                if isinstance(value, str) and key not in ['language', 'voice', 'model']:
                    space_inputs[key] = text
                    text_set = True
                    break
    else:
        # List input - set first element (usually text)
        if space_inputs:
            space_inputs[HF_SPACES[space_url]['text_param_index']] = text
            text_set = True
    
    if not text_set:
        print("Warning: Could not determine which parameter to set for text input")
    
    print(f"Final inputs: {space_inputs}")
    
    # Make prediction
    try:
        if isinstance(space_inputs, dict):
            result = client.predict(**space_inputs, api_name=api_name)
        else:
            if api_name:
                result = client.predict(*space_inputs, api_name=api_name)
            else:
                result = client.predict(*space_inputs, fn_index=fn_index)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return False
    
    print(f"Result: {result}")
    
    # Extract audio file path from result
    audio_path = None
    
    if isinstance(result, (list, tuple)):
        # Result is a list/tuple, find the audio file
        for item in result:
            if isinstance(item, str) and (item.endswith('.wav') or item.endswith('.mp3') or item.endswith('.ogg')):
                audio_path = item
                break
    elif isinstance(result, str):
        # Result is a string path
        audio_path = result
    elif isinstance(result, dict):
        # Result is a dict, try to find audio path
        for key, value in result.items():
            if isinstance(value, str) and (value.endswith('.wav') or value.endswith('.mp3') or value.endswith('.ogg')):
                audio_path = value
                break
    
    if not audio_path:
        print("Error: Could not find audio file in result")
        return False
    
    print(f"Audio file: {audio_path}")
    
    # Play the audio
    return play_audio(audio_path)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    space_url = sys.argv[1]
    text = sys.argv[2] if len(sys.argv) > 2 else "Hello world!"
    
    success = synthesize_and_play(space_url, text)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
