import logging
import asyncio
import json
import re
import torch
from typing import List, Dict, Any, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from dataclasses import dataclass
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Türkçe NLP için
try:
    from zemberek import TurkishMorphology
    ZEMBEREK_AVAILABLE = True
except ImportError:
    ZEMBEREK_AVAILABLE = False
    print("Zemberek kurulu değil. Türkçe NLP özellikleri devre dışı.")

# LangChain entegrasyonu
try:
    from langchain_community.llms import HuggingFacePipeline
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("LangChain kurulu değil. Gelişmiş AI özellikleri devre dışı.")

logger = logging.getLogger(__name__)

@dataclass
class KonusmaMesaji:
    role: str  # "user" veya "assistant"
    content: str
    timestamp: datetime

@dataclass
class AracCagrisi:
    arac_adi: str
    parametreler: Dict[str, Any]
    durum: str = "bekliyor"
    sonuc: Optional[Dict[str, Any]] = None
    hata_mesaji: Optional[str] = None

class YapayZekaOrkestratori:
    def __init__(self):
        # AI model ve tokenizer
        self.model = None
        self.tokenizer = None
        self.morphology = None
        self.langchain_chain = None
        self._model_loaded = False
        
        # Model adı - GGUF Telekom AI modeli (v5 eklendi)
        self.model_name = "Choyrens/ChoyrensAI-Telekom-Agent-v5-gguf"
        
        # Türkçe NLP için Zemberek
        try:
            from zemberek import TurkishMorphology
            self.morphology = TurkishMorphology.create_with_defaults()
            logger.info("Zemberek Türkçe NLP başarıyla yüklendi")
        except ImportError:
            logger.warning("Zemberek bulunamadı, basit Türkçe işleme kullanılacak")
            self.morphology = None
        
        # Model yükleme
        self._load_model()
    
    def _load_model(self):
        """GGUF Telekom AI modelini yükle"""
        try:
            logger.info(f"AI modeli yükleniyor: {self.model_name}")
            
            # GGUF model için llama-cpp-python kullan
            try:
                from llama_cpp import Llama
                import torch
                
                logger.info("GGUF Telekom AI modeli llama-cpp-python ile yükleniyor...")
                
                # Model yolu - v5 için dinamik yükleme
                import os
                from huggingface_hub import snapshot_download
                
                # Model'i Hugging Face'den indir
                model_path = snapshot_download(
                    repo_id=self.model_name,
                    local_dir="./models"
                )
                
                # GGUF dosyasını bul
                gguf_files = [f for f in os.listdir(model_path) if f.endswith('.gguf')]
                if gguf_files:
                    model_file = os.path.join(model_path, gguf_files[0])
                else:
                    raise FileNotFoundError(f"GGUF dosyası bulunamadı: {model_path}")
                
                logger.info(f"Model dosyası: {model_path}")
                
                # GGUF model yükleme - llama-cpp-python ile (v5 için optimize edildi)
                self.model = Llama(
                    model_path=model_file,
                    n_ctx=8192,  # Context length artırıldı (v5 için maksimum)
                    n_threads=16,  # Thread sayısını artır
                    n_batch=32,  # Batch size artır
                    n_gpu_layers=0,  # CPU kullan
                    verbose=False,  # Verbose kapalı
                    use_mlock=True,  # Memory locking
                    use_mmap=True,  # Memory mapping
                    seed=42  # Deterministic results
                )
                
                # Tokenizer için basit bir wrapper
                class SimpleTokenizer:
                    def __init__(self):
                        self.pad_token = "<pad>"
                        self.eos_token = "</s>"
                        self.bos_token = "<s>"
                    
                    def encode(self, text, **kwargs):
                        # Basit tokenization
                        return text.split()
                    
                    def decode(self, tokens, **kwargs):
                        # Basit detokenization
                        return " ".join(tokens)
                
                self.tokenizer = SimpleTokenizer()
                
                # LangChain kurulumu
                if LANGCHAIN_AVAILABLE:
                    self._setup_langchain()
                
                self._model_loaded = True
                logger.info("✅ GGUF Telekom AI modeli başarıyla yüklendi!")
                
            except ImportError:
                logger.warning("llama-cpp-python bulunamadı, basit AI kullanılacak")
                self._model_loaded = False
                
        except Exception as e:
            logger.error(f"❌ Model yükleme hatası: {e}")
            self._model_loaded = False
            logger.info("⚠️ AI doğal yanıt verecek - model yükleme başarısız")
    
    def _setup_langchain(self):
        """LangChain pipeline kurulumu"""
        try:
            from transformers import pipeline
            
            # HuggingFace pipeline oluştur
            pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=128,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )
            
            # LangChain LLM wrapper
            llm = HuggingFacePipeline(pipeline=pipe)
            
            # Prompt template - AI'ya mantıklı yönlendirme
            template = """Sen bir Telekom AI asistanısın. Kullanıcının sorununu mantıklı bir şekilde anla ve uygun çözüm öner.

Kullanıcı: {user_input}
Yanıt:"""
            
            prompt = PromptTemplate(
                input_variables=["user_input"],
                template=template
            )
            
            self.langchain_chain = LLMChain(llm=llm, prompt=prompt)
            logger.info("LangChain pipeline başarıyla kuruldu")
            
        except Exception as e:
            logger.error(f"LangChain kurulum hatası: {e}")
    
    def _turkish_preprocessing(self, text: str) -> str:
        """Türkçe metin ön işleme"""
        if not ZEMBEREK_AVAILABLE or not self.morphology:
            return text.lower()
        
        try:
            # Zemberek ile lemmatization - güncellenmiş API kullanımı
            analysis = self.morphology.analyze(text)
            lemmas = []
            for result in analysis:
                # Zemberek API'sinin farklı versiyonları için uyumluluk
                if hasattr(result, 'analysis') and result.analysis:
                    lemmas.append(result.analysis[0].dictionary_item.lemma)
                elif hasattr(result, 'dictionary_item') and result.dictionary_item:
                    lemmas.append(result.dictionary_item.lemma)
                elif hasattr(result, 'lemma'):
                    lemmas.append(result.lemma)
                else:
                    # Eğer hiçbiri çalışmazsa, orijinal kelimeyi kullan
                    continue
            
            return " ".join(lemmas).lower() if lemmas else text.lower()
        except Exception as e:
            logger.warning(f"Türkçe ön işleme hatası: {e}")
            return text.lower()
    
    async def _generate_response(self, dialogue: List[Dict[str, str]]) -> str:
        """AI yanıt üretimi - AI'ya mantıklı yönlendirme"""
        try:
            # Son kullanıcı mesajını al
            user_message = ""
            for msg in reversed(dialogue):
                if msg["role"] == "user":
                    user_message = msg["content"]
                    break
            
            logger.info(f"AI modeli yanıt üretiyor: {user_message}")
            
            # GGUF modeli kullan (eğer yüklüyse)
            if self._model_loaded and self.model:
                try:
                    logger.info("GGUF modeli yanıt üretiyor...")
                    
                    # AI'ya mantıklı yönlendirme veren prompt
                    prompt = f"""<|im_start|>system
Sen Choyrens AI, Telekom müşteri hizmetleri asistanısın. Kullanıcıyla mantıklı ve tutarlı bir konuşma yap.

KİŞİLİĞİN:
- Samimi ve yardımsever ol
- Telekom hizmetleri konusunda uzman ol
- Mantıklı ve tutarlı yanıtlar ver
- Kullanıcının sorununu anla ve çözüm öner
- Gereksiz teknik terimler kullanma
- Doğal Türkçe konuş

YANIT TARZIN:
- "Merhaba! Size nasıl yardımcı olabilirim?" gibi samimi
- "Anlıyorum, bu durum gerçekten zor olabilir" gibi empatik
- "Hemen kontrol edeyim" gibi yardımsever
- "Size en uygun çözümü bulacağım" gibi güven verici

MANTIKLI YÖNLENDİRME:
- Kullanıcının sorununu anla
- Uygun Telekom hizmetini öner
- Gerektiğinde araç çağır
- Tutarlı ve anlaşılır yanıtlar ver
- Konu dışına çıkma

ARAÇ ÇAĞRISI: Gerektiğinde araç çağır. Format: [arac_adi]

Telekom araçları:
- get_current_package: Mevcut paket bilgisi
- get_past_bills: Geçmiş faturalar
- get_current_bill: Mevcut fatura
- check_network_status: Ağ durumu
- test_internet_speed: İnternet hızı testi
- get_remaining_quotas: Kalan kotas
- get_available_packages: Kullanılabilir paketler
- get_customer_profile: Müşteri profili
- create_support_ticket: Destek talebi oluşturma
- pay_bill: Fatura ödeme
- setup_autopay: Otomatik ödeme
- get_payment_history: Ödeme geçmişi
- change_package: Paket değiştirme
- get_package_details: Paket detayları
- update_customer_contact: İletişim bilgisi güncelleme
- enable_roaming: Yurtdışı hizmetleri
- suspend_line: Hat askıya alma
- reactivate_line: Hat aktifleştirme
- close_support_ticket: Destek talebi kapatma
- get_support_ticket_status: Destek talebi durumu
- get_user_support_tickets: Destek talepleri listesi
- auth_register: Kayıt olma
- auth_login: Giriş yapma

ÖNEMLİ: Mantıklı ve tutarlı yanıtlar ver, Telekom odaklı kal.
<|im_end|>
<|im_start|>user
{user_message}
<|im_end|>
<|im_start|>assistant
"""
                    
                    # Model çağrısı - mantıklı yönlendirme için optimize edildi
                    response = self.model(
                        prompt,
                        max_tokens=2048,
                        temperature=0.7,  # Daha tutarlı
                        top_p=0.9,  # Daha odaklı
                        repeat_penalty=1.1,  # Tekrarı azalt
                        stop=["<|im_end|>", "<|im_start|>"]
                    )
                    
                    # Response parsing
                    if hasattr(response, 'choices') and response.choices:
                        ai_response = response.choices[0].text.strip()
                    elif hasattr(response, 'text'):
                        ai_response = response.text.strip()
                    elif isinstance(response, dict) and 'choices' in response:
                        ai_response = response['choices'][0]['text'].strip()
                    else:
                        ai_response = str(response).strip()
                    
                    # Response temizleme
                    ai_response = ai_response.replace('<|im_start|>', '').replace('<|im_end|>', '').strip()
                    logger.info(f"🤖 GGUF YANITI: '{ai_response}'")
                    
                    return ai_response
                    
                except Exception as e:
                    logger.warning(f"GGUF modeli hatası, doğal yanıt veriyor: {e}")
            
            # LangChain kullan (eğer mevcutsa ve model yüklüyse)
            if LANGCHAIN_AVAILABLE and self.langchain_chain and self._model_loaded:
                try:
                    import asyncio
                    # Timeout ile invoke kullan
                    loop = asyncio.get_event_loop()
                    response = await asyncio.wait_for(
                        loop.run_in_executor(None, self.langchain_chain.invoke, {"user_input": user_message}),
                        timeout=30.0
                    )
                    logger.info(f"LangChain yanıtı: {response}")
                    return str(response).strip()
                except asyncio.TimeoutError:
                    logger.warning("LangChain timeout, AI doğal yanıt veriyor")
                except Exception as e:
                    logger.warning(f"LangChain hatası, AI doğal yanıt veriyor: {e}")
            
            # AI'nin mantıklı yanıtı
            logger.info("AI mantıklı yanıt veriyor...")
            return "Merhaba! Ben Choyrens AI, Telekom müşteri hizmetleri asistanınızım. Size nasıl yardımcı olabilirim? Fatura, paket, teknik destek veya başka bir konuda sorularınızı yanıtlayabilirim. 😊"
            
        except Exception as e:
            logger.error(f"AI yanıt üretme hatası: {e}")
            return "Üzgünüm, şu anda bir sorun yaşıyorum. Lütfen bir dakika sonra tekrar deneyin! 😅"
    
    async def _parse_tool_calls(self, text: str, session_token: str = None) -> List[AracCagrisi]:
        """AI yanıtından araç çağrılarını parse et - minimum müdahale"""
        arac_cagrilari = []
        
        try:
            # AI yanıtını temizle
            cleaned_text = text.strip()
            logger.info(f"Parse edilecek metin: {cleaned_text}")
            
            # Sadece açık araç çağrılarını bul - AI'nin kendi kararını vermesine izin ver
            import re
            
            # Regex ile araç çağrılarını bul - sadece açık format
            tool_pattern = r'\[([a-zA-Z_]+)\]'
            tool_matches = re.findall(tool_pattern, text)
            
            for tool_name in tool_matches:
                # Basit araç mapping - AI'nin kendi kararını vermesine izin ver
                valid_tools = [
                    "get_current_package", "get_past_bills", "get_current_bill", 
                    "check_network_status", "test_internet_speed", "get_remaining_quotas",
                    "get_available_packages", "get_customer_profile", "create_support_ticket",
                    "pay_bill", "setup_autopay", "get_payment_history", "change_package",
                    "get_package_details", "update_customer_contact", "enable_roaming",
                    "suspend_line", "reactivate_line", "close_support_ticket",
                    "get_support_ticket_status", "get_user_support_tickets",
                    "auth_register", "auth_login"
                ]
                
                if tool_name in valid_tools:
                    parametreler = {"session_token": session_token} if session_token else {}
                    arac_cagrilari.append(AracCagrisi(tool_name, parametreler))
                    logger.info(f"AI araç seçti: {tool_name}")
            
            logger.info(f"AI toplam {len(arac_cagrilari)} araç seçti")
            
        except Exception as e:
            logger.error(f"Araç parse hatası: {e}")
        
        return arac_cagrilari
    
    async def kullanici_mesaj_isle(self, mesaj: str, kullanici_id: str, oturum_id: str, session_token: str = None) -> Dict[str, Any]:
        """Ana mesaj işleme fonksiyonu - AI'ya minimum müdahale"""
        logger.info(f"AI Orchestrator'a iletilen session_token: {session_token}")
        
        try:
            logger.info(f"Kullanıcı mesajı işleniyor: {kullanici_id} - {mesaj[:50]}...")
            
            # Konuşma bağlamını hazırla - AI'nin doğal akışını bozma
            dialogue = [{"role": "user", "content": mesaj}]
            logger.info(f"Bağlam mesaj sayısı: {len(dialogue)}")
            
            # AI yanıtı üret - minimum müdahale
            logger.info("AI yanıtı üretiliyor...")
            ai_response = await self._generate_response(dialogue)
            logger.info(f"AI yanıtı üretildi: {ai_response[:100]}...")
            
            # Araç çağrılarını parse et - sadece açık çağrılar
            logger.info("🔧 ARAÇ PARSE SÜRECİ:")
            arac_cagrilari = await self._parse_tool_calls(ai_response, session_token)
            logger.info(f"📊 Araç çağrısı sayısı: {len(arac_cagrilari)}")
            
            for i, arac in enumerate(arac_cagrilari):
                logger.info(f"   🛠️ Araç {i+1}: {arac.arac_adi}")
                logger.info(f"   📋 Parametreler: {arac.parametreler}")
            
            # Araç çağrılarını yürüt - AI'nin kararını destekle
            if arac_cagrilari:
                logger.info(f"🚀 {len(arac_cagrilari)} ARAÇ YÜRÜTME SÜRECİ:")
                for i, arac in enumerate(arac_cagrilari):
                    logger.info(f"   🔄 Araç {i+1} yürütülüyor: {arac.arac_adi}")
                    try:
                        # Telekom API çağrısı
                        logger.info(f"   📞 Telekom API'ye çağrı yapılıyor...")
                        sonuc = await self._telekom_arac_cagir(arac.arac_adi, arac.parametreler)
                        arac.sonuc = sonuc
                        arac.durum = "tamamlandi"
                        logger.info(f"   ✅ Araç {i+1} başarılı: {arac.arac_adi}")
                        logger.info(f"   📊 Sonuç: {str(sonuc)[:100]}...")
                    except Exception as e:
                        logger.error(f"   ❌ Araç {i+1} hatası: {arac.arac_adi} - {e}")
                        arac.durum = "hata"
                        arac.hata_mesaji = str(e)
            
            # Final yanıt - AI'nin yanıtını koru
            logger.info("Final yanıt hazırlanıyor...")
            final_yanit = ai_response  # AI'nin yanıtını olduğu gibi kullan
            
            # Sonucu hazırla
            sonuc = {
                "yanit_id": f"YANIT_{uuid.uuid4().hex[:8]}",
                "yanit": final_yanit,
                "guven_puani": 0.9 if self._model_loaded else 0.7,
                "arac_cagrilari": [
                    {
                        "arac_adi": arac.arac_adi,
                        "parametreler": arac.parametreler,
                        "durum": arac.durum,
                        "sonuc": arac.sonuc,
                        "hata_mesaji": arac.hata_mesaji
                    }
                    for arac in arac_cagrilari
                ],
                "metadata": {
                    "oturum_id": oturum_id,
                    "kullanici_id": kullanici_id,
                    "islenme_zamani": datetime.now().isoformat(),
                    "baglam_mesaj_sayisi": len(dialogue),
                    "model_loaded": self._model_loaded
                }
            }
            
            logger.info(f"Mesaj işleme tamamlandı: {sonuc['yanit_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Mesaj işleme hatası: {e}")
            # Hata durumunda bile AI yanıtı üret
            return {
                "yanit_id": f"ERROR_{uuid.uuid4().hex[:8]}",
                "yanit": "AI şu anda düşünüyor, lütfen tekrar deneyin.",
                "guven_puani": 0.5,
                "arac_cagrilari": [],
                "metadata": {
                    "oturum_id": oturum_id,
                    "kullanici_id": kullanici_id,
                    "islenme_zamani": datetime.now().isoformat(),
                    "error": str(e)
                }
            }
    
    async def _fallback_response(self, mesaj: str, session_token: str = None) -> Dict[str, Any]:
        """Model yüklenmediğinde fallback yanıt"""
        # Basit keyword detection
        mesaj_lower = mesaj.lower()
        
        if any(word in mesaj_lower for word in ["geçmiş", "fatura", "ödeme"]):
            arac_adi = "get_past_bills"
            parametreler = {"session_token": session_token, "limit": 12} if session_token else {"limit": 12}
        elif any(word in mesaj_lower for word in ["paket", "tarife"]):
            arac_adi = "get_available_packages"
            parametreler = {}
        elif any(word in mesaj_lower for word in ["kota", "kullanım"]):
            arac_adi = "get_remaining_quotas"
            parametreler = {"session_token": session_token} if session_token else {}
        elif any(word in mesaj_lower for word in ["ağ", "bağlantı"]):
            arac_adi = "check_network_status"
            parametreler = {"region": "Istanbul"}
        else:
            arac_adi = "get_past_bills"
            parametreler = {"session_token": session_token, "limit": 12} if session_token else {"limit": 12}
        
        # Araç çağrısı yap
        try:
            sonuc = await self._telekom_arac_cagir(arac_adi, parametreler)
            durum = "tamamlandi"
            hata_mesaji = None
        except Exception as e:
            sonuc = None
            durum = "hata"
            hata_mesaji = str(e)
        
        return {
            "yanit_id": f"FALLBACK_{uuid.uuid4().hex[:8]}",
            "yanit": f"Fallback yanıt: {arac_adi} çağrıldı",
            "guven_puani": 0.5,
            "arac_cagrilari": [
                {
                    "arac_adi": arac_adi,
                    "parametreler": parametreler,
                    "durum": durum,
                    "sonuc": sonuc,
                    "hata_mesaji": hata_mesaji
                }
            ],
            "metadata": {
                "oturum_id": "FALLBACK",
                "kullanici_id": "FALLBACK",
                "islenme_zamani": datetime.now().isoformat(),
                "baglam_mesaj_sayisi": 0
            }
        }
    
    async def _telekom_arac_cagir(self, arac_adi: str, parametreler: Dict[str, Any]) -> Any:
        """Telekom API araç çağrısı"""
        try:
            logger.info(f"AI Telekom araç çağrısı: {arac_adi} - {parametreler}")
            
            # AI endpoint fonksiyonları mapping
            from .ai_endpoint_functions import ai_endpoint_functions
            
            function_mapping = {
                # Fatura İşlemleri
                "get_current_bill": ai_endpoint_functions.telekom_get_current_bill,
                "get_past_bills": ai_endpoint_functions.telekom_get_bill_history,
                "pay_bill": ai_endpoint_functions.telekom_pay_bill,
                "get_payment_history": ai_endpoint_functions.telekom_get_payment_history,
                "setup_autopay": ai_endpoint_functions.telekom_setup_autopay,
                
                # Paket İşlemleri
                "get_current_package": ai_endpoint_functions.telekom_get_current_package,
                "get_available_packages": ai_endpoint_functions.telekom_get_available_packages,
                "change_package": ai_endpoint_functions.telekom_change_package,
                "get_package_details": ai_endpoint_functions.telekom_get_package_details,
                "get_remaining_quotas": ai_endpoint_functions.telekom_get_remaining_quotas,
                
                # Müşteri İşlemleri
                "get_customer_profile": ai_endpoint_functions.telekom_get_customer_profile,
                "update_customer_contact": ai_endpoint_functions.telekom_update_customer_contact,
                "enable_roaming": ai_endpoint_functions.telekom_enable_roaming,
                
                # Ağ ve Teknik İşlemler
                "check_network_status": ai_endpoint_functions.telekom_check_network_status,
                "test_internet_speed": ai_endpoint_functions.telekom_test_internet_speed,
                "suspend_line": ai_endpoint_functions.telekom_suspend_line,
                "reactivate_line": ai_endpoint_functions.telekom_reactivate_line,
                
                # Destek İşlemleri
                "create_support_ticket": ai_endpoint_functions.telekom_create_support_ticket,
                "close_support_ticket": ai_endpoint_functions.telekom_close_support_ticket,
                "get_support_ticket_status": ai_endpoint_functions.telekom_get_support_ticket_status,
                "get_user_support_tickets": ai_endpoint_functions.telekom_get_user_support_tickets,
                
                # Kimlik Doğrulama
                "auth_register": ai_endpoint_functions.telekom_auth_register,
                "auth_login": ai_endpoint_functions.telekom_auth_login,
            }
            
            if arac_adi not in function_mapping:
                logger.warning(f"Bilinmeyen araç: {arac_adi}")
                return None
            
            # Fonksiyonu çağır
            function = function_mapping[arac_adi]
            logger.info(f"Araç çağrısı: {arac_adi} -> {function.__name__}")
            result = await function(**parametreler)
            
            logger.info(f"AI Telekom API yanıtı: {result}")
            logger.info(f"Araç {arac_adi} sonucu başarılı: {result.get('success', False)}")
            return result
            
        except Exception as e:
            logger.error(f"AI Telekom araç çağrısı hatası: {e}")
            raise
    
    async def sistem_durumu_getir(self) -> Dict[str, Any]:
        """Sistem durumu bilgilerini getir"""
        return {
            "status": "healthy",
            "model_loaded": self._model_loaded,
            "model_name": self.model_name,
            "turkish_nlp": ZEMBEREK_AVAILABLE,
            "langchain_available": LANGCHAIN_AVAILABLE,
            "timestamp": datetime.now().isoformat(),
            "version": "2.2.0",
            "ai_guidance_level": "logical"  # AI'nin mantıklı yönlendirme seviyesi
        }

# Global orkestratör örneği
ai_orchestrator = YapayZekaOrkestratori() 