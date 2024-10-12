import os
from gradio_client import Client

client = Client("parler-tts/parler-tts-expresso", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
print(endpoints)
result = client.predict(
		text="Please surprise me and speak in whatever voice you enjoy.",
		description="Elisabeth; Elisabeth\'s female voice; very clear audio",
		# 3,
		api_name="/gen_tts"
)