import os
from test_overrides import _get_param_examples, _override_params
from gradio_client import Client, file

model = "CAMB-AI/mars6-turbo-demo"
client = Client(model, hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)

api_name = '/inference'
fn_index = None
end_parameters = None
text = 'This is what my voice sounds like.'

end_parameters = _get_param_examples(
	endpoints['named_endpoints'][api_name]['parameters']
)
print(end_parameters)


space_inputs = end_parameters
# override some or all default parameters
space_inputs = _override_params(end_parameters, model)

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
	# space_inputs = {str(i): value for i, value in enumerate(space_inputs)}

print(space_inputs)
# print(*space_inputs)
# print(**space_inputs)

# result = client.predict(
# 	**space_inputs,
# 	api_name=api_name,
#     fn_index=fn_index
# )
print(result)