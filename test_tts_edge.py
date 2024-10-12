import os
from gradio_client import Client, file

client = Client("innoai/Edge-TTS-Text-to-Speech", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
result = client.predict(
		"Please surprise me and speak in whatever voice you enjoy.",
		"en-US-EmmaMultilingualNeural - en-US (Female)",
		0,
		0,
		api_name="/predict"
)