import os
import tempfile
import shutil
from fastapi import UploadFile, HTTPException

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}

def get_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename or "")
    return ext.lower()

def validate_audio_extension(filename: str):
    ext = get_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

def save_temp_audio_file(file: UploadFile) -> str:
    validate_audio_extension(file.filename)

    ext = get_extension(file.filename)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            shutil.copyfileobj(file.file, tmp)
            return tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {str(e)}")

def cleanup_temp_file(filepath: str):
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            # Log failure
            print(f"Failed to delete temp file {filepath}: {str(e)}")
