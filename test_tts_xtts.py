import os
from gradio_client import Client, file

client = Client("coqui/xtts", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
result = client.predict(
        "Quick test.",	# str  in 'What should I say!? (max 512 characters).' Textbox component
        'en', #lang
        'https://cdn-uploads.huggingface.co/production/uploads/63d52e0c4e5642795617f668/V6-rMmI-P59DA4leWDIcK.wav', # voice sample
        None, # mic voice sample
        False, #use_mic
        False, #cleanup_reference
        False, #auto_detect
        True, #ToS
		fn_index=1
)