# src/extract_text.py
import os
import re
import docx2txt
from PyPDF2 import PdfReader
import spacy
from sentence_transformers import SentenceTransformer, util
from src.skills_db import ALL_SKILLS, ALIASES

nlp = spacy.load("en_core_web_sm")

# Load embeddings model
model = SentenceTransformer("all-MiniLM-L6-v2")

def read_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower().strip()

    if ext == ".pdf":
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif ext == ".docx":
        return docx2txt.process(file_path)

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    else:
        raise ValueError(f"Unsupported file format: {ext}. Please upload .txt, .pdf, or .docx")

def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()
    return ALIASES.get(skill, skill)

def extract_skills_from_resume(text):
    text = text.lower()
    doc = nlp(text)
    found_skills = set()

    # Token-based
    for token in doc:
        norm = normalize_skill(token.text)
        if norm in ALL_SKILLS:
            found_skills.add(norm)

    # Phrase-based
    for phrase in ALL_SKILLS:
        if phrase in text:
            found_skills.add(normalize_skill(phrase))

    return list(found_skills)

# ---------------- EDUCATION EXTRACTION ---------------- #

EDU_KEYWORDS = {
    "bachelor": ["bachelor", "b.sc", "btech", "b.tech", "bca", "bba", "undergraduate"],
    "master": ["master", "m.sc", "mtech", "m.tech", "mca", "mba", "postgraduate"],
    "phd": ["phd", "doctorate", "doctoral"]
}

STREAM_KEYWORDS = [
    "computer science", "information technology", "it",
    "electronics", "mechanical", "civil", "electrical",
    "commerce", "arts", "engineering"
]

def extract_education(text):
    """Extracts education qualifications (degree level + stream)."""
    text = text.lower()
    found = {"bachelor": False, "master": False, "phd": False, "streams": []}

    # Detect degree level
    for level, keywords in EDU_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                found[level] = True

    # Detect streams
    for stream in STREAM_KEYWORDS:
        if stream in text:
            found["streams"].append(stream)

    return found

def compare_education(resume_edu, jd_edu):
    """Compare resume vs JD education with flexibility for graduate/postgraduate levels."""
    matched = []
    missing = []

    # Degree level check
    for level in ["bachelor", "master", "phd"]:
        if jd_edu[level]:
            if resume_edu[level]:
                matched.append(level)
            else:
                missing.append(level)

    # Stream check
    if jd_edu["streams"]:
        for stream in jd_edu["streams"]:
            if stream in resume_edu["streams"]:
                matched.append(stream)
            else:
                missing.append(stream)

    return matched, missing

# ---------------- SEMANTIC MATCH ---------------- #

def semantic_match(resume_skills, jd_skills, threshold=0.75):
    """Use embeddings to find semantically close skills."""
    if not resume_skills or not jd_skills:
        return [], jd_skills

    resume_emb = model.encode(resume_skills, convert_to_tensor=True)
    jd_emb = model.encode(jd_skills, convert_to_tensor=True)

    matched = []
    missing = jd_skills.copy()

    cos_scores = util.cos_sim(jd_emb, resume_emb)  # JD x Resume
    for i, jd_skill in enumerate(jd_skills):
        best_match_idx = cos_scores[i].argmax().item()
        best_score = cos_scores[i][best_match_idx].item()
        if best_score >= threshold:
            matched.append(jd_skill)
            if jd_skill in missing:
                missing.remove(jd_skill)

    return matched, missing

# ---------------- SUGGESTIONS ---------------- #

def generate_suggestions(missing_skills, edu_missing):
    suggestions = []
    if missing_skills:
        suggestions.append(f"Consider learning or highlighting these missing skills: {', '.join(missing_skills)}")
    if edu_missing:
        suggestions.append(f"Education gap: The job expects {', '.join(edu_missing)}.")
    if not suggestions:
        suggestions.append("Great! Your resume aligns very well with the JD.")
    return suggestions

def calculate_score(matched, jd_total):
    if jd_total == 0:
        return 100
    return round((len(matched) / jd_total) * 100, 2)
