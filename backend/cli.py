import sys
from fetcher import fetch_papers
from summarizer import summarize_abstract
from downloader import download_paper
from session import Session
from config import MAX_RESULTS_PER_PAGE

def print_papers(papers, session):
    for i, paper in enumerate(papers, 1):
        selected_mark = "[*]" if session.is_selected(paper['link']) else "[ ]"
        print(f"{selected_mark} {i}. {paper['title']}")
        quick_sum = summarize_abstract(paper["summary"], quick=True)
        print(f"    Quick summary: {quick_sum}\n")

def print_selected(session):
    selected = session.list_selected()
    if not selected:
        print("No papers selected yet.")
        return
    print("\n--- Selected Papers ---")
    for i, paper in enumerate(selected, 1):
        print(f"{i}. {paper['title']} ({paper['link']})")
    print(f"Total selected: {len(selected)}\n")

def cli_loop():
    print("Welcome to the interactive arXiv fetcher & downloader! 🚀")
    topic = input("Enter your main topic: ").strip()
    keywords = input("Enter keywords (comma separated): ").strip().split(",")
    keywords = [k.strip() for k in keywords if k.strip()]
    category = input("Optional arXiv category code (e.g. cs.CL) or press Enter to skip: ").strip() or None
    max_per_page = MAX_RESULTS_PER_PAGE

    session = Session(topic, keywords, category, max_per_page)

    while True:
        # Load current page papers
        if session.current_page not in session.papers_cache:
            start_index = session.current_page * max_per_page
            papers = fetch_papers(topic, keywords, start=start_index, max_results=max_per_page, category=category)
            if not papers:
                print("No more papers found.")
                if session.current_page > 0:
                    session.current_page -= 1
                else:
                    print("No papers at all, exiting.")
                    sys.exit(0)
            else:
                session.add_papers(session.current_page, papers)

        papers = session.get_papers(session.current_page)
        print(f"\n--- Page {session.current_page + 1} ---")
        print_papers(papers, session)

        print("Commands:")
        print("  select <num1,num2,...>   - Select papers by numbers")
        print("  deselect <num1,num2,...> - Deselect papers by numbers")
        print("  details <num>            - Show full summary of a paper")
        print("  list_selected            - List selected papers")
        print("  download_selected        - Download all selected papers")
        print("  next                    - Next page")
        print("  prev                    - Previous page")
        print("  exit                    - Quit")

        cmd = input("Enter command: ").strip().lower()
        if not cmd:
            continue

        parts = cmd.split()
        action = parts[0]

        if action == "select" and len(parts) > 1:
            nums = parts[1].split(",")
            for n in nums:
                if n.isdigit():
                    idx = int(n) - 1
                    if 0 <= idx < len(papers):
                        paper = papers[idx]
                        session.select_paper(paper)
                        print(f"Selected: {paper['title']}")
                    else:
                        print(f"Invalid paper number: {n}")
                else:
                    print(f"Invalid input: {n}")

        elif action == "deselect" and len(parts) > 1:
            nums = parts[1].split(",")
            for n in nums:
                if n.isdigit():
                    idx = int(n) - 1
                    if 0 <= idx < len(papers):
                        paper = papers[idx]
                        session.deselect_paper(paper['link'])
                        print(f"Deselected: {paper['title']}")
                    else:
                        print(f"Invalid paper number: {n}")
                else:
                    print(f"Invalid input: {n}")

        elif action == "details" and len(parts) == 2:
            n = parts[1]
            if n.isdigit():
                idx = int(n) - 1
                if 0 <= idx < len(papers):
                    paper = papers[idx]
                    print(f"\n--- Details for '{paper['title']}' ---")
                    print(paper['summary'])
                else:
                    print("Invalid paper number.")
            else:
                print("Invalid input.")

        elif action == "list_selected":
            print_selected(session)

        elif action == "download_selected":
            selected = session.list_selected()
            if not selected:
                print("No papers selected to download.")
            else:
                for paper in selected:
                    download_paper(paper['link'])
                print(f"Downloaded {len(selected)} papers.")

        elif action == "next":
            session.current_page += 1

        elif action == "prev":
            if session.current_page > 0:
                session.current_page -= 1
            else:
                print("Already at first page.")

        elif action == "exit":
            print("Exiting. Goodbye!")
            sys.exit(0)

        else:
            print("Unknown command. Try again.")

if __name__ == "__main__":
    cli_loop()
