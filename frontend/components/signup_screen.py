import streamlit as st

def render_signup_screen():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 1.5em;
        font-family: 'Inter', sans-serif;
    }
    .signup-container {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(25px);
        border-radius: 2.5em;
        padding: 4em;
        margin: 2em auto;
        max-width: 600px;
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        border: 2px solid rgba(255,255,255,0.9);
        animation: slideInUp 0.8s ease;
        font-family: 'Poppins', sans-serif;
    }
    .signup-header {
        text-align: center;
        margin-bottom: 3em;
    }
    .signup-title {
        font-size: 4.5em;
        font-weight: 900;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6, #1d4ed8, #2563eb, #1e40af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5em;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
        letter-spacing: -2px;
    }
    .signup-subtitle {
        font-size: 1.6em;
        color: #000000;
        margin-bottom: 0.5em;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5em;
        margin-bottom: 2em;
    }
    .form-group {
        margin-bottom: 2.5em;
        position: relative;
        animation: fadeInUp 0.8s ease;
    }
    .form-group.full-width {
        grid-column: 1 / -1;
    }
    .form-label {
        display: block;
        font-size: 1.5em;
        color: #000000;
        margin-bottom: 1.2em;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
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
    .form-input.error {
        border-color: #f44336;
        box-shadow: 0 0 20px rgba(244,67,54,0.4);
    }
    .form-input.success {
        border-color: #4caf50;
        box-shadow: 0 0 20px rgba(76,175,80,0.4);
    }
    .signup-button {
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
            0 20px 45px rgba(102,126,234,0.6),
            0 0 0 1px rgba(255,255,255,0.2);
        background: linear-gradient(45deg, #764ba2, #667eea, #764ba2);
    }
    .signup-button:active {
        transform: translateY(-3px) scale(1.02);
    }
    .back-button {
        width: 100%;
        padding: 1.8em;
        font-size: 1.5em;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(45deg, #4facfe, #00f2fe, #4facfe);
        color: #fff;
        border: none;
        border-radius: 1.5em;
        cursor: pointer;
        transition: all 0.5s ease;
        box-shadow: 
            0 12px 30px rgba(79,172,254,0.4),
            0 0 0 1px rgba(255,255,255,0.1);
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        overflow: hidden;
    }
    .back-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    .back-button:hover::before {
        left: 100%;
    }
    .back-button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 15px 40px rgba(79,172,254,0.6),
            0 0 0 1px rgba(255,255,255,0.2);
        background: linear-gradient(45deg, #00f2fe, #4facfe, #00f2fe);
    }
    .back-button:active {
        transform: translateY(-3px) scale(1.02);
    }
    .login-link {
        text-align: center;
        margin-top: 2em;
        font-size: 1.1em;
        color: #e3f8fc;
        font-family: 'Inter', sans-serif;
    }
    .login-link a {
        color: #667eea;
        text-decoration: none;
        font-weight: bold;
        transition: color 0.3s ease;
    }
    .login-link a:hover {
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
    .validation-indicator {
        position: absolute;
        right: 1.2em;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.2em;
        transition: all 0.3s ease;
    }
    .validation-indicator.valid {
        color: #4caf50;
    }
    .validation-indicator.invalid {
        color: #f44336;
    }
    .password-strength {
        margin-top: 0.5em;
        font-size: 0.9em;
        color: #e3f8fc;
        font-family: 'Inter', sans-serif;
    }
    .strength-bar {
        height: 4px;
        background: rgba(255,255,255,0.3);
        border-radius: 2px;
        margin-top: 0.3em;
        overflow: hidden;
    }
    .strength-fill {
        height: 100%;
        transition: all 0.3s ease;
        border-radius: 2px;
    }
    .strength-weak { background: #f44336; width: 25%; }
    .strength-medium { background: #ff9800; width: 50%; }
    .strength-strong { background: #4caf50; width: 75%; }
    .strength-very-strong { background: #00c853; width: 100%; }
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
    @media (max-width: 600px) {
        .signup-container {
            margin: 1em;
            padding: 2em;
        }
        .signup-title {
            font-size: 3.2em;
        }
        .form-row {
            grid-template-columns: 1fr;
        }
        .form-input {
            padding: 1em 1.2em;
            font-size: 1em;
        }
        .signup-button, .back-button {
            padding: 1.5em;
            font-size: 1.4em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Logo ve başlık
    st.markdown("""
    <div class="signup-container">
        <div class="signup-header">
            <div class="logo-container">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712037.png" alt="UniqeAi Logo" class="logo-icon"/>
            </div>
            <div class="signup-title">Kayıt Ol</div>
            <div class="signup-subtitle">Hesabınızı Oluşturun</div>
        </div>
    """, unsafe_allow_html=True)

    # Hata ve başarı mesajları
    if st.session_state.get("signup_error"):
        st.markdown(f"<div class='error-message'>❌ {st.session_state['signup_error']}</div>", unsafe_allow_html=True)
    
    if st.session_state.get("signup_success"):
        st.markdown(f"<div class='success-message'>✅ {st.session_state['signup_success']}</div>", unsafe_allow_html=True)

    # Form işleme
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Kullanıcı Adı", placeholder="Kullanıcı adınızı girin", key="signup_username")
        first_name = st.text_input("Ad", placeholder="Adınızı girin", key="signup_first_name")
        last_name = st.text_input("Soyad", placeholder="Soyadınızı girin", key="signup_last_name")
        email = st.text_input("E-posta", placeholder="E-posta adresinizi girin", key="signup_email")
        phone = st.text_input("Telefon", placeholder="Telefon numaranızı girin", key="signup_phone")
        password = st.text_input("Şifre", type="password", placeholder="Güçlü bir şifre oluşturun", key="signup_password")
        confirm_password = st.text_input("Şifre Tekrar", type="password", placeholder="Şifrenizi tekrar girin", key="signup_confirm_password")
        
        if st.button("🚀 Hesap Oluştur", use_container_width=True, key="signup_button"):
            if all([username, first_name, last_name, email, phone, password, confirm_password]):
                if password == confirm_password:
                    if len(password) >= 6:
                        # Kayıt başarılı - direkt chat ekranına yönlendir
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.session_state["current_screen"] = "chat"
                        st.session_state["signup_success"] = f"Hesabınız başarıyla oluşturuldu! Hoş geldiniz, {username}!"
                        st.session_state["signup_error"] = None
                        st.rerun()
                    else:
                        st.session_state["signup_error"] = "Şifre en az 6 karakter olmalıdır!"
                        st.session_state["signup_success"] = None
                        st.rerun()
                else:
                    st.session_state["signup_error"] = "Şifreler eşleşmiyor!"
                    st.session_state["signup_success"] = None
                    st.rerun()
            else:
                st.session_state["signup_error"] = "Lütfen tüm alanları doldurun!"
                st.session_state["signup_success"] = None
                st.rerun()
        
        if st.button("🔙 Giriş Yap", use_container_width=True, key="go_to_login"):
            st.session_state["current_screen"] = "login"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True) 