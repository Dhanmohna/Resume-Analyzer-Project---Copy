import spacy

nlp = spacy.load("en_core_web_sm")

def calculate_similarity(resume_doc, job_description):
    """
    Pass the pre-processed resume_doc here instead of raw text 
    to avoid re-processing the resume 50 times in a loop.
    """
    job_doc = nlp(job_description)
    if not job_doc.vector_norm or not resume_doc.vector_norm:
        return 0.0
        
    similarity_score = resume_doc.similarity(job_doc)
    return round(similarity_score * 100, 2)