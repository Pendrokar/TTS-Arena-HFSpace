import edge_tts
import tempfile

def edge_text_to_speech(text, voice):
    voice_short_name = voice.split(" - ")[0]
    communicate = edge_tts.Communicate(text, voice_short_name)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        communicate.save_sync(tmp_path)
    return tmp_path