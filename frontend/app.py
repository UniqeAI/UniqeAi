import streamlit as st
from streamlit.components.v1 import html
import time
import random
from datetime import datetime

# Tema ayarları
def set_theme():
    st.set_page_config(
        page_title="CHOYRENS AI",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Tema renkleri
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    if st.session_state.theme == 'dark':
        theme_colors = {
            'primary_blue': '#3b82f6',  # Mavi
            'dark_blue': '#1e3a8a',    # Koyu mavi
            'light_blue': '#e0f2fe',   # Açık mavi
            'bg_color': '#0f172a',     # Lacivertimsi koyu
            'card_bg': '#1e293b',      # Koyu gri-mavi
            'text_color': '#f8fafc',   # Beyaz
            'text_secondary': '#cbd5e1',
            'border_color': 'rgba(59, 130, 246, 0.15)',
            'shadow': 'rgba(59, 130, 246, 0.10)'
        }
    else:
        theme_colors = {
            'primary_blue': '#2563eb',  # Mavi
            'dark_blue': '#1e40af',    # Koyu mavi
            'light_blue': '#e0f2fe',   # Açık mavi
            'bg_color': '#f8fafc',     # Beyaz
            'card_bg': '#ffffff',      # Beyaz
            'text_color': '#1e293b',   # Koyu gri-mavi
            'text_secondary': '#64748b',
            'border_color': 'rgba(37, 99, 235, 0.10)',
            'shadow': 'rgba(37, 99, 235, 0.08)'
        }
    
    # Tüm beyaz boşlukları kaldıran kapsamlı CSS
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');
        
        :root {{
            --primary-blue: {theme_colors['primary_blue']};
            --dark-blue: {theme_colors['dark_blue']};
            --light-blue: {theme_colors['light_blue']};
            --bg-color: {theme_colors['bg_color']};
            --card-bg: {theme_colors['card_bg']};
            --text-color: {theme_colors['text_color']};
            --text-secondary: {theme_colors['text_secondary']};
            --border-color: {theme_colors['border_color']};
            --shadow: {theme_colors['shadow']};
        }}
        
        /* Tüm sayfa arka planı */
        html, body, #root, .stApp {{
            background-color: var(--bg-color) !important;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 100vh !important;
        }}
        
        /* Ana container */
        .stApp > div:first-child {{
            background-color: var(--bg-color) !important;
        }}
        
        /* Streamlit'in tüm beyaz container'ları */
        .main .block-container,
        .stApp [data-testid="stAppViewContainer"],
        .stApp [data-testid="stAppViewBlockContainer"],
        .css-18e3th9,
        .css-1d391kg,
        .css-1y4p8pa,
        .css-1lcbmhc,
        .css-1outpf7 {{
            background-color: var(--bg-color) !important;
            padding: 1rem !important;
            padding-bottom: 1rem !important;
            margin: 0 !important;
            max-width: 100% !important;
        }}
        
        /* Chat mesajları container'ı */
        .chat-messages {{
            background-color: var(--bg-color) !important;
            padding: 1rem !important;
            margin-bottom: 1rem !important;
        }}
        
        /* Quick action butonları */
        .quick-access {{
            background-color: var(--card-bg) !important;
            border-top: 1px solid var(--border-color) !important;
        }}
        
        /* Mesaj giriş alanı */
        .stChatInput {{
            background-color: var(--bg-color) !important;
            padding: 0 1rem !important;
            margin-bottom: 0 !important;
        }}
        
        /* Footer ve boşluklar */
        footer {{
            display: none !important;
        }}
        
        /* Diğer öğeler */
        .logo-container {{
            background-color: var(--card-bg) !important;
        }}
        
        /* Tüm yazı renkleri */
        body, .stMarkdown, .stMarkdown p, .stMarkdown div {{
            color: var(--text-color) !important;
        }}
        
        /* Streamlit header gizle */
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
        
        /* Streamlit toolbar gizle */
        .stToolbar {{
            display: none !important;
        }}
        
        /* Mesaj baloncukları */
        .user-message {{
            background: linear-gradient(135deg, {theme_colors['primary_blue']}, {theme_colors['dark_blue']});
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 0 18px;
            max-width: 80%;
            margin-left: auto;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px {theme_colors['shadow']};
            animation: fadeIn 0.3s ease;
        }}
        
        .bot-message {{
            background: {theme_colors['card_bg']};
            color: {theme_colors['text_color']};
            padding: 12px 16px;
            border-radius: 18px 18px 18px 0;
            max-width: 80%;
            margin-right: auto;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px {theme_colors['shadow']};
            border: 1px solid {theme_colors['border_color']};
            animation: fadeIn 0.3s ease;
        }}
        
        .message-content {{
            font-size: 0.95rem;
            line-height: 1.5;
            word-wrap: break-word;
        }}
        
        .message-time {{
            font-size: 0.7rem;
            opacity: 0.8;
            text-align: right;
            margin-top: 4px;
            color: {theme_colors['text_secondary']};
        }}
        
        /* Kart konteyner stilleri - Ortalı ve Renkli */
        .feature-cards-container {{
            display: flex;
            justify-content: center;
            gap: 1.2rem;
            margin: 2.5rem auto;
            max-width: 900px;
            padding: 1.5rem 1rem;
            flex-wrap: wrap;
            align-items: stretch;
        }}
        
        .feature-card {{
            background: linear-gradient(135deg, {theme_colors['card_bg']}, {theme_colors['primary_blue']}25);
            border-radius: 12px;
            padding: 1.2rem 1rem;
            box-shadow: 0 6px 18px {theme_colors['shadow']};
            border: 2px solid transparent;
            transition: all 0.4s ease;
            margin-bottom: 1rem;
            max-width: 220px;
            text-align: center;
            flex: 1;
            min-width: 180px;
            position: relative;
            overflow: hidden;
        }}
        
        .feature-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00ffff, #0080ff, #ff00ff);
        }}
        
        .feature-card:nth-child(1),
        .feature-card:nth-child(2),
        .feature-card:nth-child(3) {{
            border-color: {theme_colors['primary_blue']}40;
            background: linear-gradient(135deg, {theme_colors['card_bg']}, {theme_colors['primary_blue']}15, {theme_colors['light_blue']}30);
            box-shadow: 0 6px 18px {theme_colors['primary_blue']}20;
        }}
        .feature-card:nth-child(1):hover,
        .feature-card:nth-child(2):hover,
        .feature-card:nth-child(3):hover {{
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 12px 30px {theme_colors['primary_blue']}40, 0 0 25px {theme_colors['primary_blue']}30;
            border-color: {theme_colors['primary_blue']}90;
        }}
        .feature-card .feature-icon {{
            color: {theme_colors['primary_blue']};
            filter: drop-shadow(0 0 8px {theme_colors['primary_blue']}40);
        }}
        .feature-card .feature-title {{
            background: linear-gradient(45deg, {theme_colors['primary_blue']}, {theme_colors['light_blue']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .feature-desc {{
            font-size: 0.75rem;
            color: {theme_colors['text_secondary']} !important;
            line-height: 1.4;
            opacity: 0.9;
        }}
        
        /* İstatistik kartları - Ortalı ve Renkli */
        .stats-container {{
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 2.5rem auto;
            max-width: 700px;
            padding: 0 1.5rem;
            flex-wrap: wrap;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, {theme_colors['card_bg']}, {theme_colors['primary_blue']}20);
            border-radius: 12px;
            padding: 1rem 0.8rem;
            box-shadow: 0 6px 18px {theme_colors['shadow']};
            border: 2px solid transparent;
            text-align: center;
            min-width: 110px;
            max-width: 140px;
            flex: 1;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {theme_colors['primary_blue']}, {theme_colors['light_blue']});
        }}
        
        .stat-card:nth-child(1),
        .stat-card:nth-child(2),
        .stat-card:nth-child(3) {{
            border-color: {theme_colors['primary_blue']}30;
            background: linear-gradient(135deg, {theme_colors['card_bg']}, {theme_colors['primary_blue']}10, {theme_colors['light_blue']}20);
            box-shadow: 0 6px 18px {theme_colors['primary_blue']}20;
        }}
        .stat-card:nth-child(1):hover,
        .stat-card:nth-child(2):hover,
        .stat-card:nth-child(3):hover {{
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 10px 25px {theme_colors['primary_blue']}40, 0 0 20px {theme_colors['primary_blue']}30;
            border-color: {theme_colors['primary_blue']}80;
        }}
        .stat-card p {{
            background: linear-gradient(45deg, {theme_colors['primary_blue']}, {theme_colors['light_blue']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 6px {theme_colors['primary_blue']}30);
        }}
        
        /* Chat Header Logo Styles */
        .chat-header-logo {{
            display: flex;
            align-items: center;
            gap: 15px;
            justify-content: center;
        }}
        
        .chat-header-symbol {{
            width: 50px;
            height: 50px;
            background: linear-gradient(45deg, #00ffff, #0080ff, #8000ff);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: 0 0 20px rgba(0,255,255,0.3);
        }}
        
        .chat-header-symbol::before {{
            content: '';
            position: absolute;
            width: 40px;
            height: 40px;
            border: 2px solid rgba(0,255,255,0.3);
            border-radius: 50%;
            border-top: 2px solid #00ffff;
            animation: logoRotate 3s linear infinite;
        }}
        
        .chat-header-text {{
            font-family: 'Orbitron', monospace;
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(45deg, #00ffff, #0080ff, #8000ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1px;
        }}
        
        /* Compact logo for login/register */
        .logo-container {{
            text-align: center;
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: var(--card-bg);
            border-radius: 16px;
            box-shadow: 0 4px 12px var(--shadow);
            border: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
        }}
        
        .logo-symbol {{
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #00ffff, #0080ff, #8000ff);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: 0 0 20px rgba(0,255,255,0.3);
        }}
        
        .logo-symbol::before {{
            content: '';
            position: absolute;
            width: 70px;
            height: 70px;
            border: 2px solid rgba(0,255,255,0.3);
            border-radius: 50%;
            border-top: 2px solid #00ffff;
            animation: logoRotate 4s linear infinite;
        }}
        
        .logo-symbol::after {{
            content: '';
            position: absolute;
            width: 80px;
            height: 80px;
            border: 1px solid rgba(0,255,255,0.2);
            border-radius: 50%;
            border-right: 1px solid #00ffff;
            animation: logoRotate 6s linear infinite reverse;
        }}
        
        .logo-text {{
            display: flex;
            flex-direction: column;
            line-height: 1.1;
        }}
        
        .choyrens-text {{
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(45deg, #00ffff, #0080ff, #8000ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1px;
        }}
        
        .ai-text {{
            font-size: 1.2rem;
            font-weight: 400;
            color: var(--text-secondary);
            letter-spacing: 3px;
            margin-top: 0.2rem;
        }}
        
        /* Streamlit butonları styling */
        .stButton > button {{
            background: linear-gradient(135deg, var(--primary-blue), var(--dark-blue)) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            font-weight: 600 !important;
            padding: 0.5rem 2rem !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px var(--shadow) !important;
        }}
        
        /* Quick action butonları container */
        .quick-access-container {{
            background: var(--card-bg) !important;
            padding: 0.8rem 1rem;
            box-shadow: 0 2px 10px var(--shadow);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            margin: 1rem 0;
        }}
        
        /* Quick action butonları */
        .quick-access-container .stButton > button {{
            background: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--primary-blue) !important;
            border-radius: 12px !important;
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-align: center !important;
            min-height: 55px !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            white-space: pre-line !important;
            font-family: 'Segoe UI', system-ui, sans-serif !important;
            line-height: 1.3 !important;
            box-shadow: 0 2px 4px var(--shadow) !important;
        }}
        
        .quick-access-container .stButton > button:hover {{
            background: linear-gradient(135deg, var(--primary-blue), var(--dark-blue)) !important;
            color: white !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 4px 12px var(--shadow) !important;
            border-color: var(--primary-blue) !important;
        }}
        
        /* Input ve form elemanları */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox select {{
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
            border: 1px solid var(--border-color) !important;
        }}
        
        /* Chat input styling */
        .stChatInput input {{
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 20px !important;
            padding: 12px 16px !important;
        }}
        
        /* Chat input normal akış */
        .stChatInput {{
            position: relative !important;
            bottom: auto !important;
            left: auto !important;
            right: auto !important;
            width: auto !important;
            margin: 1rem 0 !important;
            padding: 0 !important;
        }}
        
        /* Chat input container normal akış */
        .stChatInput > div {{
            position: relative !important;
            bottom: auto !important;
            width: 100% !important;
        }}
        
        /* Streamlit main container - chat input padding kaldır */
        .main, .main > div {{
            padding-bottom: 0 !important;
        }}
        
        /* Streamlit app container - alt boşluk kaldır */
        [data-testid="stAppViewContainer"] .main .block-container {{
            padding-bottom: 1rem !important;
        }}
        
        /* Animasyonlar */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes logoRotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        <style>
        .active-dot {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%%;
            background: linear-gradient(135deg, {theme_colors['primary_blue']}, {theme_colors['light_blue']});
            margin-right: 0.4rem;
            box-shadow: 0 0 8px {theme_colors['primary_blue']}60;
            animation: activePulse 1.2s infinite alternate;
            vertical-align: middle;
        }}
        @keyframes activePulse {{
            0%% {{ opacity: 0.7; box-shadow: 0 0 8px {theme_colors['primary_blue']}60; }}
            100%% {{ opacity: 1; box-shadow: 0 0 16px {theme_colors['primary_blue']}90; }}
        }}
        </style>
    </style>
    """, unsafe_allow_html=True)

# Tema değiştirme fonksiyonu
def toggle_theme():
    """Tema arasında geçiş yapar"""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'
    st.rerun()

# Tema butonu
def theme_button():
    """Tema değiştirme butonu"""
    col1, col2, col3 = st.columns([8, 1, 1])
    
    with col3:
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        theme_text = "Karanlık" if st.session_state.theme == 'light' else "Aydınlık"
        
        if st.button(f"{theme_icon}", 
                    key="theme_toggle", 
                    help=f"{theme_text} moda geç",
                    use_container_width=True):
            toggle_theme()

# Ana sayfa - Choyrens AI logolu tasarım
def home_page():
    # Tema butonu
    theme_button()
    
    # Başlık ve logo alanı - Chat ekranındaki logo ile aynı
    st.markdown("""
    <div class="chat-header-logo" style="margin-bottom: 1.5rem;">
        <div class="chat-header-symbol">
            <div style="font-family: 'Orbitron', sans-serif; font-weight: 900; color: white; font-size: 1rem;">AI</div>
        </div>
        <div class="chat-header-text">CHOYRENS AI</div>
    </div>
    <div style="color:var(--text-secondary); font-size:1rem; text-align:center; margin-bottom:2rem;">
        Akıllı Telekom Asistanınız
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Hizmet kartları - Modern kart tasarımı
    st.markdown("""
    <div class="feature-cards-container">
        <div class="feature-card">
            <div class="feature-icon">✅</div>
            <h3 class="feature-title">7/24 Hizmet</h3>
            <p class="feature-desc">Her zaman yanınızda, istediğiniz zaman destek alın.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">Anında Yanıt</h3>
            <p class="feature-desc">Sorularınıza saniyeler içinde çözüm, beklemeye son.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔐</div>
            <h3 class="feature-title">Güvenli</h3>
            <p class="feature-desc">Verileriniz güvende, %100 gizlilikle hizmet.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Butonlar
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Hemen Başla", key="start_chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    
    with col2:
        if st.button("🔐 Giriş Yap", key="login_btn", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
    
    # Bölücü çizgi
    st.markdown('<div class="modern-divider"></div>', unsafe_allow_html=True)
    
    # İstatistik kartları
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <h4>Yanıt Süresi</h4>
            <p>&lt;1s</p>
        </div>
        <div class="stat-card">
            <h4>Başarı Oranı</h4>
            <p>%99</p>
        </div>
        <div class="stat-card">
            <h4><span class='active-dot'></span>Aktif Hizmet</h4>
            <p>24/7</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat sayfası
def chat_page():
    # Tema butonu
    theme_button()
    
    # Chat başlığı
    st.markdown("""
    <div class="chat-header-logo">
        <div class="chat-header-symbol">
            <div style="font-family: 'Orbitron', sans-serif; font-weight: 900; color: white; font-size: 1rem;">AI</div>
        </div>
        <div class="chat-header-text">CHOYRENS AI</div>
    </div>
    <div style="color:var(--text-secondary); font-size:0.9rem; text-align:center; margin-bottom:1.5rem;">
        Size nasıl yardımcı olabilirim?
    </div>
    """, unsafe_allow_html=True)
    
    # Geri butonu
    if st.button("← Ana Sayfa", key="back_home"):
        st.session_state.page = 'home'
        st.rerun()
    
    # Mesaj konteyneri
    st.markdown('<div class="chat-messages" id="chatContainer">', unsafe_allow_html=True)
    
    # Mesajları göster
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div class="message-content">{message["content"]}</div>
                    <div class="message-time">{message["time"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <div class="message-content">{message["content"]}</div>
                    <div class="message-time">{message["time"]}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        # İlk mesaj
        st.markdown("""
        <div class="bot-message">
            <div class="message-content">Merhaba! Ben Choyrens AI, size nasıl yardımcı olabilirim?</div>
            <div class="message-time">12:34</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Kısayol butonları
    st.markdown('<div class="quick-access-container">', unsafe_allow_html=True)
    cols = st.columns(4)
    quick_actions = [
        ("💰\nFatura", "Fatura bilgilerimi göster"),
        ("📱\nTarife", "Tarife seçeneklerini listele"),
        ("🛠️\nDestek", "Teknik destek konuları"),
        ("🎁\nKampanya", "Güncel kampanyalar")
    ]
    
    for col, (icon, action) in zip(cols, quick_actions):
        with col:
            if st.button(icon, key=f"quick_{action}", use_container_width=True, 
                        help=action.split(":")[0] if ":" in action else action):
                send_message(action)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mesaj giriş alanı
    if prompt := st.chat_input("Mesajınızı yazın..."):
        send_message(prompt)
        st.rerun()
    
    # Chat otomatik kaydırma
    add_navigation_script()

# Login sayfası
def login_page():
    # Tema butonu
    theme_button()
    
    st.markdown("""
    <div class="logo-container">
        <div class="logo-symbol">
            <div style="font-family: 'Orbitron', sans-serif; font-weight: 900; color: white; font-size: 1.2rem;">AI</div>
        </div>
        <div class="logo-text">
            <div class="choyrens-text">CHOYRENS</div>
            <div class="ai-text">Giriş Yapın</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Ana Sayfa", key="back_home_login"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("### 🔐 Giriş Yap")
    
    # Test form elemanları - karanlık mod uyumluluğunu test etmek için
    with st.form("login_form"):
        username = st.text_input("👤 Kullanıcı Adı", placeholder="kullanici@telekom.com")
        password = st.text_input("🔒 Şifre", type="password", placeholder="Şifrenizi girin")
        
        col1, col2 = st.columns(2)
        with col1:
            remember_me = st.checkbox("Beni Hatırla")
        with col2:
            auto_login = st.checkbox("Otomatik Giriş")
        
        # Demo text area
        message = st.text_area("📝 Ek Mesaj (Opsiyonel)", 
                              placeholder="Giriş yaparken bir mesaj bırakabilirsiniz...",
                              height=100)
        
        submitted = st.form_submit_button("🚀 Giriş Yap", use_container_width=True)
        
        if submitted:
            if username and password:
                st.success(f"✅ Hoş geldiniz, {username}!")
                st.session_state.page = 'chat'
                st.rerun()
            else:
                st.error("❌ Lütfen kullanıcı adı ve şifre girin!")
    
    st.markdown("---")
    
    # Kayıt ol seçeneği
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Hesabınız yok mu?**")
    with col2:
        if st.button("📝 Kayıt Ol", key="register_redirect", use_container_width=True):
            st.session_state.page = 'register'
            st.rerun()
    
    st.info("💡 Demo: Herhangi bir kullanıcı adı ve şifre ile giriş yapabilirsiniz.")

# Kayıt ol sayfası
def register_page():
    # Tema butonu
    theme_button()
    
    st.markdown("""
    <div class="logo-container">
        <div class="logo-symbol">
            <div style="font-family: 'Orbitron', sans-serif; font-weight: 900; color: white; font-size: 1.2rem;">AI</div>
        </div>
        <div class="logo-text">
            <div class="choyrens-text">CHOYRENS</div>
            <div class="ai-text">Kayıt Olun</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Giriş Sayfası", key="back_login"):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown("### 📝 Kayıt Ol")
    
    # Kayıt formu
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Ad", placeholder="Adınız")
            email = st.text_input("📧 E-posta", placeholder="ornek@telekom.com")
            password = st.text_input("🔒 Şifre", type="password", placeholder="Güçlü bir şifre girin")
        
        with col2:
            surname = st.text_input("👤 Soyad", placeholder="Soyadınız")
            phone = st.text_input("📱 Telefon", placeholder="05XX XXX XX XX")
            password_confirm = st.text_input("🔒 Şifre Tekrar", type="password", placeholder="Şifrenizi tekrar girin")
        
        # Ek bilgiler
        birth_date = st.date_input("🎂 Doğum Tarihi")
        gender = st.selectbox("👫 Cinsiyet", ["Seçiniz", "Erkek", "Kadın", "Diğer"])
        
        # Tercihler
        st.markdown("**📋 Tercihler:**")
        col1, col2 = st.columns(2)
        with col1:
            newsletter = st.checkbox("📰 Haber bültenine abone ol")
            sms_notifications = st.checkbox("📱 SMS bildirimleri")
        with col2:
            email_notifications = st.checkbox("📧 E-posta bildirimleri")
            promotional_offers = st.checkbox("🎁 Promosyon teklifleri")
        
        # Kullanım koşulları
        terms_accepted = st.checkbox("✅ Kullanım koşullarını ve gizlilik politikasını kabul ediyorum")
        
        # Ek notlar
        notes = st.text_area("📝 Ek Notlar (Opsiyonel)", 
                            placeholder="Özel istekleriniz veya notlarınız...",
                            height=80)
        
        submitted = st.form_submit_button("🎉 Kayıt Ol", use_container_width=True)
        
        if submitted:
            if not all([name, surname, email, phone, password, password_confirm]):
                st.error("❌ Lütfen tüm zorunlu alanları doldurun!")
            elif password != password_confirm:
                st.error("❌ Şifreler eşleşmiyor!")
            elif not terms_accepted:
                st.error("❌ Kullanım koşullarını kabul etmelisiniz!")
            elif len(password) < 6:
                st.error("❌ Şifre en az 6 karakter olmalıdır!")
            else:
                st.success(f"🎉 Kayıt başarılı! Hoş geldiniz {name} {surname}!")
                st.balloons()
                st.session_state.page = 'chat'
                st.rerun()
    
    st.markdown("---")
    
    # Giriş yap seçeneği
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Zaten hesabınız var mı?**")
    with col2:
        if st.button("🔐 Giriş Yap", key="login_redirect", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
    
    st.info("💡 Demo: Form doldurarak kayıt olabilir ve doğrudan uygulamaya erişebilirsiniz.")

# Mesaj gönderme fonksiyonu - Optimize edilmiş Python
def send_message(message):
    """Kullanıcı mesajını gönderir ve bot yanıtını alır"""
    if message:
        current_time = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "content": message, "time": current_time})
        
        # Bot yanıtını hesapla
        with st.spinner("Choyrens AI yazıyor..."):
            time.sleep(0.3)
            bot_response = generate_bot_response(message)
            current_time = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({"role": "bot", "content": bot_response, "time": current_time})

# Bot yanıt üretme fonksiyonu - Saf Python
def generate_bot_response(message):
    """Kullanıcı mesajına göre bot yanıtı üretir"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["fatura", "ödeme", "borç", "para"]):
        return "💳 **Fatura bilgileriniz:**\n\n- Son ödeme: 25 Ağustos 2025\n- Tutar: 159.99 TL\n- Kalan data: 4.8 GB / 20 GB\n- Durum: ✅ Ödenmiş"
    elif any(word in message_lower for word in ["tarife", "paket", "plan", "gb"]):
        return "📱 **Mevcut tarifeniz:** Premium 5G\n\n**Yeni tarifeler:**\n- Standart: 129 TL (100 GB)\n- Ekstra: 169 TL (150 GB)\n- Premium: 229 TL (Sınırsız)"
    elif any(word in message_lower for word in ["destek", "sorun", "problem", "yardım"]):
        return "🛠️ **Teknik destek:**\n\n- 📞 Telefon: 444 0 123\n- 💬 Canlı chat: 7/24 aktif\n- 📧 E-posta: destek@telekom.com\n- 🎫 Ticket oluşturma sistemi"
    elif any(word in message_lower for word in ["kampanya", "indirim", "promosyon", "teklif"]):
        return "🎁 **Özel kampanyalar:**\n\n- Yeni abonelere %30 indirim\n- 1 yıllık taahhütte 2 ay bedava\n- Arkadaş getir kampanyası\n- Premium telefonlarda vade farksız"
    elif any(word in message_lower for word in ["merhaba", "selam", "hey", "iyi"]):
        return "Merhaba! Ben Choyrens AI, size nasıl yardımcı olabilirim? Fatura, tarife, teknik destek veya kampanyalar hakkında soru sorabilirsiniz."
    else:
        return random.choice([
            "Anladım, size nasıl yardımcı olabilirim?",
            "Bu konuda daha fazla bilgi verebilir misiniz?",
            "Size bu konuda yardımcı olabilirim. Lütfen daha detay verin."
        ])

# JavaScript fonksiyonları
def add_navigation_script():
    html("""
    <script>
    function navigateTo(page) {
        console.log('Navigate to:', page);
    }
    
    function quickAction(action) {
        console.log('Quick action:', action);
        // Not needed anymore - using Streamlit buttons with direct send_message() calls
    }
    
    function sendMessage() {
        const input = document.getElementById('userInput');
        if (input && input.value.trim() !== '') {
            window.streamlitApi?.runMethod('send_message', input.value);
            input.value = '';
        }
    }
    
    function scrollChat() {
        const container = document.getElementById('chatContainer');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }
    
    setTimeout(scrollChat, 100);
    </script>
    """)

# Ana uygulama
def main():
    set_theme()
    add_navigation_script()
    
    # Session state başlatma
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "bot", "content": "Merhaba! Ben Choyrens AI, size nasıl yardımcı olabilirim?", "time": datetime.now().strftime("%H:%M")}
        ]
    
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    # Sayfa yönlendirme
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'chat':
        chat_page()
    elif st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'register':
        register_page()

if __name__ == "__main__":
    main() 