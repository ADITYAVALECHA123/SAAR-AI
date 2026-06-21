import streamlit as st
from frontend.services.video import upload_video, ask_video_question

def render_video():
    st.markdown("## 🎬 Video Summarization")
    if "video_result" not in st.session_state:
        st.session_state.video_result = None
    tab1, = st.tabs(["📁 Upload Video"])
    with tab1:
        vid_file = st.file_uploader("Upload video file", type=["mp4", "mov", "avi", "mkv"])
        if vid_file and st.button("🚀 Generate Summary", key="vid_summarize"):
            with st.spinner("Processing uploaded video..."):
                result = upload_video(vid_file, st.session_state.token)
                if (result and result.get("status")=="success"):
                    st.session_state.video_result = (result["data"])
                    st.success("Video processed successfully!")
                else:
                    st.error("Video processing Fail")
    if st.session_state.video_result:
        res = st.session_state.video_result
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:.9rem">
                <span style="font-size:1.4rem">🎬</span>
                <div>
                    <div style="font-weight:600;font-size:1rem">{res['title']}</div>
                    <div style="font-size:.78rem;color:var(--muted)">Video Analysis</div>
                </div>
            </div>
            <div style="font-size:.78rem;color:var(--muted);margin-bottom:.3rem">Topics detected</div>
            <div>{"".join(f'<span class="tag">{t}</span>' for t in res['topics'])}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-header">📝 Transcript</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="transcript-box">{res["transcript"].replace(chr(10), "<br>")}</div>',
                        unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="section-header">✨ AI Summary</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="height:100%">
                <div style="font-size:.9rem;line-height:1.65">{res['summary']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(
    '<div class="section-header">⏱ Timeline Summary</div>',
    unsafe_allow_html=True
)

        st.markdown(f"""
            <div class="card">
            <div style="font-size:.9rem;line-height:1.7">
            {res['timeline_summary']}
            </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">💬 Ask This Video</div>',unsafe_allow_html=True)
        video_question = st.text_input("Ask a question about this video",placeholder="Ask something from this video...",key="video_question")
        if st.button("Ask Video ➤",key="ask_video_btn",use_container_width=False):
            if not video_question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Analyzing video..."):
                    result= ask_video_question(video_question,st.session_state.token)
                    answer = result.get("answer", "")
                    sources = result.get("sources", "")
                    st.markdown(f"""<div class="card">
                    <div style="font-size:.92rem;line-height:1.7">
                        {answer}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                    if sources:
                        pills = "".join(f'<span class="source-pill">📎 {s}</span>'for s in sources)
                        st.markdown(
                        f'''
                        <div style="margin-top:1rem">
                            <div style="font-size:.78rem;color:var(--muted);margin-bottom:.4rem">
                                Sources
                            </div>
                            {pills}
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )