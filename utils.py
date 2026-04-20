import fitz
import re
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from deep_translator import GoogleTranslator

os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"
os.environ["USE_TORCH"] = "1"

# loading the model

model_name = "sshleifer/distilbart-cnn-12-6"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

summarizer = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer
)

# this is to extract the text from the pdf


def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in doc:
        text += page.get_text("text")

    return clean_text(text)

# this remove tha extra spacing and etc .


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    return text.strip()

# here we do chunking process of the pdf t0 generate chunks


def chunk_text(text, max_words=700):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks

# chunk summarization happens here


def summarize_chunk(chunk):
    try:
        summary = summarizer(
            chunk[:1000],
            max_length=130,
            min_length=40,
            do_sample=False
        )
        return summary[0]['summary_text']
    except:
        return ""


def generate_summary(text):
    chunks = chunk_text(text, max_words=700)

    chunk_summaries = []

    for chunk in chunks:
        chunk = chunk[:1000]

        summary = summarizer(
            chunk,
            max_length=130,
            min_length=40,
            do_sample=False
        )[0]['generated_text']

        chunk_summaries.append(summary)

    combined = " ".join(chunk_summaries)

    final = summarizer(
        combined[:1000],
        max_length=200,
        min_length=80,
        do_sample=False
    )[0]['generated_text']

    return final


def limit_words(text, max_words=500):
    words = text.split()
    return " ".join(words[:max_words])

# google translator dor hindi translation


def translate_to_hindi(text):
    try:
        return GoogleTranslator(source='en', target='hi').translate(text)
    except:
        return "Translation Error"
