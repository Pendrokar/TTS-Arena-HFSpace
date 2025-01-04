import gradio as gr
from .config import *
from .messages import *

with gr.Blocks() as tts_info:
    gr.Markdown(TTS_INFO)
    gr.HTML(TTS_DATASET_IFRAME)