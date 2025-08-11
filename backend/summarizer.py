import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_abstract(abstract, quick=True):
    if quick:
        prompt = f"Summarize this abstract in 1-2 sentences under 30 words:\n\n{abstract}"
    else:
        prompt = f"Summarize this abstract in bullet points covering main problem, method, and results:\n\n{abstract}"
    response = model.generate_content(prompt)
    return response.text.strip()
