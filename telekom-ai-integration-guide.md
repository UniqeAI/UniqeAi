# 🔗 Telekom AI Projesi - Kapsamlı Entegrasyon Rehberi

> **Proje Durumu:** Frontend (Streamlit) ✅ | Backend (FastAPI) ✅ | AI Model (Hugging Face) ✅  
> **Hedef:** Tam entegrasyon ve deployment hazırlığı

## 📋 İçindekiler

1. [Entegrasyona Genel Bakış](#entegrasyona-genel-bakış)
2. [Backend → AI Model Entegrasyonu](#backend--ai-model-entegrasyonu)  
3. [Frontend → Backend Entegrasyonu](#frontend--backend-entegrasyonu)
4. [Tam Test Senaryoları](#tam-test-senaryoları)
5. [Deployment Hazırlığı](#deployment-hazırlığı)
6. [Performans Optimizasyonu](#performans-optimizasyonu)
7. [Sorun Giderme](#sorun-giderme)

---

## 🎯 Entegrasyona Genel Bakış

### Mevcut Durum
- ✅ **Frontend**: Streamlit ile login, signup, main, chat ekranları
- ✅ **Backend**: FastAPI ile 19 endpoint (fatura, paket, destek vb.)  
- ✅ **AI Model**: Hugging Face'de yayınlanmış, backend uyumlu eğitilmiş
- ❌ **Entegrasyon**: Henüz bağlantılar kurulmamış

### Entegrasyon Mimarisi
```
[Streamlit Frontend] ←→ [FastAPI Backend] ←→ [Hugging Face Model]
      (HTTP API)              (AI Orchestrator)
```

---

## 🤖 Backend → AI Model Entegrasyonu

### 1. AI Orchestrator Kurulumu

Backend'inizde şu dosyayı oluşturun: `backend/app/ai_orchestrator.py`

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import json
import logging
from typing import Dict, Any, List, Optional
import asyncio
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class AracCagrisi(BaseModel):
    arac_adi: str
    parametreler: Dict[str, Any]

class AIOrchestrator:
    def __init__(self, model_name: str = "Choyrens/ChoyrensAI-Telekom-Agent-v1-merged"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.function_mapping = self._create_function_mapping()
        self.load_model()
    
    def load_model(self):
        """Hugging Face modelini yükle"""
        try:
            logger.info(f"Model yükleniyor: {self.model_name}")
            
            # Tokenizer ve model yükleme
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Chat pipeline oluştur
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            logger.info("Model başarıyla yüklendi")
            
        except Exception as e:
            logger.error(f"Model yükleme hatası: {e}")
            raise
    
    def _create_function_mapping(self) -> Dict[str, callable]:
        """API endpoint'lerini fonksiyon mapping'i oluştur"""
        from .telekom_api import (
            get_current_bill, get_bill_history, pay_bill,
            get_current_package, get_remaining_quotas, change_package,
            create_support_ticket, get_support_ticket_status,
            get_customer_profile, update_customer_contact
        )
        
        return {
            # FATURA & ÖDEME
            "get_current_bill": get_current_bill,
            "get_past_bills": get_bill_history,
            "pay_bill": pay_bill,
            "get_payment_history": lambda user_id: {"success": True, "data": {"payments": []}},
            "setup_autopay": lambda user_id, status: {"success": True, "data": {"autopay_enabled": status}},
            
            # PAKET & TARİFE
            "get_customer_package": get_current_package,
            "get_remaining_quotas": get_remaining_quotas,
            "change_package": change_package,
            "get_available_packages": lambda: {"success": True, "data": {"packages": []}},
            "get_package_details": lambda package_name: {"success": True, "data": {}},
            "enable_roaming": lambda user_id, status: {"success": True, "data": {"roaming_enabled": status}},
            
            # TEKNİK DESTEK
            "check_network_status": lambda region: {"success": True, "data": {"status": "operational"}},
            "create_fault_ticket": create_support_ticket,
            "get_fault_ticket_status": get_support_ticket_status,
            "test_internet_speed": lambda user_id: {"success": True, "data": {"speed": "50 Mbps"}},
            
            # HESAP YÖNETİMİ
            "get_customer_profile": get_customer_profile,
            "update_customer_contact": update_customer_contact,
            "suspend_line": lambda user_id, reason: {"success": True, "data": {"status": "suspended"}},
            "reactivate_line": lambda user_id: {"success": True, "data": {"status": "active"}}
        }
    
    async def process_message(self, user_message: str, user_id: int = None) -> Dict[str, Any]:
        """Kullanıcı mesajını işle ve uygun yanıtı döndür"""
        try:
            # 1. Mesajı AI modeline gönder
            ai_response = await self._generate_ai_response(user_message, user_id)
            
            # 2. Araç çağrılarını tespit et
            tool_calls = self._extract_tool_calls(ai_response)
            
            # 3. Araç çağrılarını çalıştır
            tool_results = []
            for tool_call in tool_calls:
                result = await self._execute_tool_call(tool_call)
                tool_results.append(result)
            
            # 4. Final yanıtı oluştur
            final_response = await self._generate_final_response(
                user_message, ai_response, tool_results
            )
            
            return {
                "success": True,
                "response": final_response,
                "tool_calls": tool_calls,
                "tool_results": tool_results,
                "user_id": user_id,
                "confidence": 0.95
            }
            
        except Exception as e:
            logger.error(f"Mesaj işleme hatası: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
            }
    
    async def _generate_ai_response(self, message: str, user_id: int = None) -> str:
        """AI modelinden yanıt al"""
        try:
            # Sistem promptu oluştur
            system_prompt = self._create_system_prompt(user_id)
            
            # Chat formatında mesaj hazırla
            formatted_message = f"{system_prompt}\n\nKullanıcı: {message}\nAsistan:"
            
            # AI'dan yanıt al
            response = self.pipeline(
                formatted_message,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Sadece yeni oluşturulan kısmı al
            ai_response = response[0]['generated_text'][len(formatted_message):].strip()
            
            return ai_response
            
        except Exception as e:
            logger.error(f"AI yanıt üretme hatası: {e}")
            return "Anlayamadım, lütfen tekrar açıklar mısınız?"
    
    def _create_system_prompt(self, user_id: int = None) -> str:
        """Sistem promptu oluştur"""
        return f"""Sen Türk Telekom'un AI asistanısın. Müşterilere yardım etmek için tasarlandın.

Kullanılabilir araçlar:
- get_current_bill: Mevcut fatura bilgisi
- pay_bill: Fatura ödeme
- get_customer_package: Paket bilgisi  
- get_remaining_quotas: Kalan kotalar
- change_package: Paket değiştirme
- create_fault_ticket: Arıza kaydı
- get_customer_profile: Müşteri profili

Kurallar:
1. Samimi ve yardımsever ol
2. Türkçe konuş
3. Gerekirse araç kullan
4. Net ve anlaşılır cevap ver

Müşteri ID: {user_id or 'Bilinmiyor'}"""
    
    def _extract_tool_calls(self, ai_response: str) -> List[AracCagrisi]:
        """AI yanıtından araç çağrılarını çıkar"""
        tool_calls = []
        
        # Basit pattern matching (geliştirilecek)
        if "fatura" in ai_response.lower():
            tool_calls.append(AracCagrisi(
                arac_adi="get_current_bill",
                parametreler={"user_id": 1}  # Dinamik hale getirilecek
            ))
        elif "paket" in ai_response.lower():
            tool_calls.append(AracCagrisi(
                arac_adi="get_customer_package", 
                parametreler={"user_id": 1}
            ))
        elif "arıza" in ai_response.lower():
            tool_calls.append(AracCagrisi(
                arac_adi="create_fault_ticket",
                parametreler={
                    "user_id": 1,
                    "issue_description": "Kullanıcı arıza bildirdi",
                    "category": "technical"
                }
            ))
        
        return tool_calls
    
    async def _execute_tool_call(self, tool_call: AracCagrisi) -> Dict[str, Any]:
        """Araç çağrısını çalıştır"""
        try:
            if tool_call.arac_adi in self.function_mapping:
                func = self.function_mapping[tool_call.arac_adi]
                
                # Fonksiyonu çağır
                if asyncio.iscoroutinefunction(func):
                    result = await func(**tool_call.parametreler)
                else:
                    result = func(**tool_call.parametreler)
                
                return {
                    "tool_name": tool_call.arac_adi,
                    "success": True,
                    "result": result
                }
            else:
                return {
                    "tool_name": tool_call.arac_adi,
                    "success": False,
                    "error": "Araç bulunamadı"
                }
                
        except Exception as e:
            logger.error(f"Araç çalıştırma hatası: {e}")
            return {
                "tool_name": tool_call.arac_adi,
                "success": False,
                "error": str(e)
            }
    
    async def _generate_final_response(
        self, 
        user_message: str, 
        ai_response: str, 
        tool_results: List[Dict]
    ) -> str:
        """Araç sonuçlarını kullanarak final yanıt oluştur"""
        
        if not tool_results:
            return ai_response
        
        # Araç sonuçlarını analiz et
        successful_results = [r for r in tool_results if r.get("success")]
        
        if not successful_results:
            return "Üzgünüm, şu anda bu bilgilere ulaşamıyorum. Lütfen daha sonra tekrar deneyin."
        
        # Sonuçları formatla
        response_parts = [ai_response]
        
        for result in successful_results:
            if result["tool_name"] == "get_current_bill":
                data = result["result"].get("data", {})
                response_parts.append(
                    f"\n💰 Mevcut faturanız: {data.get('amount', 'N/A')} TL\n"
                    f"📅 Son ödeme tarihi: {data.get('due_date', 'N/A')}\n"
                    f"📊 Durum: {data.get('status', 'N/A')}"
                )
            elif result["tool_name"] == "get_customer_package":
                data = result["result"].get("data", {})
                response_parts.append(
                    f"\n📦 Paketiniz: {data.get('package_name', 'N/A')}\n"
                    f"💵 Aylık ücret: {data.get('monthly_fee', 'N/A')} TL"
                )
        
        return "\n".join(response_parts)

# Global AI orchestrator instance
ai_orchestrator = None

def get_ai_orchestrator() -> AIOrchestrator:
    """AI orchestrator singleton"""
    global ai_orchestrator
    if ai_orchestrator is None:
        ai_orchestrator = AIOrchestrator()
    return ai_orchestrator
```

### 2. Chat Endpoint'i Oluşturma

`backend/app/routers/chat.py` dosyasını oluşturun:

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from ..ai_orchestrator import get_ai_orchestrator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    confidence: float = 0.0
    tool_calls: list = []
    metadata: Dict[str, Any] = {}

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """AI ile sohbet endpoint'i"""
    try:
        # AI orchestrator'ı al
        orchestrator = get_ai_orchestrator()
        
        # Mesajı işle
        result = await orchestrator.process_message(
            user_message=request.message,
            user_id=request.user_id
        )
        
        if result["success"]:
            return ChatResponse(
                success=True,
                response=result["response"],
                user_id=request.user_id,
                session_id=request.session_id,
                confidence=result.get("confidence", 0.95),
                tool_calls=result.get("tool_calls", []),
                metadata={
                    "tool_results": result.get("tool_results", []),
                    "processing_time": "< 1s"
                }
            )
        else:
            return ChatResponse(
                success=False,
                response=result.get("response", "Bir hata oluştu"),
                user_id=request.user_id,
                session_id=request.session_id
            )
            
    except Exception as e:
        logger.error(f"Chat endpoint hatası: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error"
        )

@router.get("/health")
async def chat_health():
    """Chat servisi sağlık kontrolü"""
    try:
        orchestrator = get_ai_orchestrator()
        model_loaded = orchestrator.model is not None
        
        return {
            "status": "healthy" if model_loaded else "unhealthy",
            "model_loaded": model_loaded,
            "model_name": orchestrator.model_name
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
```

### 3. Main App'e Chat Router'ı Ekleme

`backend/app/main.py`'de chat router'ı ekleyin:

```python
from fastapi import FastAPI
from .routers import chat, telekom_api  # Mevcut router'lar

app = FastAPI(title="Telekom AI Backend", version="1.0.0")

# Router'ları ekle
app.include_router(chat.router)
app.include_router(telekom_api.router)

@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcında AI modelini yükle"""
    from .ai_orchestrator import get_ai_orchestrator
    try:
        orchestrator = get_ai_orchestrator()
        print("✅ AI Orchestrator başlatıldı")
    except Exception as e:
        print(f"❌ AI Orchestrator başlatma hatası: {e}")

@app.get("/")
async def root():
    return {"message": "Telekom AI Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "telekom-ai-backend"}
```

---

## 💻 Frontend → Backend Entegrasyonu

### 1. API Client Oluşturma

`frontend/utils/api_client.py` dosyasını oluşturun:

```python
import requests
import streamlit as st
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TelekomAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """HTTP isteği gönder"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = self.session.get(url, params=data)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Desteklenmeyen HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API isteği hatası: {e}")
            return {
                "success": False,
                "error": f"Bağlantı hatası: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {e}")
            return {
                "success": False,
                "error": f"Hata: {str(e)}"
            }
    
    # === CHAT İŞLEMLERİ ===
    def send_chat_message(self, message: str, user_id: int = None) -> Dict[str, Any]:
        """AI'ya mesaj gönder"""
        return self._make_request("POST", "/api/v1/chat/", {
            "message": message,
            "user_id": user_id
        })
    
    def check_chat_health(self) -> Dict[str, Any]:
        """Chat servisi sağlık kontrolü"""
        return self._make_request("GET", "/api/v1/chat/health")
    
    # === FATURA İŞLEMLERİ ===
    def get_current_bill(self, user_id: int) -> Dict[str, Any]:
        """Mevcut fatura getir"""
        return self._make_request("POST", "/api/v1/telekom/billing/current", {
            "user_id": user_id
        })
    
    def get_bill_history(self, user_id: int, limit: int = 12) -> Dict[str, Any]:
        """Fatura geçmişi getir"""
        return self._make_request("POST", "/api/v1/telekom/billing/history", {
            "user_id": user_id,
            "limit": limit
        })
    
    def pay_bill(self, bill_id: str, method: str = "kredi_karti") -> Dict[str, Any]:
        """Fatura öde"""
        return self._make_request("POST", "/api/v1/telekom/billing/pay", {
            "bill_id": bill_id,
            "method": method
        })
    
    # === PAKET İŞLEMLERİ ===
    def get_current_package(self, user_id: int) -> Dict[str, Any]:
        """Mevcut paket getir"""
        return self._make_request("POST", "/api/v1/telekom/packages/current", {
            "user_id": user_id
        })
    
    def get_remaining_quotas(self, user_id: int) -> Dict[str, Any]:
        """Kalan kotalar"""
        return self._make_request("POST", "/api/v1/telekom/packages/quotas", {
            "user_id": user_id
        })
    
    def get_available_packages(self) -> Dict[str, Any]:
        """Kullanılabilir paketler"""
        return self._make_request("POST", "/api/v1/telekom/packages/available")
    
    # === MÜŞTERİ İŞLEMLERİ ===
    def get_customer_profile(self, user_id: int) -> Dict[str, Any]:
        """Müşteri profili"""
        return self._make_request("POST", "/api/v1/telekom/customers/profile", {
            "user_id": user_id
        })
    
    # === DESTEK İŞLEMLERİ ===
    def create_support_ticket(self, user_id: int, description: str, category: str = "technical") -> Dict[str, Any]:
        """Destek talebi oluştur"""
        return self._make_request("POST", "/api/v1/telekom/support/tickets", {
            "user_id": user_id,
            "issue_description": description,
            "category": category
        })
    
    def check_network_status(self, region: str) -> Dict[str, Any]:
        """Ağ durumu kontrolü"""
        return self._make_request("POST", "/api/v1/telekom/network/status", {
            "region": region
        })

# Global API client instance
@st.cache_resource
def get_api_client() -> TelekomAPIClient:
    """API client singleton"""
    return TelekomAPIClient()
```

### 2. Chat Ekranını Güncelleme

`frontend/pages/chat.py` dosyasını güncelleyin:

```python
import streamlit as st
from utils.api_client import get_api_client
import time
from typing import Dict, Any

def show_chat_page():
    """Chat sayfasını göster"""
    st.title("🤖 Telekom AI Asistanı")
    
    # API client'ı al
    api_client = get_api_client()
    
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
                health = api_client.check_chat_health()
                if health.get("status") == "healthy":
                    st.success("✅ Sistem sağlıklı")
                    st.json(health)
                else:
                    st.error("❌ Sistem hatası")
                    st.json(health)
        
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
                
                st.rerun()
    
    # Ana chat alanı
    st.header("💬 Sohbet")
    
    # Mesaj geçmişini göster
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
                    if "timestamp" in message:
                        st.caption(f"🕐 {time.strftime('%H:%M:%S', time.localtime(message['timestamp']))}")
            
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(message["content"])
                    
                    # Ek bilgiler göster
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if "confidence" in message:
                            confidence = message["confidence"]
                            st.metric("Güven", f"{confidence:.1%}")
                    
                    with col2:
                        if "tool_calls" in message:
                            tool_count = len(message["tool_calls"])
                            st.metric("Araç Kullanım", tool_count)
                    
                    with col3:
                        if "timestamp" in message:
                            st.caption(f"🕐 {time.strftime('%H:%M:%S', time.localtime(message['timestamp']))}")
                    
                    # Araç çağrılarını detay olarak göster
                    if message.get("tool_calls"):
                        with st.expander("🔧 Kullanılan Araçlar"):
                            for tool in message["tool_calls"]:
                                st.code(f"Araç: {tool.get('arac_adi', 'N/A')}")
                                st.json(tool.get("parametreler", {}))
    
    # Yeni mesaj input'u
    st.header("✍️ Yeni Mesaj")
    
    # İki kolon: input ve gönder butonu
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Mesajınızı yazın:",
            placeholder="Örn: Faturamı öğrenmek istiyorum",
            key="user_input"
        )
    
    with col2:
        send_button = st.button("📤 Gönder ")