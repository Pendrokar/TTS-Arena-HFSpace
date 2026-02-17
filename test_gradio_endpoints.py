#!/usr/bin/env python3
"""
Test script to retrieve and validate Gradio API endpoints for all uncommented models
in the AVAILABLE_MODELS variable from models.py.

This test:
1. Iterates through all uncommented models in AVAILABLE_MODELS
2. Retrieves the actual Gradio API endpoints from the remote space
3. Validates that the configured endpoint in HF_SPACES exists and is accessible
4. Validates that any overridden inputs in OVERRIDE_INPUTS are valid for that space
"""

import os
import sys
import signal
from gradio_client import Client
from app.models import AVAILABLE_MODELS, HF_SPACES, OVERRIDE_INPUTS


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Client initialization timed out")


def create_client_with_timeout(space_url: str, hf_token: str, timeout_secs: int = 15):
    """Create a Gradio Client with a timeout for initialization."""
    # Use signal-based timeout (Unix/Linux/Mac)
    try:
        # use TTS host's token
        client_token = HF_SPACES[space_url]['hf_token']
    except:
        # use arena host's token
        client_token = hf_token
    if hasattr(signal, 'SIGALRM'):
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_secs)
        try:
            client = Client(
                space_url,
                token=client_token,
                headers={}
            )
            return client
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    else:
        # Windows fallback - no timeout support
        return Client(
            space_url,
            token=client_token,
            headers={}
        )


def get_space_url(model_name: str) -> str:
    """Get the Hugging Face Space URL from AVAILABLE_MODELS."""
    space_url = AVAILABLE_MODELS[model_name]
    # Handle special case where space_url is a local path (e.g., '/Edge-TTS')
    if space_url.startswith('/'):
        return None
    return space_url


def _get_param_names(endpoint_info: dict) -> list:
    """Extract parameter names from endpoint info."""
    param_names = []
    params = endpoint_info.get('parameters', [])
    for param in params:
        # Try to get parameter_name first (named params), fallback to label or index
        name = param.get('parameter_name')
        if name is None:
            name = param.get('label', f"param_{len(param_names)}")
        param_names.append(name)
    return param_names


def validate_override_inputs(model_name: str, endpoint_info: dict) -> dict:
    """
    Validate that overridden inputs exist as valid parameters for the endpoint.
    
    Returns a dictionary with validation results.
    """
    result = {
        'has_overrides': False,
        'override_keys': [],
        'invalid_keys': [],
        'valid_keys': [],
        'error': None,
    }
    
    # Check if model has override inputs
    override_inputs = OVERRIDE_INPUTS.get(model_name, {})
    
    if not override_inputs:
        return result
    
    result['has_overrides'] = True
    result['override_keys'] = list(override_inputs.keys())
    
    try:
        # Get available parameter names from endpoint
        param_names = _get_param_names(endpoint_info)
        
        # For named parameters, check if override keys exist in param_names
        # For unnamed (list-based) parameters, check if indices are valid
        for key in override_inputs.keys():
            if isinstance(key, int):
                # Unnamed parameter (index-based)
                if key < len(param_names):
                    result['valid_keys'].append(f"[{key}] (index, max: {len(param_names)-1})")
                else:
                    result['invalid_keys'].append(
                        f"[{key}] - Index out of range (max valid index: {len(param_names)-1})"
                    )
            else:
                # Named parameter
                if key in param_names:
                    result['valid_keys'].append(key)
                else:
                    result['invalid_keys'].append(key)
                    
    except Exception as e:
        result['error'] = str(e)
    
    return result


def validate_endpoint(model_name: str, client: Client, config: dict) -> dict:
    """
    Validate the configured endpoint against the actual Gradio API.
    
    Returns a dictionary with validation results.
    """
    result = {
        'model': model_name,
        'space_url': config.get('space_url'),
        'configured_function': config.get('function'),
        'endpoint_exists': False,
        'endpoint_type': None,
        'available_endpoints': [],
        'error': None,
        'override_validation': None,
    }
    
    try:
        # Retrieve API endpoints from the Gradio space
        endpoints = client.view_api(
            all_endpoints=True, 
            print_info=False, 
            return_format='dict'
        )
        
        function = config['function']
        
        # Check if it's a named endpoint (starts with '/')
        if function.startswith('/'):
            named_endpoints = endpoints.get('named_endpoints', {})
            if function in named_endpoints:
                result['endpoint_exists'] = True
                result['endpoint_type'] = 'named'
                result['endpoint_info'] = named_endpoints[function]
            else:
                result['available_endpoints'] = list(named_endpoints.keys())
        else:
            # It's an unnamed endpoint (fn_index)
            unnamed_endpoints = endpoints.get('unnamed_endpoints', {})
            if function in unnamed_endpoints:
                result['endpoint_exists'] = True
                result['endpoint_type'] = 'unnamed'
                result['endpoint_info'] = unnamed_endpoints[function]
            else:
                result['available_endpoints'] = list(unnamed_endpoints.keys())
        
        # Validate override inputs if endpoint exists
        if result['endpoint_exists']:
            result['override_validation'] = validate_override_inputs(
                model_name, 
                result['endpoint_info']
            )
                
    except Exception as e:
        result['error'] = str(e)
    
    return result


def print_validation_result(result: dict, verbose: bool = False) -> None:
    """Print the validation result in a readable format."""
    model = result['model']
    space_url = result['space_url'] or 'N/A (local path)'
    function = result['configured_function']
    
    if result['error']:
        print(f"❌ {model}")
        print(f"   Space: {space_url}")
        print(f"   Error: {result['error']}")
    elif result['endpoint_exists']:
        # Check override validation status
        override_status = ""
        override_details = []
        has_invalid_overrides = False
        
        if result.get('override_validation'):
            ov = result['override_validation']
            if ov.get('has_overrides'):
                if ov.get('invalid_keys'):
                    override_status = " ⚠️(invalid overrides)"
                    has_invalid_overrides = True
                    override_details.append(f"   Override Validation: FAILED")
                    override_details.append(f"   Invalid keys: {', '.join(ov['invalid_keys'])}")
                    if ov.get('valid_keys'):
                        override_details.append(f"   Valid keys: {', '.join(ov['valid_keys'])}")
                else:
                    override_status = " 📝(overrides valid)"
                    if verbose:
                        override_details.append(f"   Override Validation: PASSED")
                        override_details.append(f"   Override keys: {', '.join(ov['valid_keys'])}")
        
        status_emoji = "⚠️ " if has_invalid_overrides else "✅"
        print(f"{status_emoji} {model}{override_status}")
        print(f"   Space: {space_url}")
        print(f"   Function: {function} ({result['endpoint_type']})")
        
        for detail in override_details:
            print(detail)
        
        if verbose and result.get('endpoint_info'):
            params = result['endpoint_info'].get('parameters', [])
            print(f"   Parameters: {len(params)}")
            for param in params:
                param_name = param.get('parameter_name', param.get('label', 'unnamed'))
                param_type = param.get('python_type', {}).get('type', 'unknown')
                print(f"     - {param_name}: {param_type}")
    else:
        print(f"⚠️  {model}")
        print(f"   Space: {space_url}")
        print(f"   Configured Function: {function}")
        print(f"   Status: Endpoint NOT found in available endpoints!")
        if result['available_endpoints']:
            print(f"   Available endpoints: {result['available_endpoints'][:5]}")
            if len(result['available_endpoints']) > 5:
                print(f"   ... and {len(result['available_endpoints']) - 5} more")
    
    print()


def main():
    """Main function to run endpoint validation for all uncommented models."""
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    print("=" * 70)
    print("Gradio API Endpoint Validation")
    print("=" * 70)
    print()
    
    # Get only uncommented models from AVAILABLE_MODELS
    # These are the models that are actually active (not commented out)
    active_models = list(AVAILABLE_MODELS.keys())
    
    print(f"Found {len(active_models)} active models in AVAILABLE_MODELS")
    print()
    
    results = {
        'passed': [],
        'failed': [],
        'skipped': [],
    }
    
    hf_token = os.getenv('HF_TOKEN')
    
    for model_name in active_models:
        # Get space URL
        space_url = get_space_url(model_name)
        
        # Skip local-only models (like Edge-TTS with '/Edge-TTS' path)
        if space_url is None:
            print(f"⏭️  {model_name} - Skipped (local/non-Gradio endpoint)")
            results['skipped'].append(model_name)
            continue
        
        # Check if model has HF_SPACES configuration
        if model_name not in HF_SPACES:
            print(f"⚠️  {model_name} - No HF_SPACES configuration found")
            results['failed'].append({
                'model': model_name,
                'reason': 'No HF_SPACES configuration'
            })
            continue
        
        config = HF_SPACES[model_name].copy()
        config['space_url'] = space_url
        
        try:
            # Create Gradio client with 15 second timeout
            client = create_client_with_timeout(space_url, hf_token, timeout_secs=15)
            
            # Validate the endpoint
            result = validate_endpoint(model_name, client, config)
            print_validation_result(result, verbose=verbose)
            
            if result['endpoint_exists']:
                # Check if overrides are valid
                has_invalid_overrides = (
                    result.get('override_validation') 
                    and result['override_validation'].get('has_overrides')
                    and result['override_validation'].get('invalid_keys')
                )
                
                if has_invalid_overrides:
                    results['failed'].append({
                        'model': model_name,
                        'reason': f"Invalid override keys: {result['override_validation']['invalid_keys']}"
                    })
                else:
                    results['passed'].append(model_name)
            else:
                results['failed'].append({
                    'model': model_name,
                    'reason': 'Endpoint not found',
                    'available': result['available_endpoints']
                })
                
        except Exception as e:
            error_result = {
                'model': model_name,
                'space_url': space_url,
                'configured_function': config.get('function'),
                'error': str(e),
                'endpoint_exists': False,
            }
            print_validation_result(error_result)
            results['failed'].append({
                'model': model_name,
                'reason': f'Connection error: {str(e)}'
            })
    
    # Print summary
    print("=" * 70)
    print("Validation Summary")
    print("=" * 70)
    print(f"✅ Passed: {len(results['passed'])}/{len(active_models)}")
    print(f"⚠️  Failed: {len(results['failed'])}/{len(active_models)}")
    print(f"⏭️  Skipped: {len(results['skipped'])}/{len(active_models)}")
    print()
    
    if results['failed']:
        print("Failed Models:")
        for fail in results['failed']:
            print(f"  - {fail['model']}: {fail['reason']}")
        print()
        return 1
    
    print("All models validated successfully!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
