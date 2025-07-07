import streamlit as st

def render_main_screen():
    # CSS stilleri
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    .main-container {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(25px);
        border-radius: 2.5em;
        padding: 4em;
        margin: 2em auto;
        max-width: 800px;
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        border: 2px solid rgba(255,255,255,0.9);
        animation: slideInUp 0.8s ease;
        font-family: 'Poppins', sans-serif;
    }
    .main-header {
        text-align: center;
        margin-bottom: 3em;
    }
    .main-title {
        font-size: 4.5em;
        font-weight: 900;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(45deg, #dc3545, #0d6efd, #198754);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5em;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
        letter-spacing: -2px;
    }
    .main-subtitle {
        font-size: 1.6em;
        color: #000000;
        margin-bottom: 1em;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    .feature-card {
        background: rgba(255,255,255,0.1);
        border-radius: 1.5em;
        padding: 2em;
        margin: 2em 0;
        border: 2px solid rgba(220,53,69,0.3);
    }
    .feature-title {
        color: #dc3545;
        margin-bottom: 1em;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5em;
    }
    .feature-item {
        background: rgba(220,53,69,0.1);
        padding: 1.5em;
        border-radius: 1em;
        border-left: 4px solid #dc3545;
    }
    .feature-item.blue {
        background: rgba(13,110,253,0.1);
        border-left: 4px solid #0d6efd;
    }
    .feature-item.green {
        background: rgba(25,135,84,0.1);
        border-left: 4px solid #198754;
    }
    .feature-item.yellow {
        background: rgba(255,193,7,0.1);
        border-left: 4px solid #ffc107;
    }
    .feature-item h4 {
        margin-bottom: 0.5em;
        font-size: 1.2em;
        font-weight: bold;
    }
    .feature-item.blue h4 { color: #0d6efd; }
    .feature-item.green h4 { color: #198754; }
    .feature-item.yellow h4 { color: #ffc107; }
    .feature-item p {
        color: #000;
        font-size: 0.9em;
        margin: 0;
    }
    .guide-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2em;
    }
    .guide-section h4 {
        color: #0d6efd;
        margin-bottom: 1em;
        font-size: 1.3em;
        font-weight: bold;
    }
    .guide-section ul {
        color: #000;
        font-size: 0.9em;
        line-height: 1.6;
        margin: 0;
        padding-left: 1.5em;
    }
    .guide-section li {
        margin-bottom: 0.5em;
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
    @media (max-width: 600px) {
        .main-container {
            margin: 1em;
            padding: 2em;
        }
        .main-title {
            font-size: 3.2em;
        }
        .guide-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Ana container başlangıcı
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">UniqeAi</div>
        <div class="main-subtitle">Akıllı Asistanınız</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo Özellikleri
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🚀 Demo Özellikleri</div>
        <div class="feature-grid">
            <div class="feature-item">
                <h4>💬 Akıllı Sohbet</h4>
                <p>Gerçek zamanlı AI destekli müşteri hizmetleri</p>
            </div>
            <div class="feature-item blue">
                <h4>🔧 Araç Entegrasyonu</h4>
                <p>Kullanıcı bilgileri, fatura sorgulama ve daha fazlası</p>
            </div>
            <div class="feature-item green">
                <h4>📱 Responsive Tasarım</h4>
                <p>Mobil ve masaüstü uyumlu modern arayüz</p>
            </div>
            <div class="feature-item yellow">
                <h4>🧪 Test Sistemi</h4>
                <p>Otomatik demo senaryosu testleri</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Kullanım Rehberi
    st.markdown("""
    <div class="feature-card" style="border-color: rgba(13,110,253,0.3);">
        <div class="feature-title" style="color: #0d6efd;">📖 Kullanım Rehberi</div>
        <div class="guide-grid">
            <div class="guide-section">
                <h4>🎯 Hızlı Başlangıç</h4>
                <ul>
                    <li>💬 "Sohbete Başla" butonuna tıklayın</li>
                    <li>🚀 Hızlı erişim menüsünden senaryo seçin</li>
                    <li>💭 Mesajınızı yazın veya hazır cümleleri kullanın</li>
                    <li>🔍 AI asistanınızın yanıtını bekleyin</li>
                </ul>
            </div>
            <div class="guide-section">
                <h4>🔧 Demo Senaryoları</h4>
                <ul>
                    <li>💰 Fatura bilgisi sorgulama</li>
                    <li>👤 Kullanıcı bilgileri görüntüleme</li>
                    <li>🎉 Kampanya ve teklif bilgileri</li>
                    <li>🔧 Teknik destek talepleri</li>
                    <li>📦 Paket detayları ve değişiklik</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Container kapanışı
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Buton işlemleri - Container dışında
    st.markdown("<div style='margin-top: 2em;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💬 Sohbete Başla", use_container_width=True, key="start_chat"):
            st.session_state["current_screen"] = "chat"
            st.rerun()
    
    with col2:
        if st.button("📊 Hesabımı Yönet", use_container_width=True, key="manage_account"):
            st.info("Hesap yönetimi özelliği yakında eklenecek!")
    
    with col3:
        if st.button("🎯 Teklifleri Gör", use_container_width=True, key="view_offers"):
            st.info("Kampanya ve teklifler yakında eklenecek!")
    
    with col4:
        if st.button("🔧 Destek Al", use_container_width=True, key="get_support"):
            st.info("Teknik destek özelliği yakında eklenecek!")
    
    if st.button("🚪 Çıkış Yap", use_container_width=True, key="logout"):
        st.session_state["logged_in"] = False
        st.session_state["current_screen"] = "login"
        st.rerun() 