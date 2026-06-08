import os
from dotenv import load_dotenv
from groq import Groq

# Ensure environment variables are parsed locally inside this module scope
load_dotenv()

def analyze_resume_with_groq(resume_text, target_role):
    print("\n🤖 [Groq Log 1] Entered analyze_resume_with_groq function successfully!")
    
    api_key = os.getenv("GROQ_API_KEY")
    print(f"🤖 [Groq Log 2] Checking API Key status... Extracted prefix: {api_key[:10] if api_key else '❌ NONE'}")
    
    if not api_key:
        print("❌ [Groq Log Error] Execution stopped because GROQ_API_KEY is missing from .env context.")
        return "⚠️ Error: GROQ_API_KEY is not configured on the backend server engine."

    prompt = f"""
    Analyze the following resume for the target role: {target_role}

    1. Suggest top 3 suitable job roles (including how they align with {target_role}).
    2. List important missing skills for a {target_role} position.
    3. Give 3 specific improvement suggestions for the resume text.

    Resume:
    {resume_text}   
    """

    try:
        print("🤖 [Groq Log 3] Initializing Groq client...")
        client = Groq(api_key=api_key)
        
        print("🤖 [Groq Log 4] Dispatching payload data to Groq Cloud (Waiting for response)...")
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional HR resume analyzer."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile", 
        )
        
        print("✅ [Groq Log 5] Response successfully received from Groq!")
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"❌ [Groq Log Error] API Pipeline crashed! Exception details: {str(e)}")
        if "429" in str(e):
            return "⚠️ Groq is temporarily busy (Rate Limit). Please wait 60 seconds and try again."
        return f"An error occurred during contextual analysis processing: {e}"