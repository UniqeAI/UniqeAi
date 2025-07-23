import streamlit as st

def render_main_screen():
    # CSS stilleri
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    .main-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
        padding: 2em;
        font-family: 'Inter', sans-serif;
    }
    
    .hero-section {
        text-align: center;
        margin-bottom: 4em;
        padding: 3em 2em;
        background: rgba(255,255,255,0.95);
        border-radius: 2em;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5em;
        color: white;
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    
    .main-title {
        font-size: 4em;
        font-weight: 900;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5em;
        letter-spacing: -2px;
    }
    
    .main-subtitle {
        font-size: 1.5em;
        color: #64748b;
        margin-bottom: 1em;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .main-description {
        font-size: 1.1em;
        color: #94a3b8;
        margin-bottom: 2em;
        font-weight: 400;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2em;
        margin: 3em 0;
    }
    
    .feature-card {
        background: white;
        border-radius: 1.5em;
        padding: 2.5em;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        width: 60px;
        height: 60px;
        margin: 0 auto 1.5em;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8em;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .feature-icon.green {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    }
    
    .feature-icon.blue {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    }
    
    .feature-icon.purple {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    }
    
    .feature-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1em;
        font-family: 'Poppins', sans-serif;
    }
    
    .feature-description {
        font-size: 1em;
        color: #64748b;
        line-height: 1.6;
    }
    
    .cta-buttons {
        display: flex;
        gap: 1.5em;
        justify-content: center;
        margin: 2em 0;
        flex-wrap: wrap;
    }
    
    .cta-button {
        padding: 1.2em 2.5em;
        font-size: 1.1em;
        font-weight: 600;
        border: none;
        border-radius: 1em;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5em;
        font-family: 'Inter', sans-serif;
    }
    
    .cta-button.primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    
    .cta-button.primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(102,126,234,0.4);
    }
    
    .cta-button.secondary {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
    }
    
    .cta-button.secondary:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5em;
        margin: 3em 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 1em;
        padding: 2em;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .stat-number {
        font-size: 2.5em;
        font-weight: 900;
        color: #667eea;
        margin-bottom: 0.5em;
        font-family: 'Poppins', sans-serif;
    }
    
    .stat-label {
        font-size: 0.9em;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5em;
        }
        .hero-section {
            padding: 2em 1em;
        }
        .cta-buttons {
            flex-direction: column;
            align-items: center;
        }
        .cta-button {
            width: 100%;
            max-width: 300px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Ana container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <div class="logo-container">
            <div class="logo-icon">💬</div>
        </div>
        <h1 class="main-title">CayrosAi</h1>
        <p class="main-subtitle">Akıllı Telekom Müşteri Hizmetleri Asistanı</p>
        <p class="main-description">
            7/24 hizmet veren yapay zeka destekli asistanınız. Fatura sorgulama, paket 
            değişikliği, teknik destek ve daha fazlası için hemen başlayın.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Özellik kartları
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon green">✓</div>
            <h3 class="feature-title">7/24 Hizmet</h3>
            <p class="feature-description">
                Her zaman yanınızda,<br>
                istediğiniz zaman destek alın
            </p>
        </div>
        <div class="feature-card">
            <div class="feature-icon blue">⚡</div>
            <h3 class="feature-title">Anında Yanıt</h3>
            <p class="feature-description">
                Sorularınız için beklemek yok,<br>
                anında çözüm
            </p>
        </div>
        <div class="feature-card">
            <div class="feature-icon purple">🎯</div>
            <h3 class="feature-title">Akıllı Çözüm</h3>
            <p class="feature-description">
                Duygu analizi ile<br>
                kişiselleştirilmiş deneyim
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    st.markdown("""
    <div class="cta-buttons">
        <button class="cta-button primary" onclick="window.location.reload()">
            🚀 Hemen Başla
        </button>
        <button class="cta-button secondary" onclick="window.location.reload()">
            🔐 Giriş Yap
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Performans göstergeleri
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">7/24</div>
            <div class="stat-label">Kesintisiz Hizmet</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">&lt;1sn</div>
            <div class="stat-label">Yanıt Süresi</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">%99</div>
            <div class="stat-label">Başarı Oranı</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">Sabır</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Streamlit butonlar
    st.markdown("<div style='margin-top: 2em;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Hemen Başla", use_container_width=True, key="start_chat"):
            st.session_state["current_screen"] = "chat"
            st.rerun()
    
    with col2:
        if st.button("🔐 Giriş Yap", use_container_width=True, key="go_to_login"):
            st.session_state["current_screen"] = "login"
            st.rerun()
    
    with col3:
        if st.button("📝 Kayıt Ol", use_container_width=True, key="go_to_signup"):
            st.session_state["current_screen"] = "signup"
            st.rerun() 