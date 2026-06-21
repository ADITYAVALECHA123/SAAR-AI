import streamlit as st
from frontend.services.research_services import search_papers, summarize_paper, save_paper_library, ask_research_question
def render_research():
    st.markdown("## 🔍 Research Papers")
    query = st.text_input("🔍  Search papers…")
    source_filter = st.selectbox("Sources", ["arXiv"])
    sort_option=st.selectbox("Sort By", ["relevance", "title", "year"])
    if "research_results" not in st.session_state:
        st.session_state.research_results = []
    if "research_page" not in st.session_state:
        st.session_state.research_page = 1
    if "paper_summaries" not in st.session_state:
        st.session_state.paper_summaries = {}
    PAGE_SIZE = 5
    if st.button("Search"):
        if query.strip() == "":
            st.warning("Enter a query")
        else:
            with st.spinner("Searching..."):
                st.session_state.research_results = (search_papers(query=query, source=source_filter, sort_by=sort_option))
                st.session_state.research_page = 1
    start_idx = ((st.session_state.research_page - 1) * PAGE_SIZE)
    end_idx = start_idx + PAGE_SIZE
    if not isinstance(st.session_state.research_results, list):
        st.session_state.research_results = []
    papers_to_show = (st.session_state.research_results[start_idx:end_idx])
    for idx, paper in enumerate(papers_to_show):
        unique_id= f"{st.session_state.research_page}_{idx}"
        year = paper.get("year")
        source = paper.get("source", "Unknown")
        source_badge = {
            "arXiv": "📗 arXiv"
        }.get(source, f"📄 {source}")
        st.markdown(
            f"""
            <div class="card">
                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    margin-bottom:.5rem ">
                    <div style="
                        font-weight:600;
                        font-size:1rem ">
                        {paper.get('title')}
                    </div>
                    <div style="
                        font-size:.75rem;
                        padding:.25rem .6rem;
                        border-radius:999px;
                        background:rgba(91,141,239,.08);
                        border:1px solid rgba(91,141,239,.15); ">
                        {source_badge}
                    </div>
                    <div style="
                        font-size:.75rem;
                        padding:.25rem .6rem;
                        border-radius:999px;
                        background:rgba(91,141,239,.08);
                        border:1px solid rgba(91,141,239,.15); ">
                        {year}
                    </div>
                </div>
                <div style="
                    font-size:.8rem;
                    color:gray;
                    margin-bottom:.6rem ">
                    {paper.get('authors')}
                </div>
                <div style="
                    font-size:.9rem;
                    line-height:1.6;
                    margin-bottom:.8rem ">
                    {paper.get('summary')[:450]}...
                </div>
                <a href="{paper.get('pdf_url')}"
                   target="_blank">
                   📄 View PDF
                </a>
            </div>
            """,
            unsafe_allow_html=True)
        col1, col2, _ = st.columns([1.4, 1.4, 4])
        summary_key = unique_id
        with col1:
            if st.button("✨ Summarize",key=f"sum_{unique_id}"):
                with st.spinner("Generating summary..."):
                    st.session_state.paper_summaries[summary_key] = summarize_paper(paper["title"],paper["summary"])
        if summary_key in st.session_state.paper_summaries:
            st.markdown(
                f"""
                <div class="card">
                    <div style="
                        font-weight:600;
                        margin-bottom:.5rem ">
                        ✨ Paper Summary
                    </div>
                    <div style="
                        font-size:.9rem;
                        line-height:1.7 ">
                        {st.session_state.paper_summaries[summary_key]}
                    </div>
                </div>""",
                unsafe_allow_html=True)
        with col2:
            if st.button("💾 Save",key=f"save_{unique_id}"):
                pdf_url= paper.get("pdf_url")
                if not pdf_url:
                    st.error("PDF URL not available for this paper")
                else:
                    result = save_paper_library(
                        paper["title"],
                        paper["authors"],
                        paper["summary"],
                        pdf_url,
                        st.session_state.token)
                    status = result.get("status", "failed")
                    if status == "already exists":
                        st.warning("Paper already saved.")
                    elif status == "saved":
                        st.success("Paper saved to library.")
                    elif status == "pdf unavailable":
                        st.warning("Download link is not available. Please upload PDF mannually")
                    elif status =="download failed":
                        st.error("Failed to download paper.")
    total_results = len(st.session_state.research_results)
    total_pages = max(1,(total_results + PAGE_SIZE - 1)// PAGE_SIZE)
    prev_col, info_col, next_col = st.columns([1, 2, 1])
    with prev_col:
        if st.button("⬅ Previous",disabled=(st.session_state.research_page == 1)):
            st.session_state.research_page -= 1
            st.rerun()
    with info_col:
        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding-top:.5rem;
                font-size:.9rem;
                color:gray; ">
                Page
                {st.session_state.research_page}
                of
                {total_pages}
            </div>
            """,unsafe_allow_html=True)
    with next_col:
        if st.button("Next ➡", disabled=(st.session_state.research_page >= total_pages)):
            st.session_state.research_page += 1
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-header">'
        '💬 Ask Research Papers'
        '</div>',
        unsafe_allow_html=True
    )
    research_question = st.text_input("Ask a question from saved research papers", placeholder=("Ask something from research papers..."),key="research_question")
    if st.button("Ask Papers ➤",key="ask_research_btn"):
        if not research_question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Analyzing research papers..."):

                result= (ask_research_question( question=research_question, token=st.session_state.token))
                answer = result.get("answer", "")
                sources = result.get("sources", [])
            st.markdown(
                f"""
                <div class="card">
                    <div style="
                        font-size:.92rem;
                        line-height:1.7 ">
                        {answer}
                    </div>
                </div>
                """, unsafe_allow_html=True )
            if sources:
                pills = "".join(
                    f'''
                    <span class="source-pill">
                        📎 {s}
                    </span>
                    '''
                    for s in sources
                )
                st.markdown(
                    f"""
                    <div style="
                        margin-top:1rem ">
                        <div style="
                            font-size:.78rem;
                            color:var(--muted);
                            margin-bottom:.4rem ">
                            Sources
                        </div>
                        {pills}
                    </div> """, unsafe_allow_html=True )