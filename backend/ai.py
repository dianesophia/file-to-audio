import gradio as gr
import fitz
from gtts import gTTS
from transformers import pipeline
import uuid
import os

# Load AI summarizer (CPU-friendly model)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def process_pdf(pdf_file):
    doc = fitz.open(pdf_file.name)
    summaries = []

    print("Total pages:", len(doc))

    # Summarize each page separately
    for page_number, page in enumerate(doc, start=1):
        page_text = page.get_text().strip()

        if len(page_text) < 100:
            continue  # skip empty or very small pages

        print(f"Summarizing page {page_number}...")

        try:
            result = summarizer(
                page_text,
                max_length=120,
                min_length=40,
                do_sample=False
            )[0]["summary_text"]

            summaries.append(f"Page {page_number}: {result}")

        except Exception as e:
            print(f"Skipping page {page_number} due to error:", e)

    # Combine all summaries
    final_summary = "\n\n".join(summaries)

    # Convert summary to speech
    audio_file = f"{uuid.uuid4()}.mp3"
    tts = gTTS(final_summary)
    tts.save(audio_file)

    return final_summary, audio_file


# Create Gradio UI
ui = gr.Interface(
    fn=process_pdf,
    inputs=gr.File(label="Upload PDF"),
    outputs=[
        gr.Textbox(label="AI Summary (All Pages)"),
        gr.Audio(label="Audio Output")
    ],
    title="📄 AI PDF Reader (Page-by-Page)",
    description="Upload a PDF → AI summarizes each page → Audio reads everything"
)

ui.launch()
