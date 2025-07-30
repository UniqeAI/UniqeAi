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