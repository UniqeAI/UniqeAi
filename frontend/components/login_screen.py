import streamlit as st
from datetime import datetime

def render_choyrens_header():
    """CHOYRENS AI header'ını render et"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: var(--primary-blue); font-family: 'Orbitron', sans-serif; margin: 0;">
            🤖 CHOYRENS AI
        </h1>
        <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Telekom AI Asistanı
        </p>
    </div>
    """, unsafe_allow_html=True)

def login_screen():
    """Login ekranını göster"""
    render_choyrens_header()
    st.title("🔐 Giriş Yap")
    
    # Login formu
    with st.form(key="login_form"):
        username = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adınızı girin")
        password = st.text_input("🔒 Şifre", type="password", placeholder="Şifrenizi girin")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_button = st.form_submit_button("🚀 Giriş Yap", use_container_width=True)
        
        if login_button:
            if username and password:
                st.success(f"✅ Hoş geldiniz, {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = 'chat'
                st.rerun()
            else:
                st.error("❌ Lütfen kullanıcı adı ve şifre girin!")
    
    # Kayıt ol linki
    st.markdown("<div style='margin-top: 2rem; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("**Hesabınız yok mu?**", unsafe_allow_html=True)
    
    if st.button("📝 Kayıt Ol", key="register_from_login", use_container_width=True):
        st.session_state.page = 'register'
        st.rerun()
    
    # Ana sayfaya dön
    if st.button("🏠 Ana Sayfa", key="back_home_login", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True) 