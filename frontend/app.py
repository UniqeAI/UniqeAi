import streamlit as st
from components.login_screen import render_login_screen
from components.signup_screen import render_signup_screen
from components.chat_screen import render_chat_screen
from components.main_screen import render_main_screen
from datetime import datetime
import random

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="CayrosAi - Akıllı Telekom Asistanı",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Demo kullanıcıları - kullanıcı adı tabanlı
DEMO_USERS = {
    "admin": {"password": "123", "name": "Admin Kullanıcı"},
    "demo": {"password": "demo123", "name": "Demo Kullanıcı"},
    "test": {"password": "test123", "name": "Test Kullanıcı"}
}

# Demo yanıtlar - CayrosAi teması
DEMO_RESPONSES = [
    "Merhaba! CayrosAi'ya hoş geldiniz. Size nasıl yardımcı olabilirim?",
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

def main():
    # Session state başlangıç değerleri
    if "current_screen" not in st.session_state:
        st.session_state.current_screen = "main"
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    
    # Ekran yönlendirme
    if st.session_state.current_screen == "main":
        render_main_screen()
    elif st.session_state.current_screen == "login":
        render_login_screen()
    elif st.session_state.current_screen == "signup":
        render_signup_screen()
    elif st.session_state.current_screen == "chat":
        render_chat_screen()
    else:
        # Varsayılan olarak ana ekranı göster
        st.session_state.current_screen = "main"
        render_main_screen()

if __name__ == "__main__":
    main()
