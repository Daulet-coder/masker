import os
import cv2
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from docx import Document
from config.settings import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(Image.fromarray(gray), lang='eng+rus+kaz')

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, 300)
    return "\n".join(pytesseract.image_to_string(page, lang='eng+rus+kaz') for page in pages)

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(file_path)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    return ""
