import streamlit as st
from components.login_screen import render_login_screen
from components.signup_screen import render_signup_screen
from components.chat_screen import render_chat_screen
from components.main_screen import render_main_screen
from datetime import datetime
import random

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="UniqeAi Chat Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Demo verileri
DEMO_USERS = {
    "admin": {"password": "123", "name": "Admin User"},
    "demo": {"password": "demo123", "name": "Demo User"},
    "test": {"password": "test123", "name": "Test User"}
}

DEMO_RESPONSES = [
    "Merhaba! Size nasıl yardımcı olabilirim?",
    "Bu konuda size detaylı bilgi verebilirim.",
    "Anlıyorum, bu durumu çözmek için birkaç seçeneğiniz var.",
    "Teknik destek ekibimiz size yardımcı olacaktır.",
    "Bu işlem için gerekli adımları takip edebilirsiniz.",
    "Sistemimizde bu bilgiyi buldum, size aktarıyorum.",
    "Bu konuda uzman ekibimizle görüşebilirsiniz.",
    "İşleminiz başarıyla tamamlandı.",
    "Başka bir konuda yardıma ihtiyacınız var mı?",
    "Size en iyi hizmeti sunmaya devam edeceğiz."
]

# CSS stilleri
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {
    background: linear-gradient(135deg, #e8f4fd 0%, #f8f9fa 100%);
    min-height: 100vh;
}
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
.stButton > button {
    border-radius: 15px;
    font-weight: bold;
    transition: all 0.3s ease;
    font-family: 'Poppins', sans-serif;
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(220,53,69,0.4);
}
.stTextInput > div > div > input {
    border-radius: 15px;
    border: 2px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.95);
    color: #000000;
    transition: all 0.3s ease;
    font-family: 'Poppins', sans-serif;
    padding: 12px 20px;
}
.stTextInput > div > div > input:focus {
    border-color: #dc3545;
    box-shadow: 0 0 25px rgba(220,53,69,0.4);
    color: #000000;
    background: rgba(255,255,255,1);
}
.stTextInput > div > div > input::placeholder {
    color: rgba(0,0,0,0.6);
    font-family: 'Poppins', sans-serif;
}
.stAlert {
    border-radius: 15px;
    border: none;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}
.stInfo {
    background: rgba(13,110,253,0.1);
    border-left: 4px solid #0d6efd;
    color: #000000;
}
.stSuccess {
    background: rgba(25,135,84,0.1);
    border-left: 4px solid #198754;
    color: #000000;
}
.stError {
    background: rgba(220,53,69,0.1);
    border-left: 4px solid #dc3545;
    color: #000000;
}
.stWarning {
    background: rgba(255,193,7,0.1);
    border-left: 4px solid #ffc107;
    color: #000000;
}
/* Loading animasyonu */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,.3);
    border-radius: 50%;
    border-top-color: #dc3545;
    animation: spin 1s ease-in-out infinite;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
/* Responsive tasarım */
@media (max-width: 768px) {
    .main .block-container {
        padding: 0.5rem;
    }
}
/* Koyu tema seçeneği */
.dark-theme {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
}
.dark-theme .stTextInput > div > div > input {
    background: rgba(255,255,255,0.1);
    color: #ffffff;
    border-color: rgba(255,255,255,0.2);
}
.dark-theme .stTextInput > div > div > input::placeholder {
    color: rgba(255,255,255,0.7);
}
/* Demo banner - Telekom renkleri */
.demo-banner {
    background: linear-gradient(135deg, #dc3545 0%, #0d6efd 50%, #198754 100%);
    color: white;
    padding: 1rem;
    border-radius: 15px;
    margin-bottom: 1rem;
    text-align: center;
    font-weight: bold;
    box-shadow: 0 4px 15px rgba(220,53,69,0.3);
}
</style>
""", unsafe_allow_html=True)

def show_demo_banner():
    """Demo banner'ını göster"""
    st.markdown("""
    <div class="demo-banner">
        🚀 DEMO MODE - UniqeAi Chat Uygulaması
        <br>
        <small>Demo kullanıcıları: admin/123, demo/demo123, test/test123</small>
        <br>
        <small>🔧 Araç entegrasyonu • 📱 Responsive tasarım • 🧪 Test sistemi</small>
    </div>
    """, unsafe_allow_html=True)

def get_demo_response():
    """Demo için rastgele yanıt döndür"""
    return random.choice(DEMO_RESPONSES)

def main():
    # Demo banner'ını göster
    show_demo_banner()
    
    # Session state başlatma
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_screen" not in st.session_state:
        st.session_state.current_screen = "login"
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "dark_theme" not in st.session_state:
        st.session_state.dark_theme = False
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "demo_mode" not in st.session_state:
        st.session_state.demo_mode = True
    
    # Ekran yönlendirmesi
    if st.session_state.logged_in:
        if st.session_state.current_screen == "chat":
            render_chat_screen()
        else:
            render_main_screen()
    else:
        if st.session_state.current_screen == "signup":
            render_signup_screen()
        else:
            render_login_screen()

if __name__ == "__main__":
    main() 