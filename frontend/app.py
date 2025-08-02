import streamlit as st
from components.login_screen import show_login_screen, check_login_status, logout
from components.chat_screen import chat_screen
from utils.api_client import get_api_client

# Sayfa yapılandırması
st.set_page_config(
    page_title="Telekom Müşteri Portalı",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    .user-message {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .ai-message {
        background: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .user-info {
        background: #e8f5e8;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #4caf50;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Ana header
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Telekom Müşteri Portalı</h1>
        <p>Güvenli ve kişiselleştirilmiş müşteri deneyimi</p>
    </div>
    """, unsafe_allow_html=True)

    # Login durumu kontrolü
    if not check_login_status():
        return
    
    # Kullanıcı bilgileri
    user_name = st.session_state.get("user_name", "Kullanıcı")
    user_id = st.session_state.get("user_id", "N/A")
    
    # Sidebar
    with st.sidebar:
        st.title("👤 Kullanıcı Paneli")
        
        # Kullanıcı bilgileri
        st.markdown(f"""
        <div class="user-info">
            <strong>Hoş geldiniz, {user_name}!</strong><br>
            <small>User ID: {user_id}</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigasyon
        st.title("🧭 Navigasyon")
        
        if st.button("🏠 Ana Sayfa", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("💬 AI Chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
        
        if st.button("📊 Fatura İşlemleri", use_container_width=True):
            st.session_state.page = 'billing'
            st.rerun()
        
        if st.button("📦 Paket İşlemleri", use_container_width=True):
            st.session_state.page = 'packages'
            st.rerun()
        
        if st.button("🛠️ Destek", use_container_width=True):
            st.session_state.page = 'support'
            st.rerun()
        
        st.markdown("---")
        
        # Çıkış
        if st.button("🚪 Çıkış Yap", use_container_width=True, type="secondary"):
            logout()
        
        # Sistem durumu
        st.markdown("### 📊 Sistem Durumu")
        
        # API sağlık kontrolü
        api_client = get_api_client()
        health_result = api_client.check_chat_health()
        
        if health_result.get("success"):
            st.success("✅ Backend Bağlantısı")
        else:
            st.error("❌ Backend Bağlantısı")
    
    # Sayfa içeriği
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'chat':
        chat_screen()
    elif st.session_state.page == 'billing':
        show_billing_page()
    elif st.session_state.page == 'packages':
        show_packages_page()
    elif st.session_state.page == 'support':
        show_support_page()
    else:
        show_home_page()

def show_home_page():
    st.title("🏠 Ana Sayfa")
    
    # Hoş geldin mesajı
    user_name = st.session_state.get("user_name", "Kullanıcı")
    st.success(f"✅ Hoş geldiniz, {user_name}!")
    
    # Hızlı erişim kartları
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 AI Asistan</h3>
            <p>Yapay zeka destekli müşteri hizmetleri</p>
            </div>
        """, unsafe_allow_html=True)
    
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Fatura Yönetimi</h3>
            <p>Fatura görüntüleme ve ödeme işlemleri</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📦 Paket Yönetimi</h3>
            <p>Paket bilgileri ve değişiklik işlemleri</p>
            </div>
        """, unsafe_allow_html=True)
    
        st.markdown("""
        <div class="metric-card">
            <h3>🛠️ Destek Sistemi</h3>
            <p>Teknik destek ve sorun çözümü</p>
            </div>
        """, unsafe_allow_html=True)

def show_billing_page():
    st.title("📊 Fatura İşlemleri")
    
    api_client = get_api_client()
    
    # Mevcut fatura
    with st.expander("💰 Mevcut Fatura", expanded=True):
        result = api_client.get_current_bill()
        if result.get("success"):
            data = result.get("data", {})
            st.success(f"✅ Mevcut fatura: {data.get('amount', 0)} TL")
            st.json(data)
        else:
            st.error(f"❌ Hata: {result.get('error')}")
    
    # Geçmiş faturalar
    with st.expander("📜 Geçmiş Faturalar"):
        limit = st.slider("Gösterilecek fatura sayısı", 1, 24, 5)
        if st.button("Geçmiş faturaları getir"):
            result = api_client.get_bill_history(limit)
            if result.get("success"):
                data = result.get("data", {})
                st.success(f"✅ {len(data.get('bills', []))} adet fatura bulundu")
                st.json(data)
            else:
                st.error(f"❌ Hata: {result.get('error')}")
    
    # Ödeme geçmişi
    with st.expander("💳 Ödeme Geçmişi"):
        if st.button("Ödeme geçmişini getir"):
            result = api_client.get_payment_history()
            if result.get("success"):
                data = result.get("data", {})
                st.success(f"✅ {len(data.get('payments', []))} adet ödeme bulundu")
                st.json(data)
            else:
                st.error(f"❌ Hata: {result.get('error')}")

def show_packages_page():
    st.title("📦 Paket İşlemleri")
    
    api_client = get_api_client()
    
    # Mevcut paket
    with st.expander("📱 Mevcut Paket", expanded=True):
        result = api_client.get_current_package()
        if result.get("success"):
            data = result.get("data", {})
            if data:
                st.success(f"✅ Paket: {data.get('package_name', 'N/A')}")
                st.json(data)
            else:
                st.warning("⚠️ Aktif paket bulunamadı")
        else:
            st.error(f"❌ Hata: {result.get('error')}")
    
    # Kalan kotalar
    with st.expander("📊 Kalan Kotalar"):
        if st.button("Kotaları getir"):
            result = api_client.get_remaining_quotas()
            if result.get("success"):
                data = result.get("data", {})
                st.success("✅ Kotalar getirildi")
                st.json(data)
            else:
                st.error(f"❌ Hata: {result.get('error')}")

def show_support_page():
    st.title("🛠️ Destek Sistemi")
    
    api_client = get_api_client()
    
    # Destek talepleri
    with st.expander("📋 Destek Talepleri", expanded=True):
        if st.button("Destek taleplerini getir"):
            result = api_client.get_users_tickets()
            if result.get("success"):
                data = result.get("data", {})
                tickets = data.get("tickets", [])
                st.success(f"✅ {len(tickets)} adet destek talebi bulundu")
                st.json(data)
            else:
                st.error(f"❌ Hata: {result.get('error')}")
    
    # Yeni destek talebi
    with st.expander("➕ Yeni Destek Talebi"):
        description = st.text_area("Sorun açıklaması")
        category = st.selectbox("Kategori", ["technical", "billing", "service"])
        
        if st.button("Destek talebi oluştur"):
            if description:
                result = api_client.create_support_ticket(description, category)
                if result.get("success"):
                    st.success("✅ Destek talebi oluşturuldu!")
                    st.json(result.get("data"))
                else:
                    st.error(f"❌ Hata: {result.get('error')}")
            else:
                st.warning("⚠️ Sorun açıklaması gerekli!")

if __name__ == "__main__":
    main() 