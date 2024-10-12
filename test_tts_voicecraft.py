import os
from gradio_client import Client

client = Client("pyp1/VoiceCraft_gradio", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
print(endpoints)
result = client.predict(
		-1, #seed
		0.08, #left_margin
		0.08, #right_margin
		16000, #codec_audio_sr
		50, #codec_sr
		0, #top_k
		0.9, #top_p
		1, #temperature
		"3", #stop_repetition
		4, #sample_batch_size
		"1", #kvcache
		"[1388,1898,131]", #silence_tokens
		'https://cdn-uploads.huggingface.co/production/uploads/641de0213239b631552713e4/iKHHqWxWy6Zfmp6QP6CZZ.wav', #audio_path
		"I cannot believe that the same model can also do text to speech synthesis too!", #transcript
		True, #smart_transcript
		3.016, #prompt_end_time
		0.46, #edit_start_time
		3.808, #edit_end_time
		"Newline", #split_text
		None, #selected_sentence
		api_name="/run" #api_name
)