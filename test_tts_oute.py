import os
from gradio_client import Client, handle_file

# client = Client("OuteAI/OuteTTS-0.2-500M-Demo", hf_token=os.getenv('HF_TOKEN'))
client = Client("ameerazam08/OuteTTS-0.2-500M-Demo", hf_token=os.getenv('HF_TOKEN'))

endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)

result = client.predict(
		text="Please surprise me and speak in whatever voice you enjoy.",
		temperature=0.1,
		repetition_penalty=1.1,
		language="en",
		speaker_selection="female_1",
		reference_audio=None,
		reference_text=None,
		# reference_audio=handle_file('EN_B00004_S00051_W000213.wav'),
		# reference_text="Our model manager is Graham, whom we observed leading a small team of chemical engineers within a multinational European firm we'll call",
		api_name="/generate_tts"
)
print(result)