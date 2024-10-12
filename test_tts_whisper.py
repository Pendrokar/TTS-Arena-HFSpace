import os
from gradio_client import Client, file

# client = Client("Pendrokar/WhisperSpeech", hf_token=os.getenv('HF_TOKEN'))
# client = Client("collabora/WhisperSpeech")

# client = Client(src="https://collabora-whisperspeech.hf.space", max_workers=1, hf_token=os.getenv('HF_TOKEN'))
client = Client(src="collabora/WhisperSpeech", max_workers=1, hf_token=os.getenv('HF_TOKEN'))
# endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)

def somefunc():
    pass
result = client.predict(
		# "/whisper_speech_demo",
    	# somefunc,
		multilingual_text="Test.",
		# speaker_audio=file('https://upload.wikimedia.org/wikipedia/commons/7/75/Winston_Churchill_-_Be_Ye_Men_of_Valour.ogg'),
		speaker_audio=None,
		# speaker_url=file('https://upload.wikimedia.org/wikipedia/commons/7/75/Winston_Churchill_-_Be_Ye_Men_of_Valour.ogg'),
		# speaker_url="",
		speaker_url=None,
		cps=14,
		api_name="/whisper_speech_demo",
		# fn_index=0
)
# result = client.predict(
# 		["Please surprise me and speak in whatever voice you enjoy.",
# 		None,
# 		'https://cdn-uploads.huggingface.co/production/uploads/641de0213239b631552713e4/iKHHqWxWy6Zfmp6QP6CZZ.wav',
# 		14],
# 		api_name="/whisper_speech_demo",
# 		fn_index=0
# )