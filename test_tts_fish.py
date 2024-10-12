import os
from gradio_client import Client, handle_file

client = Client("fishaudio/fish-speech-1", hf_token=os.getenv('HF_TOKEN'))
# printz = client.view_api(all_endpoints=True, print_info=False, return_format='dict')
# print(printz)
result = client.predict(
		text="Please surprise me and speak in whatever voice you enjoy.",
		enable_reference_audio=True,
		reference_audio=handle_file('https://cdn-uploads.huggingface.co/production/uploads/641de0213239b631552713e4/iKHHqWxWy6Zfmp6QP6CZZ.wav'),
		reference_text="In the first half of the 20th century, science fiction familiarized the world with the concept of artificially intelligent robots. It began with the “heartless” Tin man from the Wizard of Oz and continued with the humanoid robot that impersonated Maria in Metropolis. By the 1950s, we had a generation of scientists, mathematicians, and philosophers with the concept of artificial intelligence (or AI) culturally assimilated in their minds.",
		max_new_tokens=1024,
		chunk_length=200,
		top_p=0.7,
		repetition_penalty=1.2,
		temperature=0.7,
		batch_infer_num=1,
		if_load_asr_model=False,
		api_name="/inference_wrapper"
)
print(result[1])