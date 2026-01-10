from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import fitz
from gtts import gTTS
import uuid
import os

app = FastAPI()

# Allow frontend or Postman access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create audio folder if not exists
os.makedirs("audio", exist_ok=True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Save uploaded PDF
    pdf_name = f"{uuid.uuid4()}.pdf"
    pdf_path = pdf_name

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Read PDF
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text() + "\n"

    if not full_text.strip():
        return {"error": "No readable text found in PDF"}

    # Convert text to audio
    audio_name = f"{uuid.uuid4()}.mp3"
    audio_path = f"audio/{audio_name}"

    tts = gTTS(full_text)
    tts.save(audio_path)

    return {
        "message": "PDF processed successfully",
        "audio_url": f"http://127.0.0.1:8000/audio/{audio_name}"
    }

# Serve audio files
app.mount("/audio", StaticFiles(directory="audio"), name="audio")
