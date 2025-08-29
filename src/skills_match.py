# src/skills_match.py
import spacy

# Load SpaCy medium English model
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

def exact_match(resume_skills, job_skills):
    """
    Compare skills using exact string matching.
    """
    resume_set = set([skill.lower() for skill in resume_skills])
    job_set = set([skill.lower() for skill in job_skills])
    matched_skills = resume_set.intersection(job_set)
    return list(matched_skills)

def semantic_match(resume_skills, job_skills, threshold=0.75):
    """
    Compare skills using semantic similarity (SpaCy vectors).
    Returns skills from resume that are semantically similar to job skills.
    """
    matched_skills = []
    job_docs = [nlp(skill.lower()) for skill in job_skills]

    for r_skill in resume_skills:
        r_doc = nlp(r_skill.lower())
        if r_doc.vector_norm == 0:
            continue
        for j_doc in job_docs:
            if j_doc.vector_norm == 0:
                continue
            if r_doc.similarity(j_doc) >= threshold:
                matched_skills.append(r_skill)
                break

    return list(set(matched_skills))  # Remove duplicates
