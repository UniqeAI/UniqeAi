import streamlit as st
from streamlit.components.v1 import html
import time
import random
from datetime import datetime
import sys
import os
from streamlit_cookies_manager import EncryptedCookieManager  # <-- EKLENDİ

# Utils klasörünü path'e ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# API client'ı import et
try:
    from utils.api_client import get_api_client
    API_CLIENT_AVAILABLE = True
except ImportError:
    API_CLIENT_AVAILABLE = False
    print("API client bulunamadı, mock modunda çalışıyor")

# Çerez yöneticisi
cookies = EncryptedCookieManager(
    prefix="choyrens_",
    password="gizli-bir-anahtar"
)
if not cookies.ready():
    st.stop()

# Oturum kontrolü: Çerezde varsa session_state'e aktar
if cookies.get("is_logged_in") == "1":
    if not st.session_state.get("is_logged_in"):
        st.session_state.is_logged_in = True
        st.session_state.user_info = {
            "email": cookies.get("user_email"),
            "full_name": cookies.get("user_full_name"),
            "user_id": cookies.get("user_id"),
            "phone": cookies.get("user_phone"),
            "username": cookies.get("user_username"),
        }
        # Eğer email var ama diğer bilgiler eksikse backend'den çek
        if st.session_state.user_info["email"] and not st.session_state.user_info["full_name"]:
            api_client = get_api_client()
            user_info_response = api_client.get_current_user()
            if user_info_response.get("success") and user_info_response.get("data"):
                user_data = user_info_response["data"]
                st.session_state.user_info = user_data
                cookies["user_full_name"] = user_data.get("full_name", "")
                cookies["user_id"] = user_data.get("user_id", "")
                cookies["user_phone"] = user_data.get("phone", "")
                cookies["user_username"] = user_data.get("username", "")
else:
    st.session_state.is_logged_in = False
    st.session_state.user_info = None

# Giriş başarılı olduğunda:
def on_login_success(user_info):
    st.session_state.is_logged_in = True
    st.session_state.user_info = user_info
    cookies["is_logged_in"] = "1"
    cookies["user_email"] = user_info.get("email", "")
    cookies["user_full_name"] = user_info.get("full_name", "")
    cookies["user_id"] = user_info.get("user_id", "")
    cookies["user_phone"] = user_info.get("phone", "")
    cookies["user_username"] = user_info.get("username", "")

# Çıkış fonksiyonu:
def logout():
    st.session_state.is_logged_in = False
    st.session_state.user_info = None
    cookies["is_logged_in"] = "0"
    cookies["user_email"] = ""
    cookies["user_full_name"] = ""
    cookies["user_id"] = ""
    cookies["user_phone"] = ""
    cookies["user_username"] = ""
    st.rerun()

# Tema ayarları
def set_theme():
    import platform
    import os
    st.set_page_config(
        page_title="CHOYRENS AI",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    # Otomatik tema algılama (sistem karanlık/aydınlık)
    if 'theme' not in st.session_state:
        # Streamlit 1.25+ ile birlikte, tarayıcıdan tema algılamak mümkün
        # Ancak Python tarafında doğrudan algılamak mümkün değil, bu yüzden varsayılanı sistemin varsayılanına göre ayarlıyoruz
        # Windows/macOS/Linux için farklı yaklaşımlar gerekebilir
        # Burada sadece varsayılanı 'light' olarak bırakıyoruz, isterseniz 'dark' yapabilirsiniz
        st.session_state.theme = 'light'
        try:
            # Sadece macOS ve bazı Linux sistemlerinde çalışır
            if platform.system() == 'Darwin':
                import subprocess
                result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], capture_output=True, text=True)
                if 'Dark' in result.stdout:
                    st.session_state.theme = 'dark'
            elif platform.system() == 'Windows':
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                if value == 0:
                    st.session_state.theme = 'dark'
        except Exception:
            pass
    if st.session_state.theme == 'dark':
        theme_colors = {
            'primary_blue': '#3b82f6',
            'dark_blue': '#1e3a8a',
            'light_blue': '#e0f2fe',
            'bg_color': '#0f172a',
            'card_bg': '#1e293b',
            'text_color': '#f8fafc',
            'text_secondary': '#cbd5e1',
            'border_color': 'rgba(59, 130, 246, 0.15)',
            'shadow': 'rgba(59, 130, 246, 0.10)'
        }
    else:
        theme_colors = {
            'primary_blue': '#2563eb',
            'dark_blue': '#1e40af',
            'light_blue': '#e0f2fe',
            'bg_color': '#f8fafc',
            'card_bg': '#ffffff',
            'text_color': '#1e293b',
            'text_secondary': '#64748b',
            'border_color': 'rgba(37, 99, 235, 0.10)',
            'shadow': 'rgba(37, 99, 235, 0.08)'
        }
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
        html, body, #root, .stApp {{
            background-color: var(--bg-color) !important;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 100vh !important;
        }}
        .main .block-container {{
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }}
        .animated-card {{
            background: linear-gradient(145deg, {theme_colors['primary_blue']}15, {theme_colors['light_blue']}25);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid {theme_colors['border_color']};
            box-shadow: 0 8px 32px {theme_colors['shadow']};
            transition: all 0.4s ease;
            animation: cardEntrance 0.6s ease-out;
            position: relative;
            overflow: hidden;
        }}
        .animated-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px {theme_colors['primary_blue']}30;
        }}
        .animated-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #00ffff, #0080ff, #8000ff);
        }}
        .chat-container {{
            display: flex;
            flex-direction: column;
            height: 100vh;
            width: 100%;
        }}
        .chat-header {{
            flex: 0 0 auto;
            padding: 1rem;
            background: linear-gradient(135deg, {theme_colors['primary_blue']}, {theme_colors['dark_blue']});
            color: white;
            box-shadow: 0 4px 12px {theme_colors['shadow']};
            z-index: 10;
        }}
        .messages-area {{
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            background: linear-gradient(180deg, {theme_colors['bg_color']}, {theme_colors['card_bg']}20);
            max-height: 66.67vh;
            min-height: 200px;
        }}
        .input-area {{
            flex: 0 0 auto;
            padding: 1rem;
            background: {theme_colors['card_bg']};
            border-top: 1px solid {theme_colors['border_color']};
            box-shadow: 0 -4px 12px {theme_colors['shadow']}20;
        }}
        .user-message {{
            background: linear-gradient(135deg, {theme_colors['primary_blue']}, {theme_colors['dark_blue']});
            color: white;
            padding: 14px 18px;
            border-radius: 22px 22px 0 22px;
            max-width: 85%;
            margin-left: auto;
            margin-bottom: 16px;
            box-shadow: 0 4px 16px {theme_colors['shadow']};
            animation: fadeInUp 0.4s ease;
            position: relative;
        }}
        .user-message::after {{
            content: '';
            position: absolute;
            right: -8px;
            bottom: 0;
            width: 20px;
            height: 20px;
            background: linear-gradient(135deg, {theme_colors['primary_blue']}, {theme_colors['dark_blue']});
            clip-path: polygon(0 0, 100% 100%, 100% 0);
        }}
        .bot-message {{
            background: linear-gradient(135deg, {theme_colors['card_bg']}, {theme_colors['light_blue']}20);
            color: {theme_colors['text_color']};
            padding: 14px 18px;
            border-radius: 22px 22px 22px 0;
            max-width: 85%;
            margin-right: auto;
            margin-bottom: 16px;
            box-shadow: 0 4px 16px {theme_colors['shadow']}20;
            border: 1px solid {theme_colors['border_color']};
            animation: fadeInUp 0.4s ease 0.1s both;
            position: relative;
        }}
        .bot-message::after {{
            content: '';
            position: absolute;
            left: -8px;
            bottom: 0;
            width: 20px;
            height: 20px;
            background: linear-gradient(135deg, {theme_colors['card_bg']}, {theme_colors['light_blue']}20);
            clip-path: polygon(0 0, 0 100%, 100% 0);
            border-left: 1px solid {theme_colors['border_color']};
            border-bottom: 1px solid {theme_colors['border_color']};
        }}
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes cardEntrance {{
            from {{ opacity: 0; transform: scale(0.95) translateY(20px); }}
            to {{ opacity: 1; transform: scale(1) translateY(0); }}
        }}
        @keyframes gradientFlow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .logo-header {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            padding: 1rem;
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
            box-shadow: 0 0 25px rgba(0,255,255,0.4);
            animation: logoRotate 6s linear infinite;
        }}
        .logo-text {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(45deg, #00ffff, #0080ff, #8000ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1.5px;
            text-shadow: 0 0 10px rgba(0,128,255,0.3);
        }}
        .quick-action-btn {{
            background: linear-gradient(135deg, {theme_colors['primary_blue']}15, {theme_colors['light_blue']}30) !important;
            border: 1px solid {theme_colors['border_color']} !important;
            color: {theme_colors['primary_blue']} !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            margin: 0.25rem !important;
        }}
        .quick-action-btn:hover {{
            background: linear-gradient(135deg, {theme_colors['primary_blue']}, {theme_colors['dark_blue']}) !important;
            color: white !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 6px 20px {theme_colors['primary_blue']}40 !important;
        }}
        .card {{
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 14px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
            text-align: center;
            transition: transform 0.2s ease;
            border-top: 3px solid #00cfff;
            max-width: 220px;
            margin-left: auto;
            margin-right: auto;
        }}
        .card:hover {{
            transform: scale(1.03);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.09);
        }}
        .emoji {{
            font-size: 22px;
            margin-bottom: 7px;
        }}
        .title {{
            font-weight: 700;
            font-size: 15px;
            color: {theme_colors['text_color']};
        }}
        .desc {{
            color: {theme_colors['text_secondary']};
            font-size: 12px;
            margin-top: 3px;
        }}
        .stats-row {{
            display: flex;
            justify-content: center;
            gap: 54px; /* Mesafe daha da artırıldı */
            margin-top: 2.2rem;
            margin-bottom: 0.5rem;
        }}
        .stat-card {{
            background: var(--card-bg);
            border-radius: 10px;
            box-shadow: 0 2px 8px var(--shadow);
            padding: 7px 12px; /* Daha küçük padding */
            min-width: 60px;
            max-width: 80px;
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 11px; /* Daha küçük font */
            color: {theme_colors['text_color']};
            border: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
        }}
        .stat-card.stat-blue {{ border-top: 3px solid #00cfff; }}
        .stat-card.stat-purple {{ border-top: 3px solid #a233ff; }}
        .stat-card.stat-orange {{ border-top: 3px solid #ffaa00; }}
        .stat-value {{
            font-weight: 700;
            font-size: 0.95rem; /* Daha küçük */
            color: {theme_colors['primary_blue']};
            margin-bottom: 2px;
        }}
        .stat-label {{
            font-size: 0.75rem; /* Daha küçük */
            color: {theme_colors['text_secondary']};
        }}
        @media (max-width: 700px) {{
            .stats-row {{ flex-direction: column; gap: 14px; align-items: center; }}
            .stat-card {{ min-width: 0; max-width: 98vw; }}
        }}
        .primary-logo {{
            margin-bottom: 0.15rem !important; /* Minimum boşluk */
            margin-top: 1.0rem !important;
            max-width: 420px;
            margin-left: auto;
            margin-right: auto;
        }}
        .chat-header, .chat-header-logo {{
            margin-bottom: 0.08rem !important; /* Minimum boşluk */
            padding-bottom: 0 !important;
        }}
        .messages-area, .messages-container {{
            padding-top: 0 !important;
            margin-top: 0 !important;
            justify-content: flex-start !important;
            align-items: flex-start !important;
        }}
        .custom-btn-row {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 18px;
            margin-top: 1.2rem;
            margin-bottom: 0.2rem;
            width: 100%;
        }}
        .custom-btn {{
            background: #e5e7eb;
            color: #1e293b !important;
            border: none;
            border-radius: 8px;
            font-size: 0.98rem;
            font-weight: 600;
            padding: 0.42rem 1.05rem;
            min-width: 110px;
            min-height: 32px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
            transition: background 0.18s, transform 0.18s;
            cursor: pointer;
            margin: 0 2px;
        }}
        .custom-btn:hover {{
            background: #cbd5e1;
            color: #1e293b !important;
            transform: scale(1.03);
        }}
        .custom-btn.login-btn {{
            background: #e5e7eb;
            color: #1e293b !important;
        }}
        .custom-btn:hover {{
            background: #1e40af;
            color: #fff !important;
            transform: scale(1.03);
        }}
        .custom-btn.login-btn:hover {{
            background: #cbd5e1;
            color: #1e293b !important;
        }}
        .stButton>button.custom-btn {{ width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# Tema değiştirme butonu
def theme_button():
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, key="theme_toggle", help="Karanlık/Aydınlık Mod", use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# Navigasyon script'i ekleme
def add_navigation_script():
    st.markdown("""
    <script>
    // Sayfa yüklendiğinde çalışacak script
    window.addEventListener('load', function() {
        // Smooth scrolling için
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)

# CHOYRENS logo showcase
def choyrens_logo_showcase():
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 15px; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: white; margin-bottom: 0.25rem;">CHOYRENS AI</div>
            <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.9);">Yapay Zeka Asistanınız</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_choyrens_header():
    st.markdown('''
    <style>
        .choyrens-header {
            width: 100vw;
            max-width: 100vw;
            background: var(--card-bg, #fff);
            color: var(--text-color, #222);
            border-bottom: 1px solid var(--border-color, #eee);
            box-shadow: 0 2px 12px rgba(0,0,0,0.03);
            z-index: 1000;
            position: fixed;
            top: 0;
            left: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 18px 32px 10px 32px;
        }
        .choyrens-header-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .ai-core {
            width: 38px;
            height: 38px;
            background: linear-gradient(45deg, #00ffff 0%, #0080ff 25%, #8000ff 50%, #ff00ff 75%, #00ffff 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 32px rgba(0, 255, 255, 0.8), 0 0 60px rgba(128, 0, 255, 0.6), inset 0 2px 16px rgba(255, 255, 255, 0.3);
        }
        .core-text {
            font-family: 'Orbitron', monospace;
            font-size: 18px;
            font-weight: 900;
            color: #fff;
            text-shadow: 0 0 18px rgba(255,255,255,1), 0 0 32px rgba(0,255,255,0.8), 0 0 40px rgba(128,0,255,0.6);
        }
        .choyrens-header-title {
            font-family: 'Orbitron', monospace;
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: 2px;
            background: linear-gradient(45deg, #00ffff 0%, #0080ff 25%, #8000ff 50%, #ff00ff 75%, #00ffff 100%);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-left: 8px;
        }
        
        /* Sidebar toggle butonunu gizle */
        .st-emotion-cache-pd6qx2,
        .st-emotion-cache-189uypx {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
        
        /* Streamlit header ve toolbar'ını gizle */
        .stAppHeader,
        .st-emotion-cache-gkoddq,
        .stAppToolbar,
        .st-emotion-cache-14vh5up,
        .st-emotion-cache-1j22a0y,
        .st-emotion-cache-70qvj9,
        .st-emotion-cache-8ezv7j,
        .st-emotion-cache-scp8yw,
        .stToolbarActions,
        .st-emotion-cache-1p1m4ay,
        .stAppDeployButton,
        .stMainMenu,
        .st-emotion-cache-czk5ss {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
        
        /* Özel sidebar toggle butonu */
        .custom-sidebar-toggle {
            position: fixed !important;
            top: 90px !important;
            left: 10px !important;
            z-index: 999 !important;
            background: var(--card-bg, #fff) !important;
            border: 1px solid var(--border-color, #eee) !important;
            border-radius: 8px !important;
            padding: 8px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 40px !important;
            height: 40px !important;
        }
        .custom-sidebar-toggle:hover {
            background: var(--light-blue, #e0f2fe) !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }
        .custom-sidebar-toggle svg {
            width: 20px !important;
            height: 20px !important;
            color: var(--text-color, #222) !important;
        }
        
        /* Sidebar'ı her zaman görünür yap */
        .stSidebar {
            display: block !important;
        }
        
        @media (max-width: 768px) {
            .choyrens-header {
                flex-direction: column;
                gap: 8px;
                padding: 12px 4vw 8px 4vw;
            }
            .choyrens-header-title {
                font-size: 1.3rem;
                margin-left: 0;
            }
            .custom-sidebar-toggle {
                top: 70px !important;
                left: 5px !important;
                width: 35px !important;
                height: 35px !important;
            }
        }
        .choyrens-content {
            padding-top: 90px;
        }
        @media (max-width: 768px) {
            .choyrens-content { padding-top: 70px; }
        }
    </style>
    <div class="choyrens-header">
        <div class="choyrens-header-logo">
            <div class="ai-core"><span class="core-text">AI</span></div>
            <div class="choyrens-header-title">CHOYRENS AI</div>
        </div>
    </div>
    
    <div class="choyrens-content">
    ''', unsafe_allow_html=True)
    
    # JavaScript ile sidebar toggle fonksiyonu
    st.markdown('''
    <script>
    function toggleSidebar() {
        const sidebar = document.querySelector('.stSidebar');
        const button = document.querySelector('.custom-sidebar-toggle svg');
        
        if (sidebar) {
            const isVisible = sidebar.style.display !== 'none';
            
            if (isVisible) {
                // Sidebar'ı gizle
                sidebar.style.display = 'none';
                button.innerHTML = '<path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>';
            } else {
                // Sidebar'ı göster
                sidebar.style.display = 'block';
                button.innerHTML = '<path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>';
            }
        }
    }
    
    // Sayfa yüklendiğinde sidebar'ı göster
    document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.querySelector('.stSidebar');
        if (sidebar) {
            sidebar.style.display = 'block';
        }
    });
    </script>
    ''', unsafe_allow_html=True)

# Ana sayfa
def home_page():
    render_choyrens_header()
    
    # Ana başlık
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--primary-blue); font-size: 2.5rem; margin-bottom: 0.5rem;">🤖 CHOYRENS AI</h1>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">Telekom destek hizmetleriniz için yapay zeka asistanınız</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Giriş durumuna göre farklı içerik göster
    if st.session_state.is_logged_in and st.session_state.user_info:
        user_info = st.session_state.user_info
        st.markdown(f"""
        <div style="background: var(--card-bg); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; border: 1px solid var(--border-color); text-align: center;">
            <h2 style="color: var(--primary-blue); margin-bottom: 1rem;">🎉 Hoş Geldiniz!</h2>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 1.1rem;">
                <strong>{user_info.get('full_name', 'Kullanıcı')}</strong> olarak giriş yaptınız.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat butonu
        if st.button("💬 Chat'e Git", key="go_to_chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    else:
        # Giriş yapılmamışsa ana içerik
        st.markdown("""
        <div style="background: var(--card-bg); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; border: 1px solid var(--border-color); text-align: center;">
            <h2 style="color: var(--primary-blue); margin-bottom: 1rem;">🚀 Hemen Başlayın</h2>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 1.1rem;">
                Telekom destek hizmetleriniz için AI asistanınızı kullanmaya başlayın.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Giriş ve kayıt butonları
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Giriş Yap", key="login_from_home", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
        with col2:
            if st.button("📝 Kayıt Ol", key="register_from_home", use_container_width=True):
                st.session_state.page = 'register'
                st.rerun()
    
    # Özellik kartları
    st.markdown("### ✨ Özellikler")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid var(--border-color); height: 200px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🚀</div>
                <h3 style="color: var(--primary-blue); margin-bottom: 0.5rem;">Anında Destek</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">7/24 kesintisiz hizmet ile her an yanınızdayız</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid var(--border-color); height: 200px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">💎</div>
                <h3 style="color: var(--primary-blue); margin-bottom: 0.5rem;">Premium Hizmet</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">Özel çözümlerle ihtiyaçlarınıza özel hizmet</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid var(--border-color); height: 200px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔒</div>
                <h3 style="color: var(--primary-blue); margin-bottom: 0.5rem;">Güvenli İletişim</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">Bankalar seviyesinde şifreleme ile güvendesiniz</p>
            </div>
        """, unsafe_allow_html=True)
    
    # İstatistikler
    st.markdown("### 📊 Performans İstatistikleri")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid var(--border-color);">
                <div style="font-size: 2rem; color: var(--primary-blue); font-weight: bold; margin-bottom: 0.5rem;"><1sn</div>
                <div style="color: var(--text-secondary); font-size: 0.9rem;">Yanıt Süresi</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid var(--border-color);">
                <div style="font-size: 2rem; color: var(--primary-blue); font-weight: bold; margin-bottom: 0.5rem;">%99</div>
                <div style="color: var(--text-secondary); font-size: 0.9rem;">Başarı Oranı</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid var(--border-color);">
                <div style="font-size: 2rem; color: var(--primary-blue); font-weight: bold; margin-bottom: 0.5rem;">7/24</div>
                <div style="color: var(--text-secondary); font-size: 0.9rem;">Kesintisiz Hizmet</div>
            </div>
        """, unsafe_allow_html=True)

# Chat sayfası
def chat_page():
    """Chat sayfasını göster"""
    render_choyrens_header()
    
    # API client'ı al
    if API_CLIENT_AVAILABLE:
        api_client = get_api_client()
    else:
        api_client = None
    
    # Kullanıcı bilgilerini göster
    if "user_info" in st.session_state and st.session_state.user_info:
        user_info = st.session_state.user_info
        
        # Çıkış butonu ile birlikte kullanıcı bilgileri
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: var(--card-bg); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid var(--border-color);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>👤 {user_info.get('full_name', 'Kullanıcı')}</strong>
                        <br>
                        <small style="color: var(--text-secondary);">@{user_info.get('username', 'user')}</small>
                    </div>
                    <div style="text-align: right;">
                        <small style="color: var(--text-secondary);">📧 {user_info.get('email', 'email@example.com')}</small>
                        <br>
                        <small style="color: var(--text-secondary);">📱 {user_info.get('phone', 'N/A')}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Çıkış Yap", key="logout_button", use_container_width=True):
                logout()
    
    # Session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = 1  # Demo için varsayılan
    
    # Ana içerik - Chat alanı (tam genişlik)
    st.header("💬 Sohbet")
    
    # Mesaj geçmişini göster
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div class="bot-message">
                <div class="message-content">
                    <div style="font-size: 1.1rem; margin-bottom: 8px;"><strong>Merhaba!</strong></div>
                    <div>Ben Telekom AI, size nasıl yardımcı olabilirim?</div>
                    <div style="margin-top: 10px; font-size: 0.85rem; color: var(--text-secondary);">
                        Aşağıdan mesaj yazabilirsiniz.
                    </div>
                </div>
                <div class="message-time">{}</div>
            </div>
            """.format(datetime.now().strftime("%H:%M")), unsafe_allow_html=True)
        else:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <div class="message-content">{message["content"]}</div>
                        <div class="message-time">{message.get("time", datetime.fromtimestamp(message.get("timestamp", time.time())).strftime("%H:%M"))}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="bot-message">
                        <div class="message-content">{message["content"]}</div>
                        <div class="message-time">{message.get("time", datetime.fromtimestamp(message.get("timestamp", time.time())).strftime("%H:%M"))}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Araç çağrılarını detay olarak göster
                    if message.get("tool_calls"):
                        with st.expander("🔧 Kullanılan Araçlar"):
                            for tool in message["tool_calls"]:
                                st.code(f"Araç: {tool.get('arac_adi', 'N/A')}")
                                st.json(tool.get("parametreler", {}))
    
    # Yeni mesaj input'u
    st.header("✍️ Yeni Mesaj")
    
    # Form ile Enter tuşu kontrolü
    with st.form(key="message_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Mesajınızı yazın:",
                placeholder="Örn: Backend nerede? (Enter ile gönder)",
                key="user_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Butonu aşağı kaydır
            send_button = st.form_submit_button("📤 Gönder", use_container_width=True)
    
    # Mesaj gönderme
    if send_button and user_input:
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": time.time()
        })
        
        # AI yanıtını al
        with st.spinner("AI düşünüyor..."):
            if api_client:
                response = api_client.send_chat_message(
                    message=user_input,
                    user_id=st.session_state.user_id
                )
                
                if response.get("success"):
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["response"],
                        "confidence": response.get("confidence", 0.0),
                        "tool_calls": response.get("tool_calls", []),
                        "timestamp": time.time()
                    })
                else:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"❌ Hata: {response.get('error', 'Bilinmeyen hata')}",
                        "timestamp": time.time()
                    })
            else:
                # Mock yanıt
                mock_response = generate_bot_response(user_input)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": mock_response,
                    "timestamp": time.time()
                })
        
        st.rerun()

# Login sayfası
def login_page():
    render_choyrens_header()
    st.title("🔐 Giriş Yap")
    
    # API client'ı al
    if API_CLIENT_AVAILABLE:
        api_client = get_api_client()
    else:
        st.error("❌ API bağlantısı kurulamadı!")
        return
    
    with st.form("login_form", clear_on_submit=True):
        email = st.text_input("📧 E-posta", placeholder="E-posta adresinizi girin")
        password = st.text_input("🔒 Şifre", type="password", placeholder="Şifrenizi girin")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            login_button = st.form_submit_button("🚀 Giriş Yap", use_container_width=True)
        with col2:
            back_button = st.form_submit_button("🏠 Ana Sayfa", use_container_width=True)
    
    if login_button and email and password:
        with st.spinner("Giriş yapılıyor..."):
            try:
                response = api_client.login_user(email, password)
                
                if response.get("success"):
                    user_data = response.get("data", {})
                    username = user_data.get("username", "Kullanıcı")
                    st.success(f"🎉 Hoş geldiniz, {username}!")
                    on_login_success(user_data)
                    st.session_state.page = 'chat'
                    st.rerun()
                else:
                    error_msg = response.get("error", "Giriş başarısız")
                    st.error(f"❌ {error_msg}")
                    
            except Exception as e:
                st.error(f"❌ Giriş sırasında hata oluştu: {str(e)}")
    
    elif login_button and (not email or not password):
        st.warning("⚠️ Lütfen e-posta adresi ve şifre girin!")
    
    if back_button:
        st.session_state.page = 'home'
        st.rerun()
    
    # Kayıt ol butonu
    st.markdown("<div style='margin-top:2rem; text-align:center;'>Hesabınız yok mu?</div>", unsafe_allow_html=True)
    if st.button("📝 Kayıt Ol", key="register_from_login", use_container_width=True):
        st.session_state.page = 'register'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Kayıt ol sayfası
def register_page():
    render_choyrens_header()
    
    # API client'ı al
    if API_CLIENT_AVAILABLE:
        api_client = get_api_client()
    else:
        st.error("❌ API bağlantısı kurulamadı!")
        return
    
    if st.button("← Giriş Sayfası", key="back_login"):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown("### 📝 Kayıt Ol")
    
    with st.form("register_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Ad", placeholder="Adınız")
            email = st.text_input("📧 E-posta", placeholder="ornek@choyrens.com")
            password = st.text_input("🔒 Şifre", type="password", placeholder="Güçlü bir şifre girin")
        with col2:
            surname = st.text_input("👤 Soyad", placeholder="Soyadınız")
            phone = st.text_input("📱 Telefon", placeholder="05XX XXX XX XX")
            password_confirm = st.text_input("🔒 Şifre Tekrar", type="password", placeholder="Şifrenizi tekrar girin")
        
        birth_date = st.date_input("🎂 Doğum Tarihi")
        gender = st.selectbox("👫 Cinsiyet", ["Seçiniz", "Erkek", "Kadın"])
        
        terms_accepted = st.checkbox("✅ Kullanım koşullarını ve gizlilik politikasını kabul ediyorum")
        notes = st.text_area("📝 Ek Notlar (Opsiyonel)", 
                           placeholder="Özel istekleriniz veya notlarınız...",
                           height=80)
        
        submitted = st.form_submit_button("🎉 Kayıt Ol", use_container_width=True)
        
        if submitted:
            # Validasyon
            if not all([name, surname, email, phone, password, password_confirm]):
                st.error("❌ Lütfen tüm zorunlu alanları doldurun!")
            elif password != password_confirm:
                st.error("❌ Şifreler eşleşmiyor!")
            elif not terms_accepted:
                st.error("❌ Kullanım koşullarını kabul etmelisiniz!")
            elif len(password) < 6:
                st.error("❌ Şifre en az 6 karakter olmalıdır!")
            else:
                # Kullanıcı adını ad ve soyaddan oluştur
                username = f"{name} {surname}"
                
                # Kayıt verilerini hazırla
                user_data = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "full_name": f"{name} {surname}",
                    "phone": phone,
                    "birth_date": birth_date.strftime("%Y-%m-%d") if birth_date else None,
                    "gender": gender if gender != "Seçiniz" else None,
                    "preferences": {
                        "notes": notes
                    }
                }
                
                with st.spinner("Kayıt yapılıyor..."):
                    try:
                        response = api_client.register_user(user_data)
                        
                        if response.get("success"):
                            st.success(f"🎉 Kayıt başarılı! Hoş geldiniz {name} {surname}!")
                            st.balloons()
                            
                            on_login_success(response.get("data", {}))
                            
                            st.session_state.page = 'chat'
                            st.rerun()
                        else:
                            error_msg = response.get("error", "Kayıt başarısız")
                            st.error(f"❌ {error_msg}")
                            
                    except Exception as e:
                        st.error(f"❌ Kayıt sırasında hata oluştu: {str(e)}")
    
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Zaten hesabınız var mı?**")
    with col2:
        if st.button("🔐 Giriş Yap", key="login_redirect", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
    
    st.info("💡 Demo: Form doldurarak kayıt olabilir ve doğrudan uygulamaya erişebilirsiniz.")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    set_theme()
    
    # Session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = 1  # Demo için varsayılan
    
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    
    if "page" not in st.session_state:
        st.session_state.page = 'home'
    
    # Otomatik giriş kontrolü - eğer kullanıcı giriş yapmışsa chat sayfasına yönlendir
    if st.session_state.is_logged_in and st.session_state.user_info and st.session_state.page in ['home', 'login', 'register']:
        st.session_state.page = 'chat'
    
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