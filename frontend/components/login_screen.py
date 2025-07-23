import streamlit as st

# Demo kullanıcıları - app.py'den import ediyoruz
DEMO_USERS = {
    "admin": {"password": "123", "name": "Admin Kullanıcı"},
    "demo": {"password": "demo123", "name": "Demo Kullanıcı"},
    "test": {"password": "test123", "name": "Test Kullanıcı"}
}

def handle_login():
    """Giriş işlemini yönetir"""
    username = st.session_state.get("login_username", "")
    password = st.session_state.get("login_password", "")
    
    # Basit doğrulama
    if not username or not password:
        st.session_state["login_error"] = "Lütfen kullanıcı adı ve şifrenizi girin"
        return
    
    # Kullanıcı kontrol
    if username in DEMO_USERS and DEMO_USERS[username]["password"] == password:
        st.session_state["logged_in"] = True
        st.session_state["current_user"] = DEMO_USERS[username]["name"]
        st.session_state["current_screen"] = "main"
        st.session_state["login_error"] = None
        st.session_state["login_success"] = f"Hoş geldiniz, {DEMO_USERS[username]['name']}!"
        st.rerun()
    else:
        st.session_state["login_error"] = "Kullanıcı adı veya şifre hatalı"

def render_login_screen():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2em;
        font-family: 'Inter', sans-serif;
    }
    
    .login-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 2em;
        padding: 3em;
        margin: 2em auto;
        max-width: 450px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideInUp 0.8s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .login-header {
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
    
    .login-title {
        font-size: 2.5em;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        color: #1e293b;
        margin-bottom: 0.5em;
    }
    
    .login-subtitle {
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
    
    .login-button {
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
    
    .login-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(102,126,234,0.4);
    }
    
    .signup-link {
        text-align: center;
        font-size: 0.95em;
        color: #6b7280;
    }
    
    .signup-link a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
    }
    
    .signup-link a:hover {
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
        .login-container {
            margin: 1em;
            padding: 2em;
        }
        .login-title {
            font-size: 2em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Ana container
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <div class="logo-container">
                <div class="logo-icon">💬</div>
            </div>
            <h1 class="login-title">CayrosAi'ya Giriş</h1>
            <p class="login-subtitle">Akıllı telekom asistanınızla tanışın</p>
        </div>
    """, unsafe_allow_html=True)

    # Hata ve başarı mesajları
    if st.session_state.get("login_error"):
        st.markdown(f"<div class='error-message'>❌ {st.session_state['login_error']}</div>", unsafe_allow_html=True)
    
    if st.session_state.get("login_success"):
        st.markdown(f"<div class='success-message'>✅ {st.session_state['login_success']}</div>", unsafe_allow_html=True)

    # Form alanları
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="form-label">Kullanıcı Adı</label>', unsafe_allow_html=True)
    username = st.text_input("", placeholder="admin", key="login_username", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label class="form-label">Şifre</label>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="••••••••", key="login_password", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Giriş butonu
    if st.button("Giriş Yap", use_container_width=True, key="login_button"):
        handle_login()
    
    # Kayıt ol linki
    st.markdown("""
        <div class="signup-link">
            Hesabınız yok mu? <a href="#" onclick="document.querySelector('[data-testid=\"stButton\"] button').click()">Kayıt olun</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Kayıt ol butonu (gizli)
    if st.button("Go to Signup", key="go_to_signup", type="secondary"):
        st.session_state["current_screen"] = "signup"
        st.rerun()
    
    # Demo bilgisi
    st.markdown("""
    <div style="margin-top: 2em; text-align: center; color: #6b7280; font-size: 0.9em;">
        <strong>Demo Hesapları:</strong><br>
        👤 admin - Şifre: 123<br>
        👤 demo - Şifre: demo123<br>
        👤 test - Şifre: test123
    </div>
    """, unsafe_allow_html=True) 