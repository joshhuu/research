import streamlit as st
from fetcher import fetch_papers
from downloader import download_paper
from summarizer import summarize_abstract
from session import Session

st.title("Interactive arXiv Paper Fetcher & Downloader 🚀")

# Input widgets (no default text so user can type fresh)
topic = st.sidebar.text_input("Main Topic", st.session_state.get('topic', ''))
keywords_input = st.sidebar.text_input("Keywords (comma separated)", st.session_state.get('keywords_input', ''))
category = st.sidebar.text_input("arXiv Category (optional)", st.session_state.get('category', ''))
max_results = st.sidebar.number_input("Papers per page", min_value=1, max_value=20, value=st.session_state.get('max_results', 5))

# When user clicks this, we initialize/fetch
if st.sidebar.button("Fetch Papers"):
    # Save inputs to session state
    st.session_state.topic = topic
    st.session_state.keywords_input = keywords_input
    st.session_state.category = category
    st.session_state.max_results = max_results

    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    st.session_state.session = Session(topic, keywords, category or None, max_results)
    st.session_state.summary_cache = {}
    st.session_state.papers_fetched = False
    st.session_state.current_page = 0

# Only fetch papers if user has clicked fetch before
if st.session_state.get('session') and st.session_state.get('topic') and not st.session_state.get('papers_fetched', False):
    session = st.session_state.session
    keywords = [k.strip() for k in st.session_state.keywords_input.split(",") if k.strip()]
    start_idx = st.session_state.current_page * st.session_state.max_results
    papers = fetch_papers(st.session_state.topic, keywords, start=start_idx, max_results=st.session_state.max_results, category=st.session_state.category or None)
    if papers:
        session.add_papers(st.session_state.current_page, papers)
        st.session_state.papers_fetched = True
    else:
        st.warning("No more papers found.")

# Now load papers from cache if session exists
if 'session' in st.session_state:
    session = st.session_state.session
    papers = session.get_papers(st.session_state.current_page)
else:
    st.info("Please enter your search parameters and click 'Fetch Papers' on the sidebar.")
    st.stop()

st.write(f"### Page {st.session_state.current_page + 1}")

# Display papers with selection and details
for i, paper in enumerate(papers, 1):
    selected = session.is_selected(paper['link'])
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        checked = st.checkbox("", value=selected, key=f"select_{paper['link']}")
    with col2:
        st.write(f"**{i}. {paper['title']}**")
        # Use cached summary or summarize now
        if paper['link'] in st.session_state.summary_cache:
            quick_sum = st.session_state.summary_cache[paper['link']]
        else:
            quick_sum = summarize_abstract(paper['summary'], quick=True)
            st.session_state.summary_cache[paper['link']] = quick_sum

        st.write(f"*Quick summary:* {quick_sum}")
        with st.expander("Show full summary"):
            st.write(paper['summary'])

    # Update selection state if checkbox changed
    if checked and not selected:
        session.select_paper(paper)
    elif not checked and selected:
        session.deselect_paper(paper['link'])

# Pagination buttons
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("Previous Page") and st.session_state.current_page > 0:
        st.session_state.current_page -= 1
        st.session_state.papers_fetched = False  # trigger refetch on page change
with col_next:
    if st.button("Next Page"):
        st.session_state.current_page += 1
        st.session_state.papers_fetched = False  # trigger refetch on page change

# Selected papers list
st.write("### Selected Papers")
selected = session.list_selected()
if not selected:
    st.write("No papers selected yet.")
else:
    for paper in selected:
        st.write(f"- [{paper['title']}]({paper['link']})")

# Download button
if st.button("Download Selected Papers"):
    for paper in selected:
        download_paper(paper['link'])
    st.success(f"Downloaded {len(selected)} papers.")
