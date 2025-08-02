import streamlit as st
import time
from datetime import datetime
import sys
import os

# Utils klasörünü path'e ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

# API client'ı import et
try:
    from utils.api_client import get_api_client
    API_CLIENT_AVAILABLE = True
except ImportError:
    API_CLIENT_AVAILABLE = False
    print("API client bulunamadı, mock modunda çalışıyor")

def render_choyrens_header():
    """CHOYRENS AI header'ını render et"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: var(--primary-blue); font-family: 'Orbitron', sans-serif; margin: 0;">
            🤖 CHOYRENS AI
        </h1>
        <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Telekom AI Asistanı
        </p>
    </div>
    """, unsafe_allow_html=True)

def generate_bot_response(message):
    """Mock bot yanıtı üret"""
    responses = [
        "Merhaba! Size nasıl yardımcı olabilirim?",
        "Anlıyorum, bu konuda size yardımcı olabilirim.",
        "Bu sorunuzu çözmek için size rehberlik edebilirim.",
        "Teşekkürler! Başka bir sorunuz var mı?",
        "Bu konuda daha detaylı bilgi verebilirim."
    ]
    return responses[len(message) % len(responses)]

def chat_screen():
    """Chat sayfasını göster"""
    render_choyrens_header()
    
    # API client'ı al
    if API_CLIENT_AVAILABLE:
        api_client = get_api_client()
    else:
        api_client = None
    
    # Session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = 1  # Demo için varsayılan
    
    # Debug: Session token'ı göster
    if API_CLIENT_AVAILABLE and api_client:
        st.write("🔍 **Debug - Session Token:**", api_client.session_token)
    
    # Sidebar - Kullanıcı bilgileri ve kontroller
    with st.sidebar:
        st.header("👤 Profil")
        
        # Kullanıcı ID seçici
        user_id = st.selectbox(
            "Müşteri ID",
            options=[0, 1, 2, 3, 4, 5, 6, 7],
            index=1,
            help="Test için farklı müşteri profilleri"
        )
        st.session_state.user_id = user_id
        
        # Sağlık kontrolü
        st.header("🔧 Sistem Durumu")
        if st.button("Durumu Kontrol Et"):
            with st.spinner("Kontrol ediliyor..."):
                if api_client:
                    health = api_client.check_chat_health()
                    if health.get("status") == "healthy":
                        st.success("✅ Sistem sağlıklı")
                        st.json(health)
                    else:
                        st.error("❌ Sistem hatası")
                        st.json(health)
                else:
                    st.info("🔧 API client mevcut değil")
        
        # Sohbet temizleme
        st.header("🗑️ Sohbet")
        if st.button("Sohbeti Temizle"):
            st.session_state.messages = []
            st.rerun()
        
        # Hızlı eylemler
        st.header("⚡ Hızlı Eylemler")
        quick_actions = {
            "💰 Faturamı Göster": "Mevcut faturamı gösterir misin?",
            "📦 Paketim Nedir": "Hangi paketi kullanıyorum?",
            "📊 Kalan Kotalarım": "Ne kadar kotam kaldı?",
            "🔧 Arıza Bildir": "İnternetimde sorun var, yardım eder misin?",
            "📞 Profil Bilgileri": "Profil bilgilerimi göster"
        }
        
        for action_name, action_message in quick_actions.items():
            if st.button(action_name, use_container_width=True):
                # Mesajı otomatik gönder
                st.session_state.messages.append({
                    "role": "user", 
                    "content": action_message,
                    "timestamp": time.time()
                })
                
                # AI yanıtını al
                with st.spinner("AI düşünüyor..."):
                    if api_client:
                        response = api_client.send_chat_message(
                            message=action_message,
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
                        mock_response = generate_bot_response(action_message)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": mock_response,
                            "timestamp": time.time()
                        })
                
                st.rerun()
    
    # Ana chat alanı
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
                                if tool.get("durum"):
                                    st.info(f"Durum: {tool.get('durum')}")
                                if tool.get("sonuc"):
                                    st.success("✅ Başarılı")
                                elif tool.get("hata_mesaji"):
                                    st.error(f"❌ Hata: {tool.get('hata_mesaji')}")
                                
                                # Fatura verilerini görsel olarak göster
                                if tool.get("arac_adi") == "get_past_bills" and tool.get("sonuc"):
                                    sonuc = tool.get("sonuc", {})
                                    if isinstance(sonuc, dict) and sonuc.get("bills"):
                                        bills = sonuc.get("bills", [])
                                        if bills:
                                            st.subheader("📊 Geçmiş Faturalar")
                                            
                                            # Fatura özeti
                                            total_bills = len(bills)
                                            paid_bills = len([b for b in bills if b.get("status") == "paid"])
                                            unpaid_bills = total_bills - paid_bills
                                            total_amount = sum(b.get("amount", 0) for b in bills)
                                            
                                            col1, col2, col3, col4 = st.columns(4)
                                            with col1:
                                                st.metric("Toplam Fatura", total_bills)
                                            with col2:
                                                st.metric("Ödenmiş", paid_bills)
                                            with col3:
                                                st.metric("Ödenmemiş", unpaid_bills)
                                            with col4:
                                                st.metric("Toplam Tutar", f"{total_amount} ₺")
                                            
                                            # Fatura tablosu
                                            st.subheader("📋 Fatura Detayları")
                                            
                                            # Tablo başlıkları
                                            cols = st.columns([2, 2, 2, 2, 2, 2])
                                            cols[0].markdown("**Fatura ID**")
                                            cols[1].markdown("**Tarih**")
                                            cols[2].markdown("**Son Ödeme**")
                                            cols[3].markdown("**Tutar**")
                                            cols[4].markdown("**Durum**")
                                            cols[5].markdown("**Hizmetler**")
                                            
                                            # Fatura satırları
                                            for bill in bills:
                                                cols = st.columns([2, 2, 2, 2, 2, 2])
                                                
                                                # Fatura ID
                                                cols[0].code(bill.get("bill_id", "N/A"))
                                                
                                                # Tarih
                                                bill_date = bill.get("bill_date", "")
                                                cols[1].text(bill_date)
                                                
                                                # Son ödeme
                                                due_date = bill.get("due_date", "")
                                                cols[2].text(due_date)
                                                
                                                # Tutar
                                                amount = bill.get("amount", 0)
                                                cols[3].markdown(f"**{amount} ₺**")
                                                
                                                # Durum
                                                status = bill.get("status", "")
                                                if status == "paid":
                                                    cols[4].success("✅ Ödendi")
                                                else:
                                                    cols[4].error("❌ Ödenmedi")
                                                
                                                # Hizmetler
                                                services = bill.get("services", [])
                                                service_text = ""
                                                for service in services:
                                                    service_name = service.get("service_name", "")
                                                    service_amount = service.get("amount", 0)
                                                    service_text += f"• {service_name}: {service_amount} ₺\n"
                                                cols[5].text(service_text.strip())
                                                
                                                st.divider()
                                
                                # Mevcut fatura görsel gösterimi
                                elif tool.get("arac_adi") == "get_current_bill":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("💰 Mevcut Fatura")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Fatura Tutarı", f"{sonuc.get('amount', 0)} ₺")
                                            st.metric("Son Ödeme", sonuc.get('due_date', 'N/A'))
                                        with col2:
                                            st.metric("Durum", sonuc.get('status', 'N/A'))
                                            st.metric("Fatura Tarihi", sonuc.get('bill_date', 'N/A'))
                                        
                                        # Hizmetler
                                        services = sonuc.get('services', [])
                                        if services:
                                            st.subheader("📋 Hizmet Detayları")
                                            for service in services:
                                                col1, col2 = st.columns([3, 1])
                                                col1.text(service.get('service_name', 'N/A'))
                                                col2.markdown(f"**{service.get('amount', 0)} ₺**")
                                
                                # Paket bilgileri görsel gösterimi
                                elif tool.get("arac_adi") == "get_customer_package":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📦 Mevcut Paket")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Paket Adı", sonuc.get('package_name', 'N/A'))
                                        with col2:
                                            st.metric("Aylık Ücret", f"{sonuc.get('monthly_fee', 0)} ₺")
                                        with col3:
                                            st.metric("Paket Türü", sonuc.get('package_type', 'N/A'))
                                        
                                        # Paket özellikleri
                                        features = sonuc.get('features', [])
                                        if features:
                                            st.subheader("✨ Paket Özellikleri")
                                            for feature in features:
                                                st.text(f"• {feature}")
                                
                                # Mevcut paket bilgileri görsel gösterimi (get_current_package)
                                elif tool.get("arac_adi") == "get_current_package":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📦 Mevcut Paket")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Paket Adı", sonuc.get('package_name', 'N/A'))
                                        with col2:
                                            st.metric("Aylık Ücret", f"{sonuc.get('monthly_fee', 0)} ₺")
                                        with col3:
                                            st.metric("Paket Türü", sonuc.get('package_type', 'N/A'))
                                        
                                        # Paket özellikleri
                                        features = sonuc.get('features', [])
                                        if features:
                                            st.subheader("✨ Paket Özellikleri")
                                            for feature in features:
                                                st.text(f"• {feature}")
                                        
                                        # Paket detayları
                                        st.subheader("📋 Paket Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("İnternet Hızı", sonuc.get('internet_speed', 'N/A'))
                                            st.metric("Sesli Arama", sonuc.get('voice_minutes', 'N/A'))
                                        with col2:
                                            st.metric("SMS", sonuc.get('sms_count', 'N/A'))
                                            st.metric("Sözleşme Süresi", sonuc.get('contract_duration', 'N/A'))
                                
                                # Kota bilgileri görsel gösterimi
                                elif tool.get("arac_adi") == "get_remaining_quotas":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📊 Kalan Kotalar")
                                        
                                        # İnternet kotası
                                        internet_gb = sonuc.get("internet_remaining_gb", 0)
                                        internet_percentage = sonuc.get("usage_percentage", {}).get("internet", 0)
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("🌐 İnternet", f"{internet_gb} GB")
                                        with col2:
                                            st.metric("Kullanım", f"%{internet_percentage}")
                                        with col3:
                                            if internet_percentage > 80:
                                                st.error("⚠️ Kritik")
                                            elif internet_percentage > 60:
                                                st.warning("⚠️ Dikkat")
                                            else:
                                                st.success("✅ Normal")
                                        
                                        # Sesli arama kotası
                                        voice_minutes = sonuc.get("voice_remaining_minutes", 0)
                                        voice_percentage = sonuc.get("usage_percentage", {}).get("voice", 0)
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("📞 Sesli Arama", f"{voice_minutes} dakika")
                                        with col2:
                                            st.metric("Kullanım", f"%{voice_percentage}")
                                        with col3:
                                            if voice_percentage > 80:
                                                st.error("⚠️ Kritik")
                                            elif voice_percentage > 60:
                                                st.warning("⚠️ Dikkat")
                                            else:
                                                st.success("✅ Normal")
                                        
                                        # SMS kotası
                                        sms_count = sonuc.get("sms_remaining", 0)
                                        sms_percentage = sonuc.get("usage_percentage", {}).get("sms", 0)
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("💬 SMS", f"{sms_count} adet")
                                        with col2:
                                            st.metric("Kullanım", f"%{sms_percentage}")
                                        with col3:
                                            if sms_percentage > 80:
                                                st.error("⚠️ Kritik")
                                            elif sms_percentage > 60:
                                                st.warning("⚠️ Dikkat")
                                            else:
                                                st.success("✅ Normal")
                                        
                                        # Dönem bilgisi
                                        period_end = sonuc.get("period_end", "N/A")
                                        st.info(f"📅 Dönem sonu: {period_end}")
                                
                                # Müşteri profili görsel gösterimi
                                elif tool.get("arac_adi") == "get_customer_profile":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("👤 Müşteri Profili")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Müşteri ID", sonuc.get('customer_id', 'N/A'))
                                            st.metric("Ad Soyad", sonuc.get('full_name', 'N/A'))
                                            st.metric("E-posta", sonuc.get('email', 'N/A'))
                                        with col2:
                                            st.metric("Telefon", sonuc.get('phone', 'N/A'))
                                            st.metric("Adres", sonuc.get('address', 'N/A'))
                                            st.metric("Üyelik Tarihi", sonuc.get('registration_date', 'N/A'))
                                
                                # Ödeme geçmişi görsel gösterimi
                                elif tool.get("arac_adi") == "get_payment_history":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        payments = sonuc.get('payments', [])
                                        if payments:
                                            st.subheader("💳 Ödeme Geçmişi")
                                            
                                            # Ödeme özeti
                                            total_payments = len(payments)
                                            total_amount = sum(p.get('amount', 0) for p in payments)
                                            
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.metric("Toplam Ödeme", total_payments)
                                            with col2:
                                                st.metric("Toplam Tutar", f"{total_amount} ₺")
                                            
                                            # Ödeme tablosu
                                            st.subheader("📋 Ödeme Detayları")
                                            cols = st.columns([2, 2, 2, 2, 2])
                                            cols[0].markdown("**Tarih**")
                                            cols[1].markdown("**Tutar**")
                                            cols[2].markdown("**Yöntem**")
                                            cols[3].markdown("**Durum**")
                                            cols[4].markdown("**Referans**")
                                            
                                            for payment in payments:
                                                cols = st.columns([2, 2, 2, 2, 2])
                                                cols[0].text(payment.get('payment_date', 'N/A'))
                                                cols[1].markdown(f"**{payment.get('amount', 0)} ₺**")
                                                cols[2].text(payment.get('payment_method', 'N/A'))
                                                
                                                status = payment.get('status', '')
                                                if status == 'completed':
                                                    cols[3].success("✅ Tamamlandı")
                                                else:
                                                    cols[3].error("❌ Başarısız")
                                                
                                                cols[4].code(payment.get('reference_id', 'N/A'))
                                                st.divider()
                                
                                # Sistem durumu görsel gösterimi
                                elif tool.get("arac_adi") == "get_system_health":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🔧 Sistem Durumu")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            status = sonuc.get('status', 'unknown')
                                            if status == 'healthy':
                                                st.success("✅ Sistem Sağlıklı")
                                            else:
                                                st.error("❌ Sistem Hatası")
                                        with col2:
                                            st.metric("Uptime", sonuc.get('uptime', 'N/A'))
                                        with col3:
                                            st.metric("Versiyon", sonuc.get('version', 'N/A'))
                                        
                                        # Sistem bileşenleri
                                        components = sonuc.get('components', [])
                                        if components:
                                            st.subheader("⚙️ Sistem Bileşenleri")
                                            for component in components:
                                                col1, col2 = st.columns([3, 1])
                                                col1.text(component.get('name', 'N/A'))
                                                status = component.get('status', 'unknown')
                                                if status == 'healthy':
                                                    col2.success("✅")
                                                else:
                                                    col2.error("❌")
                                
                                # Fatura ödeme görsel gösterimi
                                elif tool.get("arac_adi") == "pay_bill":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("💳 Fatura Ödeme")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Ödeme ID", sonuc.get('payment_id', 'N/A'))
                                            st.metric("Fatura ID", sonuc.get('bill_id', 'N/A'))
                                        with col2:
                                            st.metric("Tutar", f"{sonuc.get('amount', 0)} ₺")
                                            st.metric("Yöntem", sonuc.get('method', 'N/A'))
                                        with col3:
                                            status = sonuc.get('status', 'unknown')
                                            if status == 'completed':
                                                st.success("✅ Başarılı")
                                            else:
                                                st.error("❌ Başarısız")
                                            st.metric("Onay Kodu", sonuc.get('confirmation_code', 'N/A'))
                                        
                                        # İşlem detayları
                                        st.subheader("📋 İşlem Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**İşlem Tarihi:** {sonuc.get('transaction_date', 'N/A')}")
                                        with col2:
                                            st.info(f"**Durum:** {sonuc.get('status', 'N/A')}")
                                        
                                        # Başarı mesajı
                                        if sonuc.get('status') == 'completed':
                                            st.success("🎉 Fatura ödeme işlemi başarıyla tamamlandı!")
                                        else:
                                            st.error("❌ Fatura ödeme işlemi başarısız oldu.")
                                
                                # Otomatik ödeme görsel gösterimi
                                elif tool.get("arac_adi") == "setup_autopay":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🔄 Otomatik Ödeme")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                            st.metric("Ödeme Yöntemi", sonuc.get('payment_method', 'N/A'))
                                        with col2:
                                            autopay_enabled = sonuc.get('autopay_enabled', False)
                                            if autopay_enabled:
                                                st.success("✅ Aktif")
                                            else:
                                                st.error("❌ Pasif")
                                            st.metric("Kart Türü", sonuc.get('card_type', 'N/A'))
                                        with col3:
                                            st.metric("Kart Son 4", sonuc.get('card_last4', 'N/A'))
                                            st.metric("Limit", f"{sonuc.get('auto_payment_limit', 0)} ₺")
                                        
                                        # Detaylar
                                        st.subheader("📋 Otomatik Ödeme Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Son Güncelleme:** {sonuc.get('last_updated', 'N/A')}")
                                        with col2:
                                            st.info(f"**Sonraki Ödeme:** {sonuc.get('next_payment_date', 'N/A')}")
                                        
                                        # Durum mesajı
                                        if sonuc.get('autopay_enabled'):
                                            st.success("🎉 Otomatik ödeme başarıyla aktifleştirildi!")
                                        else:
                                            st.warning("⚠️ Otomatik ödeme devre dışı bırakıldı.")
                                
                                # Paket değiştirme görsel gösterimi
                                elif tool.get("arac_adi") == "change_package":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🔄 Paket Değiştirme")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Değişiklik ID", sonuc.get('change_id', 'N/A'))
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                        with col2:
                                            st.metric("Mevcut Paket", sonuc.get('current_package', 'N/A'))
                                            st.metric("Yeni Paket", sonuc.get('new_package', 'N/A'))
                                        with col3:
                                            status = sonuc.get('status', 'unknown')
                                            if status == 'pending':
                                                st.warning("⏳ Beklemede")
                                            elif status == 'completed':
                                                st.success("✅ Tamamlandı")
                                            else:
                                                st.error("❌ Hata")
                                            st.metric("Tahmini Maliyet", f"{sonuc.get('estimated_cost', 0)} ₺")
                                        
                                        # Detaylar
                                        st.subheader("📋 Değişiklik Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Geçerlilik Tarihi:** {sonuc.get('effective_date', 'N/A')}")
                                            st.info(f"**İşlem Ücreti:** {sonuc.get('processing_fee', 0)} ₺")
                                        with col2:
                                            st.info(f"**Toplam Maliyet:** {sonuc.get('total_cost', 0)} ₺")
                                        
                                        # Durum mesajı
                                        if sonuc.get('status') == 'pending':
                                            st.info("📝 Paket değişikliği talebiniz alındı. 7 gün içinde aktif olacak.")
                                        elif sonuc.get('status') == 'completed':
                                            st.success("🎉 Paket değişikliği başarıyla tamamlandı!")
                                
                                # Kullanılabilir paketler görsel gösterimi
                                elif tool.get("arac_adi") == "get_available_packages":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📦 Kullanılabilir Paketler")
                                        
                                        packages = sonuc.get('packages', [])
                                        if packages:
                                            st.metric("Toplam Paket Sayısı", sonuc.get('total_count', 0))
                                            
                                            # Paket kartları
                                            for i, package in enumerate(packages):
                                                with st.expander(f"📦 {package.get('package_name', 'N/A')}"):
                                                    col1, col2 = st.columns(2)
                                                    with col1:
                                                        st.metric("Aylık Ücret", f"{package.get('monthly_fee', 0)} ₺")
                                                        st.text(f"📝 {package.get('description', 'Açıklama yok')}")
                                                    with col2:
                                                        features = package.get('features', {})
                                                        st.text(f"🌐 İnternet: {features.get('internet_gb', 0)} GB")
                                                        st.text(f"📞 Dakika: {features.get('voice_minutes', 0)}")
                                                        st.text(f"💬 SMS: {features.get('sms_count', 0)}")
                                                        roaming = "✅" if features.get('roaming_enabled', False) else "❌"
                                                        st.text(f"🌍 Roaming: {roaming}")
                                
                                # Paket detayları görsel gösterimi
                                elif tool.get("arac_adi") == "get_package_details":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📋 Paket Detayları")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Paket Adı", sonuc.get('package_name', 'N/A'))
                                            st.metric("Aylık Ücret", f"{sonuc.get('monthly_fee', 0)} ₺")
                                        with col2:
                                            features = sonuc.get('features', {})
                                            st.metric("İnternet", f"{features.get('internet_gb', 0)} GB")
                                            st.metric("Dakika", features.get('voice_minutes', 0))
                                        with col3:
                                            st.metric("SMS", features.get('sms_count', 0))
                                            roaming = "✅" if features.get('roaming_enabled', False) else "❌"
                                            st.metric("Roaming", roaming)
                                        
                                        # Özellikler
                                        st.subheader("✨ Paket Özellikleri")
                                        features = sonuc.get('features', {})
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**İnternet:** {features.get('internet_gb', 0)} GB")
                                            st.info(f"**Sesli Arama:** {features.get('voice_minutes', 0)} dakika")
                                        with col2:
                                            st.info(f"**SMS:** {features.get('sms_count', 0)} adet")
                                            roaming_status = "Aktif" if features.get('roaming_enabled', False) else "Pasif"
                                            st.info(f"**Roaming:** {roaming_status}")
                                        
                                        # Açıklama
                                        if sonuc.get('description'):
                                            st.subheader("📝 Paket Açıklaması")
                                            st.info(sonuc.get('description'))
                                
                                # Arıza bildirimi görsel gösterimi
                                elif tool.get("arac_adi") == "create_fault_ticket":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🛠️ Arıza Bildirimi")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Ticket ID", sonuc.get('ticket_id', 'N/A'))
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                        with col2:
                                            st.metric("Kategori", sonuc.get('category', 'N/A'))
                                            st.metric("Öncelik", sonuc.get('priority', 'N/A'))
                                        with col3:
                                            status = sonuc.get('status', 'unknown')
                                            if status == 'open':
                                                st.warning("⏳ Açık")
                                            elif status == 'closed':
                                                st.success("✅ Kapalı")
                                            else:
                                                st.error("❌ Hata")
                                            st.metric("Referans No", sonuc.get('reference_number', 'N/A'))
                                        
                                        # Detaylar
                                        st.subheader("📋 Arıza Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Oluşturulma Tarihi:** {sonuc.get('created_date', 'N/A')}")
                                            st.info(f"**Atanan Kişi:** {sonuc.get('assigned_to', 'N/A')}")
                                        with col2:
                                            st.info(f"**Tahmini Çözüm:** {sonuc.get('estimated_resolution', 'N/A')}")
                                        
                                        # Sorun açıklaması
                                        st.subheader("📝 Sorun Açıklaması")
                                        st.text_area("Açıklama", sonuc.get('issue_description', 'Açıklama yok'), disabled=True)
                                        
                                        # Durum mesajı
                                        if sonuc.get('status') == 'open':
                                            st.success("🎉 Arıza bildirimi başarıyla oluşturuldu!")
                                        else:
                                            st.error("❌ Arıza bildirimi oluşturulamadı.")
                                
                                # Arıza durumu görsel gösterimi
                                elif tool.get("arac_adi") == "get_fault_ticket_status":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📊 Arıza Durumu")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Ticket ID", sonuc.get('ticket_id', 'N/A'))
                                            st.metric("İlerleme", f"%{sonuc.get('progress', 0)}")
                                        with col2:
                                            status = sonuc.get('status', 'unknown')
                                            if status == 'in_progress':
                                                st.info("🔄 İşlemde")
                                            elif status == 'completed':
                                                st.success("✅ Tamamlandı")
                                            elif status == 'open':
                                                st.warning("⏳ Açık")
                                            else:
                                                st.error("❌ Hata")
                                            st.metric("Teknisyen", sonuc.get('assigned_technician', 'N/A'))
                                        with col3:
                                            st.metric("Son Güncelleme", sonuc.get('last_updated', 'N/A'))
                                        
                                        # İlerleme çubuğu
                                        progress = sonuc.get('progress', 0)
                                        st.progress(progress / 100)
                                        
                                        # Detaylar
                                        st.subheader("📋 Durum Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Tahmini Tamamlanma:** {sonuc.get('estimated_completion', 'N/A')}")
                                        with col2:
                                            st.info(f"**Notlar:** {sonuc.get('notes', 'N/A')}")
                                
                                # İnternet hız testi görsel gösterimi
                                elif tool.get("arac_adi") == "test_internet_speed":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🚀 İnternet Hız Testi")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("İndirme Hızı", f"{sonuc.get('download_speed_mbps', 0)} Mbps")
                                            st.metric("Yükleme Hızı", f"{sonuc.get('upload_speed_mbps', 0)} Mbps")
                                        with col2:
                                            st.metric("Ping", f"{sonuc.get('ping_ms', 0)} ms")
                                            st.metric("Jitter", f"{sonuc.get('jitter_ms', 0)} ms")
                                        with col3:
                                            quality = sonuc.get('connection_quality', 'unknown')
                                            if quality == 'excellent':
                                                st.success("⭐ Mükemmel")
                                            elif quality == 'good':
                                                st.info("👍 İyi")
                                            elif quality == 'fair':
                                                st.warning("⚠️ Orta")
                                            else:
                                                st.error("❌ Kötü")
                                            st.metric("Paket Kaybı", f"%{sonuc.get('packet_loss_percent', 0)}")
                                        
                                        # Hız grafiği
                                        st.subheader("📊 Hız Analizi")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Test Tarihi:** {sonuc.get('test_date', 'N/A')}")
                                            st.info(f"**Sunucu Konumu:** {sonuc.get('server_location', 'N/A')}")
                                        with col2:
                                            st.info(f"**Test Süresi:** {sonuc.get('test_duration_seconds', 0)} saniye")
                                            st.info(f"**Protokol:** {sonuc.get('protocol', 'N/A')}")
                                        
                                        # Bağlantı kalitesi
                                        st.subheader("🔍 Bağlantı Kalitesi")
                                        quality = sonuc.get('connection_quality', 'unknown')
                                        if quality == 'excellent':
                                            st.success("🎉 Bağlantınız mükemmel! Video streaming ve oyun için ideal.")
                                        elif quality == 'good':
                                            st.info("👍 Bağlantınız iyi. Çoğu aktivite için uygun.")
                                        elif quality == 'fair':
                                            st.warning("⚠️ Bağlantınız orta seviyede. Bazı aktiviteler yavaş olabilir.")
                                        else:
                                            st.error("❌ Bağlantınızda sorun var. Teknik destek ile iletişime geçin.")
                                
                                # Roaming görsel gösterimi
                                elif tool.get("arac_adi") == "enable_roaming":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🌍 Roaming Hizmeti")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                            st.metric("Günlük Ücret", f"{sonuc.get('daily_fee', 0)} ₺")
                                        with col2:
                                            roaming_enabled = sonuc.get('roaming_enabled', False)
                                            if roaming_enabled:
                                                st.success("✅ Aktif")
                                            else:
                                                st.error("❌ Pasif")
                                            st.metric("Aktivasyon Ücreti", f"{sonuc.get('activation_fee', 0)} ₺")
                                        with col3:
                                            st.metric("Aylık Limit", f"{sonuc.get('monthly_limit', 0)} ₺")
                                            st.metric("Geçerlilik Tarihi", sonuc.get('effective_date', 'N/A'))
                                        
                                        # Desteklenen ülkeler
                                        st.subheader("🌐 Desteklenen Ülkeler")
                                        countries = sonuc.get('supported_countries', [])
                                        if countries:
                                            cols = st.columns(4)
                                            for i, country in enumerate(countries):
                                                cols[i % 4].info(f"🇪🇺 {country}")
                                        
                                        # Durum mesajı
                                        if sonuc.get('roaming_enabled'):
                                            st.success("🎉 Roaming hizmeti başarıyla aktifleştirildi!")
                                        else:
                                            st.warning("⚠️ Roaming hizmeti devre dışı bırakıldı.")
                                
                                # Ağ durumu görsel gösterimi
                                elif tool.get("arac_adi") == "check_network_status":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📡 Ağ Durumu")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Bölge", sonuc.get('region', 'N/A'))
                                            st.metric("Durum", sonuc.get('status', 'N/A'))
                                        with col2:
                                            coverage = sonuc.get('coverage', 'unknown')
                                            if coverage == 'excellent':
                                                st.success("⭐ Mükemmel")
                                            elif coverage == 'good':
                                                st.info("👍 İyi")
                                            elif coverage == 'fair':
                                                st.warning("⚠️ Orta")
                                            else:
                                                st.error("❌ Kötü")
                                            st.metric("Son Güncelleme", sonuc.get('last_updated', 'N/A'))
                                        with col3:
                                            st.metric("Uptime", sonuc.get('performance_metrics', {}).get('uptime', 'N/A'))
                                            st.metric("Yanıt Süresi", sonuc.get('performance_metrics', {}).get('response_time', 'N/A'))
                                        
                                        # Hizmet durumları
                                        st.subheader("📊 Hizmet Durumları")
                                        services = sonuc.get('services', {})
                                        if services:
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                for service, status in list(services.items())[:3]:
                                                    if status == 'operational':
                                                        st.success(f"✅ {service.upper()}")
                                                    else:
                                                        st.error(f"❌ {service.upper()}")
                                            with col2:
                                                for service, status in list(services.items())[3:]:
                                                    if status == 'operational':
                                                        st.success(f"✅ {service.upper()}")
                                                    else:
                                                        st.warning(f"⚠️ {service.upper()}")
                                        
                                        # Performans metrikleri
                                        st.subheader("📈 Performans Metrikleri")
                                        metrics = sonuc.get('performance_metrics', {})
                                        if metrics:
                                            col1, col2, col3 = st.columns(3)
                                            with col1:
                                                st.info(f"**Uptime:** {metrics.get('uptime', 'N/A')}")
                                            with col2:
                                                st.info(f"**Yanıt Süresi:** {metrics.get('response_time', 'N/A')}")
                                            with col3:
                                                st.info(f"**Paket Kaybı:** {metrics.get('packet_loss', 'N/A')}")
                                        
                                        # Durum mesajı
                                        if sonuc.get('status') == 'operational':
                                            st.success("🎉 Ağ durumu mükemmel! Tüm hizmetler çalışıyor.")
                                        else:
                                            st.warning("⚠️ Ağ durumunda sorun var. Teknik destek ile iletişime geçin.")
                                
                                # İletişim güncelleme görsel gösterimi
                                elif tool.get("arac_adi") == "update_customer_contact":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📞 İletişim Bilgileri Güncelleme")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                            st.metric("İletişim Türü", sonuc.get('contact_type', 'N/A'))
                                        with col2:
                                            st.metric("Eski Değer", sonuc.get('old_value', 'N/A'))
                                            st.metric("Yeni Değer", sonuc.get('new_value', 'N/A'))
                                        with col3:
                                            status = sonuc.get('status', 'unknown')
                                            if status == 'updated':
                                                st.success("✅ Güncellendi")
                                            else:
                                                st.error("❌ Hata")
                                            st.metric("Doğrulama Gerekli", "Evet" if sonuc.get('verification_required') else "Hayır")
                                        
                                        # Detaylar
                                        st.subheader("📋 Güncelleme Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Güncelleme Tarihi:** {sonuc.get('updated_date', 'N/A')}")
                                            st.info(f"**Doğrulama Yöntemi:** {sonuc.get('verification_method', 'N/A')}")
                                        with col2:
                                            st.info(f"**Durum:** {sonuc.get('status', 'N/A')}")
                                        
                                        # Durum mesajı
                                        if sonuc.get('status') == 'updated':
                                            st.success("🎉 İletişim bilgileri başarıyla güncellendi!")
                                        else:
                                            st.error("❌ İletişim bilgileri güncellenemedi.")
                                
                                # Hat askıya alma görsel gösterimi
                                elif tool.get("arac_adi") == "suspend_line":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("⏸️ Hat Askıya Alma")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                            st.metric("Askıya Alma ID", sonuc.get('suspension_id', 'N/A'))
                                        with col2:
                                            status = sonuc.get('status', 'unknown')
                                            if status == 'suspended':
                                                st.warning("⏸️ Askıya Alındı")
                                            else:
                                                st.error("❌ Hata")
                                            st.metric("Yeniden Aktivasyon Ücreti", f"{sonuc.get('reactivation_fee', 0)} ₺")
                                        with col3:
                                            st.metric("Askıya Alma Tarihi", sonuc.get('suspended_date', 'N/A'))
                                            st.metric("Tahmini Aktivasyon", sonuc.get('estimated_reactivation_date', 'N/A'))
                                        
                                        # Etkilenen hizmetler
                                        st.subheader("🔧 Etkilenen Hizmetler")
                                        services = sonuc.get('affected_services', [])
                                        if services:
                                            cols = st.columns(len(services))
                                            for i, service in enumerate(services):
                                                cols[i].error(f"❌ {service.upper()}")
                                        
                                        # Detaylar
                                        st.subheader("📋 Askıya Alma Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Sebep:** {sonuc.get('reason', 'N/A')}")
                                        with col2:
                                            st.info(f"**Durum:** {sonuc.get('status', 'N/A')}")
                                        
                                        # Durum mesajı
                                        if sonuc.get('status') == 'suspended':
                                            st.warning("⚠️ Hat başarıyla askıya alındı. Yeniden aktivasyon için ücret ödemeniz gerekiyor.")
                                        else:
                                            st.error("❌ Hat askıya alınamadı.")
                                
                                # Hat yeniden aktifleştirme görsel gösterimi
                                elif tool.get("arac_adi") == "reactivate_line":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🔄 Hat Yeniden Aktifleştirme")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                            st.metric("Aktivasyon ID", sonuc.get('reactivation_id', 'N/A'))
                                        with col2:
                                            status = sonuc.get('status', 'unknown')
                                            if status == 'active':
                                                st.success("✅ Aktif")
                                            else:
                                                st.error("❌ Hata")
                                            st.metric("İşlem Süresi", f"{sonuc.get('processing_time_minutes', 0)} dakika")
                                        with col3:
                                            st.metric("Aktivasyon Tarihi", sonuc.get('reactivated_date', 'N/A'))
                                            st.metric("Ücret Ödendi", "Evet" if sonuc.get('reactivation_fee_paid') else "Hayır")
                                        
                                        # Geri yüklenen hizmetler
                                        st.subheader("🔧 Geri Yüklenen Hizmetler")
                                        services = sonuc.get('services_restored', [])
                                        if services:
                                            cols = st.columns(len(services))
                                            for i, service in enumerate(services):
                                                cols[i].success(f"✅ {service.upper()}")
                                        
                                        # Durum mesajı
                                        if sonuc.get('status') == 'active':
                                            st.success("🎉 Hat başarıyla yeniden aktifleştirildi!")
                                        else:
                                            st.error("❌ Hat yeniden aktifleştirilemedi.")
                                
                                # Arıza talebini kapatma görsel gösterimi
                                elif tool.get("arac_adi") == "close_fault_ticket":
                                    sonuc = tool.get("sonuc", {})
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🛠️ Arıza Talebi Kapatma")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Ticket ID", sonuc.get('ticket_id', 'N/A'))
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                        with col2:
                                            st.metric("Kapanma Tarihi", sonuc.get('closed_date', 'N/A'))
                                            st.metric("Kapanma Durumu", sonuc.get('status', 'N/A'))
                                        # Sorun açıklaması
                                        st.subheader("📝 Sorun Açıklaması")
                                        st.text_area("Açıklama", sonuc.get('issue_description', 'Açıklama yok'), disabled=True)
                                        # Başarı mesajı
                                        if sonuc.get('status') == 'closed':
                                            st.success("🎉 Arıza talebi başarıyla kapatıldı!")
                                        else:
                                            st.warning("⏳ Arıza talebi kapatma işlemi beklemede veya başarısız.")
                                
                                # Arıza taleplerim görsel gösterimi
                                elif tool.get("arac_adi") == "get_users_tickets":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("📋 Arıza Taleplerim")
                                        
                                        # Özet bilgiler
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Toplam Talep", sonuc.get('total_count', 0))
                                        with col2:
                                            st.metric("Açık Talepler", sonuc.get('open_count', 0))
                                        with col3:
                                            st.metric("Kapalı Talepler", sonuc.get('closed_count', 0))
                                        
                                        # Talep listesi
                                        tickets = sonuc.get('tickets', [])
                                        if tickets:
                                            st.subheader("📝 Talep Detayları")
                                            for ticket in tickets:
                                                with st.expander(f"🎫 {ticket.get('ticket_id', 'N/A')} - {ticket.get('subject', 'N/A')}"):
                                                    col1, col2 = st.columns(2)
                                                    with col1:
                                                        st.info(f"**Durum:** {ticket.get('status', 'N/A')}")
                                                        st.info(f"**Kategori:** {ticket.get('category', 'N/A')}")
                                                        st.info(f"**Öncelik:** {ticket.get('priority', 'N/A')}")
                                                    with col2:
                                                        st.info(f"**Oluşturulma:** {ticket.get('created_date', 'N/A')}")
                                                        st.info(f"**Atanan:** {ticket.get('assigned_to', 'N/A')}")
                                                        if ticket.get('closed_date'):
                                                            st.info(f"**Kapatılma:** {ticket.get('closed_date', 'N/A')}")
                                                        if ticket.get('resolution'):
                                                            st.info(f"**Çözüm:** {ticket.get('resolution', 'N/A')}")
                                        
                                        # Durum mesajı
                                        if tickets:
                                            st.success("📋 Arıza talepleriniz başarıyla getirildi.")
                                        else:
                                            st.info("📝 Henüz arıza talebiniz bulunmuyor.")
                                
                                # Kullanıcı bilgisi görsel gösterimi
                                elif tool.get("arac_adi") == "get_user_by_id":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("👤 Kullanıcı Bilgileri")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                            st.metric("Ad Soyad", sonuc.get('name', 'N/A'))
                                            st.metric("E-posta", sonuc.get('email', 'N/A'))
                                        with col2:
                                            st.metric("Telefon", sonuc.get('phone', 'N/A'))
                                            st.metric("Durum", sonuc.get('status', 'N/A'))
                                            st.metric("Kayıt Tarihi", sonuc.get('registration_date', 'N/A'))
                                        
                                        # Kullanıcı detayları
                                        st.subheader("📋 Kullanıcı Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Kullanıcı Seviyesi:** {sonuc.get('customer_tier', 'N/A')}")
                                            st.info(f"**Son Giriş:** {sonuc.get('last_login', 'N/A')}")
                                        with col2:
                                            st.info(f"**Aktif Hizmetler:** {sonuc.get('active_services', 'N/A')}")
                                            st.info(f"**Hesap Durumu:** {sonuc.get('account_status', 'N/A')}")
                                        
                                        # Adres bilgisi
                                        if sonuc.get('address'):
                                            st.subheader("📍 Adres Bilgisi")
                                            st.info(f"**Adres:** {sonuc.get('address', 'N/A')}")
                                        
                                        # Başarı mesajı
                                        st.success("👤 Kullanıcı bilgileri başarıyla getirildi.")
                                
                                # Mevcut kullanıcı görsel gösterimi
                                elif tool.get("arac_adi") == "get_current_user":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("👤 Mevcut Kullanıcı Bilgileri")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                            st.metric("Ad Soyad", sonuc.get('name', 'N/A'))
                                            st.metric("E-posta", sonuc.get('email', 'N/A'))
                                        with col2:
                                            st.metric("Telefon", sonuc.get('phone', 'N/A'))
                                            st.metric("Durum", sonuc.get('status', 'N/A'))
                                            st.metric("Kayıt Tarihi", sonuc.get('registration_date', 'N/A'))
                                        
                                        # Kullanıcı detayları
                                        st.subheader("📋 Kullanıcı Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Kullanıcı Seviyesi:** {sonuc.get('customer_tier', 'N/A')}")
                                            st.info(f"**Son Giriş:** {sonuc.get('last_login', 'N/A')}")
                                        with col2:
                                            st.info(f"**Aktif Hizmetler:** {sonuc.get('active_services', 'N/A')}")
                                            st.info(f"**Hesap Durumu:** {sonuc.get('account_status', 'N/A')}")
                                        
                                        # Başarı mesajı
                                        st.success("👤 Kullanıcı bilgileriniz başarıyla getirildi.")
                                
                                # AI model bilgisi görsel gösterimi
                                elif tool.get("arac_adi") == "get_ai_model_info":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🤖 AI Model Bilgileri")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Model Türü", sonuc.get('model_type', 'N/A'))
                                            st.metric("Model Adı", sonuc.get('model_name', 'N/A'))
                                        with col2:
                                            mock_mode = sonuc.get('is_mock_mode', False)
                                            if mock_mode:
                                                st.warning("⚠️ Mock Mod")
                                            else:
                                                st.success("✅ Gerçek AI Mod")
                                            real_ai_mode = sonuc.get('is_real_ai_mode', False)
                                            if real_ai_mode:
                                                st.success("✅ Gerçek AI Aktif")
                                            else:
                                                st.warning("⚠️ Gerçek AI Pasif")
                                        
                                        # Model detayları
                                        st.subheader("📋 Model Detayları")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.info(f"**Son Güncelleme:** {sonuc.get('last_updated', 'N/A')}")
                                        with col2:
                                            st.info(f"**Model Versiyonu:** {sonuc.get('model_version', 'N/A')}")
                                        
                                        # Durum mesajı
                                        if sonuc.get('is_real_ai_mode'):
                                            st.success("🎉 AI model bilgileri başarıyla getirildi. Gerçek AI modu aktif!")
                                        else:
                                            st.info("ℹ️ AI model bilgileri getirildi. Mock mod kullanılıyor.")
                                
                                # Telekom giriş görsel gösterimi
                                elif tool.get("arac_adi") == "telekom_login":
                                    sonuc = tool.get("sonuc", {})
                                    
                                    if sonuc and isinstance(sonuc, dict):
                                        st.subheader("🔐 Telekom Giriş Sonucu")
                                        
                                        # Giriş durumu
                                        success = sonuc.get('success', False)
                                        if success:
                                            st.success("✅ Giriş Başarılı")
                                        else:
                                            st.error("❌ Giriş Başarısız")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Kullanıcı ID", sonuc.get('user_id', 'N/A'))
                                            st.metric("Ad Soyad", sonuc.get('name', 'N/A'))
                                        with col2:
                                            st.metric("E-posta", sonuc.get('email', 'N/A'))
                                            st.metric("Durum", sonuc.get('status', 'N/A'))
                                        
                                        # Session bilgileri
                                        if success:
                                            st.subheader("🔑 Session Bilgileri")
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.info(f"**Session Token:** {sonuc.get('session_token', 'N/A')[:20]}...")
                                            with col2:
                                                st.info(f"**Token Geçerlilik:** {sonuc.get('token_expiry', 'N/A')}")
                                        
                                        # Mesaj
                                        message = sonuc.get('message', '')
                                        if message:
                                            st.info(f"**Mesaj:** {message}")
                                        
                                        # Başarı/hata mesajı
                                        if success:
                                            st.success("🎉 Telekom giriş işlemi başarıyla tamamlandı!")
                                        else:
                                            st.error("❌ Telekom giriş işlemi başarısız oldu.")
    
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