#!/usr/bin/env python3
import json
import os

from gradio_client import handle_file
from app.models import DEFAULT_VOICE_SAMPLE, DEFAULT_VOICE_TRANSCRIPT, DEFAULT_VOICE_PROMPT

# HF_SPACES data from models.py
hf_spaces = {
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
        'speaker': 'EN-Default',    # DEFAULT_VOICE_SAMPLE=EN-Default
        'speed': 1.0,
        'language': 'EN',
    },
    'mrfakename/MetaVoice-1B-v0.1': {
        1: 5,   # float (numeric value between 0.0 and 10.0) in 'Speech Stability - improves text following for a challenging speaker' Slider component
        2: 5,   # float (numeric value between 1.0 and 5.0) in 'Speaker similarity - How closely to match speaker identity and speech style.' Slider component
        3: "Preset voices", # Literal['Preset voices', 'Upload target voice']  in 'Choose voice' Radio component
        4: "Bria",  # Literal['Bria', 'Alex', 'Jacob']  in 'Preset voices' Dropdown component
        5: None,    # filepath  in 'Upload a clean sample to clone. Sample should contain 1 speaker, be between 30-90 seconds and not contain background noise.' Audio component
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
        'ref_audio': handle_file('voice_samples/EN_B00004_S00051_W000213.mp3'),
        'ref_text': 'Our model manager is Graham, whom we observed leading a small team of chemical engineers within a multinational European firm we\'ll call Kruger Bern.',
        'remove_silence': False,
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
    #   'model_choice': 'Zyphra/Zonos-v0.1-hybrid',
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

# Create files
output_dir = 'app/inputs'
os.makedirs(output_dir, exist_ok=True)

for key, value in hf_spaces.items():
    # Create safe filename from key
    filename = key.replace('/', '__') + '.json'
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
    
    print(f"Created: {filepath}")

print(f"\nTotal files created: {len(hf_spaces)}")
