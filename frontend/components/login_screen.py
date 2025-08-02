import streamlit as st
from utils.api_client import get_api_client

def show_login_screen():
    """Login ekranını göster"""
    
    st.title("🔐 Telekom Müşteri Portalı")
    st.markdown("---")
    
    # Tab seçimi
    tab1, tab2 = st.tabs(["📧 Giriş Yap", "📝 Yeni Kayıt"])
    
    api_client = get_api_client()
    
    with tab1:
        st.header("Giriş Yap")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="ornek@email.com")
            password = st.text_input("Şifre", type="password", placeholder="Şifrenizi girin")
        
            col1, col2 = st.columns([1, 1])
            with col1:
                login_button = st.form_submit_button("🔑 Giriş Yap", use_container_width=True)
            with col2:
                demo_button = st.form_submit_button("🎯 Demo Giriş", use_container_width=True)
        
        if login_button:
            if email and password:
                with st.spinner("Giriş yapılıyor..."):
                    result = api_client.login_user(email, password)
                    
                    if result.get("success"):
                        st.success("✅ Giriş başarılı!")
                        st.session_state["logged_in"] = True
                        st.session_state["user_name"] = result.get("user_name", "Kullanıcı")
                        st.session_state["user_id"] = result.get("user_id")
                        st.session_state["session_token"] = result.get("session_token")
                        st.rerun()
                    else:
                        st.error(f"❌ Giriş başarısız: {result.get('error', 'Bilinmeyen hata')}")
            else:
                st.warning("⚠️ Email ve şifre gerekli!")
        
        if demo_button:
            # Demo kullanıcı bilgileri
            demo_users = [
                {"email": "enes.faruk.aydin@email.com", "password": "enes123", "name": "Enes Faruk Aydın"},
                {"email": "nisa.nur.ozkal@email.com", "password": "nisa123", "name": "Nisa Nur Özkal"},
                {"email": "sedat.kilicoglu@email.com", "password": "sedat123", "name": "Sedat Kılıçoğlu"}
            ]
            
            st.info("🎯 Demo kullanıcıları:")
            for user in demo_users:
                st.code(f"Email: {user['email']} | Şifre: {user['password']} | İsim: {user['name']}")
    
        # Kayıtlı kullanıcı bilgileri
        with st.expander("📋 Kayıtlı Kullanıcı Bilgileri"):
            st.markdown("""
            **Test için kullanabileceğiniz kullanıcılar:**
            
            | Email | Şifre | İsim |
            |-------|-------|------|
            | enes.faruk.aydin@email.com | enes123 | Enes Faruk Aydın |
            | nisa.nur.ozkal@email.com | nisa123 | Nisa Nur Özkal |
            | sedat.kilicoglu@email.com | sedat123 | Sedat Kılıçoğlu |
            | erkan.tanriover@email.com | erkan123 | Erkan Tanrıöver |
            | ahmet.nazif.gemalmaz@email.com | ahmet123 | Ahmet Nazif Gemalmaz |
            | ziisan.sahin@email.com | ziisan123 | Ziişan Şahin |
            """)
    
    with tab2:
        st.header("Yeni Kayıt")
        
        with st.form("register_form"):
            name = st.text_input("Ad Soyad", placeholder="Adınız ve soyadınız")
            email = st.text_input("Email", placeholder="ornek@email.com")
            password = st.text_input("Şifre", type="password", placeholder="Şifrenizi girin")
            password_confirm = st.text_input("Şifre Tekrar", type="password", placeholder="Şifrenizi tekrar girin")
            
            register_button = st.form_submit_button("📝 Kayıt Ol", use_container_width=True)
            
            if register_button:
                if name and email and password and password_confirm:
                    if password == password_confirm:
                        with st.spinner("Kayıt oluşturuluyor..."):
                            result = api_client.register_user({
                                "name": name,
                                "email": email,
                                "password": password
                            })
                            
                            if result.get("success"):
                                st.success("✅ Kayıt başarılı!")
                                st.session_state["logged_in"] = True
                                st.session_state["user_name"] = result.get("user_name", name)
                                st.session_state["user_id"] = result.get("user_id")
                                st.session_state["session_token"] = result.get("session_token")
                                st.rerun()
                            else:
                                st.error(f"❌ Kayıt başarısız: {result.get('error', 'Bilinmeyen hata')}")
                    else:
                        st.error("❌ Şifreler eşleşmiyor!")
                else:
                    st.warning("⚠️ Tüm alanlar gerekli!")

def check_login_status():
    """Login durumunu kontrol et"""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if not st.session_state["logged_in"]:
        show_login_screen()
        return False
    
    return True

def logout():
    """Çıkış yap"""
    if "logged_in" in st.session_state:
        del st.session_state["logged_in"]
    if "user_name" in st.session_state:
        del st.session_state["user_name"]
    if "user_id" in st.session_state:
        del st.session_state["user_id"]
    if "session_token" in st.session_state:
        del st.session_state["session_token"]
    
    st.success("👋 Çıkış yapıldı!")
    st.rerun() 