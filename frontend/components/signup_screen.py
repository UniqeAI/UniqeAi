import streamlit as st

def handle_signup():
    """Kayıt işlemini yönetir"""
    name = st.session_state.get("signup_name", "")
    username = st.session_state.get("signup_username", "")
    email = st.session_state.get("signup_email", "")
    password = st.session_state.get("signup_password", "")
    password_confirm = st.session_state.get("signup_password_confirm", "")
    
    # Basit doğrulama
    if not all([name, username, password, password_confirm]):
        st.session_state["signup_error"] = "Lütfen gerekli alanları doldurun"
        return
    
    if password != password_confirm:
        st.session_state["signup_error"] = "Şifreler eşleşmiyor"
        return
    
    if len(password) < 3:
        st.session_state["signup_error"] = "Şifre en az 3 karakter olmalı"
        return
    
    # Kullanıcı adı uzunluk kontrolü
    if len(username) < 3:
        st.session_state["signup_error"] = "Kullanıcı adı en az 3 karakter olmalı"
        return
    
    # E-posta formatı basit kontrolü (eğer doldurulduysa)
    if email and ("@" not in email or "." not in email):
        st.session_state["signup_error"] = "Geçerli bir e-posta adresi girin"
        return
    
    # Başarılı kayıt
    st.session_state["signup_error"] = None
    st.session_state["signup_success"] = f"Kayıt başarılı! Hoş geldiniz, {name}!"
    st.session_state["logged_in"] = True
    st.session_state["current_user"] = name
    st.session_state["current_screen"] = "main"
    st.rerun()

def render_signup_screen():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2em;
        font-family: 'Inter', sans-serif;
    }
    
    .signup-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 2em;
        padding: 3em;
        margin: 2em auto;
        max-width: 500px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideInUp 0.8s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .signup-header {
        text-align: center;
        margin-bottom: 2.5em;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5em;
    }
    
    .logo-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2em;
        color: white;
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    
    .signup-title {
        font-size: 2.5em;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        color: #1e293b;
        margin-bottom: 0.5em;
    }
    
    .signup-subtitle {
        font-size: 1.1em;
        color: #64748b;
        margin-bottom: 0.5em;
        font-weight: 500;
    }
    
    .form-group {
        margin-bottom: 1.5em;
    }
    
    .form-label {
        display: block;
        font-size: 1em;
        color: #374151;
        margin-bottom: 0.5em;
        font-weight: 600;
    }
    
    .form-input {
        width: 100%;
        padding: 1em 1.2em;
        font-size: 1em;
        border: 2px solid #e5e7eb;
        border-radius: 0.8em;
        background: #f9fafb;
        color: #374151;
        transition: all 0.3s ease;
        font-weight: 500;
        box-sizing: border-box;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #667eea;
        background: white;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
    }
    
    .form-input::placeholder {
        color: #9ca3af;
    }
    
    .signup-button {
        width: 100%;
        padding: 1.2em;
        font-size: 1.1em;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.8em;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 1.5em;
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    
    .signup-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(102,126,234,0.4);
    }
    
    .login-link {
        text-align: center;
        font-size: 0.95em;
        color: #6b7280;
    }
    
    .login-link a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
    }
    
    .login-link a:hover {
        text-decoration: underline;
    }
    
    .error-message {
        background: #fef2f2;
        color: #ef4444;
        padding: 0.8em 1em;
        border-radius: 0.8em;
        margin-bottom: 1em;
        border: 1px solid #fecaca;
        font-size: 0.9em;
    }
    
    .success-message {
        background: #f0fdf4;
        color: #22c55e;
        padding: 0.8em 1em;
        border-radius: 0.8em;
        margin-bottom: 1em;
        border: 1px solid #bbf7d0;
        font-size: 0.9em;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @media (max-width: 768px) {
        .signup-container {
            margin: 1em;
            padding: 2em;
        }
        .signup-title {
            font-size: 2em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Ana container
    st.markdown("""
    <div class="signup-container">
        <div class="signup-header">
            <div class="logo-container">
                <div class="logo-icon">💬</div>
            </div>
            <h1 class="signup-title">Kayıt Ol</h1>
            <p class="signup-subtitle">Zaten hesabınız var mı? <a href="#" style="color: #667eea; text-decoration: none; font-weight: 600;">Giriş Yap</a></p>
        </div>
    """, unsafe_allow_html=True)

    # Hata ve başarı mesajları
    if st.session_state.get("signup_error"):
        st.markdown(f"<div class='error-message'>❌ {st.session_state['signup_error']}</div>", unsafe_allow_html=True)
    
    if st.session_state.get("signup_success"):
        st.markdown(f"<div class='success-message'>✅ {st.session_state['signup_success']}</div>", unsafe_allow_html=True)

    # Form alanları
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="form-label">Ad Soyad</label>', unsafe_allow_html=True)
    name = st.text_input("", placeholder="Adınız ve soyadınız", key="signup_name", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="form-label">Kullanıcı Adı</label>', unsafe_allow_html=True)
    username = st.text_input("", placeholder="kullaniciadi", key="signup_username", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="form-label">E-posta (İsteğe bağlı)</label>', unsafe_allow_html=True)
    email = st.text_input("", placeholder="ornek@email.com", key="signup_email", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="form-label">Şifre</label>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="••••••••", key="signup_password", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="form-label">Şifre Tekrar</label>', unsafe_allow_html=True)
    password_confirm = st.text_input("", type="password", placeholder="••••••••", key="signup_password_confirm", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Kayıt ol butonu
    if st.button("Kayıt Ol", use_container_width=True, key="signup_button"):
        handle_signup()
    
    # Giriş yap linki
    st.markdown("""
        <div class="login-link">
            Zaten hesabınız var mı? <a href="#" onclick="document.querySelector('[data-testid=\"stButton\"] button').click()">Giriş Yap</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Giriş yap butonu (gizli)
    if st.button("Go to Login", key="go_to_login", type="secondary"):
        st.session_state["current_screen"] = "login"
        st.rerun() 