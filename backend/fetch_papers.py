import os
import feedparser
import requests
from summarize import summarize_abstract
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://export.arxiv.org/api/query"
DOWNLOAD_DIR = "papers"

def build_search_query(topic, keywords, category=None):
    topic_part = f"all:({topic.strip().replace(' ', '+')})"
    keywords_str = " OR ".join(k.strip().replace(" ", "+") for k in keywords)
    keywords_part = f"({keywords_str})"
    query = f"{topic_part}+AND+{keywords_part}"
    if category:
        query += f"+AND+cat:{category.strip()}"
    return query

def fetch_papers(topic, keywords, max_results=5, sort_by="submittedDate", sort_order="descending", category=None):
    query_param = build_search_query(topic, keywords, category)
    url = f"{BASE_URL}?search_query={query_param}&start=0&max_results={max_results}&sortBy={sort_by}&sortOrder={sort_order}"

    print(f"🔍 Fetching from: {url}")

    headers = {"User-Agent": "MyResearchBot/0.1 (mailto:your_email@example.com)"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ HTTP Error: {response.status_code}")
        return []

    feed = feedparser.parse(response.text)
    if not feed.entries:
        print("⚠️ No papers found. Try different keywords or category.")
        return []

    papers = []
    for entry in feed.entries:
        title = entry.title.strip()
        summary = entry.summary.strip()
        link = entry.link

        quick_summary = summarize_abstract(summary, quick=True)

        print(f"✅ Found: {title}")
        print(f"   📝 Quick Summary: {quick_summary}\n")

        papers.append({
            "title": title,
            "summary": summary,
            "link": link,
            "quick_summary": quick_summary
        })

    return papers

def download_paper(paper_link, download_dir=DOWNLOAD_DIR):
    # arXiv PDF link construction: replace /abs/ with /pdf/
    pdf_url = paper_link.replace("/abs/", "/pdf/") + ".pdf"
    print(f"⬇️ Downloading PDF from: {pdf_url}")

    response = requests.get(pdf_url)
    if response.status_code != 200:
        print(f"❌ Failed to download {pdf_url} (status: {response.status_code})")
        return False

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Use paper ID as filename (last part of URL after /abs/)
    paper_id = paper_link.split("/")[-1]
    file_path = os.path.join(download_dir, f"{paper_id}.pdf")

    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved: {file_path}")
    return True

if __name__ == "__main__":
    print("Welcome to the arXiv paper fetcher & downloader! 🚀")
    topic = input("Enter your main topic (e.g., natural language processing): ").strip()
    keywords_input = input("Enter keywords (comma separated, e.g., deep learning, transformer, nlp): ").strip()
    keywords = [k for k in keywords_input.split(",") if k.strip()]
    category = input("Optional - Enter arXiv category code (e.g., cs.CL) or press Enter to skip: ").strip() or None
    max_results = input("How many papers do you want to fetch? (default 5): ").strip()
    max_results = int(max_results) if max_results.isdigit() else 5

    results = fetch_papers(topic, keywords, max_results=max_results, category=category)

    print(f"\n📄 Total Papers Found: {len(results)}")
    for i, paper in enumerate(results, 1):
        print(f"{i}. {paper['title']}")
        print(f"   Link: {paper['link']}")
        print(f"   Quick Summary: {paper['quick_summary']}\n")

    if results:
        selection = input("Enter paper numbers to download (comma separated, e.g. 1,3) or press Enter to skip: ").strip()
        if selection:
            selected_indices = []
            for part in selection.split(","):
                if part.strip().isdigit():
                    idx = int(part.strip())
                    if 1 <= idx <= len(results):
                        selected_indices.append(idx - 1)
                    else:
                        print(f"⚠️ Invalid paper number ignored: {idx}")
                else:
                    print(f"⚠️ Invalid input ignored: {part}")

            for idx in selected_indices:
                paper = results[idx]
                download_paper(paper['link'])
        else:
            print("No papers selected for download. Exiting.")
    else:
        print("No papers fetched, nothing to download.")
