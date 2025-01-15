import os
from gradio_client import Client, handle_file

client = Client("FunAudioLLM/CosyVoice2-0.5B", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)

result = client.predict(
		tts_text="CosyVoice is undergoing a comprehensive upgrade, providing more accurate, stable, faster, and better voice generation capabilities.",
		mode_checkbox_group="3s Voice Clone",
		prompt_text='The Hispaniola was rolling scuppers under in the ocean swell. The booms were tearing at the blocks, the rudder was banging to and fro, and the whole ship creaking, groaning, and jumping like a manufactory.',
		prompt_wav_upload=handle_file("https://cdn-uploads.huggingface.co/production/uploads/63d52e0c4e5642795617f668/V6-rMmI-P59DA4leWDIcK.wav"),
		prompt_wav_record=None,
		instruct_text=None,
		seed=0,
		stream="false",
		api_name="/generate_audio"
)
print(result)