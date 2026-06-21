import streamlit as st

def _init_state():
    defaults = {
        # =========================
        # Navigation
        # =========================
        "page": "Dashboard",

        # =========================
        # Authentication
        # =========================
        "authenticated": False,
        "user": None,
        "token": None,
        "auth_tab": "login",
        "auth_error": "",
        "auth_success": "",

        # =========================
        # Chat System
        # =========================
        "chat_history": [],
        "streaming": True,
        "chat_session_id":None,
        "chat_sessions":[],

        # =========================
        # AI Settings
        # =========================
        "model": "Mistral 7B",
        "temperature": 0.7,
        "top_k": 5,
        "chunk_size": 512,

        # =========================
        # Analytics
        # =========================
        "total_queries": 148,
        "avg_response_ms": 412,

        # =========================
        # File / RAG System
        # =========================
        "documents": [
            {
                "name": "Attention Is All You Need.pdf",
                "size": "2.3 MB",
                "date": "2025-04-01",
                "pages": 15
            },
            {
                "name": "BERT Language Model.pdf",
                "size": "1.8 MB",
                "date": "2025-03-28",
                "pages": 12
            },
        ],

        "uploaded_files": [],
        "paper_results": [],
        "video_result": None,

        # =========================
        # UI Preferences
        # =========================
        "theme": "Dark (default)",
        "font_size": "Medium",

        # =========================
        # Future Features
        # =========================
        "selected_agent": None,
        "selected_workspace": None,
        "notifications": [],
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


_init_state()