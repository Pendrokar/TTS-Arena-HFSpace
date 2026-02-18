import os
import json
from gradio_client import handle_file
from .init import *
from .db import *

# Load HF_SPACES from individual JSON files in app/tts_spaces/
def _load_hf_spaces():
    """Load HF Spaces configuration from JSON files in app/tts_spaces/ directory."""
    spaces = {}
    spaces_dir = os.path.join(os.path.dirname(__file__), 'tts_spaces')
    
    if os.path.isdir(spaces_dir):
        for filename in os.listdir(spaces_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(spaces_dir, filename)
                # Convert filename back to key format: coqui__xtts.json -> coqui/xtts
                key = filename[:-5].replace('__', '/')
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        spaces[key] = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Failed to load {filepath}: {e}")
    
    return spaces

def _load_hf_space_inputs():
    """Load HF Spaces configuration from JSON files in app/tts_spaces/ directory."""
    inputs = {}
    inputs_dir = os.path.join(os.path.dirname(__file__), 'inputs')
    
    if os.path.isdir(inputs_dir):
        for filename in os.listdir(inputs_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(inputs_dir, filename)
                # Convert filename back to key format: coqui__xtts.json -> coqui/xtts
                key = filename[:-5].replace('__', '/')
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        inputs[key] = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Failed to load {filepath}: {e}")
    
    return inputs

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
    'coqui/xtts': 'tonyassi/voice-clone', # ZeroGPU clone
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
    # 'innoai/Edge-TTS-Text-to-Speech': '/Edge-TTS', # using Edge API

    # IMS-Toucan
    # 'Flux9665/MassivelyMultilingualTTS': 'Flux9665/MassivelyMultilingualTTS', # 5.1

    # StyleTTS v2
    # 'Pendrokar/style-tts-2': 'Pendrokar/style-tts-2', #  more votes in OG arena; emotionless

    # StyleTTS Kokoro v0.19
    # 'hexgrad/kokoro': 'hexgrad/Kokoro-TTS',
    # StyleTTS Kokoro v0.23
    # 'hexgrad/Kokoro-TTS/0.23': 'hexgrad/Kokoro-TTS',
    # StyleTTS Kokoro v1.0
    'hexgrad/Kokoro-API': 'hexgrad/Kokoro-API',

    # MaskGCT (by Amphion)
    # 'amphion/maskgct': 'amphion/maskgct', # DEMANDS 300 seconds of ZeroGPU!
    # 'Svngoku/maskgct-audio-lab': 'Svngoku/maskgct-audio-lab', # DEMANDS 300 seconds of ZeroGPU!

    # GPT-SoVITS
    # 'lj1995/GPT-SoVITS-v2': 'lj1995/GPT-SoVITS-v2',
    # 'lj1995/GPT-SoVITS-ProPlus': 'lj1995/GPT-SoVITS-ProPlus',

    # OuteTTS 500M
    # 'OuteAI/OuteTTS-0.2-500M-Demo': 'OuteAI/OuteTTS-0.2-500M-Demo',
    # 'ameerazam08/OuteTTS-0.2-500M-Demo': 'ameerazam08/OuteTTS-0.2-500M-Demo', # ZeroGPU Space
    # OuteTTS 1B
    # 'OuteAI/OuteTTS-0.3-1B-Demo': 'OuteAI/OuteTTS-0.3-1B-Demo',

    # llasa 1b TTS
    # 'HKUST-Audio/Llasa-1B-finetuned-for-two-speakers': 'HKUST-Audio/Llasa-1B-finetuned-for-two-speakers',
    # llasa 3b TTS
    'srinivasbilla/llasa-3b-tts': 'srinivasbilla/llasa-3b-tts',
    # llasa 8b TTS
    # 'srinivasbilla/llasa-8b-tts': 'srinivasbilla/llasa-8b-tts', # ZeroGPU Pro account expired

    # Mars5
    # 'CAMB-AI/mars5_space': 'CAMB-AI/mars5_space', # slow inference; Unstable

    # Mars6
    # 'CAMB-AI/mars6-turbo-demo': 'CAMB-AI/mars6-turbo-demo',

    # Zonos
    # 'Steveeeeeeen/Zonos': 'Steveeeeeeen/Zonos',
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
    # 'fishaudio/openaudio-s1-mini': 'fishaudio/openaudio-s1-mini',

    # MegaTTS
    # 'ByteDance/MegaTTS3': 'ByteDance/MegaTTS3',

    # smallest.ai Lightning v3.1
    'smallestai/smallest-ai-tts-lightningv3.1-demo': 'smallestai/smallest-ai-tts-lightningv3.1-demo',

    # Qwen3 TTS
    'Qwen/Qwen3-TTS': 'Qwen/Qwen3-TTS',
    'Qwen/Qwen3-TTS-Voice-Design': 'Qwen/Qwen3-TTS-Voice-Design', # voice by prompt

    # MOSS TTS
    'OpenMOSS-Team/MOSS-TTS': 'OpenMOSS-Team/MOSS-TTS',

    # Pocket TTS
    'NeuralFalcon/Pocket-TTS': 'NeuralFalcon/Pocket-TTS',

    # KaniTTS
    'nineninesix/KaniTTS': 'nineninesix/KaniTTS',

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

HF_SPACES = _load_hf_spaces()

# special token
HF_SPACES['hexgrad/Kokoro-API']['hf_token'] = os.getenv('KOKORO')

# for zero-shot TTS - voice sample used by XTTS (11 seconds)
DEFAULT_VOICE_SAMPLE_STR = 'voice_samples/xtts_sample.wav'
DEFAULT_VOICE_SAMPLE = handle_file(DEFAULT_VOICE_SAMPLE_STR)
DEFAULT_VOICE_TRANSCRIPT = "The Hispaniola was rolling scuppers under in the ocean swell. The booms were tearing at the blocks, the rudder was banging to and fro, and the whole ship creaking, groaning, and jumping like a manufactory."
DEFAULT_VOICE_PROMPT = "female voice; very clear audio"

# Older gradio spaces use unnamed parameters, both types are valid
OVERRIDE_INPUTS = _load_hf_space_inputs()


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
top_five = [
    'NeuralFalcon/Pocket-TTS',
    'smallestai/smallest-ai-tts-lightningv3.1-demo',
    'Qwen/Qwen3-TTS-Voice-Design',
    'Qwen/Qwen3-TTS',
]

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
