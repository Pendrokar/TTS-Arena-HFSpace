import os
from gradio_client import Client, file

client = Client("hexgrad/Kokoro-API", hf_token=os.getenv('KOKORO'))
# endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
result = client.predict(
    text='Hello there, you.',
    voice='af_heart',
    speed=1,
    api_name='/predict'
)

print(result)

# text="Oh, hello there!!",
# voice="af",
# ps=None,
# speed=1,
# trim=3000,
# use_gpu=False,