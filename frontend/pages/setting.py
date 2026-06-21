import streamlit as st
from frontend.services.setting import save_settings

def render_setting():
    st.markdown("## ⚙️ Settings")
    user = st.session_state.user

    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="section-header">🤖 Model Configuration</div>', unsafe_allow_html=True)
        model_options = ['llama-3.3-70b-versatile', 'qwen/qwen-32b', 'openai/gpt-oss-120b']
        model = st.selectbox("Language Model",model_options,index=model_options.index(st.session_state.selected_model))

        st.session_state.selected_model = model

        chunk_size = st.slider(
            "Chunk Size (tokens)",
            min_value=128, max_value=2048, step=64,
            value=st.session_state.chunk_size,
        )
        st.session_state.chunk_size = chunk_size

        top_k = st.slider(
            "Top-K Retrieval",
            min_value=1, max_value=20,
            value=st.session_state.top_k,
        )
        st.session_state.top_k = top_k

        if "temperature" not in st.session_state:
            st.session_state.temperature = 0.3
        temperature = st.slider("Temperature",0.0, 1.0,value=st.session_state.temperature,step=0.05)
        st.session_state.temperature = temperature

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">🎨 Interface</div>', unsafe_allow_html=True)
        theme_options = ["Dark (default)","OLED Black","Midnight Blue"]
        theme = st.selectbox("Theme",theme_options,index=theme_options.index(st.session_state.get("theme","Dark (default)")))
        font_options = ["Medium","Small","Large"]
        font = st.selectbox("Font Size",font_options,index=font_options.index(st.session_state.get("font_size","Medium")))
        st.markdown("<br>", unsafe_allow_html=True)

        # Account section
        st.markdown('<div class="section-header">👤 Account</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:.88rem;margin-bottom:1rem;line-height:1.8">
            <span style="color:var(--muted)">Name:</span> <strong>{user['name']}</strong><br>
            <span style="color:var(--muted)">Email:</span> <strong>{user['email']}</strong>
        </div>
        """, unsafe_allow_html=True)

        if st.button("💾 Save Settings"):
            token = st.session_state.token
            payload={
                "selected_model": model,
                "chunk_size": chunk_size,
                "top_k": top_k,
                "temperature": temperature,
                "theme": theme,
                "font_size": font
            }
            data, status=save_settings(token, payload)
            if status == 200:
                st.session_state.theme = theme
                st.session_state.font_size = font
                st.success("Settings saved successfully!")
            else:
                st.error(data.get("detail", "Failed to save settings"))
    with right:
        st.markdown("""
        <div class="card">
            <div style="font-weight:600;font-size:.95rem;margin-bottom:.9rem">💡 Tuning Tips</div>
            <div style="font-size:.82rem;color:var(--muted);line-height:1.75">
                <strong style="color:var(--text)">Chunk Size</strong><br>
                Smaller (256–512) → precise retrieval<br>
                Larger (1024–2048) → more context per chunk<br><br>
                <strong style="color:var(--text)">Top-K</strong><br>
                Lower (3–5) → faster, focused answers<br>
                Higher (10–20) → broader coverage<br><br>
                <strong style="color:var(--text)">Temperature</strong><br>
                0.0 → deterministic / factual<br>
                0.7–1.0 → creative / varied
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <div style="font-weight:600;font-size:.95rem;margin-bottom:.9rem">📌 Current Config</div>
            <div style="font-size:.84rem;line-height:1.9">
                <span style="color:var(--muted)">Model:</span>
                <strong>{st.session_state.selected_model}</strong><br>
                <span style="color:var(--muted)">Chunk size:</span>
                <strong>{st.session_state.chunk_size} tokens</strong><br>
                <span style="color:var(--muted)">Top-K:</span>
                <strong>{st.session_state.top_k}</strong><br>
                <span style="color:var(--muted)">Temp:</span>
                <strong>{temperature}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)