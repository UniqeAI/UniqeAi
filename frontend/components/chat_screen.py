import streamlit as st
import time
import datetime
import random

# Demo yanıtlar - app.py'den alınmış
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

def get_ai_response(user_message):
    """Basit AI yanıtı simülasyonu"""
    time.sleep(1)  # Gerçekçi yanıt süre simülasyonu
    return random.choice(DEMO_RESPONSES)

def render_chat_screen():
    # CSS stilleri
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    .chat-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5em 2em;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .chat-title {
        font-size: 1.8em;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 0.3em;
    }
    
    .chat-subtitle {
        font-size: 0.95em;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .chat-messages {
        flex: 1;
        padding: 2em;
        max-width: 800px;
        margin: 0 auto;
        width: 100%;
        overflow-y: auto;
    }
    
    .message-bubble {
        margin-bottom: 1.5em;
        animation: slideInUp 0.3s ease;
        max-width: 70%;
    }
    
    .message-bubble.user {
        margin-left: auto;
        text-align: right;
    }
    
    .message-bubble.ai {
        margin-right: auto;
        text-align: left;
    }
    
    .message-content {
        padding: 1.2em 1.5em;
        border-radius: 1.2em;
        font-size: 1em;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .message-content.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 0.3em;
    }
    
    .message-content.ai {
        background: white;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 0.3em;
    }
    
    .message-time {
        font-size: 0.8em;
        color: #94a3b8;
        margin-top: 0.5em;
        font-weight: 500;
    }
    
    .message-avatar {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        margin-bottom: 0.5em;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2em;
        font-weight: 600;
    }
    
    .message-avatar.user {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        margin-left: auto;
    }
    
    .message-avatar.ai {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-right: auto;
    }
    
    .chat-input-container {
        background: white;
        padding: 1.5em 2em;
        border-top: 1px solid #e2e8f0;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.1);
        position: sticky;
        bottom: 0;
    }
    
    .chat-input-wrapper {
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        gap: 1em;
        align-items: center;
    }
    
    .chat-input {
        flex: 1;
        padding: 1em 1.5em;
        border: 2px solid #e2e8f0;
        border-radius: 1.5em;
        font-size: 1em;
        background: #f8fafc;
        color: #1e293b;
        transition: all 0.3s ease;
    }
    
    .chat-input:focus {
        outline: none;
        border-color: #667eea;
        background: white;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
    }
    
    .chat-input::placeholder {
        color: #94a3b8;
    }
    
    .send-button {
        padding: 1em 1.5em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 1.5em;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        min-width: 80px;
    }
    
    .send-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
    
    .send-button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
    
    .typing-indicator {
        padding: 1em 1.5em;
        background: #f1f5f9;
        border-radius: 1.2em;
        border-bottom-left-radius: 0.3em;
        color: #64748b;
        font-style: italic;
        margin-bottom: 1.5em;
        max-width: 70%;
        animation: pulse 1.5s infinite;
    }
    
    .quick-replies {
        padding: 1em 2em;
        background: #f8fafc;
        border-top: 1px solid #e2e8f0;
    }
    
    .quick-replies-title {
        font-size: 0.9em;
        color: #64748b;
        margin-bottom: 0.8em;
        font-weight: 600;
    }
    
    .quick-reply-buttons {
        display: flex;
        gap: 0.8em;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .quick-reply-button {
        padding: 0.8em 1.2em;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 1.5em;
        cursor: pointer;
        font-size: 0.9em;
        color: #64748b;
        transition: all 0.3s ease;
    }
    
    .quick-reply-button:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    @media (max-width: 768px) {
        .chat-messages {
            padding: 1em;
        }
        .message-bubble {
            max-width: 85%;
        }
        .chat-input-wrapper {
            flex-direction: column;
            gap: 0.8em;
        }
        .chat-input {
            width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Sohbet mesajları için session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Merhaba! CayrosAi'ya hoş geldiniz. Size nasıl yardımcı olabilirim?", "timestamp": datetime.datetime.now()}
        ]

    # Ana container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat header
    st.markdown("""
    <div class="chat-header">
        <div class="chat-title">💬 CayrosAi</div>
        <div class="chat-subtitle">Akıllı Telekom Asistanı</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        timestamp = message["timestamp"].strftime("%H:%M")
        
        if role == "user":
            st.markdown(f"""
            <div class="message-bubble user">
                <div class="message-avatar user">👤</div>
                <div class="message-content user">{content}</div>
                <div class="message-time">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-bubble ai">
                <div class="message-avatar ai">🤖</div>
                <div class="message-content ai">{content}</div>
                <div class="message-time">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Typing indicator
    if st.session_state.get("typing", False):
        st.markdown("""
        <div class="typing-indicator">
            CayrosAi yazıyor...
        </div>
        """, unsafe_allow_html=True)
    
    # Quick replies
    st.markdown("""
    <div class="quick-replies">
        <div class="quick-replies-title">💡 Hızlı sorular:</div>
        <div class="quick-reply-buttons">
            <button class="quick-reply-button" onclick="sendQuickReply('Fatura bilgimi öğrenebilir miyim?')">💰 Fatura Bilgisi</button>
            <button class="quick-reply-button" onclick="sendQuickReply('Paket değişikliği yapmak istiyorum')">📦 Paket Değişikliği</button>
            <button class="quick-reply-button" onclick="sendQuickReply('Teknik destek almak istiyorum')">🔧 Teknik Destek</button>
            <button class="quick-reply-button" onclick="sendQuickReply('Kampanya bilgilerini öğrenebilir miyim?')">🎁 Kampanyalar</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input("", placeholder="Mesajınızı yazın...", key="user_input", label_visibility="collapsed")
        
        with col2:
            send_button = st.form_submit_button("Gönder", use_container_width=True)
        
        if send_button and user_input:
            # Kullanıcı mesajını ekle
            st.session_state.messages.append({
                "role": "user", 
                "content": user_input,
                "timestamp": datetime.datetime.now()
            })
            
            # Typing indicator'ı göster
            st.session_state.typing = True
            st.rerun()
    
    # AI yanıtı oluştur
    if st.session_state.get("typing", False):
        with st.spinner(""):
            ai_response = get_ai_response(st.session_state.messages[-1]["content"])
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.datetime.now()
            })
            st.session_state.typing = False
            st.rerun()
    
    # Geri dön butonu
    if st.button("← Ana Sayfa", key="back_to_main"):
        st.session_state["current_screen"] = "main"
        st.rerun() 