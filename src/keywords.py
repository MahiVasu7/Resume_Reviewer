# src/keywords.py
import re

def count_keywords(text: str, keywords: list) -> int:
    """
    Count how many of the given keywords appear in the text.
    """
    text_lower = text.lower()
    count = 0
    for kw in keywords:
        # simple exact match
        if re.search(rf"\b{re.escape(kw.lower())}\b", text_lower):
            count += 1
    return count
