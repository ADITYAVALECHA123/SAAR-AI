import streamlit as st

# ─────────────────────────────────────────────
#  Global CSS
# ─────────────────────────────────────────────

def load_css():
    theme = st.session_state.get("theme","Dark (default)")
    if theme == "OLED Black":
        bg_color = "#000000"
        surface_color = "#0A0A0A"
        surface2_color = "#111111"

    elif theme == "Midnight Blue":
        bg_color = "#0B1120"
        surface_color = "#111827"
        surface2_color = "#1F2937"

    else:
        bg_color = "#1C1F26"
        surface_color = "#252A33"
        surface2_color = "#2E3440"

    font_size = st.session_state.get(
        "font_size",
        "Medium"
    )

    font_map = {
        "Small": "14px",
        "Medium": "16px",
        "Large": "18px"
    }

    base_font = font_map.get(
        font_size,
        "16px"
    )
    st.markdown(f"""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {{
    --bg:        {bg_color};
    --surface:   {surface_color};
    --surface2:  {surface2_color};
    --border:    #2E3138;
    --accent:    #38BDF8;
    --accent2:   #3d6fe3;
    --green:     #34D399;
    --amber:     #FBBF24;
    --red:       #F87171;
    --text:      #E8EAED;
    --muted:     #8B8FA8;
    --radius:    14px;
    --shadow:    0 4px 24px rgba(0,0,0,.45);
}}

/* ── Reset & Base ── */
html, body, [class*="css"] {{
    font-size: {base_font};
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1.8rem 2rem 3rem 2rem !important; max-width: 1280px; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}}
[data-testid="stSidebar"] .block-container {{ padding: 1.2rem !important; }}

[data-testid="stSidebarNav"] {{display: none !important;}}

/* ── Card ── */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    box-shadow: var(--shadow);
    transition: transform .18s ease, box-shadow .18s ease;
}}
.card:hover {{transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,.55); }}

/* ── Auth Card ── */
.auth-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.4rem 2.8rem;
    box-shadow: 0 8px 48px rgba(0,0,0,.6);
    max-width: 440px;
    margin: 0 auto;
}}

/* ── Auth tabs ── */
.auth-tab-row {{
    display: flex;
    gap: 0;
    background: var(--surface2);
    border-radius: 10px;
    padding: 4px;
    margin-bottom: 1.8rem;
}}
.auth-tab {{
    flex: 1;
    text-align: center;
    padding: .5rem;
    border-radius: 8px;
    font-size: .88rem;
    font-weight: 600;
    cursor: pointer;
    transition: background .18s, color .18s;
    color: var(--muted);
}}
.auth-tab.active {{
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: #fff;
}}

/* ── Auth logo ── */
.auth-logo {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: .7rem;
    margin-bottom: 1.8rem;
}}
.auth-logo-icon {{
    width: 44px; height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    box-shadow: 0 4px 16px rgba(91,141,239,.35);
}}
.auth-logo-text {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -.02em;
}}

/* ── Auth divider ── */
.auth-divider {{
    display: flex;
    align-items: center;
    gap: .8rem;
    margin: 1.2rem 0;
    color: var(--muted);
    font-size: .78rem;
}}
.auth-divider::before,
.auth-divider::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
}}

/* ── Social btn ── */
.social-btn {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: .6rem;
    width: 100%;
    padding: .6rem;
    border-radius: 9px;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    font-size: .88rem;
    font-weight: 500;
    cursor: pointer;
    transition: border-color .15s, background .15s;
    margin-bottom: .5rem;
}}
.social-btn:hover {{
    border-color: var(--accent);
    background: rgba(91,141,239,.08);
}}

/* ── Input label override ── */
.auth-label {{
    font-size: .8rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .07em;
    margin-bottom: .3rem;
}}

/* ── Auth features list ── */
.feature-item {{
    display: flex;
    align-items: flex-start;
    gap: .7rem;
    padding: .7rem 0;
    border-bottom: 1px solid var(--border);
    font-size: .88rem;
}}
.feature-item:last-child {{ border-bottom: none; }}
.feature-icon {{
    width: 30px; height: 30px; border-radius: 8px;
    background: rgba(91,141,239,.12);
    border: 1px solid rgba(91,141,239,.25);
    display: flex; align-items: center; justify-content: center;
    font-size: .9rem; flex-shrink: 0;
}}
.feature-title {{ font-weight: 600; margin-bottom: .1rem; }}
.feature-desc  {{ font-size: .78rem; color: var(--muted); }}

/* ── Error / success alerts in auth ── */
.auth-error {{
    background: rgba(248,113,113,.1);
    border: 1px solid rgba(248,113,113,.35);
    border-left: 4px solid var(--red);
    color: var(--red);
    border-radius: 8px;
    padding: .6rem 1rem;
    font-size: .84rem;
    margin-bottom: .9rem;
}}
.auth-success {{
    background: rgba(52,211,153,.1);
    border: 1px solid rgba(52,211,153,.3);
    border-left: 4px solid var(--green);
    color: var(--green);
    border-radius: 8px;
    padding: .6rem 1rem;
    font-size: .84rem;
    margin-bottom: .9rem;
}}

/* ── Metric Card ── */
.metric-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem;
    text-align: center;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
    transition: transform .18s ease;
}}
.metric-card:hover {{ transform: translateY(-3px); }}
.metric-card::before {{
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}}
.metric-value {{ font-size: 2.2rem; font-weight: 700; line-height: 1; margin-bottom: .3rem; }}
.metric-label {{ font-size: .78rem; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }}
.metric-delta {{ font-size: .8rem; margin-top: .5rem; }}
.delta-up   {{ color: var(--green); }}
.delta-down {{ color: var(--red); }}

/* ── Section Header ── */
.section-header {{
    font-size: 1.05rem; font-weight: 600;
    color: var(--muted);
    text-transform: uppercase; letter-spacing: .1em;
    margin-bottom: 1rem; padding-bottom: .5rem;
    border-bottom: 1px solid var(--border);
}}

/* ── Gradient Button ── */
.grad-btn {{
    display: inline-flex; align-items: center; gap: .5rem;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    color: #fff; font-weight: 600; font-size: .9rem;
    padding: .6rem 1.4rem; border-radius: 8px; border: none;
    cursor: pointer; transition: opacity .2s, transform .15s;
    text-decoration: none;
}}
.grad-btn:hover {{ opacity: .88; transform: scale(1.02); }}

/* ── Chat bubbles ── */
.chat-wrap {{ display: flex; flex-direction: column; gap: .8rem; padding: .5rem 0; }}

.bubble {{ display: flex; gap: .75rem; align-items: flex-start; }}
.bubble-user {{ flex-direction: row-reverse; }}

.avatar {{
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
}}
.avatar-ai   {{ background: linear-gradient(135deg, var(--accent), var(--accent2)); }}
.avatar-user {{ background: var(--surface2); border: 1px solid var(--border); }}

.msg {{
    max-width: 72%;
    padding: .75rem 1.1rem;
    border-radius: 14px;
    font-size: .93rem;
    line-height: 1.55;
}}
.msg-ai {{
    background: var(--surface2);
    border: 1px solid var(--border);
    border-top-left-radius: 4px;
}}
.msg-user {{
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    color: #fff;
    border-top-right-radius: 4px;
}}

/* ── Source pill ── */
.source-pill {{
    display: inline-flex; align-items: center; gap: .35rem;
    background: rgba(91,141,239,.12); border: 1px solid rgba(91,141,239,.3);
    color: var(--accent); font-size: .75rem; font-weight: 500;
    padding: .25rem .7rem; border-radius: 20px; margin: .2rem .15rem;
    cursor: pointer; transition: background .15s;
}}
.source-pill:hover {{ background: rgba(91,141,239,.22); }}

/* ── Typing dots ── */
.typing-indicator {{ display: flex; align-items: center; gap: 5px; padding: .6rem 0; }}
.typing-indicator span {{
    width: 7px; height: 7px; background: var(--muted);
    border-radius: 50%; display: inline-block;
    animation: bounce .9s infinite ease-in-out;
}}
.typing-indicator span:nth-child(2) {{ animation-delay: .15s; }}
.typing-indicator span:nth-child(3) {{ animation-delay: .30s; }}
@keyframes bounce {{
    0%,80%,100% {{ transform: translateY(0); opacity: .4; }}
    40%          {{ transform: translateY(-6px); opacity: 1; }}
}}

/* ── Paper Card ── */
.paper-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    margin-bottom: .9rem;
    box-shadow: var(--shadow);
    transition: transform .15s, border-color .15s;
}}
.paper-card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}
.paper-title {{ font-size: 1rem; font-weight: 600; margin-bottom: .3rem; }}
.paper-authors {{ font-size: .8rem; color: var(--muted); margin-bottom: .55rem; }}
.paper-abstract {{ font-size: .85rem; color: #B0B4C4; line-height: 1.55; }}

/* ── Doc Row ── */
.doc-row {{
    display: flex; align-items: center; justify-content: space-between;
    padding: .8rem 1rem; margin-bottom: .5rem;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; transition: border-color .15s;
}}
.doc-row:hover {{ border-color: var(--accent); }}
.doc-name {{ font-size: .9rem; font-weight: 500; }}
.doc-meta {{ font-size: .75rem; color: var(--muted); }}

/* ── Upload Zone ── */
[data-testid="stFileUploader"] {{
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
    transition: border-color .2s !important;
}}
[data-testid="stFileUploader"]:hover {{ border-color: var(--accent) !important; }}

/* ── Inputs & Selects ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] select {{
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(91,141,239,.18) !important;
}}

/* ── Streamlit buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
    padding: .55rem 1.3rem !important;
    transition: opacity .2s, transform .15s !important;
}}
.stButton > button:hover {{ opacity: .85 !important; transform: scale(1.02) !important; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 260px !important;
    max-width: 260px !important;
    transform: none !important;
    visibility: visible !important;
}}
[data-testid="stSidebar"] .block-container {{ padding: 1.2rem !important; }}

/* ── Hide collapse arrow button ── */
[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}

/* ── Alert ── */
.success-alert {{
    background: rgba(52,211,153,.12); border: 1px solid rgba(52,211,153,.35);
    border-left: 4px solid var(--green);
    color: var(--green); border-radius: 10px;
    padding: .8rem 1.1rem; font-size: .88rem;
}}
.info-alert {{
    background: rgba(91,141,239,.1); border: 1px solid rgba(91,141,239,.3);
    border-left: 4px solid var(--accent);
    color: var(--accent); border-radius: 10px;
    padding: .8rem 1.1rem; font-size: .88rem;
}}

/* ── Sidebar Nav ── */
.nav-item {{
    display: flex; align-items: center; gap: .7rem;
    padding: .65rem .9rem; border-radius: 9px;
    font-size: .92rem; font-weight: 500;
    cursor: pointer; transition: background .15s, color .15s;
    color: var(--muted); margin-bottom: .2rem;
    border: 1px solid transparent;
}}
.nav-item:hover {{ background: var(--surface2); color: var(--text); }}
.nav-item.active {{
    background: rgba(91,141,239,.15);
    color: var(--accent);
    border-color: rgba(91,141,239,.3);
}}
.nav-section-label {{
    font-size: .7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: .1em; color: var(--muted);
    padding: .8rem .9rem .3rem; margin-top: .4rem;
}}

/* ── Video / Transcript ── */
.transcript-box {{
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; padding: 1rem 1.2rem;
    max-height: 260px; overflow-y: auto;
    font-size: .85rem; line-height: 1.65;
    color: #C0C4D6;
    font-family: 'DM Mono', monospace;
}}
.transcript-box::-webkit-scrollbar {{ width: 5px; }}
.transcript-box::-webkit-scrollbar-track {{ background: transparent; }}
.transcript-box::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 10px; }}

/* ── Logo ── */
.logo-wrap {{
    display: flex; align-items: center; gap: .6rem;
    padding: .6rem .8rem 1.4rem;
}}
.logo-icon {{
    width: 36px; height: 36px; border-radius: 9px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}}
.logo-name {{ font-size: 1.1rem; font-weight: 700; }}
.logo-tag  {{ font-size: .68rem; color: var(--muted); }}

/* ── Progress bar ── */
.prog-wrap {{ background: var(--surface2); border-radius: 20px; height: 7px; overflow: hidden; margin-top: .4rem; }}
.prog-fill  {{ height: 100%; border-radius: 20px;
              background: linear-gradient(90deg, var(--accent), var(--accent2)); }}

/* ── Tag badge ── */
.tag {{
    display: inline-block;
    background: rgba(91,141,239,.14); color: var(--accent);
    border: 1px solid rgba(91,141,239,.28);
    font-size: .72rem; font-weight: 600;
    padding: .18rem .6rem; border-radius: 20px; margin: .15rem .1rem;
}}

/* ── Settings toggle row ── */
.setting-row {{
    display: flex; align-items: center; justify-content: space-between;
    padding: .75rem 0; border-bottom: 1px solid var(--border);
}}
.setting-label {{ font-size: .92rem; }}
.setting-sub   {{ font-size: .78rem; color: var(--muted); }}

/* ── Spinner override ── */
[data-testid="stSpinner"] {{ color: var(--accent) !important; }}
/* ── Auth page: hide sidebar ── */
.auth-hide-sidebar [data-testid="stSidebar"] {{
    display: none !important;
}}

/* ── Password strength bar ── */
.pw-strength-wrap {{ margin-top: .4rem; }}
.pw-strength-bar  {{ height: 5px; border-radius: 10px; transition: width .3s; }}
.pw-strength-label {{ font-size: .73rem; margin-top: .25rem; }}

/* ── User chip in sidebar ── */
.user-chip {{
    display: flex; align-items: center; gap: .55rem;
    padding: .6rem .8rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: .8rem;
}}
.user-avatar {{
    width: 30px; height: 30px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: .85rem; font-weight: 700; color: #fff; flex-shrink: 0;
}}
.user-name  {{ font-size: .88rem; font-weight: 600; line-height: 1.2; }}
.user-email {{ font-size: .72rem; color: var(--muted);}}
</style>
""", unsafe_allow_html=True)