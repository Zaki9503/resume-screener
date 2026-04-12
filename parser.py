import pdfplumber
import PyPDF2
import pytesseract
from pdf2image import convert_from_bytes

# Windows path (edit if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_with_pdfplumber(file):
    text = ""
    try:
        file.seek(0)
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + " "
    except:
        pass
    return text


def extract_with_pypdf2(file):
    text = ""
    try:
        file.seek(0)
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + " "
    except:
        pass
    return text


def extract_with_ocr(file):
    text = ""
    try:
        file.seek(0)
        images = convert_from_bytes(
            file.read(),
            poppler_path=r"C:\poppler\Library\bin"
        )
        for img in images:
            text += pytesseract.image_to_string(img) + " "
    except Exception as e:
        print("OCR Error:", e)
    return text


def extract_text_from_pdf(file):
    text = extract_with_pdfplumber(file)

    if len(text.strip()) < 50:
        text = extract_with_pypdf2(file)

    if len(text.strip()) < 50:
        text = extract_with_ocr(file)

    return clean_resume_text(text)

import re

def clean_resume_text(text):
    text = text.lower()

    # remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # remove phone numbers / long numbers
    text = re.sub(r'\b\d{5,}\b', ' ', text)

    # remove symbols
    text = re.sub(r'[^a-zA-Z0-9+#.\s]', ' ', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()