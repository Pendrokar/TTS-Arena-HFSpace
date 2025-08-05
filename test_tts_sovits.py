import os
from test_overrides import _get_param_examples, _override_params
from gradio_client import Client, handle_file

# model = "Pendrokar/GPT-SoVITS-v2"
# model = "lj1995/GPT-SoVITS-v2"
model = "lj1995/GPT-SoVITS-ProPlus"
client = Client(model, hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)


api_name = None
fn_index = None
end_parameters = None
text = 'This is what my voice sounds like.'

# has named endpoint
# audio sync function name
api_name = '/get_tts_wav'

end_parameters = _get_param_examples(
	endpoints['named_endpoints'][api_name]['parameters']
)
print(end_parameters)

# override some or all default parameters
space_inputs = _override_params(end_parameters, model)

print(space_inputs)

if(type(space_inputs) == dict):
	space_inputs['text'] = text
	result = client.predict(
		**space_inputs,
		api_name=api_name,
		fn_index=fn_index
	)
else:
	space_inputs[0] = text
	result = client.predict(
		*space_inputs,
		api_name=api_name,
		fn_index=fn_index
	)

print(result)