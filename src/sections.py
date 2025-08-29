# src/sections.py
import re
from collections import defaultdict

# Common section headers in resumes
SECTION_HEADERS = {
    "education": ["education", "academic background", "qualifications"],
    "experience": ["experience", "work history", "employment"],
    "skills": ["skills", "technical skills", "tools"],
    "projects": ["projects", "academic projects"],
    "certifications": ["certifications", "courses", "training"],
    "summary": ["summary", "profile", "objective"]
}

def detect_sections(text: str) -> dict:
    """
    Detect sections in resume text.
    Returns a dictionary {section_name: content}.
    """
    lines = text.split("\n")
    current_section = "other"
    sections = defaultdict(list)

    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue

        # Check for section header
        found_section = None
        for section, keywords in SECTION_HEADERS.items():
            for keyword in keywords:
                if re.search(rf"\b{keyword}\b", clean_line, re.IGNORECASE):
                    found_section = section
                    break
            if found_section:
                break

        if found_section:
            current_section = found_section
        else:
            sections[current_section].append(clean_line)

    # Join lines into text
    return {sec: "\n".join(content) for sec, content in sections.items()}
