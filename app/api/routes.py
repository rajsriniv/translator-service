from fastapi import APIRouter, File, UploadFile, Query
from app.services.transcriber import transcribe_audio 
from app.services.translator import translate_text 
from app.schemas.response import TranslationResponse 
 
router = APIRouter() 
 
@router.post("/translate_audio", response_model=TranslationResponse) 
async def handle_translation(file: UploadFile = File(...), 
                             target_lang: str = Query("en", description="Target language code (e.g., en, fr, hi)")): 
    lang, text = transcribe_audio(file) 
    translated = translate_text(text, lang, target_lang=target_lang) 
    return { 
        "detected_language": lang, 
        "transcription": [{"text": t} for t in text.splitlines()], 
        "translation": translated 
    } 
