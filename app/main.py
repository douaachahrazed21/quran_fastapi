from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.inference import transcrire_et_comparer
from fastapi.responses import JSONResponse
import tempfile
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à adapter si tu veux restreindre
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    sourate: int = Form(...),
    debut: int = Form(...),
    fin: int = Form(...)
):
    # Sauvegarde temporaire du fichier
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, audio.filename)

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    try:
        result = transcrire_et_comparer(audio_path, sourate, debut, fin)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        os.remove(audio_path)

    return result
