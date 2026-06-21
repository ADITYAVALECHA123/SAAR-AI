from frontend.services.analytics import get_analytics
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def render_analytics():
    st.markdown("## 📈 Analytics")
    current_user = st.session_state.user
    analytics_response = get_analytics(st.session_state.token)
    analytics = analytics_response.get("data", {})
    total_queries = analytics.get("total_queries", 0)
    avg_response = analytics.get("avg_response", 0)
    source_counts = analytics.get("source_counts", [])
    daily_counts = analytics.get("daily_counts", [])
    top_topics = analytics.get("top_topics", [])


    k1, k2, k3 = st.columns(3)
    kpis = [
        (k1, "💬", f"{total_queries}", "Total Queries"),
        (k2, "⚡", f"{avg_response} ms", "Avg Response"),
        (k3, "📄", f"{len(st.session_state.get('documents', []))}", "Docs Indexed"),
    ]
    for col, icon, val, label in kpis:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.5rem;margin-bottom:.3rem">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-header">Queries Over Time</div>', unsafe_allow_html=True)
        if daily_counts:
            days = [item["date"] for item in daily_counts]
            vals = [item["count"] for item in daily_counts]
        else:
            days = ["No Data"]
            vals = [0]
        fig, ax = plt.subplots(figsize=(5.5, 3))
        fig.patch.set_facecolor("#1C1F26")
        ax.set_facecolor("#1C1F26")
        colors = ["#5B8DEF" if v < max(vals) else "#8B5CF6" for v in vals]
        bars = ax.bar(days, vals, color=colors, width=0.55, zorder=3)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, v + .5, str(v),
                    ha='center', va='bottom', fontsize=8, color='#8B8FA8')
            ax.set_ylim(0, max(vals) * 1.25 if max(vals) > 0 else 1)
            ax.spines[['top','right','left','bottom']].set_visible(False)
            ax.tick_params(colors='#8B8FA8', labelsize=9)
            ax.yaxis.set_visible(False)
            ax.set_xlabel("Day of Week", color='#8B8FA8', fontsize=9)
            plt.tight_layout(pad=0.5)
            st.pyplot(fig)
            plt.close()

    with right:
        st.markdown('<div class="section-header">Top Query Topics</div>', unsafe_allow_html=True)
        
        if not top_topics:
            top_topics = [{"topics": "No Data", "count": 1}]
        topics = [item["topics"] for item in top_topics]
        sizes = [item["count"] for item in top_topics]
        palette = ["#5B8DEF", "#8B5CF6", "#34D399", "#FBBF24", "#F87171", "#64748B"]
        fig2, ax2 = plt.subplots(figsize=(5.5, 3))
        fig2.patch.set_facecolor("#1C1F26")
        ax2.set_facecolor("#1C1F26")
        wedges, _ = ax2.pie(
            sizes, colors=palette, startangle=140,
            wedgeprops=dict(width=0.5, edgecolor="#1C1F26", linewidth=2)
        )
        patches = [mpatches.Patch(color=palette[i], label=f"{topics[i]}  {sizes[i]}%")
                   for i in range(len(topics))]
        ax2.legend(handles=patches, loc="center right", frameon=False,
                   labelcolor='#B0B4C4', fontsize=8.5,
                   bbox_to_anchor=(1.35, 0.5))
        plt.tight_layout(pad=0.5)
        st.pyplot(fig2)
        plt.close()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📂 Source Distribution</div>', unsafe_allow_html=True)

    if not source_counts:
        source_counts = [{"source": "No Data", "count": 1}]

    sources = [item.get("source") or "Unknown" for item in source_counts]
    counts = [item.get("count", 0) for item in source_counts]
    fig_src, ax_src = plt.subplots(figsize=(6, 3))
    fig_src.patch.set_facecolor("#1C1F26")
    ax_src.set_facecolor("#1C1F26")
    colors = ["#5B8DEF","#8B5CF6","#34D399", "#FBBF24","#F87171","#64748B"]
    bars = ax_src.bar(sources,counts,color=colors[:len(sources)])
    for bar, value in zip(bars, counts):
        ax_src.text(bar.get_x() + bar.get_width()/2,value,str(value),ha="center",va="bottom",color="#B0B4C4",fontsize=9)
    ax_src.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
    ax_src.tick_params(colors="#8B8FA8")
    ax_src.yaxis.set_visible(False)
    plt.tight_layout()
    st.pyplot(fig_src)
    plt.close()