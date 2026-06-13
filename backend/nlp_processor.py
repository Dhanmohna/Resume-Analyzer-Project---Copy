import spacy

#loading english model
nlp = spacy.load("en_core_web_md")

# List of symbols often found in tech skills
tech_symbols = ['+', '#', '.', '-'] 

def clean_text(text):
    doc = nlp(text)
    cleaned_tokens = []

    for token in doc:
        # 1. Standard filters (Remove stop words, spaces, and pure punctuation like commas)
        if token.is_stop or token.is_space:
            continue
            
        # 2. Logic to SAVE technical terms like Node.js, C++, C#
        text_val = token.text.lower()
        
        # Check if the token is alphabetic OR if it contains a technical symbol
        # We check is_punct carefully because we want to remove "," but keep "++"
        if token.is_alpha or any(symbol in text_val for symbol in tech_symbols):
            # We use .text instead of .lemma_ for these symbols 
            # because sometimes lemmatization breaks "C++" into "c"
            cleaned_tokens.append(text_val)
        print(cleaned_tokens)   

    return cleaned_tokens