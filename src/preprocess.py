# src/preprocess.py
import re
import spacy

# Load English NLP model from spaCy
nlp = spacy.load("en_core_web_md")

def clean_text(text: str) -> str:
    """
    Clean the resume/job text:
    - Normalize line breaks
    - Remove extra blank lines
    - Remove extra spaces/tabs
    """
    text = text.replace('\r', '\n')
    text = re.sub(r'\n{2,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def sentences(text: str):
    """
    Split text into sentences using spaCy NLP.
    Returns a list of sentences.
    """
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]
