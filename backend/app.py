import gradio as gr
import fitz
from gtts import gTTS
import uuid

def process_pdf(pdf_file):
    doc = fitz.open(pdf_file.name)
    full_text = ""

    print("Total pages:", len(doc))

    for page_number, page in enumerate(doc, start=1):
        page_text = page.get_text().strip()
        full_text += f"\n\nPage {page_number}:\n{page_text}"

    if len(full_text.strip()) == 0:
        return "No readable text found in PDF.", None

    audio_file = f"{uuid.uuid4()}.mp3"
    tts = gTTS(full_text)
    tts.save(audio_file)

    return full_text, audio_file


# 🎨 Simple minimal CSS
css = """
.container {
    max-width: 800px;
    margin: auto;
}

.title {
    text-align: center;
    font-size: 28px;
    font-weight: 600;
}

.subtitle {
    text-align: center;
    font-size: 14px;
    color: #555;
    margin-bottom: 15px;
}

.card {
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
}

button {
    border-radius: 6px !important;
}
"""

# 🧱 Simple UI Layout
with gr.Blocks(css=css) as ui:
    with gr.Column(elem_classes="container"):
        gr.Markdown("📄 **PDF Audio Reader**", elem_classes="title")
        gr.Markdown(
            "Upload a PDF to extract text and generate audio.",
            elem_classes="subtitle"
        )

        with gr.Column(elem_classes="card"):
            pdf_input = gr.File(
                label="Upload PDF",
                file_types=[".pdf"]
            )

            generate_btn = gr.Button("Convert")

            text_output = gr.Textbox(
                label="Extracted Text",
                lines=10
            )

            audio_output = gr.Audio(
                label="Audio Output",
                type="filepath"
            )

        generate_btn.click(
            fn=process_pdf,
            inputs=pdf_input,
            outputs=[text_output, audio_output]
        )

ui.launch()
