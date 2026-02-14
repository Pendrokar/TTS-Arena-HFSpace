import os
from gradio_client import Client, file

client = Client("hexgrad/kokoro", token=os.getenv('HF_TOKEN'))
# endpoints = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(endpoints)
key = os.getenv('KOKORO')
result = client.predict(
		text='"I hate it when people lie to me."',
		voice="af",
		ps=None,
		speed=1,
		trim=0,
		use_gpu=False,
		# *[
        #     "Oh, hello there!!",
		# 	"af", #voice
		# 	None, #ps
		# 	1, #speed
		# 	3000, #trim
		# 	False, #use_gpu; fast enough with multithreaded with CPU
		# ],
        sk=key,
		api_name="/generate"
)

print(result)

# text="Oh, hello there!!",
# voice="af",
# ps=None,
# speed=1,
# trim=3000,
# use_gpu=False,