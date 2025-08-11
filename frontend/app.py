import streamlit as st
from fetch_papers import fetch_arxiv_papers
from summarize import summarize_text
from rag_pipeline import rag_query
from compare_papers import compare_papers

st.title("📚 AI Research Co-Pilot")

tab1, tab2, tab3 = st.tabs(["Search & Summarize", "Ask a Question", "Compare Papers"])

with tab1:
    topic = st.text_input("Enter research topic:")
    if st.button("Fetch Papers"):
        papers = fetch_arxiv_papers(topic)
        for p in papers:
            st.subheader(p["title"])
            st.write(summarize_text(p["summary"]))

with tab2:
    q = st.text_input("Ask a question about stored papers:")
    if st.button("Get Answer"):
        st.write(rag_query(q))

with tab3:
    p1 = st.text_area("Paste abstract of Paper 1")
    p2 = st.text_area("Paste abstract of Paper 2")
    if st.button("Compare"):
        st.write(compare_papers(p1, p2))
 