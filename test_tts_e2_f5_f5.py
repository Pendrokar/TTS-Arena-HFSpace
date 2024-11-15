import os
from gradio_client import Client, handle_file

client = Client("mrfakename/E2-F5-TTS", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
result = client.predict(
		ref_audio_input=handle_file('https://cdn-uploads.huggingface.co/production/uploads/63d52e0c4e5642795617f668/V6-rMmI-P59DA4leWDIcK.wav'),
		ref_text_input="The Hispaniola was rolling scuppers under in the ocean swell. The booms were tearing at the blocks, the rudder was banging to and fro, and the whole ship creaking, groaning, and jumping like a manufactory.",
		gen_text_input="Please surprise me and speak in whatever voice you enjoy.",
		remove_silence=False,
		cross_fade_duration_slider=0.15,
		speed_slider=1,
		api_name="/basic_tts",
)