import spacy
import gc # Import garbage collector

# 1. Do NOT load the model here! 
# nlp = spacy.load("en_core_web_md") 

_nlp = None

def get_nlp():
    """Lazy loader: loads model only when needed."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_md")
    return _nlp

# List of symbols kept outside to avoid re-declaring
tech_symbols = ['+', '#', '.', '-'] 

def clean_text(text):
    # 2. Load model only when processing starts
    nlp = get_nlp() 
    doc = nlp(text)
    cleaned_tokens = []

    for token in doc:
        if token.is_stop or token.is_space:
            continue
            
        text_val = token.text.lower()
        
        if token.is_alpha or any(symbol in text_val for symbol in tech_symbols):
            cleaned_tokens.append(text_val)

    # 3. Explicitly clear the doc object from memory after processing
    del doc
    # Force garbage collection to free the memory used by the processed doc
    gc.collect() 
    
    return cleaned_tokens