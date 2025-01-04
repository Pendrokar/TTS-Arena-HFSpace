import os
from gradio_client import Client, handle_file

client = Client("amphion/maskgct", hf_token=os.getenv('HF_TOKEN'))
endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
result = client.predict(
        prompt_wav=handle_file('https://cdn-uploads.huggingface.co/production/uploads/63d52e0c4e5642795617f668/V6-rMmI-P59DA4leWDIcK.wav'),
		target_text="Hello!!",
		target_len=-1,
		n_timesteps=25,
		api_name="/predict"
)