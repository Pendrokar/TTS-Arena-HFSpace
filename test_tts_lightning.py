import os
from gradio_client import Client

client = Client("smallestai/smallest-ai-tts-lightningv3.1-demo", token=os.getenv('HF_TOKEN'))
result = client.predict(
	text="Hello!!",
	voice="Sophia (Female, American)",
	language="Auto-detect",
	speed=1,
	api_name="/synthesize_speech"
)
print(result)