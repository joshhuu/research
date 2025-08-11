import requests
import feedparser
from config import BASE_URL, USER_AGENT

def build_search_query(topic, keywords, category=None):
    topic_part = f"all:({topic.strip().replace(' ', '+')})"
    keywords_str = " OR ".join(k.strip().replace(" ", "+") for k in keywords)
    keywords_part = f"({keywords_str})"
    query = f"{topic_part}+AND+{keywords_part}"
    if category:
        query += f"+AND+cat:{category.strip()}"
    return query

def fetch_papers(topic, keywords, start=0, max_results=5, sort_by="submittedDate", sort_order="descending", category=None):
    query_param = build_search_query(topic, keywords, category)
    url = f"{BASE_URL}?search_query={query_param}&start={start}&max_results={max_results}&sortBy={sort_by}&sortOrder={sort_order}"

    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    feed = feedparser.parse(response.text)
    papers = []
    for entry in feed.entries:
        papers.append({
            "title": entry.title.strip(),
            "summary": entry.summary.strip(),
            "link": entry.link
        })
    return papers
