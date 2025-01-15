import os
from test_overrides import _get_param_examples, _override_params
from gradio_client import Client, file

model = "Pendrokar/xVASynth-TTS"
client = Client("Pendrokar/xVASynth-TTS", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')

api_name = '/predict'
fn_index = None
end_parameters = None
text = 'This is what my voice sounds like.'

end_parameters = _get_param_examples(
	endpoints['named_endpoints'][api_name]['parameters']
)
print(end_parameters)


# override some or all default parameters
space_inputs = _override_params(end_parameters, model)

space_inputs[0] = text

print(space_inputs)
result = client.predict(
	*space_inputs,
	api_name=api_name
)
print(result)