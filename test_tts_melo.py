import os
from gradio_client import Client

client = Client("mrfakename/MeloTTS", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
result = client.predict(
		"Please surprise me and speak in whatever voice you enjoy.",	# str in 'Text to speak' Textbox component
		"EN-US",	# Literal['EN-US', 'EN-BR', 'EN_INDIA', 'EN-AU', 'EN-Default'] in 'Speaker' Dropdown component
		1.0,	# float (numeric value between 0.1 and 10.0)
		"EN",	# Literal['EN', 'ES', 'FR', 'ZH', 'JP', 'KR'] in 'Language' Radio component
		api_name="/synthesize"
)