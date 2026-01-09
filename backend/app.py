import gradio as gr
import fitz
from gtts import gTTS
import uuid

def process_pdf(pdf_file):
    # Open PDF
    doc = fitz.open(pdf_file.name)
    full_text = ""

    print("Total pages:", len(doc))

    # Extract ALL text from every page
    for page_number, page in enumerate(doc, start=1):
        page_text = page.get_text().strip()
        full_text += f"\n\nPage {page_number}:\n{page_text}"

    # Safety check
    if len(full_text.strip()) == 0:
        return "No readable text found in PDF.", None

    # Convert FULL TEXT to speech
    audio_file = f"{uuid.uuid4()}.mp3"
    tts = gTTS(full_text)
    tts.save(audio_file)

    return full_text, audio_file


# Create Gradio UI
ui = gr.Interface(
    fn=process_pdf,
    inputs=gr.File(label="Upload PDF"),
    outputs=[
        gr.Textbox(label="Extracted Text (Full Document)"),
        gr.Audio(label="Audio Output")
    ],
    title="📄 PDF Audio Reader (No AI)",
    description="Upload PDF → Reads the entire document aloud (FREE)"
)

ui.launch()
