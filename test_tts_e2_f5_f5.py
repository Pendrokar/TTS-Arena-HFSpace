import os
from gradio_client import Client, handle_file

client = Client("mrfakename/E2-F5-TTS", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
result = client.predict(
		ref_audio=handle_file('voice_samples/EN_B00004_S00051_W000213.mp3'),
		ref_text="The Hispaniola was rolling scuppers under in the ocean swell. The booms were tearing at the blocks, the rudder was banging to and fro, and the whole ship creaking, groaning, and jumping like a manufactory.",
		gen_text="Please surprise me and speak in whatever voice you enjoy.",
		remove_silence=False,
		api_name="/predict",
)