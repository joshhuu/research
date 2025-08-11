class Session:
    def __init__(self, topic, keywords, category, max_results_per_page):
        self.topic = topic
        self.keywords = keywords
        self.category = category
        self.max_results_per_page = max_results_per_page

        self.papers_cache = {}  # page_num -> list of papers
        self.selected_papers = {}  # paper_link -> paper info
        self.current_page = 0

    def add_papers(self, page_num, papers):
        self.papers_cache[page_num] = papers

    def get_papers(self, page_num):
        return self.papers_cache.get(page_num, [])

    def select_paper(self, paper):
        self.selected_papers[paper['link']] = paper

    def deselect_paper(self, paper_link):
        if paper_link in self.selected_papers:
            del self.selected_papers[paper_link]

    def is_selected(self, paper_link):
        return paper_link in self.selected_papers

    def list_selected(self):
        return list(self.selected_papers.values())

    def clear_selection(self):
        self.selected_papers = {}

    def total_selected(self):
        return len(self.selected_papers)
