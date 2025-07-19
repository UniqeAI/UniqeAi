import streamlit as st

# Normalde bu bileşenler ayrı dosyalarda olurdu, şimdilik burada taslak olarak duruyor.
# from components.login_screen import render_login
# from components.chat_screen import render_chat

def render_login():
    st.title("Giriş Yap")
    st.text_input("Kullanıcı Adı")
    st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        st.session_state["logged_in"] = True
        st.rerun() # Sayfayı yeniden çalıştırarak durumu günceller

def render_chat():
    st.title("Agent-Llama Sohbet")
    st.write("Sohbet ekranına hoş geldiniz!")
    
    # Mesajlaşma arayüzü buraya gelecek
    st.text_area("Mesaj Geçmişi", "...", height=300)
    st.text_input("Mesajınız:")

    if st.button("Çıkış Yap"):
        del st.session_state["logged_in"]
        st.rerun()

def main():
    st.set_page_config(page_title="Agent-Llama", layout="centered")

    # Session state (oturum durumu) kontrolü
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Duruma göre ekranı render et
    if st.session_state["logged_in"]:
        render_chat()
    else:
        render_login()

if __name__ == "__main__":
    main() 