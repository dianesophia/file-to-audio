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


# 🎨 Modern Premium UI Theme
css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif !important;
}

body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.gradio-container {
    max-width: 1000px !important;
    margin: 0 auto !important;
    padding: 40px 20px !important;
}

.container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.header {
    text-align: center;
    margin-bottom: 40px;
}

.title {
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
}

.subtitle {
    font-size: 18px;
    color: #64748b;
    font-weight: 400;
}

.upload-section {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 16px;
    padding: 32px;
    border: 2px dashed #cbd5e1;
    margin-bottom: 24px;
    transition: all 0.3s ease;
}

.upload-section:hover {
    border-color: #667eea;
    background: linear-gradient(135deg, #fefeff 0%, #f8fafc 100%);
}

.output-section {
    background: white;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    margin-top: 24px;
}

button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 14px 32px !important;
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(102, 126, 234, 0.5) !important;
}

button:active {
    transform: translateY(0);
}

.label {
    font-weight: 600 !important;
    font-size: 15px !important;
    color: #1e293b !important;
    margin-bottom: 12px !important;
}

textarea, .file-preview {
    border: 2px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
}

textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    outline: none !important;
}

.icon {
    font-size: 64px;
    margin-bottom: 16px;
}

audio {
    width: 100%;
    border-radius: 12px;
}

.footer {
    text-align: center;
    margin-top: 32px;
    color: #94a3b8;
    font-size: 14px;
}

/* File upload styling */
.file {
    min-height: 120px !important;
}

/* Smooth animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.container > * {
    animation: fadeIn 0.5s ease-out;
}
"""

# 🧱 UI Layout
with gr.Blocks(css=css, title="PDF Audio Reader") as ui:
    with gr.Column(elem_classes="container"):
        # Header
        with gr.Column(elem_classes="header"):
            gr.Markdown("🎧 PDF Audio Reader", elem_classes="title")
            gr.Markdown(
                "Transform your PDF documents into natural-sounding audio. Upload, extract, and listen.",
                elem_classes="subtitle"
            )
        
        # Upload Section
        with gr.Column(elem_classes="upload-section"):
            gr.Markdown("### 📄 Upload Your PDF")
            pdf_input = gr.File(
                label="Choose a PDF file",
                file_types=[".pdf"],
                elem_classes="file"
            )
            generate_btn = gr.Button("🎵 Generate Audio", size="lg")
        
        # Output Section
        with gr.Column(elem_classes="output-section"):
            gr.Markdown("### 📝 Extracted Content")
            text_output = gr.Textbox(
                label="Text from PDF",
                lines=12,
                placeholder="Your extracted text will appear here...",
                show_label=False
            )
            
            gr.Markdown("### 🔊 Audio Player", elem_classes="audio-header")
            audio_output = gr.Audio(
                label="Generated Audio",
                type="filepath",
                show_label=False
            )
        
        # Footer
        gr.Markdown(
            "Made with ❤️ using Gradio • Powered by gTTS",
            elem_classes="footer"
        )

        # Event Handler
        generate_btn.click(
            fn=process_pdf,
            inputs=pdf_input,
            outputs=[text_output, audio_output]
        )

ui.launch()