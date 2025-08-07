import os
from gradio_client import handle_file
from .init import *
from .db import *

# Models to enable, only include models that users can vote on
AVAILABLE_MODELS = {
    # 'XTTSv2': 'xtts',
    # 'WhisperSpeech': 'whisperspeech',
    # 'ElevenLabs': 'eleven',
    # 'OpenVoice': 'openvoice',
    # 'OpenVoice V2': 'openvoicev2',
    # 'Play.HT 2.0': 'playht',
    # 'Play.HT 3.0 Mini': 'playht3',
    # 'MetaVoice': 'metavoice',
    # 'MeloTTS': 'melo',
    # 'StyleTTS 2': 'styletts2',
    # 'GPT-SoVITS': 'sovits',
    # 'Vokan TTS': 'vokan',
    # 'VoiceCraft 2.0': 'voicecraft',
    # 'Parler TTS': 'parler',
    # 'Parler TTS Large': 'parlerlarge',
    # 'Fish Speech v1.4': 'fish',

    # HF Gradio Spaces: # <works with gradio version #>
    # '<keyname>':'<Space URL>'
    # gradio version that works with most spaces: 4.29
    # 'coqui/xtts': 'coqui/xtts', # 4.29 4.32; extra_headers error appears for 5.13+
    # 'coqui/xtts': 'tonyassi/voice-clone', # ZeroGPU clone
    # 'collabora/WhisperSpeech': 'collabora/WhisperSpeech', # 4.32 4.36.1
    #'myshell-ai/OpenVoice': 'myshell-ai/OpenVoice', # same devs as MeloTTS, which scores higher # extra_headers error appears for 5.13+
    #'myshell-ai/OpenVoiceV2': 'myshell-ai/OpenVoiceV2', # same devs as MeloTTS, which scores higher # extra_headers error appears for 5.13+
    # 'mrfakename/MetaVoice-1B-v0.1': 'mrfakename/MetaVoice-1B-v0.1', # 4.29 4.32
    # 'Pendrokar/xVASynth-TTS': 'Pendrokar/xVASynth-TTS', # 4.29 4.32 4.42.0
    # 'Pendrokar/xVASynth-TTS/NoDeepMoji': 'Pendrokar/xVASynth-TTS', # 4.29 4.32 4.42.0
    # 'coqui/CoquiTTS': 'coqui/CoquiTTS',
    # 'mrfakename/MeloTTS': 'mrfakename/MeloTTS', # 4.29 4.32

    # E2 & F5 TTS
    # F5 model
    'mrfakename/E2-F5-TTS': 'mrfakename/E2-F5-TTS', # 5.0
    # E2 model
    # 'mrfakename/E2-F5-TTS/E2': 'mrfakename/E2-F5-TTS', # seems to require multiple requests for setup

    # # Parler
    # Parler Large model
    # 'parler-tts/parler_tts/large': 'parler-tts/parler_tts', # 4.29 4.32 4.36.1 4.42.0
    # Parler Mini model
    # 'parler-tts/parler_tts': 'parler-tts/parler_tts', # 4.29 4.32 4.36.1 4.42.0
    # 'parler-tts/parler_tts_mini': 'parler-tts/parler_tts_mini', # Mini is the default model of parler_tts
    # 'parler-tts/parler-tts-expresso': 'parler-tts/parler-tts-expresso', # 4.29 4.32 4.36.1 4.42.0
    # Parler Mini Multi v1.1
    # 'PHBJT/multi_parler_tts': 'PHBJT/multi_parler_tts',
    # 'PHBJT/multi_parler_tts/reformatted': 'PHBJT/multi_parler_tts', # reformatted description using Gemma 2b

    # # Microsoft Edge TTS
    # 'innoai/Edge-TTS-Text-to-Speech': 'innoai/Edge-TTS-Text-to-Speech', # API disabled
    'innoai/Edge-TTS-Text-to-Speech': '/Edge-TTS', # using Edge API

    # IMS-Toucan
    # 'Flux9665/MassivelyMultilingualTTS': 'Flux9665/MassivelyMultilingualTTS', # 5.1

    # StyleTTS v2
    # 'Pendrokar/style-tts-2': 'Pendrokar/style-tts-2', #  more votes in OG arena; emotionless

    # StyleTTS Kokoro v0.19
    # 'hexgrad/kokoro': 'hexgrad/Kokoro-TTS',
    # StyleTTS Kokoro v0.23
    # 'hexgrad/Kokoro-TTS/0.23': 'hexgrad/Kokoro-TTS',
    # StyleTTS Kokoro v1.0
    'hexgrad/Kokoro-API': 'hexgrad/kokoro-API',

    # MaskGCT (by Amphion)
    # 'amphion/maskgct': 'amphion/maskgct', # DEMANDS 300 seconds of ZeroGPU!
    # 'Svngoku/maskgct-audio-lab': 'Svngoku/maskgct-audio-lab', # DEMANDS 300 seconds of ZeroGPU!

    # GPT-SoVITS
    # 'lj1995/GPT-SoVITS-v2': 'lj1995/GPT-SoVITS-v2',
    'lj1995/GPT-SoVITS-ProPlus': 'lj1995/GPT-SoVITS-ProPlus',

    # OuteTTS 500M
    # 'OuteAI/OuteTTS-0.2-500M-Demo': 'OuteAI/OuteTTS-0.2-500M-Demo',
    # 'ameerazam08/OuteTTS-0.2-500M-Demo': 'ameerazam08/OuteTTS-0.2-500M-Demo', # ZeroGPU Space
    # OuteTTS 1B
    # 'OuteAI/OuteTTS-0.3-1B-Demo': 'OuteAI/OuteTTS-0.3-1B-Demo',

    # llasa 1b TTS
    # 'HKUST-Audio/Llasa-1B-finetuned-for-two-speakers': 'HKUST-Audio/Llasa-1B-finetuned-for-two-speakers',
    # llasa 3b TTS
    # 'srinivasbilla/llasa-3b-tts': 'srinivasbilla/llasa-3b-tts',
    # llasa 8b TTS
    # 'srinivasbilla/llasa-8b-tts': 'srinivasbilla/llasa-8b-tts', # ZeroGPU Pro account expired

    # Mars5
    # 'CAMB-AI/mars5_space': 'CAMB-AI/mars5_space', # slow inference; Unstable

    # Mars6
    # 'CAMB-AI/mars6-turbo-demo': 'CAMB-AI/mars6-turbo-demo',

    # Zonos
    'Steveeeeeeen/Zonos': 'Steveeeeeeen/Zonos',
    # 'Steveeeeeeen/Zonos/hybrid': 'Steveeeeeeen/Zonos',

    # Spark
    # 'thunnai/SparkTTS': 'thunnai/SparkTTS',

    # Sesame
    # 'sesame/csm-1b' : 'sesame/csm-1b',

    # Orpheus
    'MohamedRashad/Orpheus-TTS' : 'MohamedRashad/Orpheus-TTS',

    # Index TTS
    # 'IndexTeam/IndexTTS': 'IndexTeam/IndexTTS', # hallucinations on the endquotes

    # Dia
    # 'nari-labs/Dia-1.6B': 'nari-labs/Dia-1.6B', # single speaker hallucinates

    # Chatterbox
    'ResembleAI/Chatterbox': 'ResembleAI/Chatterbox',

    # OpenAudio S1 (Fish Audio)
    'fishaudio/openaudio-s1-mini': 'fishaudio/openaudio-s1-mini',

    # MegaTTS
    'ByteDance/MegaTTS3': 'ByteDance/MegaTTS3',

    # HF TTS w issues
    # 'fishaudio/fish-speech-1': 'fishaudio/fish-speech-1', # Discontinued for OpenAudio S1
    # 'LeeSangHoon/HierSpeech_TTS': 'LeeSangHoon/HierSpeech_TTS', # irresponsive to exclamation marks # 4.29
    # 'PolyAI/pheme': '/predict#0', # sleepy HF Space
    # 'amphion/Text-to-Speech': '/predict#0', # disabled also on original HF space due to poor ratings
    # 'suno/bark': '3#0', # Hallucinates
    # 'shivammehta25/Matcha-TTS': '5#0', # seems to require multiple requests for setup
    # 'Manmay/tortoise-tts': '/predict#0', # Cannot retrieve streamed file; 403
    # 'pytorch/Tacotron2': '0#0', # old gradio
}

HF_SPACES = {
    # XTTS v2
    # 'coqui/xtts': {
    #     'name': 'XTTS v2',
    #     'function': '1',
    #     'text_param_index': 0,
    #     'return_audio_index': 1,
    #     'series': 'XTTS',
    #     'emoji': '😩', # old gradio
    # },
    # tonyassi ZeroGPU XTTS v2
    'coqui/xtts': {
        'name': 'XTTS v2',
        'function': '/predict',
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'XTTS',
        'emoji': '😩', # old gradio
        'title': 'Gradio version too old', # old gradio
    },

    # WhisperSpeech
    'collabora/WhisperSpeech': {
        'name': 'WhisperSpeech',
        'function': '/whisper_speech_demo',
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'WhisperSpeech',
        'emoji': '😷', # broken space
        'title': 'Broken space - runtime error',
    },

    # OpenVoice (MyShell.ai)
    'myshell-ai/OpenVoice': {
        'name':'OpenVoice',
        'function': '1',
        'text_param_index': 0,
        'return_audio_index': 1,
        'series': 'OpenVoice',
        'emoji': '😩', # old gradio
        'title': 'Gradio version too old', # old gradio
    },
    # OpenVoice v2 (MyShell.ai)
    'myshell-ai/OpenVoiceV2': {
        'name':'OpenVoice v2',
        'function': '1',
        'text_param_index': 0,
        'return_audio_index': 1,
        'series': 'OpenVoice',
        'emoji': '😩', # old gradio
        'title': 'Gradio version too old', # old gradio
    },

    # MetaVoice
    'mrfakename/MetaVoice-1B-v0.1': {
        'name':'MetaVoice',
        'function': '/tts',
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'MetaVoice',
        'emoji': '😷', # broken space
        'title': 'Broken space - runtime error',
    },

    # xVASynth (CPU)
    'Pendrokar/xVASynth-TTS': {
        'name': 'xVASynth v3 DeepMoji',
        'function': '/predict',
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'xVASynth',
        'title': 'Outclassed',
    },
    'Pendrokar/xVASynth-TTS/NoDeepMoji': {
        'name': 'xVASynth v3',
        'function': '/predict',
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'xVASynth',
        'space_link': 'Pendrokar/xVASynth-TTS',
        'title': 'Outclassed',
    },

    # CoquiTTS (CPU)
    'coqui/CoquiTTS': {
        'name': 'CoquiTTS',
        'function': '0',
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'CoquiTTS',
        'title': 'Outclassed',
    },

    # HierSpeech_TTS
    'LeeSangHoon/HierSpeech_TTS': {
        'name': 'HierSpeech++',
        'function': '/predict',
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'HierSpeech++',
        'emoji': '😒', # Narration voice
        'title': 'Narration voice',
    },

    # MeloTTS (MyShell.ai)
    'mrfakename/MeloTTS': {
        'name': 'MeloTTS',
        'function': '/synthesize',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'series': 'MeloTTS',
        'emoji': '😷', # broken space / Narration voice
        'title': 'Broken space / Outclassed narration voice',
    },

    # Parler Mini
    'parler-tts/parler_tts': {
        'name': 'Parler Mini',
        'function': '/gen_tts',
        'text_param_index': 0,
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Parler',
        'emoji': '😷', # broken space
        'title': 'Broken space - runtime error',
    },
    # Parler Large
    'parler-tts/parler_tts/large': {
        'name': 'Parler Large',
        'function': '/gen_tts',
        'text_param_index': 0,
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Parler',
        'emoji': '😷', # broken space
        'title': 'Broken space - runtime error',
        'space_link': 'parler-tts/parler_tts',
    },
    # Parler Mini trained on Expresso dataset
    'parler-tts/parler-tts-expresso': {
        'name': 'Parler Mini Expresso',
        'function': '/gen_tts',
        'text_param_index': 0,
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Parler',
        'emoji': '😷', # broken space
        'title': 'Broken space - runtime error', # overlly jolly voice
    },

    # Parler Mini trained on Expresso dataset
    'PHBJT/multi_parler_tts': {
        'name': 'Parler Mini Multi v1.1',
        'function': '/gen_tts',
        'text_param_index': 'text',
        'return_audio_index': 1, # 0 is the reformatted text
        'is_zero_gpu_space': True,
        'series': 'Parler',
        'title': 'Unstable',
    },

    # Parler Mini trained on Expresso dataset, reformats description using Gemma 2b
    'PHBJT/multi_parler_tts/reformatted': {
        'name': 'Parler Mini Multi v1.1r',
        'function': '/gen_tts',
        'text_param_index': 'text',
        'return_audio_index': 1, # 0 is the reformatted text
        'is_zero_gpu_space': True,
        'series': 'Parler',
        'title': 'Unstable',
    },

    # Microsoft Edge TTS
    'innoai/Edge-TTS-Text-to-Speech': {
        'name': 'Microsoft® Edge TTS',
        'function': '/predict',
        'text_param_index': 0,
        'return_audio_index': 0,
        'is_closed_source': True,
        'series': 'Edge TTS',
        'emoji': '', # Gradio API disabled
        # 'title': 'API Disabled',
        'space_link': 'innoai/Edge-TTS-Text-to-Speech', # API disabled
    },

    # Fish Speech
    'fishaudio/fish-speech-1': {
        'name': 'Fish Speech',
        'function': '/inference_wrapper',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'series': 'Fish Speech',
        'emoji': '😵', # redirects to OpenAudio
        'title': 'Deprecated: Redirects to OpenAudio', # redirects to OpenAudio
    },

    # OpenAudio S1 (Fish Audio)
    'fishaudio/openaudio-s1-mini': {
        'name': 'OpenAudio S1 Mini',
        'function': '/partial',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'series': 'Fish Speech',
        # 'emoji': '😷',
        # 'title': '😷',
    },

    # F5 TTS
    'mrfakename/E2-F5-TTS': {
        'name': 'F5 TTS',
        'function': '/basic_tts',
        'text_param_index': 'gen_text_input',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        # 'series': 'E2 TTS',
        'series': 'E2/F5 TTS',
        'title': 'Uses a voice sample from trained dataset',
    },

    # E2 TTS TODO: call switch model function
    'mrfakename/E2-F5-TTS/E2': {
        'name': 'E2 TTS',
        'function': '/basic_tts',
        'text_param_index': 'gen_text_input',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        # 'series': 'F5 TTS',
        'series': 'E2/F5 TTS',
    },

    # IMS-Toucan
    'Flux9665/MassivelyMultilingualTTS': {
        'name': 'IMS-Toucan',
		'function': "/predict",
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'IMS-Toucan',
        'title': 'Changes voice pitch on each request',
    },

    # IMS-Toucan English non-artificial
    'Flux9665/EnglishToucan': {
        'name': 'IMS-Toucan EN',
		'function': "/predict",
        'text_param_index': 0,
        'return_audio_index': 0,
        'series': 'IMS-Toucan',
        'emoji': '😒', # Narration voice
        'title': 'Narration voice',
    },

    # StyleTTS v2
    'Pendrokar/style-tts-2': {
        'name': 'StyleTTS v2',
        'function': '/synthesize',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'StyleTTS',
        'emoji': '😷', # broken space
        'title': 'Outclassed by Kokoro',
    },

    # StyleTTS Kokoro v0.19
    'hexgrad/kokoro': {
        'name': 'Kokoro v0.19',
        'function': '/generate',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': False,
        'series': 'Kokoro',
        'space_link': 'Remsky/Kokoro-TTS-Zero', # still supports v0.19
        'title': 'Deprecated: Kokoro v1.0+ improves pronunciation',
    },

    # StyleTTS Kokoro v0.23
    'hexgrad/Kokoro-TTS/0.23': {
        'name': 'StyleTTS Kokoro v23',
        'function': '/multilingual',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Kokoro',
        'title': 'Deprecated: Kokoro v1.0+ improves pronunciation',
    },

    # StyleTTS Kokoro v1.0 (CPU)
    'hexgrad/Kokoro-API': {
        'name': 'Kokoro v1.0',
        'function': '/predict',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': False,
        'series': 'Kokoro',
        'hf_token': os.getenv('KOKORO'), # router
        'space_link': 'hexgrad/kokoro', # router
    },

    # MaskGCT (by Amphion)
    'amphion/maskgct': {
        'name': 'MaskGCT',
        'function': '/predict',
        'text_param_index': 1,
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'MaskGCT',
        'emoji': '🥵', # requires 300s reserved ZeroGPU!
        'title': 'Requires 300s reserved ZeroGPU time! Cannot afford!',
    },
    'Svngoku/maskgct-audio-lab': {
        'name': 'MaskGCT',
        'function': '/predict',
        'text_param_index': 1,
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'MaskGCT',
        'emoji': '🥵', # requires 300s reserved ZeroGPU!
        'title': 'Requires 300s reserved ZeroGPU time! Cannot afford!',
    },

    # GPT-SoVITS v2
    'lj1995/GPT-SoVITS-v2': {
        'name': 'GPT-SoVITS v2',
        'function': '/get_tts_wav',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'GPT-SoVITS',
        'title': 'Outclassed',
    },

    # GPT-SoVITS ProPlus
    'lj1995/GPT-SoVITS-ProPlus': {
        'name': 'GPT-SoVITS ProPlus',
        'function': '/get_tts_wav',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'GPT-SoVITS',
        'title': 'Outclassed',
    },

    # OuteTTS v0.2 500M
    'ameerazam08/OuteTTS-0.2-500M-Demo': {
        'name': 'OuteTTS v0.2 500M',
        'function': '/generate_tts',
        'text_param_index': 0,
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'OuteTTS',
        'emoji': '🥵', # requires 300s reserved ZeroGPU!
        'title': 'Requires 300s reserved ZeroGPU time! Cannot afford!',
    },
    # OuteTTS v0.3 1B
    'OuteAI/OuteTTS-0.3-1B-Demo': {
        'name': 'OuteTTS v0.3 1B',
        'function': '/generate_tts',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'OuteTTS',
        'emoji': '🥵', # requires 300s reserved ZeroGPU!
        'title': 'Requires 300s reserved ZeroGPU time! Cannot afford!',
    },

    # LlaSa 1B
    'HKUST-Audio/Llasa-1B-finetuned-for-two-speakers': {
        'name': 'LLaSA 1B',
        'function': '/predict',
        'text_param_index': 'input_text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'LLaSA',
        # 'emoji': '😷', # broken space
        'title': 'Broken space - Runtime error',
    },

    # LlaSa 3B
    'srinivasbilla/llasa-3b-tts': {
        'name': 'LLaSA 3B',
        'function': '/infer',
        'text_param_index': 'target_text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'LLaSA',
        # 'emoji': '😷', # broken space
        # 'title': 'Broken space - ZeroGPU Pro account expired',
    },

    # LlaSa 8B
    'srinivasbilla/llasa-8b-tts': {
        'name': 'LLaSA 8B',
        'function': '/infer',
        'text_param_index': 'target_text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'LLaSA',
        # 'emoji': '😷', # broken space
        # 'title': 'Broken space - ZeroGPU Pro account expired',
    },

    # Mars5
    'CAMB-AI/mars5_space': {
        'name': 'MARS 5',
        'function': '/on_click',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': False,
        'series': 'MARS',
    },

    # Mars6
    'CAMB-AI/mars6-turbo-demo': {
        'name': 'MARS 6',
        'function': '/inference',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': False,
        'is_closed_source': True,
        'series': 'MARS',
        'title': 'Unstable',
    },

    # Zonos
    'Steveeeeeeen/Zonos': {
        'name': 'Zonos T',
        'function': '/generate_audio',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Zonos',
        # 'title': 'Outclassed',
    },
    'Steveeeeeeen/Zonos/hybrid': {
        'name': 'Zonos H',
        'function': '/generate_audio',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Zonos',
        'title': 'Outclassed',
        'space_link': 'Steveeeeeeen/Zonos',
    },

    # Spark-TTS
    'thunnai/SparkTTS': {
        'name': 'Spark-TTS',
        'function': '/voice_clone',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Spark-TTS',
        'title': 'Outclassed',
    },

    'sesame/csm-1b' : {
        'name': 'CSM 1B',
        'function': '/infer',
        'text_param_index': 'gen_conversation_input',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'CSM-1B',
        'title': 'Outclassed',
    },

    'MohamedRashad/Orpheus-TTS' : {
        'name': 'Orpheus 3B v0.1',
        'function': '/generate_speech',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Orpheus',
    },

    'IndexTeam/IndexTTS' : {
        'name': 'Index TTS',
        'function': '/gen_single',
        'text_param_index': 'text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Index',
        'title': 'Outclassed',
    },

    'nari-labs/Dia-1.6B' : {
        'name': 'Dia',
        'function': '/generate_audio',
        'text_param_index': 'text_input',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Dia',
        'title': 'Outclassed',
    },

    'ResembleAI/Chatterbox' : {
        'name': 'Chatterbox',
        'function': '/generate_tts_audio',
        'text_param_index': 'text_input',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'Chatterbox',
    },

    'ByteDance/MegaTTS3': {
        'name': 'MegaTTS',
        'function': '/predict',
        'text_param_index': 'inp_text',
        'return_audio_index': 0,
        'is_zero_gpu_space': True,
        'series': 'MegaTTS',
    },
}

# for zero-shot TTS - voice sample used by XTTS (11 seconds)
DEFAULT_VOICE_SAMPLE_STR = 'voice_samples/xtts_sample.wav'
DEFAULT_VOICE_SAMPLE = handle_file(DEFAULT_VOICE_SAMPLE_STR)
DEFAULT_VOICE_TRANSCRIPT = "The Hispaniola was rolling scuppers under in the ocean swell. The booms were tearing at the blocks, the rudder was banging to and fro, and the whole ship creaking, groaning, and jumping like a manufactory."
DEFAULT_VOICE_PROMPT = "female voice; very clear audio"

# Older gradio spaces use unnamed parameters, both types are valid
OVERRIDE_INPUTS = {
#     'coqui/xtts': {
#         1: 'en',
#         2: DEFAULT_VOICE_SAMPLE_STR, # voice sample
#         3: None, # mic voice sample
#         4: False, #use_mic
#         5: False, #cleanup_reference
#         6: False, #auto_detect
#     },
    # tonyassi ZeroGPU space of XTTS:
    'coqui/xtts': {
        1: DEFAULT_VOICE_SAMPLE, # voice sample
        # 'audio': DEFAULT_VOICE_SAMPLE, # voice sample
    },
    'collabora/WhisperSpeech': {
        1: DEFAULT_VOICE_SAMPLE, # voice sample
        2: DEFAULT_VOICE_SAMPLE, # voice sample URL
        3: 14.0, #Tempo - Gradio Slider issue: takes min. rather than value
    },
    'myshell-ai/OpenVoice': {
        1: 'default', # style
        2: 'https://huggingface.co/spaces/myshell-ai/OpenVoiceV2/resolve/main/examples/speaker0.mp3', # voice sample
    },
    'myshell-ai/OpenVoiceV2': {
        1: 'en_us', # style
        2: 'https://huggingface.co/spaces/myshell-ai/OpenVoiceV2/resolve/main/examples/speaker0.mp3', # voice sample
    },
    'PolyAI/pheme': {
        1: 'YOU1000000044_S0000798', # voice
        2: 210,
        3: 0.7, #Tempo - Gradio Slider issue: takes min. rather than value
    },
    'Pendrokar/xVASynth-TTS': {
        1: 'x_ex04', #fine-tuned voice model name
        3: 1.0, #pacing/duration - Gradio Slider issue: takes min. rather than value
    },
    'Pendrokar/xVASynth-TTS/NoDeepMoji': {
        1: 'x_ex02', #fine-tuned voice model name
        3: 1.0, #pacing/duration - Gradio Slider issue: takes min. rather than value
        10: False, #Use DeepMoji
    },
    'suno/bark': {
        1: 'Speaker 3 (en)', # voice
    },
    'amphion/Text-to-Speech': {
        1: 'LikeManyWaters', # voice
    },
    'LeeSangHoon/HierSpeech_TTS': {
        1: handle_file('https://huggingface.co/spaces/LeeSangHoon/HierSpeech_TTS/resolve/main/example/female.wav'), # voice sample
        2: 0.333,
        3: 0.333,
        4: 1,
        5: 1,
        6: 0,
        7: 1111,
    },
    'Manmay/tortoise-tts': {
        1: None, # text-from-file
        2: 'angie', # voice
        3: 'disabled', # second voice for a dialogue
        4: 'No', # split by newline
    },
    'mrfakename/MeloTTS': {
        'speaker': 'EN-Default',	# DEFAULT_VOICE_SAMPLE=EN-Default
        'speed': 1.0,
        'language': 'EN',
    },
    'mrfakename/MetaVoice-1B-v0.1': {
		1: 5,	# float (numeric value between 0.0 and 10.0) in 'Speech Stability - improves text following for a challenging speaker' Slider component
		2: 5,	# float (numeric value between 1.0 and 5.0) in 'Speaker similarity - How closely to match speaker identity and speech style.' Slider component
		3: "Preset voices",	# Literal['Preset voices', 'Upload target voice']  in 'Choose voice' Radio component
		4: "Bria",	# Literal['Bria', 'Alex', 'Jacob']  in 'Preset voices' Dropdown component
		5: None,	# filepath  in 'Upload a clean sample to clone. Sample should contain 1 speaker, be between 30-90 seconds and not contain background noise.' Audio component
    },
    'parler-tts/parler_tts': { # mini
        1: 'Laura; Laura\'s ' + DEFAULT_VOICE_PROMPT, #description / voice prompt
        2: False, #use_large
    },
    'parler-tts/parler_tts/large': {
        1: 'Laura; Laura\'s ' + DEFAULT_VOICE_PROMPT, #description / voice prompt
        2: True, #use_large
    },
    # multi-lang parler mini 1.1
    'PHBJT/multi_parler_tts': {
        'description': 'a ' + DEFAULT_VOICE_PROMPT, #description / voice prompt
        'do_format': False, # Reformat description using Gemma 2b
    },
    'parler-tts/parler-tts-expresso': {
        1: 'Elisabeth; Elisabeth\'s ' + DEFAULT_VOICE_PROMPT, #description / voice prompt
    },
    'innoai/Edge-TTS-Text-to-Speech': {
        1: 'en-US-EmmaMultilingualNeural - en-US (Female)', # voice
        2: 0, # pace rate
        3: 0, # pitch
    },

    'fishaudio/fish-speech-1': {
		'normalize': False,
        'reference_audio': handle_file('https://huggingface.co/spaces/fishaudio/fish-speech-1/resolve/main/examples/English.wav'),
		'reference_text': 'In the ancient land of Eldoria, where the skies were painted with shades of mystic hues and the forests whispered secrets of old, there existed a dragon named Zephyros. Unlike the fearsome tales of dragons that plagued human hearts with terror, Zephyros was a creature of wonder and wisdom, revered by all who knew of his existence.', # reference_text
		'max_new_tokens': 1024,
		'chunk_length': 200,
		'top_p': 0.7,
		'repetition_penalty': 1.2,
		'temperature': 0.7,
		'seed': 0,
		'use_memory_cache': "never",
    },

    # OpenAudio S1 (Fish Audio)
    'fishaudio/openaudio-s1-mini': {
		'reference_id': None,
        'reference_audio': handle_file('voice_samples/English.wav'),
		'reference_text': 'In the ancient land of Eldoria, where the skies were painted with shades of mystic hues and the forests whispered secrets of old, there existed a dragon named Zephyros. Unlike the fearsome tales of dragons that plagued human hearts with terror, Zephyros was a creature of wonder and wisdom, revered by all who knew of his existence.', # reference_text
		'max_new_tokens': 0,
		'chunk_length': 0,
		'top_p': 0.9,
		'repetition_penalty': 1.1,
		'temperature': 0.9,
		'seed': 1,
		'use_memory_cache': "on",
    },

    # F5
    'mrfakename/E2-F5-TTS': {
        'ref_audio_input': handle_file('voice_samples/EN_B00004_S00051_W000213.mp3'),
        'ref_text_input': 'Our model manager is Graham, whom we observed leading a small team of chemical engineers within a multinational European firm we\'ll call Kruger Bern.',
        'remove_silence': False,
        'cross_fade_duration_slider': 0.15,
        'nfe_slider': 32,
        'speed_slider': 1,
    },

    # E2 TODO: call switch model
    'mrfakename/E2-F5-TTS/E2': {
        'ref_audio_input': handle_file('voice_samples/EN_B00004_S00051_W000213.mp3'),
        'ref_text_input': 'Our model manager is Graham, whom we observed leading a small team of chemical engineers within a multinational European firm we\'ll call Kruger Bern.',
        'remove_silence': False,
        'cross_fade_duration_slider': 0.15,
        'nfe_slider': 32,
        'speed_slider': 1,
    },

    # IMS-Toucan
    'Flux9665/MassivelyMultilingualTTS': {
		1: "English (eng)", #language
		2: 0.6, #prosody_creativity
		3: 1, #duration_scaling_factor
		4: 41, #voice_seed
		5: -7.5, #emb1
		6: None, #reference_audio
    },

    # StyleTTS 2
    'Pendrokar/style-tts-2': {
        'voice': "f-us-2",
        'lang': 'en-us',
        'lngsteps': 8,
    },

    # StyleTTS 2 Kokoro v0.19
    'hexgrad/kokoro': {
		'voice': "af",
		'ps': None,
		'speed': 1,
		'trim': 0.5,
		'use_gpu': False, # fast enough with multithreaded CPU
        'sk': os.getenv('KOKORO'),
    },

    # StyleTTS 2 Kokoro v0.23
    'hexgrad/Kokoro-TTS/0.23': {
		'voice': "af",
		'speed': 1,
		'trim': 0.5,
        'sk': os.getenv('KOKORO'),
    },

    # StyleTTS 2 Kokoro v1.0
    'hexgrad/Kokoro-API': {
		'voice': "af_heart",
		'speed': 1,
    },

    # maskGCT (by amphion)
    'amphion/maskgct': {
        0: DEFAULT_VOICE_SAMPLE, #prompt_wav
		2: -1, #target_len
		3: 25, #n_timesteps
    },
    'Svngoku/maskgct-audio-lab': {
        0: DEFAULT_VOICE_SAMPLE, #prompt_wav
		2: -1, #target_len
		3: 25, #n_timesteps
    },
    'lj1995/GPT-SoVITS-v2': {
        'ref_wav_path': handle_file('voice_samples/EN_B00004_S00051_W000213.wav'),
        'prompt_text': "Our model manager is Graham, whom we observed leading a small team of chemical engineers within a multinational European firm we'll call",
        'prompt_language': "English",
        # text: "Please surprise me and speak in whatever voice you enjoy.",
        'text_language': "English",
        'how_to_cut': "No slice",
        'top_k': 15,
        'top_p': 1,
        'temperature': 1,
        'ref_free': False,
        'speed': 1,
        'if_freeze': False,
        'inp_refs': None,
    },
    'lj1995/GPT-SoVITS-ProPlus': {
        'ref_wav_path': handle_file('voice_samples/EN_B00004_S00051_W000213.wav'),
        'prompt_text': "Our model manager is Graham, whom we observed leading a small team of chemical engineers within a multinational European firm we'll call",
        'prompt_language': "英文", # "English" in Japanese
        # text: "Please surprise me and speak in whatever voice you enjoy.",
        'text_language': "英文", # "English" in Japanese
        'how_to_cut': "不切", # "No slice" in Japanese
        'top_k': 15,
        'top_p': 1,
        'temperature': 1,
        'ref_free': False,
        'speed': 1,
        'if_freeze': False,
        'inp_refs': None,
    },
    'ameerazam08/OuteTTS-0.2-500M-Demo': {
        1: 0.1, # temperature
        2: 1.1, # repetition_penalty
        3: "en", # language
        4: "female_1", # speaker_selection
        5: None, # reference_audio
        6: None, # reference_text
    },
    'OuteAI/OuteTTS-0.3-1B-Demo': {
		'temperature': 0.1,
		'repetition_penalty': 1.1,
		'speaker_selection': "en_female_1",
		'reference_audio': None,
    },
    'HKUST-Audio/Llasa-1B-finetuned-for-two-speakers': {
		'speaker_choice': 'kore',
    },
    'srinivasbilla/llasa-3b-tts': {
		'sample_audio_path': handle_file('voice_samples/EN_B00004_S00051_W000213.mp3'),
    },
    'srinivasbilla/llasa-8b-tts': {
		'sample_audio_path': handle_file('voice_samples/EN_B00004_S00051_W000213.mp3'),
    },

    # MARS 5
    'CAMB-AI/mars5_space': {
        'audio_file': DEFAULT_VOICE_SAMPLE,
		'prompt_text': DEFAULT_VOICE_TRANSCRIPT,
		'temperature': 0.8,
		'top_k': -1,
		'top_p': 0.2,
		'typical_p': 1,
		'freq_penalty': 2.6,
		'presence_penalty': 0.4,
		'rep_penalty_window': 100,
		'nar_guidance_w': 3,
		'deep_clone': True, # too slow for deep clone
    },

    # MARS 6
    'CAMB-AI/mars6-turbo-demo': {
        'reference_audio': DEFAULT_VOICE_SAMPLE,
		'reference_text': DEFAULT_VOICE_TRANSCRIPT,
		'ras_K': 10,
		'ras_t_r': 0.09,
		'top_p': 0.2,
		'quality_prefix': "48000",
		'clone_method': "deep-clone",
    },

    # Zonos
    'Steveeeeeeen/Zonos': {
        'model_choice':"Zyphra/Zonos-v0.1-transformer",
        'language': "en-us",
        'speaker_audio': None, # optional
        'prefix_audio': handle_file('https://huggingface.co/spaces/Steveeeeeeen/Zonos/resolve/main/assets/silence_100ms.wav'),
        # 'e1': 1,
        # 'e2': 0.05,
        # 'e3': 0.05,
        # 'e4': 0.05,
        # 'e5': 0.05,
        # 'e6': 0.05,
        # 'e7': 0.1,
        # 'e8': 0.2,
        'vq_single': 0.78,
        'fmax': 24000,
        'pitch_std': 45,
        'speaking_rate': 15,
        'dnsmos_ovrl': 4,
        'speaker_noised': False,
        'cfg_scale': 2,
        'min_p': 0.15,
        'seed': 420,
        'randomize_seed': False, # Set to False to easily recreate the state
        'unconditional_keys': ["emotion"], # makes it ignore e1-e8
    },
    # 'Steveeeeeeen/Zonos/hybrid': {
	# 	'model_choice': 'Zyphra/Zonos-v0.1-hybrid',
    # },

    # Spark-TTS
    'thunnai/SparkTTS' : {
		'prompt_text': DEFAULT_VOICE_TRANSCRIPT,
		'prompt_wav_upload': DEFAULT_VOICE_SAMPLE,
		'prompt_wav_record': None,
    },

    # csm-1b
    'sesame/csm-1b' : {
		'text_prompt_speaker_a': 'And Lake turned round upon me, a little abruptly, his odd yellowish eyes, a little like those of the sea eagle, and the ghost of his smile that flickered on his singularly pale face, with a stern and insidious look, confronted me.',
		'text_prompt_speaker_b': 'And Lake turned round upon me, a little abruptly, his odd yellowish eyes, a little like those of the sea eagle, and the ghost of his smile that flickered on his singularly pale face, with a stern and insidious look, confronted me.', #second speaker unused
		'audio_prompt_speaker_a': handle_file('voice_samples/read_speech_a.wav'),
		'audio_prompt_speaker_b': handle_file('voice_samples/read_speech_a.wav'), #second speaker unused
    },

    # Orpheus 3B 0.1
    'MohamedRashad/Orpheus-TTS' : {
		'voice': 'tara',
		'temperature': 0.6,
		'top_p': 0.95,
		'repetition_penalty': 1.1,
		'max_new_tokens': 1200,
    },

    # Index TTS
    'IndexTeam/IndexTTS' : {
		'prompt': DEFAULT_VOICE_SAMPLE, # voice
    },

    # Dia
    'nari-labs/Dia-1.6B': {
		'audio_prompt_input': None,
		'max_new_tokens': 860, # min tokens as we use only a single speaker
		'cfg_scale': 3, # 1-5 # Higher values increase adherence to the text prompt.
		'temperature': 1.3, # Lower values make the output more deterministic, higher values increase randomness.
		'top_p': 0.95, # Filters vocabulary to the most likely tokens cumulatively reaching probability P.
		'cfg_filter_top_k': 35, # Top k filter for CFG guidance.
		'speed_factor': 0.94, # Adjusts the speed of the generated audio (1.0 = original speed).
    },

    # Chatterbox
    'ResembleAI/Chatterbox': {
		'audio_prompt_path_input': handle_file('https://cdn-uploads.huggingface.co/production/uploads/642c0b71eb6e214d4f8897a3/H8qgQbv6e8bgGVCM-w4mq.wav'), # voice; chosen by Manmay of Resemble AI org - https://huggingface.co/spaces/ResembleAI/Chatterbox/discussions/14#686cd36e9479e00d8d3fc079
		'exaggeration_input': 0.5, # 1-2
		'temperature_input': 0.8, # Lower values make the output more deterministic, higher values increase randomness.
		'seed_num_input': 1, # Seed for random number generation, can be any integer.
		'cfgw_input': 0.5, # CFG/Pace weight, can be any float value.
    },

    # MegaTTS
    'ByteDance/MegaTTS3': {
		'inp_audio': handle_file('voice_samples/xtts_sample_megatts.wav'),
		'inp_npy': handle_file('voice_samples/xtts_sample_megatts.npy'),
		'infer_timestep': 32,
		'p_w': 1.4,
		't_w': 3,
    },
}

# minor mods to model from the same space
OVERRIDE_INPUTS['Steveeeeeeen/Zonos/hybrid'] = OVERRIDE_INPUTS['Steveeeeeeen/Zonos']
OVERRIDE_INPUTS['Steveeeeeeen/Zonos/hybrid']['model_choice'] = 'Zyphra/Zonos-v0.1-hybrid'

OVERRIDE_INPUTS['PHBJT/multi_parler_tts/reformatted'] = OVERRIDE_INPUTS['PHBJT/multi_parler_tts']
OVERRIDE_INPUTS['PHBJT/multi_parler_tts/reformatted']['do_format'] = True

# Model name mapping, can include models that users cannot vote on
#not updated
model_names = {
    'styletts2': 'StyleTTS 2',
    'tacotron': 'Tacotron',
    'tacotronph': 'Tacotron Phoneme',
    'tacotrondca': 'Tacotron DCA',
    'speedyspeech': 'Speedy Speech',
    'overflow': 'Overflow TTS',
    'vits': 'VITS',
    'vitsneon': 'VITS Neon',
    'neuralhmm': 'Neural HMM',
    'glow': 'Glow TTS',
    'fastpitch': 'FastPitch',
    'jenny': 'Jenny',
    'tortoise': 'Tortoise TTS',
    'xtts2': 'Coqui XTTSv2',
    'xtts': 'Coqui XTTS',
    'openvoice': 'MyShell OpenVoice',
    'elevenlabs': 'ElevenLabs',
    'openai': 'OpenAI',
    'hierspeech': 'HierSpeech++',
    'pheme': 'PolyAI Pheme',
    'speecht5': 'SpeechT5',
    'metavoice': 'MetaVoice-1B',
}

#not updated
model_links = {
    'ElevenLabs': 'https://elevenlabs.io/',
    'Play.HT 2.0': 'https://play.ht/',
    'Play.HT 3.0 Mini': 'https://play.ht/',
    'XTTSv2': 'https://huggingface.co/coqui/XTTS-v2',
    'MeloTTS': 'https://github.com/myshell-ai/MeloTTS',
    'StyleTTS 2': 'https://github.com/yl4579/StyleTTS2',
    'Parler TTS Large': 'https://github.com/huggingface/parler-tts',
    'Parler TTS': 'https://github.com/huggingface/parler-tts',
    'Fish Speech v1.5': 'https://github.com/fishaudio/fish-speech',
    'Fish Speech v1.4': 'https://github.com/fishaudio/fish-speech',
    'GPT-SoVITS': 'https://github.com/RVC-Boss/GPT-SoVITS',
    'WhisperSpeech': 'https://github.com/WhisperSpeech/WhisperSpeech',
    'VoiceCraft 2.0': 'https://github.com/jasonppy/VoiceCraft',
    'PlayDialog': 'https://play.ht/',
    'Kokoro v0.19': 'https://huggingface.co/hexgrad/Kokoro-82M',
    'CosyVoice 2.0': 'https://github.com/FunAudioLLM/CosyVoice',
    'MetaVoice': 'https://github.com/metavoiceio/metavoice-src',
    'OpenVoice': 'https://github.com/myshell-ai/OpenVoice',
    'OpenVoice V2': 'https://github.com/myshell-ai/OpenVoice',
    'Pheme': 'https://github.com/PolyAI-LDN/pheme',
    'Vokan TTS': 'https://huggingface.co/ShoukanLabs/Vokan',
}

#not updated
closed_source = [
    'ElevenLabs',
    'Play.HT 2.0',
    'Play.HT 3.0 Mini',
    'PlayDialog',
]

# top five models in order to always have one of them picked and scrutinized
top_five = ['ByteDance/MegaTTS3']

# prioritize low vote models
sql = 'SELECT name FROM model WHERE (upvote + downvote) < 750 ORDER BY (upvote + downvote) ASC'
conn = get_db()
cursor = conn.cursor()
cursor.execute(sql)
data = cursor.fetchall()
for model in data:
    if (
        len(top_five) >= 5
    ):
        break
    if (
        model[0] in top_five
        or model[0] not in AVAILABLE_MODELS.keys()
    ):
        continue

    top_five.append(model[0])
print(f"low vote top_five: {top_five}")

def make_link_to_space(model_name, for_leaderboard=False):
    # create a anchor link if a HF space
    style = 'text-decoration: underline;text-decoration-style: dotted;'
    title = ''

    if model_name in AVAILABLE_MODELS:
        style += 'color: var(--link-text-color);'
        if '/' in model_name:
            title += model_name
    else:
        style += 'font-style: italic;'
        title += model_name

    # add HTML title with comment on model
    try:
        if HF_SPACES[model_name]['title']:
            title += '; '+ HF_SPACES[model_name]['title']
    except:
        pass

    # bolden top five models which get more scrutinized
    if model_name in top_five:
        style += 'font-weight: bold;'
        title += '; scrutinized'

    model_basename = model_name
    if model_name in HF_SPACES:
        model_basename = HF_SPACES[model_name]['name']

    try:
        if(
            for_leaderboard
            and HF_SPACES[model_name]['is_closed_source']
        ):
            model_basename += ' 🔐'
            title += '; 🔐 = online only or proprietary'
    except:
        pass


    if '/' in model_name:
        space_link = 'https://huggingface.co/spaces/'

        try:
            # Official Kokoro Space uses a router
            space_link += HF_SPACES[model_name]['space_link']
        except:
            try:
                space_link += AVAILABLE_MODELS[model_name]
            except:
                space_link += model_name
                pass
            pass

        emoji = '🤗' # HF
        try:
            emoji = HF_SPACES[model_name]['emoji']
        except:
            pass
        return (emoji +' <a target="_blank" style="'+ style +'" title="'+ title +'" href="'+ space_link +'">'+ model_basename +'</a>').strip()

    # otherwise just return without emoji
    return '<span style="'+ style +'" title="'+ title +'" href="'+ space_link +'">'+ model_name +'</span>'

def markdown_link_to_space(model_name):
    # create a anchor link if a HF space using markdown syntax
    if '/' in model_name:
        return '🤗 [' + model_name + '](https://huggingface.co/spaces/' + model_name + ')'
    # otherwise just return the model name
    return model_name
