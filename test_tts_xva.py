import os
from gradio_client import Client, file

client = Client("Pendrokar/xVASynth-TTS", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
result = client.predict(
		"Well, hello there!!",	# str  in 'Input Text' Textbox component
		"x_ex04",	# Literal['x_ex04', 'x_ex01', 'cnc_cabal', 'ccby_nvidia_hifi_92_F', 'ccby_nvidia_hifi_6671_M', 'more']  in 'Voice' Radio component
		"en",	# Literal['en', 'de', 'es', 'hi', 'zh', 'more']  in 'Language' Radio component
		1.0,	# float (numeric value between 0.5 and 2.0) in 'Duration' Slider component

		0,	# UNUSED; float (numeric value between 0 and 1.0) in 'Pitch' Slider component
		0.1,	# UNUSED; float (numeric value between 0.1 and 1.0) in 'Energy' Slider component

		0,	# Overriden by DeepMoji; float (numeric value between 0 and 1.0) in '😠 Anger' Slider component
		0,	# Overriden by DeepMoji; float (numeric value between 0 and 1.0) in '😃 Happiness' Slider component
		0,	# Overriden by DeepMoji; float (numeric value between 0 and 1.0) in '😭 Sadness' Slider component
		0,	# Overriden by DeepMoji; float (numeric value between 0 and 1.0) in '😮 Surprise' Slider component
		True,	# bool  in 'Use DeepMoji' Checkbox component

		api_name="/predict"
)