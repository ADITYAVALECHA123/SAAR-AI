import streamlit as st
from frontend.services.pdf import generate_summary, upload_pdf

import datetime
def render_pdf():
    if "pdf_summaries" not in st.session_state:
        st.session_state.pdf_summaries = {}
    if "documents" not in st.session_state:
        st.session_state.documents = []
    st.markdown("## 📄 Upload PDF")
    st.markdown('<div class="section-header">Add Documents to Your Library</div>', unsafe_allow_html=True)
    left, right = st.columns([3, 2])
    with left:
        uploaded_files = st.file_uploader("Upload PDFs",type=["pdf"], accept_multiple_files=True)
        if uploaded_files and len(uploaded_files) > 10:
            st.error("Maximum 10 files allowed")
            st.stop()
        if uploaded_files:
            for f in uploaded_files:
                MAX_SIZE_MB = 50
                if f.size > MAX_SIZE_MB * 1024 * 1024:
                    st.error(f"{f.name} exceeds 50 MB limit.")
                    continue
                try:
                    with st.spinner(f"Uploading {f.name}..."):
                        token = st.session_state.token
                        result = upload_pdf(f, token)
                    if result.get("status") == "success":
                        st.success(f"{f.name} indexed successfully ✅")
                        names = [d["name"] for d in st.session_state.documents]
                        if f.name not in names:
                            st.session_state.documents.append({
                                 "name": f.name,
                                 "size": f"{round(f.size/1024/1024, 2)} MB",
                                 "date": datetime.datetime.today().strftime("%Y-%m-%d"),})
                    else:
                        st.error(result.get("detail", "Upload failed")) 
                except Exception as e:
                    st.error(f"Upload failed: {str(e)}")
                if st.button(f"✨ Generate Summary",key=f"summary_{f.name}"):
                    with st.spinner(f"Generating summary for {f.name}..."):
                        result = generate_summary(f.name,st.session_state.token)
                        if result.get("status") == "success":
                            st.session_state.pdf_summaries[f.name] = (result["summary"])

                        else:
                            st.error(result.get("detail", "Summary generation failed"))
                    if f.name in st.session_state.pdf_summaries:
                        st.markdown("## 📘 PDF Summary")
                        st.markdown(
                            f"""
                            <div class="card">
                                <div style="font-size:.95rem;line-height:1.7">
                                    {st.session_state.pdf_summaries[f.name]}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True)

                    names = [d["name"] for d in st.session_state.documents]
                    if f.name not in names:
                        st.session_state.documents.append({
                            "name": f.name,
                            "size": f"{round(f.size/1024/1024, 2)} MB",
                            "date": datetime.datetime.today().strftime("%Y-%m-%d"),
                        })
    with right:
        st.markdown("""
        <div class="card">
            <div style="font-size:.85rem;font-weight:600;margin-bottom:.8rem">📋 Upload Guidelines</div>
            <div style="font-size:.82rem;color:var(--muted);line-height:1.7">
                ✔ PDF format only<br>
                ✔ Max file size: 50 MB<br>
                ✔ Up to 10 files at once<br>
                ✔ Text-based PDFs preferred<br>
                ✔ Files are chunked & indexed automatically<br>
                ✔ Available in Chat within seconds
            </div>
        </div>
        """, unsafe_allow_html=True)

