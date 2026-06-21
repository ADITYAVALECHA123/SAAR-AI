import streamlit as st
from frontend.services.dashboard_services import fetch_dashboard
def render_dashboard():
    st.markdown("## 📊 Dashboard")
    st.markdown('<div class="section-header">Overview</div>', unsafe_allow_html=True)

    # ── Metric cards ──
    c1, c2, c3, c4 = st.columns(4)
    response = fetch_dashboard()
    if response.get("success"):
        data = response.get("data", {})
    else:
        st.error(response.get("error"))
        data = {}
    docs = data.get("documents", 0) if data else 0
    queries = data.get("queries", 0) if data else 0
    avg = data.get("avg_response", 0) if data else 0
    acc = data.get("accuracy", 0) if data else 0
    sources = data.get("active_sources", 0) if data else 0
    recent_docs = data.get("recent_docs", []) if data else []
    recent_queries = data.get("recent_queries", []) if data else []
    metrics = [
    (c1, "🗂️", str(docs), "Documents", "", True),
    (c2, "💬", str(queries), "Total Queries", "", True),
    (c3, "⚡", f"{avg} ms", "Avg Response", "", True),
    (c4, "🚀", sources, "Active Sources", "", True)]
    for col, icon, val, label, delta, up in metrics:
        with col:
            dcolor = "delta-up" if up else "delta-down"
            darrow = "↑" if up else "↓"
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.6rem;margin-bottom:.4rem">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-delta {dcolor}">{darrow} {delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recent activity + Quick actions ──
    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="section-header">Recent Activity</div>', unsafe_allow_html=True)
        activities = []
        for q in recent_queries:
            activities.append(("💬",f"Asked: {q.get('query', 'Query')}","Recent","var(--accent)"))
        for d in recent_docs:
            source = d.get("source_type", "document").lower()
            icon_map = {"pdf": "📄","video": "🎬","research": "📚"}
            icon = icon_map.get(source, "📁")
            activities.append((icon,f"Uploaded: {d.get('filename', 'Document')}","Recent","var(--green)"))

        activities = activities[:6]
        for icon, text, time_str, color in activities:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:.9rem;padding:.65rem .9rem;
                        margin-bottom:.4rem;background:var(--surface);border:1px solid var(--border);
                        border-radius:10px;">
                <div style="width:32px;height:32px;border-radius:8px;
                            background:{color}22;border:1px solid {color}44;
                            display:flex;align-items:center;justify-content:center;font-size:.95rem;">
                    {icon}
                </div>
                <div style="flex:1">
                    <div style="font-size:.87rem">{text}</div>
                    <div style="font-size:.73rem;color:var(--muted)">{time_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Recent Uploads</div>',unsafe_allow_html=True)
        recent_docs = data.get("recent_docs", []) if data else []
        if not recent_docs:
            st.markdown("""<div class="info-alert">
                        ℹ️ No recent uploads found.
                    </div>""", unsafe_allow_html=True)
        else:
            for doc in recent_docs[:5]:
                source = doc.get(
                        "source_type",
                        "document").lower()
                badge_map = {"pdf": "📄 PDF",
            "video": "🎬 VIDEO",
            "research": "📚 RESEARCH"}
            badge = badge_map.get(
            source,
            "📁 DOCUMENT")

            st.markdown(f"""
        <div style="
            padding:.8rem 1rem;
            margin-bottom:.5rem;
            background:var(--surface);
            border:1px solid var(--border);
            border-radius:12px;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">
                <div>
                    <div style="font-weight:600">
                        {doc.get("filename")}
                    </div>

                    <div style="
                        font-size:.78rem;
                        color:var(--muted);
                    ">
                        {badge}
                    </div>
                </div>

                <div style="
                    font-size:.75rem;
                    color:var(--muted);
                ">
                    Recent
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-header">Quick Actions</div>', unsafe_allow_html=True)
        actions = [("📄 Upload PDF", "Upload PDF"), ("💬 New Chat", "Chat (Q&A)"),
                   ("🔍 Search Papers", "Research Papers"), ("🎬 Summarize Video", "Video Summarization")]
        for label, dest in actions:
            if st.button(label, key=f"qa_{dest}", use_container_width=True):
                st.session_state.page = dest
                st.rerun()