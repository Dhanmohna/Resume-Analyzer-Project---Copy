def calculate_skill_score(extracted_skills, required_skills):
    if not required_skills:
        return 0.0
    
    # Pre-process lists once to save CPU time
    extracted_lower = {s.lower().strip() for s in extracted_skills}
    required_lower = {s.lower().strip() for s in required_skills}
    
    # Calculate intersection
    matches = extracted_lower.intersection(required_lower)
    
    return (len(matches) / len(required_lower)) * 100

def calculate_resume_score(similarity_score, skill_score):
    # Your 60/40 split is great!
    return (0.6 * similarity_score) + (0.4 * skill_score)