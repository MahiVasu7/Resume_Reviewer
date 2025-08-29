# src/main.py

import re
import os
import glob
import csv
from src.skills_match import exact_match, semantic_match
from src.extract_text import extract_skills_from_resume, read_resume
from src.preprocess import clean_text
from src.scorer import score_resume
from src.feedback import generate_feedback

# -------------------------
# Configurable Weights
# -------------------------
WEIGHTS = {"skills": 0.7, "readability": 0.3}

# -------------------------
# File Paths
# -------------------------
resume_folder = "samples/resumes"    # folder containing resumes
job_file = "samples/JDS/job_description1.txt"
output_file = "outputs/resume_review_results.csv"

# -------------------------
# Helper function: Accuracy
# -------------------------
def compute_accuracy(resume_skills, job_skills):
    if not job_skills:
        return 0.0
    exact = set(s.lower() for s in resume_skills).intersection(
        s.lower() for s in job_skills
    )
    return round(len(exact) / len(job_skills) * 100, 2)

# -------------------------
# Clean job skills
# -------------------------
def clean_job_skills(job_text):
    job_text = re.sub(r"[.:]", "", job_text)  # remove punctuation
    skills = [s.strip() for s in re.split(r",|\n", job_text) if s.strip()]
    skills = [s for s in skills if len(s.split()) <= 3]  # filter long phrases
    return skills

# -------------------------
# Normalize skills
# -------------------------
def normalize_skills(skills):
    return sorted(set(s.strip().capitalize() for s in skills if s.strip()))

# -------------------------
# Display results in column format
# -------------------------
def print_column(title, items):
    print(f"{title:<25}: ", end="")
    if isinstance(items, list):
        print(", ".join(items))
    else:
        print(items)

# -------------------------
# Main function
# -------------------------
def process_resumes():
    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Read and clean job description
    try:
        job_text = read_resume(job_file)
    except FileNotFoundError:
        print(f"❌ Job description file not found: {job_file}")
        return

    job_text = clean_text(job_text)
    job_skills = normalize_skills(clean_job_skills(job_text))

    # Prepare CSV output
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "Resume File",
            "Resume Skills",
            "Job Skills",
            "Exact Match",
            "Semantic Match",
            "Skill Match Accuracy (%)",
            "Missing Skills",
            "Readability Score",
            "Final Resume-Job Fit (%)",
            "Feedback",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Loop over all resumes in folder
        for resume_file in glob.glob(os.path.join(resume_folder, "*")):
            print(f"\n=== Processing: {resume_file} ===\n")

            try:
                resume_skills = extract_skills_from_resume(resume_file)
            except FileNotFoundError:
                print(f"❌ Resume file not found: {resume_file}")
                continue

            resume_skills = normalize_skills(resume_skills)

            # Skill matching
            exact = exact_match(resume_skills, job_skills)
            semantic = semantic_match(resume_skills, job_skills)

            # Accuracy
            skill_accuracy = compute_accuracy(resume_skills, job_skills)

            # Resume scoring + feedback
            text_content = read_resume(resume_file)
            resume_scores = score_resume(text_content, job_skills)
            resume_feedback = generate_feedback(resume_scores)

            readability_score = resume_scores.get("readability_score", 50)
            final_fit = round(
                WEIGHTS["skills"] * skill_accuracy
                + WEIGHTS["readability"] * readability_score,
                2,
            )

            # Suggestions for missing skills
            missing_skills = set(s.lower() for s in job_skills) - set(
                s.lower() for s in resume_skills
            )
            skill_suggestions = [s.title() for s in missing_skills]

            # Print to console
            print_column("Resume Skills", resume_skills)
            print_column("Job Skills", job_skills)
            print_column("Exact Match", exact)
            print_column("Semantic Match", semantic)
            print_column("Skill Match Accuracy (%)", skill_accuracy)
            print_column("Missing Skills", skill_suggestions)
            print_column(
                "Resume Scores", [f"{k}: {v}" for k, v in resume_scores.items()]
            )
            print_column("Feedback", resume_feedback)
            print_column("Final Resume-Job Fit (%)", final_fit)
            print("\n====================\n")

            # Save to CSV
            writer.writerow(
                {
                    "Resume File": os.path.basename(resume_file),
                    "Resume Skills": ", ".join(resume_skills),
                    "Job Skills": ", ".join(job_skills),
                    "Exact Match": ", ".join(exact),
                    "Semantic Match": ", ".join(semantic),
                    "Skill Match Accuracy (%)": skill_accuracy,
                    "Missing Skills": ", ".join(skill_suggestions),
                    "Readability Score": readability_score,
                    "Final Resume-Job Fit (%)": final_fit,
                    "Feedback": "; ".join(resume_feedback),
                }
            )

    print(f"\n✅ Results saved to: {output_file}\n")

# -------------------------
# Run script
# -------------------------
if __name__ == "__main__":
    process_resumes()
