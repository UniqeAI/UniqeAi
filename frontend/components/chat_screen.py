import streamlit as st
import time
import datetime
import requests
import json
from typing import Dict, Any, Optional

# API konfigürasyonu
API_BASE_URL = "http://localhost:8000"  # Backend API URL
API_TIMEOUT = 30  # Saniye
MAX_RETRIES = 3

def get_tool_result(tool_name, user_id=None):
    if tool_name == "kullanıcı":
        user = {"name": "Ahmet Yılmaz", "email": "ahmet.yilmaz@email.com", "phone": "+90 532 123 4567", "package": "Premium Fiber", "status": "Aktif"}
        card = f"""
        <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); color:#000; border-radius:1em; padding:1.5em; margin-top:0.5em; box-shadow:0 4px 12px rgba(220,53,69,0.2); border: 2px solid #dc3545;'>
            <h4 style='color: #dc3545; margin-bottom: 1em; display: flex; align-items: center;'>
                <span style='background: #dc3545; color: white; padding: 0.3em 0.6em; border-radius: 50%; margin-right: 0.5em; font-size: 0.8em;'>👤</span>
                Kullanıcı Bilgileri
            </h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1em;'>
                <div style='background: rgba(220,53,69,0.1); padding: 0.8em; border-radius: 0.5em;'><b>👤 Ad:</b> {user['name']}</div>
                <div style='background: rgba(13,110,253,0.1); padding: 0.8em; border-radius: 0.5em;'><b>📧 E-posta:</b> {user['email']}</div>
                <div style='background: rgba(25,135,84,0.1); padding: 0.8em; border-radius: 0.5em;'><b>📞 Telefon:</b> {user['phone']}</div>
                <div style='background: rgba(255,193,7,0.1); padding: 0.8em; border-radius: 0.5em;'><b>📦 Paket:</b> {user['package']}</div>
            </div>
            <div style='margin-top: 1em; padding: 0.8em; background: linear-gradient(90deg, #198754, #20c997); border-radius: 0.5em; text-align: center; color: white; font-weight: bold;'>
                ✅ Durum: {user['status']}
            </div>
        </div>
        """
        return card
    elif tool_name == "fatura":
        card = f"""
        <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); color:#000; border-radius:1em; padding:1.5em; margin-top:0.5em; box-shadow:0 4px 12px rgba(13,110,253,0.2); border: 2px solid #0d6efd;'>
            <h4 style='color: #0d6efd; margin-bottom: 1em; display: flex; align-items: center;'>
                <span style='background: #0d6efd; color: white; padding: 0.3em 0.6em; border-radius: 50%; margin-right: 0.5em; font-size: 0.8em;'>💰</span>
                Fatura Bilgileri
            </h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1em;'>
                <div style='background: rgba(220,53,69,0.1); padding: 0.8em; border-radius: 0.5em;'><b>💳 Tutar:</b> 350 TL</div>
                <div style='background: rgba(13,110,253,0.1); padding: 0.8em; border-radius: 0.5em;'><b>📅 Son Ödeme:</b> 15 Mayıs 2024</div>
                <div style='background: rgba(25,135,84,0.1); padding: 0.8em; border-radius: 0.5em;'><b>📊 Dönem:</b> Nisan 2024</div>
                <div style='background: rgba(255,193,7,0.1); padding: 0.8em; border-radius: 0.5em;'><b>💳 Ödeme:</b> Bekliyor</div>
            </div>
        </div>
        """
        return card
    elif tool_name == "paket":
        card = f"""
        <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); color:#000; border-radius:1em; padding:1.5em; margin-top:0.5em; box-shadow:0 4px 12px rgba(25,135,84,0.2); border: 2px solid #198754;'>
            <h4 style='color: #198754; margin-bottom: 1em; display: flex; align-items: center;'>
                <span style='background: #198754; color: white; padding: 0.3em 0.6em; border-radius: 50%; margin-right: 0.5em; font-size: 0.8em;'>📦</span>
                Paket Detayları
            </h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1em;'>
                <div style='background: rgba(220,53,69,0.1); padding: 0.8em; border-radius: 0.5em;'><b>📱 Paket:</b> Premium Fiber</div>
                <div style='background: rgba(13,110,253,0.1); padding: 0.8em; border-radius: 0.5em;'><b>🌐 Hız:</b> 100 Mbps</div>
                <div style='background: rgba(25,135,84,0.1); padding: 0.8em; border-radius: 0.5em;'><b>📺 TV:</b> 200+ Kanal</div>
                <div style='background: rgba(255,193,7,0.1); padding: 0.8em; border-radius: 0.5em;'><b>💰 Fiyat:</b> 299 TL/ay</div>
            </div>
        </div>
        """
        return card
    return "<i>Beklenmeyen araç sonucu.</i>"

def get_bot_reply(user_message):
    msg = user_message.lower()
    
    # Backend bağlantısını kontrol et
    backend_available = check_backend_health()
    
    if backend_available and not st.session_state.get("demo_mode", True):
        # Gerçek API kullan
        api_response = retry_api_call(send_message_to_backend, user_message)
        if api_response:
            return api_response
        else:
            # API başarısız olursa demo moduna geç
            st.session_state["demo_mode"] = True
            st.warning("⚠️ API bağlantısı başarısız, demo moduna geçildi.")
    
    # Demo modu için rastgele yanıtlar
    import random
    demo_responses = [
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
    
    if "kullanıcı" in msg or "bilgim" in msg:
        return {"type": "tool_call", "tool": "kullanıcı", "text": "👤 Kullanıcı bilgisi aracı çağrılıyor..."}
    elif "fatura" in msg:
        return {"type": "text", "text": (
            "💰 Tabii, hemen fatura bilgilerinizi paylaşıyorum!\n\n"
            "📄 Son fatura tutarınız: **350 TL**\n"
            "📅 Son ödeme tarihi: **15 Mayıs 2024**\n"
            "💳 Ödeme yöntemleri: Kredi kartı, banka kartı, havale\n\n"
            "Dilerseniz detaylı fatura dökümünü de iletebilirim. Başka bir isteğiniz var mı?"
        )}
    elif "teknik destek" in msg or "arıza" in msg or "internet yok" in msg:
        return {"type": "text", "text": (
            "🔧 Teknik destek için buradayım!\n\n"
            "🛠️ Yaşadığınız sorunu biraz daha detaylandırabilir misiniz?\n"
            "📞 Gerekirse teknik ekibimize yönlendirebilirim.\n"
            "⏰ Destek saatleri: 7/24\n\n"
            "Hangi konuda yardıma ihtiyacınız var?"
        )}
    elif "kampanya" in msg or "indirim" in msg:
        return {"type": "text", "text": (
            "🎉 Size özel güncel kampanyalarımız var!\n\n"
            "📱 **10GB hediye internet** (3 ay boyunca)\n"
            "👨‍👩‍👧‍👦 **Aile paketlerinde %20 indirim**\n"
            "🎁 **Yeni abonelere 1 ay ücretsiz**\n"
            "📺 **TV+ paketi ile %15 indirim**\n\n"
            "Daha fazla kampanya bilgisi için 'daha fazla kampanya' yazabilirsiniz."
        )}
    elif "borç" in msg:
        return {"type": "text", "text": (
            "💳 Güncel borcunuz: **350 TL**\n\n"
            "📱 Ödeme yapmak için:\n"
            "• Mobil uygulamamızı kullanabilirsiniz\n"
            "• Online işlemler merkezimizi ziyaret edebilirsiniz\n"
            "• Banka şubelerinden ödeme yapabilirsiniz\n\n"
            "Hangi yöntemi tercih edersiniz?"
        )}
    elif "demo" in msg or "test" in msg:
        return {"type": "text", "text": (
            "🚀 **DEMO MODE** - Bu bir demo uygulamasıdır!\n\n"
            "🎯 Demo özellikleri:\n"
            "• 💬 Gerçek zamanlı chat\n"
            "• 🔧 Araç çağrıları\n"
            "• 📊 Veri görselleştirme\n"
            "• 🎨 Modern UI/UX\n"
            "• 🔌 API bağlantısı (backend hazır olduğunda)\n\n"
            "Gerçek uygulamada daha gelişmiş özellikler olacaktır."
        )}
    else:
        # Demo modu için rastgele yanıt
        return {"type": "text", "text": random.choice(demo_responses)}

def handle_send_message():
    user_input = st.session_state["chat_input"].strip()
    if user_input != "":
        st.session_state["chat_history"].append({
            "user": st.session_state.get("login_username", "Kullanıcı"),
            "text": user_input,
            "timestamp": datetime.datetime.now().strftime("%H:%M")
        })
        st.session_state["is_bot_typing"] = True
        st.rerun()
    
    # Bot cevabı ayrı bir adımda işlenecek

def process_bot_reply():
    if st.session_state.get("is_bot_typing", False):
        user_message = st.session_state["chat_history"][-1]["text"]
        with st.spinner("UniqeAi yazıyor..."):
            time.sleep(1.1)
        bot_reply = get_bot_reply(user_message)
        if isinstance(bot_reply, dict) and bot_reply.get("type") == "tool_call":
            # Önce araç çağrılıyor mesajı göster
            st.session_state["chat_history"].append({
                "user": "UniqeAi",
                "text": f"<b>{bot_reply['text']}</b>",
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "is_html": True
            })
            st.session_state["chat_input"] = ""
            st.session_state["is_bot_typing"] = False
            st.session_state["pending_tool_result"] = bot_reply["tool"]
            st.rerun()
        elif "pending_tool_result" in st.session_state:
            # Araç sonucu göster
            tool_name = st.session_state.pop("pending_tool_result")
            tool_result_html = get_tool_result(tool_name)
            st.session_state["chat_history"].append({
                "user": "UniqeAi",
                "text": tool_result_html,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "is_html": True
            })
            st.session_state["chat_input"] = ""
            st.session_state["is_bot_typing"] = False
            st.rerun()
        else:
            # Normal metin cevabı
            st.session_state["chat_history"].append({
                "user": "UniqeAi",
                "text": bot_reply["text"] if isinstance(bot_reply, dict) else bot_reply,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "is_html": False
            })
            st.session_state["chat_input"] = ""
            st.session_state["is_bot_typing"] = False
            st.rerun()

def render_chat_screen():
    # Bağlantı durumu (örnek, gerçek ping ile değiştirilebilir)
    connection_status = "Aktif"
    connection_color = "#198754" if connection_status == "Aktif" else "#dc3545"
    st.markdown(f"""
    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5em; margin-top: 0.5em;'>
        <div style='display: flex; align-items: center;'>
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712037.png" alt="robot" width="50" style="margin-right: 15px; filter: drop-shadow(0 4px 8px rgba(220,53,69,0.4)) hue-rotate(240deg) brightness(0.7) contrast(1.3) saturate(1.5); transition: transform 0.3s ease;"/>
            <span style="font-size: 2.5em; font-weight: bold; background: linear-gradient(45deg, #dc3545, #0d6efd, #198754); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-fill-color: transparent;">UniqeAi</span>
        </div>
        <div style='font-size: 1.1em; font-weight: 500; color: {connection_color}; display: flex; align-items: center;'>
            <span style='width: 8px; height: 8px; background: {connection_color}; border-radius: 50%; margin-right: 8px; animation: pulse 2s infinite;'></span>
            Bağlantı: {connection_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "chat_input" not in st.session_state:
        st.session_state["chat_input"] = ""
    if "is_bot_typing" not in st.session_state:
        st.session_state["is_bot_typing"] = False

    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #e8f4fd 0%, #f8f9fa 100%);
        min-height: 100vh;
        padding: 1.5em;
    }
    .chat-bubble {
        max-width: 85vw;
        padding: 1.2em 1.8em;
        border-radius: 2em;
        margin-bottom: 1em;
        font-size: 1.25em;
        word-break: break-word;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(220,53,69,0.15);
        position: relative;
        transition: all 0.3s ease;
        line-height: 1.4;
        animation: fadeInUp 0.5s ease;
        font-weight: 600;
    }
    .bubble-user {
        background: linear-gradient(90deg, #dc3545 0%, #0d6efd 100%);
        color: #fff;
        align-self: flex-end;
        margin-left: 15vw;
        transform: scale(1.02);
        font-weight: 700;
    }
    .bubble-bot {
        background: #ffffff;
        color: #000000;
        align-self: flex-start;
        margin-right: 15vw;
        border: 2px solid #dc3545;
        border-bottom-left-radius: 2em;
        border-bottom-right-radius: 2em;
        border-top-left-radius: 2em;
        border-top-right-radius: 2em;
        transform: scale(1.02);
        font-weight: 600;
        text-shadow: none;
    }
    .bubble-meta {
        font-size: 0.9em;
        color: #000000;
        margin-top: 0.3em;
        margin-left: 0.8em;
        margin-right: 0.8em;
        text-align: right;
        font-weight: 700;
    }
    @media (max-width: 600px) {
        .chat-bubble { 
            max-width: 95vw; 
            padding: 1em 1.5em;
            font-size: 1.15em;
        }
        .bubble-user { margin-left: 2vw; }
        .bubble-bot { margin-right: 2vw; }
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        border-left: 5px solid #dc3545;
        padding: 1em 1.2em;
        border-radius: 0.8em;
        margin-bottom: 1.2em;
        font-size: 1.1em;
        font-weight: 600;
    }
    .chat-container {
        padding: 1em;
        margin: 1em 0;
        border-radius: 1.5em;
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }
    @keyframes fadeInUp {
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
        50% { opacity: 0.5; }
    }
    .typing-indicator {
        animation: bounce 1.4s infinite ease-in-out;
    }
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0.8); }
        40% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

    chat_area = ""
    for msg in st.session_state["chat_history"]:
        is_user = msg["user"] != "UniqeAi"
        bubble_class = "bubble-user" if is_user else "bubble-bot"
        align = "right" if is_user else "left"
        msg_text_html = msg['text'] if msg.get('is_html') else msg['text'].replace('\n', '<br/>')
        # Araç sonucu ise bubble-meta eklenmesin
        show_meta = not (msg.get('is_html') and (msg['text'].strip().startswith('<table') or msg['text'].strip().startswith('<div')))
        chat_area += f"""
        <div style='display: flex; flex-direction: column; align-items: {align};'>
            <div class='chat-bubble {bubble_class}'>
                {msg_text_html}
                {f"<div class='bubble-meta'>{msg['user']} • {msg['timestamp']}</div>" if show_meta else ''}
            </div>
        </div>
        """
    st.markdown(chat_area, unsafe_allow_html=True)

    # Yazıyor göstergesi
    if st.session_state.get("is_bot_typing", False):
        st.markdown("""
        <div style='display: flex; align-items: center; margin: 0.5em 0 1em 0;'>
            <div class='chat-bubble bubble-bot' style='opacity:0.8;'>
                <span>🤖 UniqeAi yazıyor <span class='dot-anim typing-indicator'>●●●</span></span>
            </div>
        </div>
        <style>
        .dot-anim { letter-spacing: 0.2em; animation: dots 1.2s steps(3, end) infinite; }
        @keyframes dots { 0%, 20% { color: #2196f3; } 40% { color: #000; } 60%, 100% { color: #2196f3; } }
        </style>
        """, unsafe_allow_html=True)
        process_bot_reply()

    st.text_input(
        "Mesaj",
        value=st.session_state["chat_input"],
        key="chat_input",
        on_change=handle_send_message,
        placeholder="Mesajınızı yazın...",
        label_visibility="collapsed"
    )
    # Kısa yol cümleleri - Gelişmiş demo senaryoları
    shortcut_sentences = [
        "💰 Fatura bilgimi öğrenmek istiyorum",
        "🎉 Kampanyalar hakkında bilgi almak istiyorum",
        "📦 Paket detaylarımı görmek istiyorum",
        "🔧 Teknik destek almak istiyorum",
        "👤 Kullanıcı bilgilerimi göster",
        "💳 Borç durumumu öğrenmek istiyorum",
        "📱 Yeni paket teklifleri almak istiyorum",
        "🛠️ Arıza bildirimi yapmak istiyorum"
    ]
    
    st.markdown("<div style='height: 1em;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); border-radius: 1em; padding: 1.5em; margin: 1em 0;'>
        <h4 style='color: #dc3545; margin-bottom: 1em; text-align: center;'>🚀 Hızlı Erişim Menüsü</h4>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1em;'>
    """, unsafe_allow_html=True)
    
    for idx, sentence in enumerate(shortcut_sentences):
        if st.button(sentence, key=f'shortcut_{idx}', help=sentence, use_container_width=True):
            st.session_state["chat_history"].append({
                "user": st.session_state.get("login_username", "Kullanıcı"),
                "text": sentence,
                "timestamp": datetime.datetime.now().strftime("%H:%M")
            })
            st.session_state["is_bot_typing"] = True
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Hata mesajı örneği (kullanıcıya özel hata durumu varsa göster)
    if st.session_state.get("chat_error"):
        st.markdown(f"<div class='error-message'>{st.session_state['chat_error']}</div>", unsafe_allow_html=True)
    
    # Demo test butonu
    st.markdown("<div style='height: 2em;'></div>", unsafe_allow_html=True)
    show_test_results()

def send_message_to_backend(message: str, user_id: str = None) -> Optional[Dict[str, Any]]:
    """
    Arka yüze mesaj gönder ve yanıt al
    """
    try:
        payload = {
            "message": message,
            "user_id": user_id or st.session_state.get("user_id", "demo_user"),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.session_state.get('auth_token', 'demo_token')}"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/chat",
            json=payload,
            headers=headers,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Hatası: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏰ API yanıt vermedi. Lütfen tekrar deneyin.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Sunucuya bağlanılamıyor. Demo modunda çalışıyoruz.")
        return None
    except Exception as e:
        st.error(f"❌ Beklenmeyen hata: {str(e)}")
        return None

def retry_api_call(func, *args, **kwargs):
    """
    API çağrısını yeniden deneme mantığı
    """
    for attempt in range(MAX_RETRIES):
        try:
            result = func(*args, **kwargs)
            if result is not None:
                return result
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                st.error(f"❌ {MAX_RETRIES} deneme sonrası başarısız: {str(e)}")
                return None
            else:
                st.warning(f"⚠️ Deneme {attempt + 1}/{MAX_RETRIES} başarısız, yeniden deneniyor...")
                time.sleep(2 ** attempt)  # Exponential backoff
    return None

def check_backend_health() -> bool:
    """
    Backend sağlık kontrolü
    """
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_demo_tests():
    """
    Demo senaryolarının otomatik testleri
    """
    test_scenarios = [
        {
            "name": "Kullanıcı Bilgisi Testi",
            "input": "kullanıcı bilgilerimi göster",
            "expected_tool": "kullanıcı"
        },
        {
            "name": "Fatura Bilgisi Testi", 
            "input": "fatura bilgimi öğrenmek istiyorum",
            "expected_type": "text"
        },
        {
            "name": "Teknik Destek Testi",
            "input": "teknik destek almak istiyorum", 
            "expected_type": "text"
        },
        {
            "name": "Kampanya Testi",
            "input": "kampanyalar hakkında bilgi almak istiyorum",
            "expected_type": "text"
        }
    ]
    
    results = []
    for scenario in test_scenarios:
        try:
            response = get_bot_reply(scenario["input"])
            if "expected_tool" in scenario:
                success = response.get("type") == "tool_call" and response.get("tool") == scenario["expected_tool"]
            else:
                success = response.get("type") == scenario["expected_type"]
            
            results.append({
                "scenario": scenario["name"],
                "success": success,
                "response": response
            })
        except Exception as e:
            results.append({
                "scenario": scenario["name"], 
                "success": False,
                "error": str(e)
            })
    
    return results

def show_test_results():
    """
    Test sonuçlarını göster
    """
    if st.button("🧪 Demo Testlerini Çalıştır", key="run_tests"):
        with st.spinner("Testler çalıştırılıyor..."):
            results = run_demo_tests()
        
        st.markdown("### 📊 Test Sonuçları")
        
        for result in results:
            if result["success"]:
                st.success(f"✅ {result['scenario']} - BAŞARILI")
            else:
                st.error(f"❌ {result['scenario']} - BAŞARISIZ")
                if "error" in result:
                    st.error(f"Hata: {result['error']}")
        
        success_count = sum(1 for r in results if r["success"])
        total_count = len(results)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    border-radius: 1em; padding: 1.5em; margin: 1em 0; 
                    border: 2px solid #198754;'>
            <h4 style='color: #198754; margin-bottom: 1em;'>📈 Test Özeti</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1em;'>
                <div style='background: rgba(25,135,84,0.1); padding: 0.8em; border-radius: 0.5em;'>
                    <b>✅ Başarılı:</b> {success_count}
                </div>
                <div style='background: rgba(220,53,69,0.1); padding: 0.8em; border-radius: 0.5em;'>
                    <b>❌ Başarısız:</b> {total_count - success_count}
                </div>
            </div>
            <div style='margin-top: 1em; padding: 0.8em; background: linear-gradient(90deg, #198754, #20c997); 
                        border-radius: 0.5em; text-align: center; color: white; font-weight: bold;'>
                🎯 Başarı Oranı: %{(success_count/total_count*100):.1f}
            </div>
        </div>
        """, unsafe_allow_html=True) 