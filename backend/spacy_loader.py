import spacy

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        # 'sm' is crucial for 512MB memory limits
        _nlp = spacy.load("en_core_web_sm")
    return _nlp