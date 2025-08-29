# src/readability.py
from textstat import flesch_reading_ease

def get_readability_score(text: str) -> float:
    """
    Compute the Flesch Reading Ease score for the resume text.
    Higher score = easier to read.
    """
    return flesch_reading_ease(text)
