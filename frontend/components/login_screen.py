import streamlit as st

# Demo kullanıcıları - app.py'den import ediyoruz
DEMO_USERS = {
    "admin": {"password": "123", "name": "Admin User"},
    "demo": {"password": "demo123", "name": "Demo User"},
    "test": {"password": "test123", "name": "Test User"}
}

def handle_login():
    username = st.session_state.get("login_username", "").strip()
    password = st.session_state.get("login_password", "").strip()
    
    # Giriş validasyonu iyileştirmesi
    if not username or not password:
        st.session_state["login_error"] = "Kullanıcı adı ve şifre alanları boş bırakılamaz."
        st.rerun()
    
    # Demo kullanıcıları kontrolü
    if username in DEMO_USERS and password == DEMO_USERS[username]["password"]:
        st.session_state["logged_in"] = True
        st.session_state["current_screen"] = "main"
        st.session_state["login_error"] = ""
        st.session_state["login_username"] = username
        st.session_state["username"] = username
        st.rerun()
    else:
        # Kayıtlı kullanıcılar arasında kontrol
        registered = st.session_state.get("registered_users", [])
        if any(u["username"] == username and u["password"] == password for u in registered):
            st.session_state["logged_in"] = True
            st.session_state["current_screen"] = "main"
            st.session_state["login_error"] = ""
            st.session_state["login_username"] = username
            st.session_state["username"] = username
            st.rerun()
        else:
            st.session_state["login_error"] = "Kullanıcı adı veya şifre hatalı ya da kayıtlı değilsiniz."
            st.rerun()

def render_login_screen():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 1.5em;
        font-family: 'Inter', sans-serif;
    }
    .login-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(25px);
        border-radius: 2.5em;
        padding: 4em;
        margin: 2em auto;
        max-width: 550px;
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        border: 2px solid rgba(255,255,255,0.9);
        animation: slideInUp 1s ease;
        position: relative;
        overflow: hidden;
        font-family: 'Poppins', sans-serif;
    }
    .login-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.1), transparent);
        transition: left 0.8s ease;
    }
    .login-container:hover::before {
        left: 100%;
    }
    .login-header {
        text-align: center;
        margin-bottom: 3em;
        position: relative;
    }
    .login-title {
        font-size: 4.5em;
        font-weight: 900;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6, #1d4ed8, #2563eb, #1e40af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5em;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: titleGlow 2s ease-in-out infinite alternate;
        letter-spacing: -2px;
    }
    .login-subtitle {
        font-size: 1.6em;
        color: #000000;
        margin-bottom: 0.5em;
        font-weight: 700;
        letter-spacing: 1px;
        font-family: 'Inter', sans-serif;
    }
    .form-group {
        margin-bottom: 2.5em;
        position: relative;
        animation: fadeInUp 0.8s ease;
    }
    .form-label {
        display: block;
        font-size: 1.5em;
        color: #000000;
        margin-bottom: 1.2em;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        letter-spacing: 0.8px;
        position: relative;
        font-family: 'Inter', sans-serif;
    }
    .form-label::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.3s ease;
    }
    .form-group:focus-within .form-label::after {
        width: 100%;
    }
    .form-input {
        width: 100%;
        padding: 1.8em 2.5em;
        font-size: 1.4em;
        border: 3px solid rgba(0,0,0,0.08);
        border-radius: 1.5em;
        background: rgba(255,255,255,0.98);
        color: #000000;
        transition: all 0.5s ease;
        box-shadow: 
            0 8px 25px rgba(0,0,0,0.08),
            0 0 0 1px rgba(255,255,255,0.1);
        font-weight: 500;
        letter-spacing: 0.8px;
        position: relative;
        font-family: 'Inter', sans-serif;
    }
    .form-input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 
            0 0 30px rgba(102,126,234,0.3),
            0 8px 25px rgba(0,0,0,0.1);
        transform: translateY(-5px) scale(1.02);
        background: rgba(255,255,255,1);
    }
    .form-input::placeholder {
        color: #666666;
        font-weight: 400;
        font-style: italic;
        transition: color 0.3s ease;
    }
    .form-input:focus::placeholder {
        color: #999999;
    }
    .login-button {
        width: 100%;
        padding: 2.2em;
        font-size: 1.8em;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(45deg, #667eea, #764ba2, #667eea);
        color: #fff;
        border: none;
        border-radius: 1.5em;
        cursor: pointer;
        transition: all 0.5s ease;
        box-shadow: 
            0 15px 35px rgba(102,126,234,0.4),
            0 0 0 1px rgba(255,255,255,0.1);
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        overflow: hidden;
        margin-bottom: 1em;
    }
    .login-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    .login-button:hover::before {
        left: 100%;
    }
    .login-button:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 
            0 20px 45px rgba(102,126,234,0.6),
            0 0 0 1px rgba(255,255,255,0.2);
        background: linear-gradient(45deg, #764ba2, #667eea, #764ba2);
    }
    .login-button:active {
        transform: translateY(-3px) scale(1.02);
    }
    .signup-button {
        width: 100%;
        padding: 2.2em;
        font-size: 1.8em;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(45deg, #764ba2, #667eea, #764ba2);
        color: #fff;
        border: none;
        border-radius: 1.5em;
        cursor: pointer;
        transition: all 0.5s ease;
        box-shadow: 
            0 15px 35px rgba(118,75,162,0.4),
            0 0 0 1px rgba(255,255,255,0.1);
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        overflow: hidden;
    }
    .signup-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    .signup-button:hover::before {
        left: 100%;
    }
    .signup-button:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 
            0 20px 45px rgba(118,75,162,0.6),
            0 0 0 1px rgba(255,255,255,0.2);
        background: linear-gradient(45deg, #667eea, #764ba2, #667eea);
    }
    .signup-button:active {
        transform: translateY(-3px) scale(1.02);
    }
    .success-animation {
        animation: successPulse 0.6s ease;
    }
    .error-animation {
        animation: errorShake 0.6s ease;
    }
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 5px rgba(102,126,234,0.3)); }
        to { filter: drop-shadow(0 0 15px rgba(118,75,162,0.6)); }
    }
    @keyframes successPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    .signup-link {
        text-align: center;
        margin-top: 2em;
        font-size: 1.1em;
        color: #e3f8fc;
        font-family: 'Inter', sans-serif;
    }
    .signup-link a {
        color: #667eea;
        text-decoration: none;
        font-weight: bold;
        transition: color 0.3s ease;
    }
    .signup-link a:hover {
        color: #764ba2;
        text-shadow: 0 0 8px rgba(118,75,162,0.5);
    }
    .error-message {
        background: rgba(244,67,54,0.2);
        color: #ffcdd2;
        padding: 1em 1.2em;
        border-radius: 0.8em;
        margin-bottom: 1.5em;
        border-left: 4px solid #f44336;
        font-size: 1em;
        animation: shake 0.5s ease;
        font-family: 'Inter', sans-serif;
    }
    .success-message {
        background: rgba(76,175,80,0.2);
        color: #c8e6c9;
        padding: 1em 1.2em;
        border-radius: 0.8em;
        margin-bottom: 1.5em;
        border-left: 4px solid #4caf50;
        font-size: 1em;
        animation: slideInDown 0.5s ease;
        font-family: 'Inter', sans-serif;
    }
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    .input-icon {
        position: absolute;
        right: 1.2em;
        top: 50%;
        transform: translateY(-50%);
        color: #888;
        font-size: 1.2em;
    }
    .password-toggle {
        position: absolute;
        right: 1.2em;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        color: #888;
        cursor: pointer;
        font-size: 1.2em;
        transition: color 0.3s ease;
    }
    .password-toggle:hover {
        color: #667eea;
    }
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2em;
        gap: 1em;
    }
    .logo-icon {
        width: 80px;
        height: 80px;
        filter: drop-shadow(0 4px 8px rgba(30,58,138,0.4)) hue-rotate(240deg) brightness(0.7) contrast(1.3) saturate(1.5);
        transition: transform 0.3s ease;
    }
    .logo-icon:hover {
        transform: scale(1.1) rotate(5deg);
        filter: drop-shadow(0 6px 12px rgba(25,118,210,0.6)) hue-rotate(240deg) brightness(0.9) contrast(1.4) saturate(1.8);
    }
    @media (max-width: 600px) {
        .login-container {
            margin: 1em;
            padding: 2em;
        }
        .login-title {
            font-size: 3.2em;
        }
        .form-input {
            padding: 1em 1.2em;
            font-size: 1em;
        }
        .login-button, .signup-button {
            padding: 1.5em;
            font-size: 1.4em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Logo ve başlık
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <div class="logo-container">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712037.png" alt="UniqeAi Logo" class="logo-icon"/>
            </div>
            <div class="login-title">UniqeAi</div>
            <div class="login-subtitle">Akıllı Asistanınız</div>
        </div>
    """, unsafe_allow_html=True)

    # Hata ve başarı mesajları
    if st.session_state.get("login_error"):
        st.markdown(f"<div class='error-message'>❌ {st.session_state['login_error']}</div>", unsafe_allow_html=True)
    
    if st.session_state.get("login_success"):
        st.markdown(f"<div class='success-message'>✅ {st.session_state['login_success']}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Kullanıcı Adı", placeholder="Kullanıcı adınızı girin", key="login_username")
        password = st.text_input("Şifre", type="password", placeholder="Şifrenizi girin", key="login_password")
        
        if st.button("🚀 Giriş Yap", use_container_width=True, key="login_button"):
            handle_login()
        
        if st.button("📝 Kayıt Ol", use_container_width=True, key="go_to_signup"):
            st.session_state["current_screen"] = "signup"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True) 