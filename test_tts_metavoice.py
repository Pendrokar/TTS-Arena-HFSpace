import os
from gradio_client import Client, file

client = Client("mrfakename/MetaVoice-1B-v0.1", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
print(endpoints)
result = client.predict(
        "Please surprise me and speak in whatever voice you enjoy.",	# str  in 'What should I say!? (max 512 characters).' Textbox component
		5,	# float (numeric value between 0.0 and 10.0) in 'Speech Stability - improves text following for a challenging speaker' Slider component
		5,	# float (numeric value between 1.0 and 5.0) in 'Speaker similarity - How closely to match speaker identity and speech style.' Slider component
		"Preset voices",	# Literal['Preset voices', 'Upload target voice']  in 'Choose voice' Radio component
		"Bria",	# Literal['Bria', 'Alex', 'Jacob']  in 'Preset voices' Dropdown component
		None,	# filepath  in 'Upload a clean sample to clone. Sample should contain 1 speaker, be between 30-90 seconds and not contain background noise.' Audio component
		api_name="/tts"
)