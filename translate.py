# filename: translation_api.py

from fastapi import File, UploadFile, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer
import os
from pywhispercpp.model import Model
import shutil
import tempfile

app = FastAPI()
white_listed_ext = [".wav", ".mp3"]
whisper_model = Model('large-v2', n_threads=4)
print(hasattr(whisper_model, "detect_language"))

LANGUAGE_PAIR = "Helsinki-NLP/opus-mt-mul-en"
tokenizer = MarianTokenizer.from_pretrained(LANGUAGE_PAIR)
model = MarianMTModel.from_pretrained(LANGUAGE_PAIR)

class TranslationRequest(BaseModel):
    text: str

@app.post("/translate_audio")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded.")
        _, ext = os.path.splitext(file.filename)
        ext = ext.lower()
        if ext not in white_listed_ext:
            raise HTTPException(status_code=400, detail="File must have an extension (e.g., .wav, .mp3)")
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        segments = whisper_model.transcribe(tmp_path)
        transcription = [
            {"text": seg.text.strip()}
            for seg in segments
        ]
        transcribed_text = ''
        for seg in segments:
            transcribed_text += seg.text.strip()
        inputs = tokenizer(transcribed_text, return_tensors="pt", truncation=True, padding=True)
            
        translated_tokens = model.generate(**inputs)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return {"translation": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")