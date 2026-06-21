import streamlit as st
from frontend.services.auth import api_login, pw_strength, validate_signup, api_signup
from frontend.services.setting import fetch_settings
# ═══════════════════════════════════════════════════════
#  AUTH PAGE
# ═══════════════════════════════════════════════════════
def render_auth():
    # Hide sidebar on auth screen
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        .block-container { max-width: 960px !important; padding-top: 3rem !important; }
    </style>
    """, unsafe_allow_html=True)
    left_col, right_col = st.columns([1, 1], gap="large")
    # ── LEFT: Feature showcase ──
    with left_col:
        st.markdown("""
                    <div style="padding: 2rem 1rem;">
                        <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:2rem">
                            <div style="width:44px;height:44px;border-radius:12px;
                                        background:linear-gradient(135deg,#5B8DEF,#8B5CF6);
                                        display:flex;align-items:center;justify-content:center;
                                        font-size:1.4rem;box-shadow:0 4px 16px rgba(91,141,239,.35);">
                            </div>
                            <div style="font-size:1.5rem;font-weight:700;letter-spacing:-.02em">Saar</div>
                        </div>
                    <div style="font-size:1.8rem;font-weight:700;line-height:1.25;margin-bottom:.7rem">
                        Your AI-powered<br>research workspace
                    </div>
                    <div style="font-size:.95rem;color:var(--muted);margin-bottom:2.2rem;line-height:1.6">
                        Upload papers, ask questions, and surface insights from your document library — all in one place.
                    </div>
        """, unsafe_allow_html=True)

        features = [
            ("💬", "RAG-powered Q&A", "Ask questions and get answers grounded in your documents"),
            ("📄", "PDF Library", "Upload and manage research papers, reports, and more"),
            ("🎬", "Video Summaries", "Summarise YouTube lectures and talks instantly"),
            ("🔍", "Paper Search", "Discover and explore academic papers with ease"),
            ("📈", "Analytics", "Track query patterns and document usage over time"),
        ]
        for icon, title, desc in features:
            st.markdown(f"""
            <div class="feature-item">
                <div class="feature-icon">{icon}</div>
                <div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:2rem;padding:1rem 1.2rem;
                    background:rgba(91,141,239,.07);
                    border:1px solid rgba(91,141,239,.2);
                    border-radius:12px;font-size:.83rem;color:var(--muted);line-height:1.6">
            <span style="color:var(--amber)">★★★★★</span><br>
            <em>"Saar cut my literature review time in half. The RAG chat is remarkably accurate."</em><br>
            <span style="font-size:.75rem;margin-top:.3rem;display:block">— PhD Researcher, MIT</span>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT: Auth form ──
    with right_col:
        tab = st.session_state.auth_tab
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign In", use_container_width=True):
                st.session_state.auth_tab = "login"
                st.session_state.auth_error = ""
                st.session_state.auth_success = ""
                st.rerun()
        with col2:
            if st.button("Create Account", use_container_width=True):
                st.session_state.auth_tab = "signup"
                st.session_state.auth_error = ""
                st.session_state.auth_success = ""
                st.rerun()
        # Error / success banners
        if st.session_state.auth_error:
            st.markdown(f'<div class="auth-error">⚠️ {st.session_state.auth_error}</div>',
                        unsafe_allow_html=True)
        if st.session_state.auth_success:
            st.markdown(f'<div class="auth-success">✅ {st.session_state.auth_success}</div>',
                        unsafe_allow_html=True)
        # ── LOGIN FORM ──
        if st.session_state.auth_tab == "login":
            st.markdown('<div class="auth-label">Email</div>', unsafe_allow_html=True)
            login_email = st.text_input("Email", placeholder="you@example.com",
                                        label_visibility="collapsed", key="login_email")

            st.markdown('<div class="auth-label" style="margin-top:.8rem">Password</div>',
                        unsafe_allow_html=True)
            login_pw = st.text_input("Password", type="password", placeholder="••••••••",
                                     label_visibility="collapsed", key="login_pw")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In →", key="do_login", use_container_width=True):
                st.session_state.auth_error = ""
                st.session_state.auth_success = ""

                email = login_email.strip().lower()
                if not email or not login_pw:
                    st.session_state.auth_error = "Please fill in all fields."
                    st.rerun()
                else:
                    with st.spinner("Signing In..."):
                        data, status = api_login(email, login_pw)
                        if status != 200:
                            st.session_state.auth_error = data.get("detail", "Login failed")
                            st.rerun()
                        else:
                            user = data.get("user")
                            if not user:
                                st.session_state.auth_error = "User data not found. Please try again."
                                st.rerun()
                            st.session_state.token = data["access_token"]
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            settings = fetch_settings(st.session_state.token)
                            if settings:
                                st.session_state.selected_model = settings.get("selected_model", "llama-3.3-70b-versatile")
                                st.session_state.chunk_size = settings.get("chunk_size", 512)
                                st.session_state.top_k = settings.get("top_k", 5)
                                st.session_state.temperature = settings.get("temperature", 0.3)
                                st.session_state.theme = settings.get("theme", "Dark (default)")
                            else:
                                st.session_state.selected_model =  "llama-3.3-70b-versatile"
                                st.session_state.chunk_size =  512
                                st.session_state.top_k =  5
                                st.session_state.temperature =  0.3
                                st.session_state.theme = "Dark (default)"
                            st.session_state.auth_error = ""
                            st.session_state.auth_success = "Welcome back!"
                            st.rerun()

        # ── SIGNUP FORM ──
        else:
            st.markdown('<div class="auth-label">Full Name</div>', unsafe_allow_html=True)
            su_name = st.text_input("Full Name", placeholder="Jane Smith",
                                    label_visibility="collapsed", key="su_name")

            st.markdown('<div class="auth-label" style="margin-top:.8rem">Email</div>',
                        unsafe_allow_html=True)
            su_email = st.text_input("Email", placeholder="jane@example.com",
                                     label_visibility="collapsed", key="su_email")

            st.markdown('<div class="auth-label" style="margin-top:.8rem">Password</div>',
                        unsafe_allow_html=True)
            su_pw = st.text_input("Password", type="password", placeholder="Min. 8 characters",
                                  label_visibility="collapsed", key="su_pw")

            # Password strength indicator
            if su_pw:
                score, label, color = pw_strength(su_pw)
                pct = int((score / 5) * 100)
                st.markdown(f"""
                <div class="pw-strength-wrap">
                    <div style="background:var(--surface2);border-radius:10px;height:5px;overflow:hidden">
                        <div class="pw-strength-bar" style="width:{pct}%;background:{color};height:5px;border-radius:10px"></div>
                    </div>
                    <div class="pw-strength-label" style="color:{color}">{label}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="auth-label" style="margin-top:.8rem">Confirm Password</div>',
                        unsafe_allow_html=True)
            su_confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password",
                                       label_visibility="collapsed", key="su_confirm")

            st.markdown("""
            <div style="font-size:.76rem;color:var(--muted);margin:.8rem 0">
                By creating an account you agree to our
                <a href="#" style="color:var(--accent)">Terms of Service</a> and
                <a href="#" style="color:var(--accent)">Privacy Policy</a>.
            </div>
            """, unsafe_allow_html=True)

            if st.button("Create Account →", key="do_signup", use_container_width=True):
                st.session_state.auth_error = ""
                st.session_state.auth_success = ""
                err = validate_signup(su_name, su_email, su_pw, su_confirm)
                if err:
                    st.session_state.auth_error = err
                    st.rerun()
                else:
                    with st.spinner("Creating Account..."):
                        data, status = api_signup(su_name, su_email, su_pw)
                        if status != 200:
                            st.session_state.auth_error = data.get("detail", "Signup failed")
                            st.rerun()
                        else:
                            st.session_state.auth_success = f"Account created! Welcome, {su_name.split()[0]}. Please sign in."
                            st.session_state.auth_tab = "login"
                            st.rerun()
            if st.button("Sign In →",key="switch_to_login",use_container_width=True):
                st.session_state.auth_tab = "login"
                st.rerun()
