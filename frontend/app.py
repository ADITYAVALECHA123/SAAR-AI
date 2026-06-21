# ─────────────────────────────────────────────
#  Library Imports
# ─────────────────────────────────────────────
from datetime import datetime, timedelta
import requests
import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
import streamlit as st
from frontend.utils.session_manager import _init_state
_init_state()
from frontend.pages.auth import render_auth
from frontend.components.sidebar import render_sidebar
from frontend.pages.dashboard import render_dashboard
from frontend.pages.chat import render_chat
from frontend.pages.analytics import render_analytics
from frontend.pages.research import render_research
from frontend.pages.library import render_library
from frontend.pages.pdf import render_pdf
from frontend.pages.video import render_video
from frontend.pages.setting import render_setting
import time
import random

import numpy as np
from dotenv import load_dotenv
from frontend.style.theme import load_css
load_dotenv()

BASE_URL = "https://saar-ai-production.up.railway.app"
BACKEND_URL = os.getenv("BACKEND_URL","https://saar-ai-production.up.railway.app/")

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(page_title="Saar",page_icon="🔬",layout="wide",initial_sidebar_state="expanded",)
load_css()
if not st.session_state.authenticated:
    render_auth()
    st.stop()
render_sidebar()
page= st.session_state.page

if page == "Dashboard":
    render_dashboard()
elif page == "Upload PDF":
    render_pdf()
elif page == "Document Library":
    render_library()
elif page == "Chat (Q&A)":
    render_chat()
elif page == "Video Summarization":
    render_video()
elif page == "Research Papers":
    render_research()
elif page == "Analytics":
    render_analytics()
elif page == "Settings":
    render_setting()
