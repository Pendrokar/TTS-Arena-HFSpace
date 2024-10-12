import os
from gradio_client import Client

client = Client("Manmay/tortoise-tts", hf_token=os.getenv('HF_TOKEN'))
result = client.predict(
		text="Please surprise me and speak in whatever voice you enjoy.",
		script=None,
		voice="angie",
		voice_b="disabled",
		seed="No",
		api_name="/predict"
)
print(result)