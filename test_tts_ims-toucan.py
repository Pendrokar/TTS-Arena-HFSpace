import os
from gradio_client import Client

client = Client("Flux9665/MassivelyMultilingualTTS", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
result = client.predict(
		prompt="What I cannot create, I do not understand.",
		language="English (eng)",
		prosody_creativity=0.5,
		duration_scaling_factor=1,
		voice_seed=27,
		emb1=-7.5,
		reference_audio=None,
		api_name="/predict"
)