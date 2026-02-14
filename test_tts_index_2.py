import os
from test_overrides import _get_param_examples, _override_params
from gradio_client import Client, file

# Note: Update this model name when IndexTTS2 becomes available on HF Spaces
model = "IndexTeam/IndexTTS-2-Demo"  # Assuming IndexTTS2 will be available under this name
client = Client(model, hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)

api_name = '/gen_single'  # Same API endpoint as the original IndexTTS
fn_index = None
end_parameters = None

# Sample text for testing IndexTTS2's enhanced emotional expression capabilities
text = 'This is what my voice sounds like with enhanced emotional expression.'

end_parameters = _get_param_examples(
	endpoints['named_endpoints'][api_name]['parameters']
)
print("Default parameters from IndexTTS2 API:")
print(end_parameters)

space_inputs = end_parameters
# override some or all default parameters with Arena-specific defaults
space_inputs = _override_params(end_parameters, model)

# Set the text input
if(type(space_inputs) == dict):
	space_inputs['text'] = text
	# IndexTTS2 specific parameters - adjust as needed based on the actual API
	# These are examples based on the Gradio interface code you provided
	# if 'emo_weight' in space_inputs:
	# 	space_inputs['emo_weight'] = 0.8
	# if 'max_text_tokens_per_segment' in space_inputs:
	# 	space_inputs['max_text_tokens_per_segment'] = 120
	
	result = client.predict(
		**space_inputs,
		api_name=api_name,
		fn_index=fn_index
	)
else:
	space_inputs[0] = text  # Assuming text is the first parameter
	result = client.predict(
		*space_inputs,
		api_name=api_name,
		fn_index=fn_index
	)

print("Final input parameters:")
print(space_inputs)

print("Prediction result:")
print(result)