#-----------------------COnverting pdf and docx to raw text--------------
import pdfplumber
from docx import Document

def extract_text_from_pdf(file):
    text=""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text  

def extract_text_from_docx(file):
    text=""
    doc = Document(file)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text          

#--------------------------Building Skill extractor-----------------------

# from utils import clean_text

# def load_skill_database():
#     with open("skill_database/skills.txt","r") as file:
#         skills = [line.strip().lower() for line in file]
#         print(skills)
#     return skills

# def extract_skills(text):
#     cleaned_text = clean_text(text)
#     skills = load_skill_database()
#     extracted_skills = []

#     for skill in skills:
#         if skill in cleaned_text:
#             extracted_skills.append(skill)
#     return list(set(extracted_skills))        









