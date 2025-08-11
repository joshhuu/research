import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://export.arxiv.org/api/query"
DOWNLOAD_DIR = "papers"
MAX_RESULTS_PER_PAGE = 5

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USER_AGENT = "MyResearchBot/0.1 (mailto:your_email@example.com)"
