from skills_db import SKILLS_DB

import re

def extract_skills(cleaned_tokens):
    # 1. Join tokens into a single searchable string
    text_content = " ".join([str(t).lower().strip() for t in cleaned_tokens])
    
    extracted_skills = []

    for skill in SKILLS_DB:
        skill_clean = skill.lower().strip()
        
        # 2. Use Regex Word Boundaries (\b)
        # This prevents 'c' from matching 'coding' and 'r' from matching 'react'
        # re.escape handles skills with symbols like 'c++' or '.net'
        pattern = rf"\b{re.escape(skill_clean)}\b"
        
        if re.search(pattern, text_content):
            extracted_skills.append(skill)
                
    return list(set(extracted_skills))