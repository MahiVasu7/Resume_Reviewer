# app.py
import os
from flask import Flask, render_template, request
from src.extract_text import read_resume, extract_skills_from_resume, semantic_match, extract_education
from src.skills_db import ALL_SKILLS

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("resume")
        jd_text = request.form.get("job_description", "").strip()

        if not jd_text:
            return "Job description is required!", 400
        if not file:
            return "Resume file is required!", 400

        # Save uploaded file
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        try:
            # Extract resume text
            resume_text = read_resume(file_path)

            # Extract skills
            resume_skills = extract_skills_from_resume(resume_text)
            jd_skills = extract_skills_from_resume(jd_text)

            # Semantic skill matching
            matched, missing = semantic_match(resume_skills, jd_skills)

            # Education extraction & matching
            resume_edu = extract_education(resume_text)
            jd_edu = extract_education(jd_text)

            edu_match = False
            if jd_edu and resume_edu:
                # Example logic: if JD requires "graduate", allow BSc, B.Tech etc.
                for req in jd_edu:
                    for edu in resume_edu:
                        if req in edu or edu in req:
                            edu_match = True
                            break

            # Calculate Resume Score
            score = (len(matched) / max(1, len(jd_skills))) * 100
            score = round(score, 2)

            # Suggestions
            suggestions = []
            if score < 50:
                suggestions.append("Your resume is missing many required skills. Consider adding relevant projects or certifications.")
            elif score < 80:
                suggestions.append("Good match! But you can improve by highlighting missing skills in projects or summary.")
            else:
                suggestions.append("Excellent match! Your resume is highly aligned with the job description.")

            if not edu_match and jd_edu:
                suggestions.append("Your education does not fully match the requirements mentioned in the JD.")

            return render_template(
                "result.html",
                resume_skills=resume_skills,
                job_skills=jd_skills,
                matched=matched,
                missing=missing,
                resume_edu=resume_edu,
                jd_edu=jd_edu,
                score=score,
                suggestions=suggestions
            )

        except Exception as e:
            return f"Error processing resume: {str(e)}", 500

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
