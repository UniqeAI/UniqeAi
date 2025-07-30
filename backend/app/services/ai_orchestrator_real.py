import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import uuid
import torch
import json
import re
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import os

from .telekom_api import telekom_api
from .ai_endpoint_functions import ai_endpoint_functions
from .user_service import user_service

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model konfigürasyonu
MODEL_NAME = "Choyrens/ChoyrensAI-Telekom-Agent-v1-merged"  # Choyrens özel modeli
# MODEL_NAME = "gpt2"  # Daha küçük model, hızlı yüklenir
PROJECT_ROOT = Path(__file__).resolve().parents[3]

@dataclass
class KonusmaMesaji:
    """Konuşma mesajı yapısı"""
    mesaj_id: str
    kullanici_id: str
    icerik: str
    zaman_damgasi: str
    mesaj_tipi: str  # "kullanici", "sistem", "ai"

@dataclass
class AracCagrisi:
    """Araç çağrısı yapısı"""
    arac_adi: str
    parametreler: Dict[str, Any]
    sonuc: Optional[Any] = None
    durum: str = "beklemede"  # beklemede, calisiyor, tamamlandi, hata
    hata_mesaji: Optional[str] = None

@dataclass
class AIYaniti:
    """Yapay zeka yanıt yapısı"""
    yanit_id: str
    orijinal_mesaj: str
    islenmis_yanit: str
    arac_cagrilari: List[AracCagrisi]
    guven_puani: float

class KonusmaYoneticisi:
    """Konuşma bağlamı yönetimi"""
    
    def __init__(self):
        self.aktif_konusmalar: Dict[str, List[KonusmaMesaji]] = {}
        self.max_mesaj_sayisi = 50  # Maksimum mesaj sayısı
        
    async def baglam_getir(self, oturum_id: str) -> List[KonusmaMesaji]:
        """Oturum için konuşma bağlamını getir"""
        if oturum_id not in self.aktif_konusmalar:
            self.aktif_konusmalar[oturum_id] = []
        
        # Son N mesajı döndür (bağlam sınırı)
        return self.aktif_konusmalar[oturum_id][-self.max_mesaj_sayisi:]
    
    async def mesaj_ekle(self, oturum_id: str, mesaj: KonusmaMesaji):
        """Konuşmaya yeni mesaj ekle"""
        if oturum_id not in self.aktif_konusmalar:
            self.aktif_konusmalar[oturum_id] = []
        
        self.aktif_konusmalar[oturum_id].append(mesaj)
        
        # Maksimum mesaj sayısını aşarsa eski mesajları temizle
        if len(self.aktif_konusmalar[oturum_id]) > self.max_mesaj_sayisi:
            self.aktif_konusmalar[oturum_id] = self.aktif_konusmalar[oturum_id][-self.max_mesaj_sayisi:]
    
    async def konusma_temizle(self, oturum_id: str):
        """Konuşma geçmişini temizle"""
        if oturum_id in self.aktif_konusmalar:
            del self.aktif_konusmalar[oturum_id]

class TelekomAracKaydi:
    """Telekom araçlarının kaydı ve yönetimi"""
    
    def __init__(self):
        self.kayitli_araclar = {
            # FATURA & ÖDEME İŞLEMLERİ
            "get_current_bill": {
                "aciklama": "Müşterinin mevcut fatura bilgilerini getirir",
                "parametreler": ["user_id"]
            },
            "get_past_bills": {
                "aciklama": "Müşterinin geçmiş faturalarını getirir",
                "parametreler": ["user_id", "limit"]
            },
            "pay_bill": {
                "aciklama": "Fatura ödemesi yapar",
                "parametreler": ["bill_id", "method"]
            },
            "get_payment_history": {
                "aciklama": "Müşterinin ödeme geçmişini getirir",
                "parametreler": ["user_id"]
            },
            "setup_autopay": {
                "aciklama": "Otomatik ödeme ayarlar",
                "parametreler": ["user_id", "status"]
            },
            
            # PAKET & TARİFE YÖNETİMİ
            "get_customer_package": {
                "aciklama": "Müşterinin mevcut paketini getirir",
                "parametreler": ["user_id"]
            },
            "get_remaining_quotas": {
                "aciklama": "Müşterinin kalan kotalarını getirir",
                "parametreler": ["user_id"]
            },
            "change_package": {
                "aciklama": "Paket değişikliği başlatır",
                "parametreler": ["user_id", "new_package_name"]
            },
            "get_available_packages": {
                "aciklama": "Kullanılabilir paketleri listeler",
                "parametreler": []
            },
            "get_package_details": {
                "aciklama": "Paket detaylarını getirir",
                "parametreler": ["package_name"]
            },
            "enable_roaming": {
                "aciklama": "Roaming hizmetini etkinleştirir/devre dışı bırakır",
                "parametreler": ["user_id", "status"]
            },
            
            # TEKNİK DESTEK & ARIZA
            "check_network_status": {
                "aciklama": "Ağ durumunu kontrol eder",
                "parametreler": ["region"]
            },
            "create_fault_ticket": {
                "aciklama": "Arıza talebi oluşturur",
                "parametreler": ["user_id", "issue_description"]
            },
            "get_fault_ticket_status": {
                "aciklama": "Arıza talebi durumunu getirir",
                "parametreler": ["ticket_id"]
            },
            "test_internet_speed": {
                "aciklama": "İnternet hız testi yapar",
                "parametreler": ["user_id"]
            },
            
            # HESAP YÖNETİMİ
            "get_customer_profile": {
                "aciklama": "Müşteri profilini getirir",
                "parametreler": ["user_id"]
            },
            "update_customer_contact": {
                "aciklama": "Müşteri iletişim bilgilerini günceller",
                "parametreler": ["user_id", "contact_type", "new_value"]
            },
            "suspend_line": {
                "aciklama": "Hatı askıya alır",
                "parametreler": ["user_id", "reason"]
            },
            "reactivate_line": {
                "aciklama": "Hatı yeniden etkinleştirir",
                "parametreler": ["user_id"]
            },
            
            # KULLANICI YÖNETİMİ
            "register_user": {
                "aciklama": "Yeni kullanıcı kaydı oluşturur",
                "parametreler": ["email", "password", "name"]
            },
            "login_user": {
                "aciklama": "Kullanıcı girişi yapar",
                "parametreler": ["email", "password"]
            },
            "get_user_by_id": {
                "aciklama": "ID ile kullanıcı bilgilerini getirir",
                "parametreler": ["user_id"]
            },
            "update_user": {
                "aciklama": "Kullanıcı bilgilerini günceller",
                "parametreler": ["user_id", "update_data"]
            },
            "logout_user": {
                "aciklama": "Kullanıcı çıkışı yapar",
                "parametreler": []
            },
            "get_all_active_users": {
                "aciklama": "Tüm aktif kullanıcıları listeler",
                "parametreler": []
            },
            
            # TELEKOM AUTH
            "telekom_register": {
                "aciklama": "Telekom sistemi için kullanıcı kaydı",
                "parametreler": ["email", "password", "name"]
            },
            "telekom_login": {
                "aciklama": "Telekom sistemi için kullanıcı girişi",
                "parametreler": ["email", "password"]
            },
            
            # TELEKOM DESTEK EK
            "close_support_ticket": {
                "aciklama": "Destek talebini kapatır",
                "parametreler": ["ticket_id"]
            },
            "get_user_support_tickets": {
                "aciklama": "Kullanıcının tüm destek taleplerini getirir",
                "parametreler": ["user_id"]
            },
            
            # MOCK TEST ENDPOINT'LERİ
            "mock_get_user_info": {
                "aciklama": "Mock kullanıcı bilgisi getirir",
                "parametreler": ["user_id"]
            },
            "mock_get_available_packages": {
                "aciklama": "Mock kullanılabilir paketleri getirir",
                "parametreler": []
            },
            "mock_get_invoice": {
                "aciklama": "Mock fatura bilgisi getirir",
                "parametreler": ["user_id"]
            },
            "mock_get_customer_info": {
                "aciklama": "Mock müşteri bilgisi getirir",
                "parametreler": ["user_id"]
            },
            "mock_get_payment_history": {
                "aciklama": "Mock ödeme geçmişi getirir",
                "parametreler": ["user_id"]
            },
            "mock_get_subscription_status": {
                "aciklama": "Mock abonelik durumu getirir",
                "parametreler": ["user_id"]
            },
            "mock_get_support_tickets": {
                "aciklama": "Mock destek talepleri getirir",
                "parametreler": ["user_id"]
            },
            "mock_get_address": {
                "aciklama": "Mock adres bilgisi getirir",
                "parametreler": ["user_id"]
            },
            "mock_get_campaigns": {
                "aciklama": "Mock kampanya bilgileri getirir",
                "parametreler": []
            },
            
            # SİSTEM ENDPOINT'LERİ
            "get_system_health": {
                "aciklama": "Sistem sağlık durumunu kontrol eder",
                "parametreler": []
            },
            "get_ai_model_info": {
                "aciklama": "AI model bilgilerini getirir",
                "parametreler": []
            }
        }
    
    def mevcut_araclari_getir(self) -> Dict[str, Dict[str, Any]]:
        """Mevcut araçları döndür"""
        return self.kayitli_araclar
    
    def arac_var_mi(self, arac_adi: str) -> bool:
        """Araç kayıtlı mı kontrol et"""
        return arac_adi in self.kayitli_araclar
    
    def arac_bilgisi_getir(self, arac_adi: str) -> Optional[Dict[str, Any]]:
        """Araç bilgilerini getir"""
        return self.kayitli_araclar.get(arac_adi)

class HuggingFaceInferenceService:
    """Gerçek Hugging Face modeli ile inference hizmeti"""
    
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.loaded = False
        self.load_model()
    
    def load_model(self):
        """Hugging Face modelini yükle"""
        try:
            logger.info(f"Model yükleniyor: {self.model_name}")
            
            # CPU için optimize edilmiş quantization ayarları
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
                llm_int8_enable_fp32_cpu_offload=True  # CPU offload aktif
            )
            
            # Tokenizer yükleme
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # CPU için device map
            device_map = {
                "model.embed_tokens": "cpu",
                "model.norm": "cpu",
                "lm_head": "cpu",
                "model.layers": "cpu"
            }
            
            # Model yükleme - CPU için optimize
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=quantization_config,
                device_map=device_map,  # CPU device map
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
                low_cpu_mem_usage=True  # Düşük CPU bellek kullanımı
            )
            
            self.loaded = True
            logger.info("✅ Model başarıyla yüklendi (CPU)")
            
        except Exception as e:
            logger.error(f"Model yükleme hatası: {e}")
            self.loaded = False
            raise
    
    async def yanit_uret(self, mesaj: str, baglam: List[KonusmaMesaji], mevcut_araclar: Dict[str, Any]) -> AIYaniti:
        """Yapay zeka yanıtı üret"""
        logger.info(f"AI yanıtı üretiliyor: {mesaj[:50]}...")
        
        try:
            # Manuel araç seçimi - önce kontrol et (model yüklenmese bile çalışır)
            mesaj_lower = mesaj.lower()
            arac_cagrilari = []
            
            # Debug için log
            logger.info(f"Mesaj: '{mesaj}' -> Lower: '{mesaj_lower}'")
            
            # Geçmiş faturalar kontrolü - daha kapsamlı
            if any(phrase in mesaj_lower for phrase in ["geçmiş faturalar", "geçmiş fatura", "gecmis faturalar", "gecmis fatura", "önceki faturalar", "eski faturalar", "fatura geçmişi", "fatura gecmisi"]):
                logger.info("Geçmiş faturalar tespit edildi - get_past_bills çağırılacak")
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_past_bills",
                    parametreler={"user_id": 1}
                ))
                response_text = "Geçmiş faturalarınızı kontrol ediyorum."
            
            # Mevcut fatura kontrolü - daha spesifik
            elif any(phrase in mesaj_lower for phrase in ["mevcut faturası", "güncel faturası", "şu anki faturası", "bu ayki faturası", "mevcut fatura", "güncel fatura"]):
                logger.info("Mevcut fatura tespit edildi - get_current_bill çağırılacak")
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_current_bill",
                    parametreler={"user_id": 1}
                ))
                response_text = "Mevcut faturanızı kontrol ediyorum."
            
            # Paket kontrolü
            elif any(phrase in mesaj_lower for phrase in ["paket", "tarife", "abonelik"]):
                logger.info("Paket tespit edildi - get_current_package çağırılacak")
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_current_package",
                    parametreler={"user_id": 1}
                ))
                response_text = "Paket bilgilerinizi kontrol ediyorum."
            
            # Kota kontrolü
            elif any(phrase in mesaj_lower for phrase in ["kota", "kalan", "quota", "remaining"]):
                logger.info("Kota tespit edildi - get_remaining_quotas çağırılacak")
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_remaining_quotas",
                    parametreler={"user_id": 1}
                ))
                response_text = "Kalan kotanızı kontrol ediyorum."
            
            # Müşteri profili kontrolü
            elif any(phrase in mesaj_lower for phrase in ["müşteri", "profil", "customer", "profile"]):
                logger.info("Müşteri profili tespit edildi - get_customer_profile çağırılacak")
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_customer_profile",
                    parametreler={"user_id": 1}
                ))
                response_text = "Müşteri profilinizi kontrol ediyorum."
            
            # Sistem durumu kontrolü
            elif any(phrase in mesaj_lower for phrase in ["sistem", "sağlık", "durum", "health", "status"]):
                logger.info("Sistem durumu tespit edildi - get_system_health çağırılacak")
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_system_health",
                    parametreler={}
                ))
                response_text = "Sistem durumunu kontrol ediyorum."
            
            else:
                # Model yüklü mü kontrol et
                if not self.loaded:
                    logger.warning("Model yüklenmedi, fallback yanıt veriliyor")
                    response_text = "Merhaba! Size nasıl yardımcı olabilirim? Fatura, paket, kota, müşteri profili veya sistem durumu hakkında soru sorabilirsiniz."
                else:
                    # Normal model generation
                    system_prompt = self._create_system_prompt(mevcut_araclar)
                    dialogue = self._prepare_dialogue(system_prompt, mesaj, baglam)
                    response_text = await self._generate_response(dialogue)
                    arac_cagrilari = self._parse_tool_calls(response_text)
            
            # Temizlenmiş yanıt
            clean_response = self._clean_response(response_text)
            
            return AIYaniti(
                yanit_id=f"YANIT_{uuid.uuid4().hex[:8]}",
                orijinal_mesaj=mesaj,
                islenmis_yanit=clean_response,
                arac_cagrilari=arac_cagrilari,
                guven_puani=0.90
            )
            
        except Exception as e:
            logger.error(f"AI yanıt üretme hatası: {e}")
            # Fallback yanıt
            return AIYaniti(
                yanit_id=f"YANIT_{uuid.uuid4().hex[:8]}",
                orijinal_mesaj=mesaj,
                islenmis_yanit="Üzgünüm, şu anda size yardımcı olamıyorum. Lütfen tekrar deneyin.",
                arac_cagrilari=[],
                guven_puani=0.10
            )
    
    def _create_system_prompt(self, mevcut_araclar: Dict[str, Any]) -> str:
        """Sistem promptu oluştur"""
        arac_listesi = "\n".join([f"- {arac}: {bilgi['aciklama']}" for arac, bilgi in mevcut_araclar.items()])
        
        return f"""Sen Türk Telekom'un yapay zeka asistanısın. Müşterilere yardım etmek için tasarlandın.

Kullanılabilir araçlar:
{arac_listesi}

ÖNEMLİ KURALLAR:
1. Samimi ve yardımsever bir dille konuş
2. Türkçe kullan
3. Kullanıcının sorduğu şeyi DİKKATLİCE ANLA:
   - "geçmiş faturalarım" = get_past_bills() kullan
   - "mevcut faturası" = get_current_bill() kullan
   - "paketlerim" = get_current_package() kullan
   - "kalan kotam" = get_remaining_quotas() kullan
4. Her zaman doğru araç çağır
5. Araç çağırırken <|begin_of_tool_code|> ... <|end_of_tool_code|> formatını kullan

Örnek kullanımlar:
- "geçmiş faturalarım" → get_past_bills(user_id=1234)
- "mevcut faturası" → get_current_bill(user_id=1234)
- "paketlerim" → get_current_package(user_id=1234)"""
    
    def _prepare_dialogue(self, system_prompt: str, mesaj: str, baglam: List[KonusmaMesaji]) -> List[Dict[str, str]]:
        """Chat formatında diyalog hazırla"""
        dialogue = [{"role": "system", "content": system_prompt}]
        
        # Bağlamı ekle (son 5 mesaj)
        recent_context = baglam[-5:] if baglam else []
        for ctx_msg in recent_context:
            if ctx_msg.mesaj_tipi == "kullanici":
                dialogue.append({"role": "user", "content": ctx_msg.icerik})
            elif ctx_msg.mesaj_tipi == "ai":
                dialogue.append({"role": "assistant", "content": ctx_msg.icerik})
        
        # Mevcut mesajı ekle
        dialogue.append({"role": "user", "content": mesaj})
        
        return dialogue
    
    async def _generate_response(self, dialogue: List[Dict[str, str]]) -> str:
        """Model ile yanıt üret"""
        try:
            # Son kullanıcı mesajını al
            user_message = ""
            for msg in reversed(dialogue):
                if msg["role"] == "user":
                    user_message = msg["content"]
                    break
            
            # Manuel araç seçimi - DEBUG için log ekle
            logger.info(f"Kullanıcı mesajı: {user_message}")
            
            # Geçmiş faturalar kontrolü - daha kapsamlı
            if any(phrase in user_message.lower() for phrase in ["geçmiş faturalar", "geçmiş fatura", "önceki faturalar", "eski faturalar", "fatura geçmişi"]):
                logger.info("Geçmiş faturalar tespit edildi - get_past_bills çağırılacak")
                return "Geçmiş faturalarınızı kontrol ediyorum.\n\n<|begin_of_tool_code|>\nprint(get_past_bills(user_id=1))\n<|end_of_tool_code|>"
            
            # Mevcut fatura kontrolü - daha spesifik
            elif any(phrase in user_message.lower() for phrase in ["mevcut faturası", "güncel faturası", "şu anki faturası", "bu ayki faturası"]):
                logger.info("Mevcut fatura tespit edildi - get_current_bill çağırılacak")
                return "Mevcut faturanızı kontrol ediyorum.\n\n<|begin_of_tool_code|>\nprint(get_current_bill(user_id=1))\n<|end_of_tool_code|>"
            
            # Paket kontrolü
            elif any(phrase in user_message.lower() for phrase in ["paket", "tarife", "abonelik"]):
                logger.info("Paket tespit edildi - get_current_package çağırılacak")
                return "Paket bilgilerinizi kontrol ediyorum.\n\n<|begin_of_tool_code|>\nprint(get_current_package(user_id=1))\n<|end_of_tool_code|>"
            
            # Kota kontrolü
            elif any(phrase in user_message.lower() for phrase in ["kota", "kalan", "quota", "remaining"]):
                logger.info("Kota tespit edildi - get_remaining_quotas çağırılacak")
                return "Kalan kotanızı kontrol ediyorum.\n\n<|begin_of_tool_code|>\nprint(get_remaining_quotas(user_id=1))\n<|end_of_tool_code|>"
            
            # Müşteri profili kontrolü
            elif any(phrase in user_message.lower() for phrase in ["müşteri", "profil", "customer", "profile"]):
                logger.info("Müşteri profili tespit edildi - get_customer_profile çağırılacak")
                return "Müşteri profilinizi kontrol ediyorum.\n\n<|begin_of_tool_code|>\nprint(get_customer_profile(user_id=1))\n<|end_of_tool_code|>"
            
            # Sistem durumu kontrolü
            elif any(phrase in user_message.lower() for phrase in ["sistem", "sağlık", "durum", "health", "status"]):
                logger.info("Sistem durumu tespit edildi - get_system_health çağırılacak")
                return "Sistem durumunu kontrol ediyorum.\n\n<|begin_of_tool_code|>\nprint(get_system_health())\n<|end_of_tool_code|>"
            
            # Basit prompt
            prompt = f"Kullanıcı: {user_message}\nAsistan: "
            
            # Tokenize
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=256)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=128,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            
            # Decode response
            response_text = self.tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True)
            
            # Eğer yanıt boşsa fallback
            if not response_text.strip():
                return "Merhaba! Size nasıl yardımcı olabilirim?"
            
            return response_text.strip()
            
        except Exception as e:
            logger.error(f"Model generation hatası: {e}")
            return "Merhaba! Size nasıl yardımcı olabilirim?"
    
    def _parse_tool_calls(self, text: str) -> List[AracCagrisi]:
        """AI yanıtından araç çağrılarını çıkar (advanced_playground.py'den uyarlandı)"""
        tool_calls = []
        
        # Tool code pattern'ini bul
        pattern = r"<\|begin_of_tool_code\|>([\s\S]*?)<\|end_of_tool_code\|>"
        match = re.search(pattern, text)
        
        if not match:
            return tool_calls
        
        tool_code_str = match.group(1).strip()
        
        # Function call pattern
        call_pattern = re.compile(r"print\((\w+)\((.*)\)\)")
        call_match = call_pattern.search(tool_code_str)
        
        if not call_match:
            return tool_calls
        
        function_name = call_match.group(1)
        args_str = call_match.group(2)
        
        try:
            params = {}
            # Argument parsing
            arg_pattern = re.compile(r"(\w+)=((?:\"(?:\\\"|[^\"])*\")|(?:'(?:\\'|[^'])*')|[^,)]+)")
            for p_match in arg_pattern.finditer(args_str):
                key = p_match.group(1)
                raw_value = p_match.group(2)
                
                # Value parsing
                if (raw_value.startswith('"') and raw_value.endswith('"')) or \
                   (raw_value.startswith("'") and raw_value.endswith("'")):
                    value = json.loads(raw_value)
                else:
                    try:
                        value = json.loads(raw_value.lower())
                    except (json.JSONDecodeError, AttributeError):
                        value = raw_value
                
                params[key] = value
            
            tool_calls.append(AracCagrisi(
                arac_adi=function_name,
                parametreler=params
            ))
            
        except Exception as e:
            logger.error(f"Araç parametreleri ayrıştırma hatası: {e}")
        
        return tool_calls
    
    def _clean_response(self, response: str) -> str:
        """Yanıtı temizle (special token'ları kaldır)"""
        # Tool code kısımlarını kaldır
        response = re.sub(r'<\|begin_of_tool_code\|>[\s\S]*?<\|end_of_tool_code\|>', '', response)
        # Diğer special token'ları kaldır
        response = re.sub(r'<\|.*?\|>', '', response)
        return response.strip()
    
    async def final_yanit_uret(self, orijinal_yanit: AIYaniti, arac_sonuclari: List[AracCagrisi]) -> str:
        """Araç sonuçlarıyla final yanıt üret"""
        logger.info("Final yanıt üretiliyor...")
        
        # Simüle edilmiş işlem süresi
        await asyncio.sleep(0.2)
        
        # Araç sonuçlarını yanıta entegre et
        final_yanit = self._arac_sonuclarini_entegre_et(orijinal_yanit.islenmis_yanit, arac_sonuclari)
        
        return final_yanit
    
    def _arac_cagrilari_tespit_et(self, mesaj: str) -> List[AracCagrisi]:
        """Mesajdan araç çağrılarını tespit et"""
        arac_cagrilari = []
        
        # Basit anahtar kelime tabanlı tespit
        mesaj_lower = mesaj.lower()
        
        # User ID tespit et (basit regex)
        user_id_match = re.search(r'\b(\d{4})\b', mesaj)
        user_id = user_id_match.group(1) if user_id_match else "1234"
        
        # FATURA & ÖDEME İŞLEMLERİ
        if any(word in mesaj_lower for word in ["fatura", "bill", "ödeme", "payment"]):
            if "mevcut" in mesaj_lower or "current" in mesaj_lower:
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_current_bill",
                    parametreler={"user_id": int(user_id)}
                ))
            elif "geçmiş" in mesaj_lower or "history" in mesaj_lower:
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_past_bills",
                    parametreler={"user_id": int(user_id), "limit": 12}
                ))
            elif "öde" in mesaj_lower or "pay" in mesaj_lower:
                bill_id_match = re.search(r'F-\d{4}-\d+', mesaj)
                bill_id = bill_id_match.group() if bill_id_match else f"F-2024-{user_id}"
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="pay_bill",
                    parametreler={"bill_id": bill_id, "method": "credit_card"}
                ))
        
        # PAKET & TARİFE YÖNETİMİ
        if any(word in mesaj_lower for word in ["paket", "package", "tarife"]):
            if "mevcut" in mesaj_lower or "current" in mesaj_lower:
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_customer_package",
                    parametreler={"user_id": int(user_id)}
                ))
            elif "kalan" in mesaj_lower or "remaining" in mesaj_lower:
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_remaining_quotas",
                    parametreler={"user_id": int(user_id)}
                ))
            elif "değiştir" in mesaj_lower or "change" in mesaj_lower:
                package_match = re.search(r'(Mega|Öğrenci|Süper|Premium)', mesaj)
                package_name = package_match.group(1) if package_match else "Mega İnternet"
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="change_package",
                    parametreler={"user_id": int(user_id), "new_package_name": package_name}
                ))
        
        # TEKNİK DESTEK & ARIZA
        if any(word in mesaj_lower for word in ["arıza", "fault", "destek", "support"]):
            if "oluştur" in mesaj_lower or "create" in mesaj_lower:
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="create_fault_ticket",
                    parametreler={"user_id": int(user_id), "issue_description": "Teknik sorun"}
                ))
            elif "durum" in mesaj_lower or "status" in mesaj_lower:
                ticket_match = re.search(r'T-\d{4}-\d+', mesaj)
                ticket_id = ticket_match.group() if ticket_match else f"T-2024-{user_id}"
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="get_fault_ticket_status",
                    parametreler={"ticket_id": ticket_id}
                ))
        
        # HESAP YÖNETİMİ
        if any(word in mesaj_lower for word in ["profil", "profile", "müşteri", "customer"]):
            arac_cagrilari.append(AracCagrisi(
                arac_adi="get_customer_profile",
                parametreler={"user_id": int(user_id)}
            ))
        
        return arac_cagrilari
    
    def _yanit_uret(self, mesaj: str, arac_cagrilari: List[AracCagrisi]) -> str:
        """Temel yanıt üretimi"""
        if not arac_cagrilari:
            return "Merhaba! Size nasıl yardımcı olabilirim? Fatura, paket, teknik destek konularında yardım edebilirim."
        
        arac_isimleri = [arac.arac_adi for arac in arac_cagrilari]
        return f"Anladım, {', '.join(arac_isimleri)} işlemlerini gerçekleştiriyorum..."
    
    def _arac_sonuclarini_entegre_et(self, temel_yanit: str, arac_sonuclari: List[AracCagrisi]) -> str:
        """Araç sonuçlarını yanıta entegre et"""
        if not arac_sonuclari:
            return temel_yanit
        
        basarili_sonuclar = [arac for arac in arac_sonuclari if arac.durum == "tamamlandi"]
        hatali_sonuclar = [arac for arac in arac_sonuclari if arac.durum == "hata"]
        
        yanit_parcalari = [temel_yanit]
        
        # Araç sonuçlarını işle
        for arac in basarili_sonuclar:
            if arac.arac_adi == "get_past_bills" and arac.sonuc:
                # Geçmiş faturalar sonucunu işle
                if isinstance(arac.sonuc, dict) and arac.sonuc.get('success'):
                    data = arac.sonuc.get('data', {})
                    bills = data.get('bills', [])
                    total_count = data.get('total_count', 0)
                    
                    if bills:
                        yanit_parcalari.append(f"\n📋 Geçmiş Faturalarınız ({total_count} adet):")
                        
                        # İlk 5 faturayı göster
                        for i, bill in enumerate(bills[:5], 1):
                            amount = bill.get('amount', 0)
                            date = bill.get('bill_date', 'Bilinmiyor')
                            status = bill.get('status', 'Bilinmiyor')
                            status_emoji = "✅" if status == "paid" else "⏳"
                            
                            yanit_parcalari.append(
                                f"   {i}. {date}: {amount} TL {status_emoji} ({status})"
                            )
                        
                        if len(bills) > 5:
                            yanit_parcalari.append(f"   ... ve {len(bills) - 5} fatura daha")
                    else:
                        yanit_parcalari.append("📋 Geçmiş faturalarınız bulunamadı.")
            
            elif arac.arac_adi == "get_current_bill" and arac.sonuc:
                # Mevcut fatura sonucunu işle
                if isinstance(arac.sonuc, dict) and arac.sonuc.get('success'):
                    data = arac.sonuc.get('data', {})
                    amount = data.get('amount', 0)
                    due_date = data.get('due_date', 'Bilinmiyor')
                    status = data.get('status', 'Bilinmiyor')
                    
                    yanit_parcalari.append(f"\n💰 Mevcut faturanız: {amount} TL")
                    yanit_parcalari.append(f"📅 Son ödeme tarihi: {due_date}")
                    yanit_parcalari.append(f"📊 Durum: {status}")
            
            elif arac.arac_adi == "get_current_package" and arac.sonuc:
                # Paket bilgisi sonucunu işle
                if isinstance(arac.sonuc, dict) and arac.sonuc.get('success'):
                    data = arac.sonuc.get('data', {})
                    package_name = data.get('package_name', 'Bilinmiyor')
                    price = data.get('price', 0)
                    
                    yanit_parcalari.append(f"\n📦 Aktif Paketiniz: {package_name}")
                    yanit_parcalari.append(f"💰 Aylık Ücret: {price} TL")
            
            elif arac.arac_adi == "get_remaining_quotas" and arac.sonuc:
                # Kota bilgisi sonucunu işle
                if isinstance(arac.sonuc, dict) and arac.sonuc.get('success'):
                    data = arac.sonuc.get('data', {})
                    internet_gb = data.get('internet_remaining_gb', 0)
                    sms_count = data.get('sms_remaining', 0)
                    call_minutes = data.get('call_remaining_minutes', 0)
                    
                    yanit_parcalari.append(f"\n📊 Kalan Kotalarınız:")
                    yanit_parcalari.append(f"   🌐 İnternet: {internet_gb} GB")
                    yanit_parcalari.append(f"   📱 SMS: {sms_count} adet")
                    yanit_parcalari.append(f"   📞 Konuşma: {call_minutes} dakika")
        
        if hatali_sonuclar:
            yanit_parcalari.append("\n❌ Bazı işlemlerde sorun oluştu, lütfen tekrar deneyin.")
        
        return " ".join(yanit_parcalari)

class YapayZekaOrkestratori:
    """Ana yapay zeka orkestratörü"""
    
    def __init__(self):
        logger.info("Yapay Zeka Orkestratörü başlatılıyor...")
        self.konusma_yoneticisi = KonusmaYoneticisi()
        self.arac_kaydi = TelekomAracKaydi()
        self.telekom_api = telekom_api
        
        # Hugging Face modelini yükle
        try:
            self.model_hizmeti = HuggingFaceInferenceService()
            logger.info("✅ Hugging Face modeli başarıyla yüklendi")
        except Exception as e:
            logger.error(f"❌ Model yükleme hatası: {e}")
            logger.warning("Fallback: Model yüklenemedi, servis çalışmayabilir")
            self.model_hizmeti = None
    
    async def kullanici_mesaj_isle(self, mesaj: str, kullanici_id: str, oturum_id: str) -> Dict[str, Any]:
        """Kullanıcı mesajını işle ve yanıt üret"""
        try:
            logger.info(f"Kullanıcı mesajı işleniyor: {kullanici_id} - {mesaj[:50]}...")
            
            # Model yüklü mü kontrol et
            if self.model_hizmeti is None:
                logger.error("Model servisi yüklenmemiş!")
                return {
                    "yanit_id": f"ERROR_{uuid.uuid4().hex[:8]}",
                    "yanit": "Üzgünüm, AI model servisi şu anda kullanılamıyor. Lütfen daha sonra tekrar deneyin.",
                    "guven_puani": 0.0,
                    "arac_cagrilari": [],
                    "metadata": {"error": "Model not loaded"}
                }
            
            # Model durumunu kontrol et
            if not hasattr(self.model_hizmeti, 'loaded') or not self.model_hizmeti.loaded:
                logger.error("Model yüklenmemiş!")
                return {
                    "yanit_id": f"ERROR_{uuid.uuid4().hex[:8]}",
                    "yanit": "Üzgünüm, AI model servisi şu anda kullanılamıyor. Lütfen daha sonra tekrar deneyin.",
                    "guven_puani": 0.0,
                    "arac_cagrilari": [],
                    "metadata": {"error": "Model not loaded"}
                }
            
            logger.info("Model servisi hazır, mesaj işleniyor...")
            
            # Mesajı ön işle
            islenmis_mesaj = self.turkce_on_isle(mesaj)
            logger.info(f"İşlenmiş mesaj: {islenmis_mesaj}")
            
            # Kullanıcı mesajını kaydet
            kullanici_mesaji = KonusmaMesaji(
                mesaj_id=f"MSG_{uuid.uuid4().hex[:8]}",
                kullanici_id=kullanici_id,
                icerik=islenmis_mesaj,
                zaman_damgasi=datetime.now().isoformat(),
                mesaj_tipi="kullanici"
            )
            await self.konusma_yoneticisi.mesaj_ekle(oturum_id, kullanici_mesaji)
            
            # Konuşma bağlamını getir
            baglam = await self.konusma_yoneticisi.baglam_getir(oturum_id)
            logger.info(f"Bağlam mesaj sayısı: {len(baglam)}")
            
            # Mevcut araçları getir
            mevcut_araclar = self.arac_kaydi.mevcut_araclari_getir()
            logger.info(f"Mevcut araç sayısı: {len(mevcut_araclar)}")
            
            # AI yanıtı üret
            logger.info("AI yanıtı üretiliyor...")
            ai_yaniti = await self.model_hizmeti.yanit_uret(islenmis_mesaj, baglam, mevcut_araclar)
            logger.info(f"AI yanıtı üretildi: {ai_yaniti.islenmis_yanit[:100]}...")
            logger.info(f"Araç çağrısı sayısı: {len(ai_yaniti.arac_cagrilari)}")
            
            # Araç çağrılarını yürüt
            if ai_yaniti.arac_cagrilari:
                logger.info(f"{len(ai_yaniti.arac_cagrilari)} araç çağrısı yürütülüyor...")
                arac_sonuclari = await self.arac_cagrilari_yurut(ai_yaniti.arac_cagrilari)
                
                # Final yanıt üret
                final_yanit = await self.model_hizmeti.final_yanit_uret(ai_yaniti, arac_sonuclari)
            else:
                final_yanit = ai_yaniti.islenmis_yanit
                arac_sonuclari = []
                logger.warning("Hiç araç çağrısı yapılmadı!")
            
            logger.info(f"Final yanıt: {final_yanit[:100]}...")
            
            # AI yanıtını kaydet
            ai_mesaji = KonusmaMesaji(
                mesaj_id=f"AI_{uuid.uuid4().hex[:8]}",
                kullanici_id="AI",
                icerik=final_yanit,
                zaman_damgasi=datetime.now().isoformat(),
                mesaj_tipi="ai"
            )
            await self.konusma_yoneticisi.mesaj_ekle(oturum_id, ai_mesaji)
            
            # Sonucu hazırla
            sonuc = {
                "yanit_id": ai_yaniti.yanit_id,
                "yanit": final_yanit,
                "guven_puani": ai_yaniti.guven_puani,
                "arac_cagrilari": [
                    {
                        "arac_adi": arac.arac_adi,
                        "durum": arac.durum,
                        "sonuc": arac.sonuc,
                        "hata_mesaji": arac.hata_mesaji
                    }
                    for arac in arac_sonuclari
                ],
                "metadata": {
                    "oturum_id": oturum_id,
                    "kullanici_id": kullanici_id,
                    "islenme_zamani": datetime.now().isoformat(),
                    "baglam_mesaj_sayisi": len(baglam)
                }
            }
            
            logger.info(f"Mesaj işleme tamamlandı: {sonuc['yanit_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Mesaj işleme hatası: {e}")
            raise
    
    def turkce_on_isle(self, mesaj: str) -> str:
        """Türkçe metin ön işleme"""
        # Basit ön işleme
        islenmis = mesaj.strip()
        
        # Türkçe karakter normalizasyonu
        islenmis = islenmis.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
        islenmis = islenmis.replace('İ', 'I').replace('Ğ', 'G').replace('Ü', 'U').replace('Ş', 'S').replace('Ö', 'O').replace('Ç', 'C')
        
        # Gereksiz boşlukları temizle
        islenmis = ' '.join(islenmis.split())
        
        return islenmis
    
    async def arac_cagrilari_yurut(self, arac_cagrilari: List[AracCagrisi]) -> List[AracCagrisi]:
        """Araç çağrılarını yürüt"""
        sonuclar = []
        
        for arac_cagrisi in arac_cagrilari:
            try:
                logger.info(f"Araç çağrısı yürütülüyor: {arac_cagrisi.arac_adi}")
                
                # Araç durumunu güncelle
                arac_cagrisi.durum = "calisiyor"
                
                # Telekom API'den ilgili fonksiyonu çağır
                sonuc = await self._telekom_arac_cagir(arac_cagrisi.arac_adi, arac_cagrisi.parametreler)
                
                # Sonucu kaydet
                arac_cagrisi.sonuc = sonuc
                arac_cagrisi.durum = "tamamlandi"
                
                logger.info(f"Araç çağrısı başarılı: {arac_cagrisi.arac_adi}")
                
            except Exception as e:
                logger.error(f"Araç çağrısı hatası: {arac_cagrisi.arac_adi} - {e}")
                arac_cagrisi.durum = "hata"
                arac_cagrisi.hata_mesaji = str(e)
            
            sonuclar.append(arac_cagrisi)
        
        return sonuclar
    
    async def _telekom_arac_cagir(self, arac_adi: str, parametreler: Dict[str, Any]) -> Any:
        """Telekom API araç çağrısı - AI endpoint fonksiyonları kullanarak"""
        try:
            logger.info(f"AI Telekom araç çağrısı: {arac_adi} - {parametreler}")
            
            # AI endpoint fonksiyonları mapping
            function_mapping = {
                # FATURA & ÖDEME İŞLEMLERİ
                "get_current_bill": ai_endpoint_functions.telekom_get_current_bill,
                "get_past_bills": ai_endpoint_functions.telekom_get_bill_history,
                "pay_bill": ai_endpoint_functions.telekom_pay_bill,
                "get_payment_history": ai_endpoint_functions.telekom_get_payment_history,
                "setup_autopay": ai_endpoint_functions.telekom_setup_autopay,
                
                # PAKET & TARİFE YÖNETİMİ
                "get_customer_package": ai_endpoint_functions.telekom_get_current_package,
                "get_remaining_quotas": ai_endpoint_functions.telekom_get_remaining_quotas,
                "change_package": ai_endpoint_functions.telekom_change_package,
                "get_available_packages": ai_endpoint_functions.telekom_get_available_packages,
                "get_package_details": ai_endpoint_functions.telekom_get_package_details,
                "enable_roaming": ai_endpoint_functions.telekom_enable_roaming,
                
                # TEKNİK DESTEK & ARIZA
                "check_network_status": ai_endpoint_functions.telekom_check_network_status,
                "create_fault_ticket": ai_endpoint_functions.telekom_create_support_ticket,
                "get_fault_ticket_status": ai_endpoint_functions.telekom_get_support_ticket_status,
                "test_internet_speed": ai_endpoint_functions.telekom_test_internet_speed,
                
                # HESAP YÖNETİMİ
                "get_customer_profile": ai_endpoint_functions.telekom_get_customer_profile,
                "update_customer_contact": ai_endpoint_functions.telekom_update_customer_contact,
                "suspend_line": ai_endpoint_functions.telekom_suspend_line,
                "reactivate_line": ai_endpoint_functions.telekom_reactivate_line,
                
                # KULLANICI YÖNETİMİ
                "register_user": ai_endpoint_functions.user_register,
                "login_user": ai_endpoint_functions.user_login,
                "get_user_by_id": ai_endpoint_functions.user_get_by_id,
                "update_user": ai_endpoint_functions.user_update,
                "logout_user": ai_endpoint_functions.user_logout,
                "get_all_active_users": ai_endpoint_functions.user_get_all_active,
                
                # TELEKOM AUTH
                "telekom_register": ai_endpoint_functions.telekom_auth_register,
                "telekom_login": ai_endpoint_functions.telekom_auth_login,
                
                # TELEKOM DESTEK EK
                "close_support_ticket": ai_endpoint_functions.telekom_close_support_ticket,
                "get_user_support_tickets": ai_endpoint_functions.telekom_get_user_support_tickets,
                
                # MOCK TEST ENDPOINT'LERİ
                "mock_get_user_info": ai_endpoint_functions.mock_get_user_info,
                "mock_get_available_packages": ai_endpoint_functions.mock_get_available_packages,
                "mock_get_invoice": ai_endpoint_functions.mock_get_invoice,
                "mock_get_customer_info": ai_endpoint_functions.mock_get_customer_info,
                "mock_get_payment_history": ai_endpoint_functions.mock_get_payment_history,
                "mock_get_subscription_status": ai_endpoint_functions.mock_get_subscription_status,
                "mock_get_support_tickets": ai_endpoint_functions.mock_get_support_tickets,
                "mock_get_address": ai_endpoint_functions.mock_get_address,
                "mock_get_campaigns": ai_endpoint_functions.mock_get_campaigns,
                
                # SİSTEM ENDPOINT'LERİ
                "get_system_health": ai_endpoint_functions.system_get_health,
                "get_ai_model_info": ai_endpoint_functions.system_get_ai_model_info,
                
                # KULLANICI BİLGİLERİ
                "get_current_user": self._get_current_user
            }
            
            if arac_adi not in function_mapping:
                logger.warning(f"Bilinmeyen araç: {arac_adi}")
                return None
            
            # Fonksiyonu çağır
            function = function_mapping[arac_adi]
            result = await function(**parametreler)
            
            logger.info(f"AI Telekom API yanıtı: {result}")
            
            return result.get("data") if result.get("success") else None
            
        except Exception as e:
            logger.error(f"AI Telekom araç çağrısı hatası: {e}")
            raise
    
    async def _get_current_user(self, **kwargs) -> Dict[str, Any]:
        """Geçerli kullanıcı bilgilerini getir"""
        try:
            logger.info("Geçerli kullanıcı bilgileri getiriliyor...")
            
            user_info = await user_service.get_current_user()
            
            if user_info:
                result = {
                    "success": True,
                    "message": "Geçerli kullanıcı bilgileri başarıyla getirildi",
                    "data": {
                        "user_id": user_info.user_id,
                        "username": user_info.username,
                        "email": user_info.email,
                        "full_name": user_info.full_name,
                        "phone": user_info.phone,
                        "preferences": user_info.preferences,
                        "last_login": user_info.last_login.isoformat() if user_info.last_login else None,
                        "is_active": user_info.is_active,
                        "metadata": user_info.metadata
                    }
                }
            else:
                result = {
                    "success": False,
                    "message": "Aktif kullanıcı bulunamadı",
                    "data": None
                }
            
            logger.info(f"Kullanıcı bilgileri yanıtı: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Kullanıcı bilgileri getirme hatası: {e}")
            return {
                "success": False,
                "message": f"Kullanıcı bilgileri getirme hatası: {str(e)}",
                "data": None
            }
    
    async def oturum_temizle(self, oturum_id: str):
        """Oturum konuşma geçmişini temizle"""
        await self.konusma_yoneticisi.konusma_temizle(oturum_id)
        logger.info(f"Oturum temizlendi: {oturum_id}")
    
    async def sistem_durumu_getir(self) -> Dict[str, Any]:
        """Sistem durumu bilgilerini getir"""
        return {
            "model_hizmeti": {
                "model_adi": self.model_hizmeti.model_name if self.model_hizmeti else "Model yüklenmedi",
                "model_loaded": self.model_hizmeti.loaded if self.model_hizmeti else False
            },
            "arac_kaydi": {
                "toplam_arac": len(self.arac_kaydi.mevcut_araclari_getir()),
                "mevcut_araclar": list(self.arac_kaydi.mevcut_araclari_getir().keys())
            },
            "konusma_yoneticisi": {
                "aktif_oturum_sayisi": len(self.konusma_yoneticisi.aktif_konusmalar),
                "max_mesaj_sayisi": self.konusma_yoneticisi.max_mesaj_sayisi
            },
            "telekom_api": {
                "musteri_sayisi": len(self.telekom_api.musteri_veritabani),
                "paket_sayisi": len(self.telekom_api.paket_veritabani),
                "destek_talep_sayisi": len(self.telekom_api.destek_talepleri)
            }
        }

# Global orkestratör örneği
ai_orchestrator = YapayZekaOrkestratori() 