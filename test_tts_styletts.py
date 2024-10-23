import os
from gradio_client import Client, file

client = Client("Pendrokar/style-tts-2", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
result = client.predict(
		text="Hello!!",
		voice="f-us-1", # voice
		lngsteps=8, # lngsteps
		api_name="/synthesize" # api_name
)