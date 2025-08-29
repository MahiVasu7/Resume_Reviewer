# src/scorer.py
from src.readability import get_readability_score
from src.keywords import count_keywords
from src.formatting import check_formatting

def score_resume(text: str, required_keywords: list) -> dict:
    """
    Score resume based on readability, keywords, and formatting.
    Returns a dictionary with scores and metrics.
    """
    readability = get_readability_score(text)
    keywords_count = count_keywords(text, required_keywords)
    formatting_issues = check_formatting(text)

    return {
        'readability_score': readability,
        'keywords_count': keywords_count,
        'formatting_issues': formatting_issues
    }
