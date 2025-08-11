import os
import requests
from config import DOWNLOAD_DIR

def download_paper(paper_link):
    pdf_url = paper_link.replace("/abs/", "/pdf/") + ".pdf"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    paper_id = paper_link.split("/")[-1]
    file_path = os.path.join(DOWNLOAD_DIR, f"{paper_id}.pdf")

    if os.path.exists(file_path):
        print(f"📄 Already downloaded: {file_path}")
        return file_path

    print(f"⬇️ Downloading {pdf_url}...")
    r = requests.get(pdf_url)
    r.raise_for_status()
    with open(file_path, "wb") as f:
        f.write(r.content)
    print(f"✅ Saved: {file_path}")
    return file_path
