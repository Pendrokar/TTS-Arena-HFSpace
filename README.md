---
title: TTS Spaces Arena
sdk: gradio
app_file: app.py
license: zlib
tags:
- arena
emoji: 🤗🏆
colorFrom: red
colorTo: red
pinned: true
short_description: Blind vote on HF TTS models!
models:
- amphion/MaskGCT
- canopylabs/orpheus-3b-0.1-ft
- coqui/XTTS-v2
- fishaudio/fish-speech-1.4
- fishaudio/fish-speech-1.5
- hexgrad/Kokoro-82M
- HKUSTAudio/Llasa-1B-two-speakers-kore-puck
- HKUSTAudio/Llasa-3B
- HKUSTAudio/Llasa-8B
- lj1995/GPT-SoVITS
- metavoiceio/metavoice-1B-v0.1
- myshell-ai/MeloTTS-English-v2
- myshell-ai/MeloTTS-English-v3
- myshell-ai/OpenVoice
- myshell-ai/OpenVoiceV2
- OuteAI/OuteTTS-0.2-500M
- OuteAI/OuteTTS-0.3-1B
- parler-tts/parler-tts-large-v1
- parler-tts/parler-tts-mini-v1
- parler-tts/parler-tts-mini-expresso
- Pendrokar/xvapitch_expresso
- sesame/csm-1b
- SparkAudio/Spark-TTS-0.5B
- SWivid/F5-TTS
- WhisperSpeech/WhisperSpeech
- Zyphra/Zonos-v0.1-hybrid
- Zyphra/Zonos-v0.1-transformer
sdk_version: 5.20.1
---

[Saved votes dataset](https://huggingface.co/datasets/Pendrokar/TTS_Arena)
[TTS tracker dataset](https://huggingface.co/datasets/Pendrokar/open_tts_tracker)

# TTS Arena

The codebase for TTS Arena v2.

The TTS Arena is a Gradio app with several components. Please refer to the `app` directory for more information.

## Running the app

```bash
RUNNING_LOCALLY=1 python app.py
```

You must set the `RUNNING_LOCALLY` environment variable to `1` when running the app locally. This prevents it from syncing with the database

The only other needed environmental variable may be 'HF_TOKEN' as anonymous accounts may get more restrictions.
