import fitz
import docx
from transformers import pipeline
from deep_translator import GoogleTranslator

# ---------------- CLEAN TEXT ----------------


def clean_text(text):
    text = " ".join(text.split())
    text = text.replace(" ,", ",").replace(" .", ".")
    return text

# ---------------- EXTRACT TEXT ----------------


def extract_text(file, file_type):
    text = ""

    if file_type == "txt":
        text = file.read().decode("utf-8")

    elif file_type == "pdf":
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()

    elif file_type == "docx":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return clean_text(text)


# ---------------- LOAD MODEL ----------------
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# ---------------- SUMMARIZATION ----------------


def summarize_text(text):
    # limit by words (NOT characters)
    words = text.split()
    words = words[:800]   # safe limit

    text = " ".join(words)

    summary = summarizer(
        text,
        max_length=600,
        min_length=300,
        do_sample=False
    )

    return summary[0]['summary_text']
# ---------------- TRANSLATION ----------------


def translate_to_hindi(text):
    return GoogleTranslator(source='auto', target='hi').translate(text)
