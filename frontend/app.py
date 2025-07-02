import streamlit as st
import time
import streamlit.components.v1 as components
import urllib.parse

# Normalde bu bileşenler ayrı dosyalarda olurdu, şimdilik burada taslak olarak duruyor.
# from components.login_screen import render_login
# from components.chat_screen import render_chat

def handle_login():
    username = st.session_state.get("login_username", "").strip()
    password = st.session_state.get("login_password", "").strip()
    # Kayıtlı kullanıcılar arasında kontrol
    registered = st.session_state.get("registered_users", [])
    if any(u["username"] == username and u["password"] == password for u in registered):
        st.session_state["logged_in"] = True
        st.session_state["screen"] = "main"
        st.session_state["login_error"] = ""
        st.rerun()
    else:
        st.session_state["login_error"] = "Kullanıcı adı veya şifre hatalı ya da kayıtlı değilsiniz."
        st.rerun()

def render_login():
    st.markdown("""
    <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 0.2em;'>
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712037.png" alt="robot" width="60" style="margin-right: 18px;"/>
        <span style="
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(90deg, #000 0%, #2196f3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-fill-color: transparent;">
            UniqeAi
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.text_input("Kullanıcı Adı", key="login_username")
    st.text_input("Şifre", type="password", key="login_password", on_change=handle_login)
    if st.button("Giriş"):
        handle_login()
    if st.session_state.get("login_error"):
        st.error(st.session_state["login_error"])
    if st.button("Kayıt Ol"):
        st.session_state["screen"] = "signup"
        st.rerun()

def render_sign_up():
    st.title("Kayıt Ol")
    st.text_input("Kullanıcı Adı", key="signup_username")
    st.text_input("E-posta", key="signup_email")
    st.text_input("Şifre", type="password", key="signup_password")
    st.text_input("Şifre (Tekrar)", type="password", key="signup_password2")
    if st.button("Kayıt Ol (Onayla)"):
        username = st.session_state.get("signup_username", "").strip()
        email = st.session_state.get("signup_email", "").strip()
        password = st.session_state.get("signup_password", "").strip()
        password2 = st.session_state.get("signup_password2", "").strip()
        if not username or not email or not password or not password2:
            st.error("Tüm alanları doldurun.")
        elif password != password2:
            st.error("Şifreler eşleşmiyor.")
        elif any(u["username"] == username for u in st.session_state["registered_users"]):
            st.error("Bu kullanıcı adı ile zaten kayıtlı bir kullanıcı var.")
        else:
            st.session_state["registered_users"].append({"username": username, "email": email, "password": password})
            st.success("Kayıt başarılı! Giriş yapılıyor...")
            st.session_state["logged_in"] = True
            st.session_state["login_username"] = username
            st.session_state["screen"] = "main"
            st.rerun()
    if st.button("Geri Dön"):
        st.session_state["screen"] = "login"
        st.rerun()

def get_bot_reply(user_message):
    msg = user_message.lower()
    if "fatura" in msg:
        return (
            "Tabii, hemen fatura bilgilerinizi paylaşıyorum!\n"
            "Son fatura tutarınız: 350 TL.\n"
            "Son ödeme tarihi: 15 Mayıs 2024.\n"
            "Dilerseniz detaylı fatura dökümünü de iletebilirim. Başka bir isteğiniz var mı?"
        )
    elif "paket" in msg or "tarife" in msg:
        return (
            "Mevcut tarifeniz: Uniqe 20GB, aylık 199 TL.\n"
            "Kalan internet: 12GB, kalan dakika: 350dk, kalan SMS: 100.\n"
            "Farklı bir paket veya tarife hakkında bilgi almak ister misiniz?"
        )
    elif "teknik destek" in msg or "arıza" in msg or "internet yok" in msg:
        return (
            "Teknik destek için buradayım!\n"
            "Yaşadığınız sorunu biraz daha detaylandırabilir misiniz? Gerekirse teknik ekibimize yönlendirebilirim."
        )
    elif "kampanya" in msg or "indirim" in msg:
        return (
            "Size özel güncel kampanyalarımız var!\n"
            "- 10GB hediye internet (3 ay boyunca)\n"
            "- Aile paketlerinde %20 indirim\n"
            "Daha fazla kampanya bilgisi için 'daha fazla kampanya' yazabilirsiniz."
        )
    elif "borç" in msg:
        return (
            "Güncel borcunuz: 350 TL.\n"
            "Ödeme yapmak için mobil uygulamamızı veya online işlemler merkezimizi kullanabilirsiniz."
        )
    else:
        return (
            "Merhaba, ben UniqeAi! Size fatura, paket, tarife, kampanya veya teknik destek konularında yardımcı olabilirim.\n"
            "Lütfen sorunuzu detaylıca yazar mısınız?"
        )

def handle_send_message():
    user_input = st.session_state["chat_input"].strip()
    if user_input != "":
        st.session_state["chat_history"].append({"user": st.session_state.get("login_username", "Kullanıcı"), "text": user_input})
        with st.spinner("UniqeAi yazıyor..."):
            time.sleep(1.1)
        bot_reply = get_bot_reply(user_input)
        st.session_state["chat_history"].append({"user": "UniqeAi", "text": bot_reply})
        st.session_state["chat_input"] = ""
        st.rerun()

def render_chat_screen():
    st.markdown("""
    <style>
    .shortcut-bar {
        position: fixed;
        left: 0; right: 0; bottom: 0;
        background: rgba(255,255,255,0.95);
        z-index: 10;
        padding: 0.5em 0 0.7em 0;
        box-shadow: 0 -2px 12px rgba(33,150,243,0.07);
    }
    .shortcut-btn {
        display: inline-block;
        padding: 0.7em 1.2em;
        margin: 0.2em;
        border-radius: 1.5em;
        font-weight: 500;
        font-size: 1em;
        color: #fff;
        background: linear-gradient(90deg, #0d47a1 0%, #2196f3 50%, #000 100%);
        border: none;
        cursor: pointer;
        transition: box-shadow 0.2s, background 0.2s;
        box-shadow: 0 2px 8px rgba(33,150,243,0.13);
        text-align: center;
    }
    .shortcut-btn:hover {
        box-shadow: 0 4px 16px rgba(33,150,243,0.22);
        opacity: 0.92;
        background: linear-gradient(90deg, #2196f3 0%, #0d47a1 100%);
    }
    .chat-input-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 0.5em;
    }
    </style>
    <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 0.2em; margin-top: 1em;'>
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712037.png" alt="robot" width="60" style="margin-right: 18px;"/>
        <span style="
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(90deg, #000 0%, #2196f3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-fill-color: transparent;">
            UniqeAi
        </span>
    </div>
    """, unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "chat_input" not in st.session_state:
        st.session_state["chat_input"] = ""
    for msg in st.session_state["chat_history"]:
        st.write(f"{msg['user']}: {msg['text']}")
    st.text_input(
        "Mesajınızı yazın ve Enter'a basın",
        value=st.session_state["chat_input"],
        key="chat_input",
        on_change=handle_send_message,
        placeholder="Mesajınızı yazın..."
    )
    # Kısa yol cümleleri
    shortcut_sentences = [
        "Fatura bilgimi öğrenmek istiyorum",
        "Kampanyalar hakkında bilgi almak istiyorum",
        "Paket detaylarımı görmek istiyorum",
        "Teknik destek almak istiyorum"
    ]
    st.markdown("<div style='height: 1em;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 1em;'>", unsafe_allow_html=True)
    for idx, sentence in enumerate(shortcut_sentences):
        if st.button(sentence, key=f'shortcut_{idx}', help=sentence, use_container_width=True):
            st.session_state["chat_history"].append({"user": st.session_state.get("login_username", "Kullanıcı"), "text": sentence})
            with st.spinner("UniqeAi yazıyor..."):
                time.sleep(1.1)
            bot_reply = get_bot_reply(sentence)
            st.session_state["chat_history"].append({"user": "UniqeAi", "text": bot_reply})
            st.rerun()
    st.markdown("""
    <style>
    .stButton > button {
        background: linear-gradient(90deg, #0d47a1 0%, #2196f3 50%, #000 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 1.5em !important;
        padding: 1em 2em !important;
        font-size: 1.1em !important;
        font-weight: 500 !important;
        margin: 0.3em 0.5em !important;
        cursor: pointer !important;
        box-shadow: 0 2px 8px rgba(33,150,243,0.13) !important;
        transition: box-shadow 0.2s, background 0.2s !important;
    }
    .stButton > button:hover {
        box-shadow: 0 4px 16px rgba(33,150,243,0.22) !important;
        opacity: 0.92 !important;
        background: linear-gradient(90deg, #2196f3 0%, #0d47a1 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main_screen():
    st.markdown("""
    <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 0.2em; margin-top: 1em;'>
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712037.png" alt="robot" width="60" style="margin-right: 18px;"/>
        <span style="
            font-size: 2.2em;
            font-weight: bold;
            background: linear-gradient(90deg, #000 0%, #2196f3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-fill-color: transparent;">
            UniqeAi Ana Ekran
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.success(f"Hoş geldin, {st.session_state.get('login_username', 'Kullanıcı')}!")
    if st.button("Çıkış Yap"):
        st.session_state["logged_in"] = False
        st.session_state["screen"] = "login"
        st.rerun()

def main():
    st.set_page_config(page_title="UniqeAi", layout="centered")
    try:
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False
        if "screen" not in st.session_state:
            st.session_state["screen"] = "login"
        if "registered_users" not in st.session_state:
            st.session_state["registered_users"] = []

        if st.session_state["logged_in"]:
            render_chat_screen()
        else:
            if st.session_state["screen"] == "login":
                render_login()
            elif st.session_state["screen"] == "signup":
                render_sign_up()
            elif st.session_state["screen"] == "main":
                main_screen()
    except Exception:
        pass

if __name__ == "__main__":
    main() 
