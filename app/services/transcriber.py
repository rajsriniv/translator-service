import whisper
from app.services.audio_utils import save_temp_audio_file, cleanup_temp_file
from langdetect import detect, detect_langs
import os

#model_path = os.path.join("models", "ggml-large-v2.bin")
model = whisper.load_model("large")

def transcribe_audio(file):
    path = save_temp_audio_file(file)
    segments = model.transcribe(path, language=None)
    full_text = segments["text"]
    if hasattr(model, "detect_language"):
        lang = segments["language"]
    else:
        lang = detect(full_text)
    cleanup_temp_file(path)
    print(full_text)
    return lang, full_text
