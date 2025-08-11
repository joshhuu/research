import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_abstract(abstract, quick=False):
    """
    Summarizes an abstract.
    - If quick=True → short 1–2 sentence (<30 words) screening summary.
    - If quick=False → fuller bullet-point style breakdown.
    """
    if not abstract.strip():
        return "No abstract provided."

    if quick:
        prompt = (
            "Summarize the following research paper abstract in 1–2 sentences "
            "under 30 words, focusing only on the core topic and contribution:\n\n"
            f"{abstract}"
        )
    else:
        prompt = (
            "Summarize the following research paper abstract into concise bullet points "
            "covering the main problem, method, and result:\n\n"
            f"{abstract}"
        )

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Error generating summary: {str(e)}]"
