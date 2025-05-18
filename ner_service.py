import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from config.settings import MODEL_NAME

class NerService:
    def __init__(self):
        self.model = AutoModelForTokenClassification.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="cpu"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.pipeline = pipeline("ner", model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")

    def predict(self, text: str) -> list:
        return self.pipeline(text)