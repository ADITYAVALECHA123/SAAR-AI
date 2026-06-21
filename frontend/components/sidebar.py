import streamlit as st
from frontend.services.chat_service import fetch_chat_sessions, load_chat_session, delete_chat_session

# ─────────────────────────────────────────────
#  SIDEBAR  (only shown when authenticated)
# ─────────────────────────────────────────────
def render_sidebar():
    if not st.session_state.get("authenticated", False):
        return

    # Defensive defaults: sidebar must never crash due to missing state.
    st.session_state.setdefault("page", "Dashboard")
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("chat_session_id", None)
    st.session_state.setdefault("chat_sessions", [])
    st.session_state.setdefault("selected_model", "")

    token = st.session_state.get("token")
    user = st.session_state.get("user") or {}

    with st.sidebar:
        st.markdown(
            """
        <div class="logo-wrap">
            <div class="logo-icon">🔬</div>
            <div>
                <div class="logo-name">Saar</div>
                <div class="logo-tag">Powered by RAG</div>
            </div>
        </div> """,
            unsafe_allow_html=True,
        )

        name = (user.get("name") or "User").strip()
        email = (user.get("email") or "").strip()
        initials = "".join(w[0].upper() for w in name.split()[:2] if w)
        st.markdown(
            f"""
        <div class="user-chip">
            <div class="user-avatar">{initials or 'U'}</div>
            <div>
                <div class="user-name">{name}</div>
                <div class="user-email">{email}</div>
            </div>
        </div>""",
            unsafe_allow_html=True,
        )

        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.chat_session_id = None
            st.session_state.selected_doc = None
            st.session_state.page = "Chat (Q&A)"
            st.rerun()

        nav_sections = {
            "WORKSPACE": [("📊", "Dashboard"), ("💬", "Chat (Q&A)"), ("📂", "Document Library")],
            "TOOLS": [("📄", "Upload PDF"), ("🎬", "Video Summarization"), ("🔍", "Research Papers")],
            "INSIGHTS": [("📈", "Analytics"), ("⚙️", "Settings")],
        }

        for section, items in nav_sections.items():
            st.markdown(
                f'<div class="nav-section-label">{section}</div>',
                unsafe_allow_html=True,
            )
            for icon, label in items:
                if st.button(
                    f"{icon}  {label}",
                    key=f"nav_{label}",
                    use_container_width=True,
                ):
                    if label=="Chat (Q&A)":
                        st.session_state.selected_doc = None
                    st.session_state.page = label
                    st.rerun()

        st.markdown("---")
        st.markdown(
            '<div class="nav-section-label">RECENT CHATS</div>',
            unsafe_allow_html=True,
        )

        # Fetch recent chat sessions only when we have a token.
        if not st.session_state.chat_sessions and token:
            try:
                sessions_resp = fetch_chat_sessions(token)
                # Expect a list; otherwise degrade gracefully.
                if isinstance(sessions_resp, list):
                    st.session_state.chat_sessions = sessions_resp
                else:
                    st.session_state.chat_sessions = []
            except Exception:
                st.session_state.chat_sessions = []

        sessions = st.session_state.chat_sessions or []

        if not sessions:
            st.caption("No conversations yet")
        else:
            # IMPORTANT: never call st.rerun() during render of each item.
            for session in sessions[:10]:
                if not isinstance(session, dict):
                    continue
                session_id = session.get("id")
                if not session_id:
                    # Avoid KeyError / invalid button keys.
                    continue

                col1, col2 = st.columns([5, 1])
                title = session.get("title", "New Chat") or "New Chat"
                if len(title) > 28:
                    title = title[:28] + "..."

                with col1:
                    if st.button(
                        f"💬 {title}",
                        key=f"session_{session_id}",
                        use_container_width=True,
                    ):
                        if token:
                            data = load_chat_session(session_id, token) or {}
                        else:
                            data = {}
                        st.session_state.chat_history = data.get("messages", [])
                        st.session_state.chat_session_id = session_id
                        st.session_state.page = "Chat (Q&A)"
                        st.rerun()

                with col2:
                    if st.button("🗑️", key=f"delete_{session_id}"):
                        if token:
                            delete_chat_session(session_id, token)
                        # Refresh after deletion.
                        st.session_state.chat_sessions = []
                        st.rerun()

                    # if st.session_state.chat_session_id == session_id:
                    #     # Keep UI consistent if current session is selected.
                    #     st.session_state.chat_history = []
                    #     st.session_state.chat_session_id = None

        st.markdown(
            f"""
        <div style="padding:.4rem .8rem">
            <div style="font-size:.72rem;color:var(--muted);margin-bottom:.3rem">ACTIVE MODEL</div>
            <div style="display:flex;align-items:center;gap:.5rem">
                <div style="width:8px;height:8px;border-radius:50%;background:var(--green);"></div>
                <span style="font-size:.88rem;font-weight:600">{st.session_state.selected_model}</span>
            </div>
        </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪  Sign Out", key="logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.token = None
            st.session_state.auth_error = ""
            st.session_state.auth_success = ""
            st.session_state.chat_history = []
            st.rerun()

# page = st.session_state.page


