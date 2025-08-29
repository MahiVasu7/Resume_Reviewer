# src/feedback.py
def generate_feedback(scores: dict) -> list:
    """
    Generate textual feedback based on scoring metrics.
    """
    feedback = []

    # Readability
    if scores['readability_score'] < 60:
        feedback.append("Resume could be easier to read. Consider simplifying sentences.")

    # Keywords
    if scores['keywords_count'] == 0:
        feedback.append("Resume is missing important keywords from the job description.")

    # Formatting
    if scores['formatting_issues']['extra_spaces'] > 0:
        feedback.append("Resume has extra spaces that could be cleaned up.")
    if scores['formatting_issues']['bullet_points'] == 0:
        feedback.append("Consider using bullet points for clarity.")

    if not feedback:
        feedback.append("Resume looks good!")

    return feedback
