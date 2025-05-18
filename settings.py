import os

TESSERACT_PATH = r"C:\Users\Daulet\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
MODEL_NAME = "yeshpanovrustem/xlm-roberta-large-ner-kazakh"
TEMP_DIR = os.path.join(os.path.dirname(__file__), "../anonym")
OPENAI_API_KEY = "....(add yours)" 
OPENAI_CHAT_MODEL = "gpt-4o-mini"