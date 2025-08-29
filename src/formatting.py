# src/formatting.py
import re

def check_formatting(text: str) -> dict:
    """
    Check for formatting issues:
    - Multiple consecutive spaces
    - Inconsistent bullet points
    Returns a dictionary with counts/issues.
    """
    issues = {}
    issues['extra_spaces'] = len(re.findall(r'  +', text))
    issues['bullet_points'] = len(re.findall(r'[\-\*\u2022]', text))
    return issues
