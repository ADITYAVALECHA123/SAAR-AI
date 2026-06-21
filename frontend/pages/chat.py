import streamlit as st
from frontend.services.chat_service import send_chat
import time
def render_chat():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[]
    if "total_queries" not in st.session_state:
        st.session_state.total_queries = 0
    st.markdown("## 💬 Chat Assistant")
    selected_doc = st.session_state.get("selected_doc")
    if selected_doc:
        col1, col2 = st.columns([5,1])
        with col1:   
            st.markdown(f"""
                        <div class="card">
                            <div style="font-weight:600">
                                💬 Chatting with:
                                {selected_doc['filename']}
                            </div>
                            <div style="font-size:.8rem;color:gray">
                                Source: {selected_doc['source_type']}
                            </div>
                        </div>""", unsafe_allow_html=True)
            with col2:
                if st.button("🔓 Exit"):
                    st.session_state.selected_doc = None
                    st.session_state.chat_history = []
                    st.session_state.chat_session_id = None
                    st.rerun()
    chat_container = st.container()
    with chat_container:
            user = st.session_state.user
            if len(st.session_state.chat_history) == 0:
                if selected_doc:
                    subtitle = (
                        f"Chatting with "
                        f"{selected_doc['filename']}")
                else:
                    subtitle = ("I have access to all your uploaded documents") 
                st.markdown(f"""
                            <div style="text-align:center;padding:3rem 0;color:var(--muted)">
                                <div style="font-size:2.5rem;margin-bottom:.8rem">🤖</div>
                                <div style="font-size:1.1rem;font-weight:600;margin-bottom:.4rem">Hi {user['name'].split()[0]}, Ask me anything</div>
                                <div style="font-size:.88rem">{subtitle}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"""
                                    <div class="bubble bubble-user" style="margin-bottom:.6rem">
                                        <div class="avatar avatar-user">👤</div>
                                        <div class="msg msg-user">{msg["content"]}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                                    <div class="bubble" style="margin-bottom:.2rem">
                                        <div class="avatar avatar-ai">🤖</div>
                                        <div class="msg msg-ai">{msg["content"]}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                        if msg.get("sources"):
                            pills = "".join(f'<span class="source-pill">📎 {s}</span>'for s in msg["sources"])
                            st.markdown(
                            f'<div style="padding-left:2.8rem;margin-bottom:.6rem">'
                            f'<div style="font-size:.73rem;color:var(--muted);margin-bottom:.25rem">Sources</div>'
                            f'{pills}</div>',
                            unsafe_allow_html=True,)
 
                        if msg.get("retrieved_chunks"):
                            with st.expander("🔍 Retrieval Debug"):
                                for chunk in msg["retrieved_chunks"]:
                                    source_name = chunk.get("source_name","unknown")
                                    source_type = chunk.get("source_type","unknown")
                                    page = chunk.get("page")
                                    score = chunk.get("score",0.0)
                                    preview = chunk.get("preview","")
                                    st.markdown(f"""
                                                **Source:** {source_name}
                                                **Type:** {source_type}
                                                **Score:** {score}
                                                **Page:** {page + 1 if page is not None else "N/A"}""")
                                    st.code(preview)
                                    st.divider()

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Message", placeholder="Ask a question about your documents…",
            label_visibility="collapsed", key="chat_input"
        )
    with col_btn:
        send = st.button("Send ➤", use_container_width=True)

    if send and user_input.strip():
        user_message = user_input.strip()
        st.session_state.chat_history.append({"role": "user","content": user_message.strip()})
        placeholder = st.empty()
        placeholder.markdown("""
        <div class="bubble">
            <div class="avatar avatar-ai">🤖</div>
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div> """, unsafe_allow_html=True)
        with st.spinner("Thinking"):
            data = send_chat(message=user_message,token=st.session_state.token,user_id=st.session_state.user["id"],
                             document_id=(selected_doc["id"] if selected_doc else None), session_id=st.session_state.get("chat_session_id"))
            if not data:
                placeholder.empty()
                st.error("Failed to get response from server")
                return
        answer = data.get("response", "No response")
        if data.get("session_id"):
            st.session_state.chat_session_id = (data["session_id"])
        sources = data.get("sources", [])
        retrieved_chunks = data.get("retrieved_chunks",[])
        stream_placeholder=st.empty()
        streamed_text=""
        for word in answer.split():
            streamed_text += word +" "
            stream_placeholder.markdown(f"""
                                        <div class="bubble">
                                            <div class="avatar avatar-ai">🤖</div>
                                            <div class="msg msg-ai">
                                                {streamed_text}
                                            </div>
                                        </div>
                                    """,unsafe_allow_html=True)
            time.sleep(0.020)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "retrieved_chunks":retrieved_chunks})
        st.session_state.total_queries += 1
        st.rerun()