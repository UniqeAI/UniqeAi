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
    from langchain.llms import HuggingFacePipeline
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
        
        # Model adı - GGUF Telekom AI modeli
        self.model_name = "Choyrens/ChoyrensAI-Telekom-Agent-v4-gguf"
        
        # Yeni model yolu
        self.local_model_path = r"C:\Users\erkan\Desktop\ChoyrensAi-models\choyrens_model_v4_gguf"
        
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
                
                # Yeni model yolu ile yükle
                model_path = self.local_model_path
                
                logger.info(f"Model dosyası: {model_path}")
                
                # GGUF model yükleme - llama-cpp-python ile
                self.model = Llama(
                    model_path=model_path,
                    n_ctx=2048,  # Context length
                    n_threads=4,  # Thread sayısı
                    n_batch=1,  # Batch size
                    verbose=False  # Verbose kapalı
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
            
            # Prompt template
            template = """Sen bir Telekom AI asistanısın. Kullanıcının sorununu anla ve uygun aracı seç.

Mevcut araçlar:
- get_past_bills: Geçmiş faturalar
- get_current_bill: Mevcut fatura
- get_available_packages: Kullanılabilir paketler
- get_remaining_quotas: Kalan kotas
- check_network_status: Ağ durumu
- test_internet_speed: İnternet hızı testi

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
            # Zemberek ile lemmatization
            analysis = self.morphology.analyze(text)
            lemmas = []
            for result in analysis:
                if result.analysis:
                    lemmas.append(result.analysis[0].dictionary_item.lemma)
            
            return " ".join(lemmas).lower() if lemmas else text.lower()
        except Exception as e:
            logger.warning(f"Türkçe ön işleme hatası: {e}")
            return text.lower()
    
    def _create_system_prompt(self, mevcut_araclar: Dict[str, Any]) -> str:
        """Gelişmiş sistem promptu oluştur"""
        
        return f"""Sen bir Telekom AI asistanısın. Kullanıcının sorununu anla ve uygun aracı seç.

Mevcut araçlar:
- get_past_bills: Geçmiş faturalar (geçmiş faturalarım, önceki faturalar)
- get_current_bill: Mevcut fatura (şu anki fatura, güncel fatura)
- get_available_packages: Kullanılabilir paketler (paketler, tarifeler)
- get_remaining_quotas: Kalan kotas (kota, kullanım)
- check_network_status: Ağ durumu (ağ, bağlantı)
- test_internet_speed: İnternet hızı testi (hız testi, speed test)

Kurallar:
- Sadece tek bir araç seç
- Liste yapma, açıklama yapma
- Sadece araç adını yaz

Örnekler:
- "geçmiş faturalarım" → get_past_bills
- "ağ durumu" → check_network_status
- "paketler" → get_available_packages

Kullanıcı sorusu: """
    
    async def _generate_response(self, dialogue: List[Dict[str, str]]) -> str:
        """Gelişmiş AI yanıt üretimi"""
        try:
            # Son kullanıcı mesajını al
            user_message = ""
            for msg in reversed(dialogue):
                if msg["role"] == "user":
                    user_message = msg["content"]
                    break
            
            logger.info(f"AI modeli yanıt üretiyor: {user_message}")
            
            # AI düşünce süreci başlıyor
            logger.info("🤔 AI DÜŞÜNCE SÜRECİ BAŞLIYOR...")
            logger.info(f"📝 Gelen mesaj: '{user_message}'")
            
            # Türkçe ön işleme
            processed_message = self._turkish_preprocessing(user_message)
            logger.info(f"🔧 İşlenmiş mesaj: '{processed_message}'")
            
            # AI analiz süreci
            logger.info("🔍 AI MESAJ ANALİZİ:")
            if "konya" in processed_message.lower():
                logger.info("   📍 Konum tespit edildi: Konya")
            if "telefon" in processed_message.lower() or "çekmiyor" in processed_message.lower():
                logger.info("   📱 Telefon/ağ sorunu tespit edildi")
            if "fatura" in processed_message.lower() or "ödeme" in processed_message.lower():
                logger.info("   💰 Fatura/ödeme konusu tespit edildi")
            if "paket" in processed_message.lower():
                logger.info("   📦 Paket konusu tespit edildi")
            if "kota" in processed_message.lower():
                logger.info("   📊 Kota konusu tespit edildi")
            
            # GGUF modeli kullan (eğer yüklüyse)
            if self._model_loaded and self.model:
                try:
                    logger.info("GGUF modeli yanıt üretiyor...")
                    
                    # GGUF modeli ile yanıt üret
                    response = self.model(
                        f"""Sen bir Telekom müşteri hizmetleri asistanısın. Kullanıcının mesajını analiz et ve düşünce sürecini göster.

DÜŞÜNCE SÜRECİ:
1. Kullanıcının konumunu ve durumunu analiz et
2. Hangi Telekom hizmeti ile ilgili olduğunu belirle
3. Uygun aracı seç ve nedenini açıkla
4. Doğal bir yanıt ver

Örnek düşünce süreci:
- "konya yolundayım telefonum çekmiyor" 
  → Kullanıcı Konya'da, telefon çekmiyor
  → Ağ durumu sorunu var
  → check_network_status aracını kullanmalıyım
  → "Konya'da telefon çekme sorunu yaşıyorsunuz. Ağ durumunu kontrol ediyorum. [check_network_status]"

Telekom araçları:
- get_past_bills: Geçmiş faturalar, önceki faturalar, fatura geçmişi
- get_current_bill: Mevcut fatura, şu anki fatura, güncel fatura
- get_available_packages: Kullanılabilir paketler, tarifeler, paket seçenekleri
- get_remaining_quotas: Kalan kota, kullanım durumu, data kullanımı
- check_network_status: Ağ durumu, bağlantı durumu, sinyal
- test_internet_speed: İnternet hızı testi, speed test

Kullanıcı: {processed_message}
Asistan:""",
                        max_tokens=100,
                        temperature=0.3,
                        stop=["Kullanıcı:", "\n\n"]
                    )
                    
                    ai_response = response['choices'][0]['text'].strip()
                    logger.info(f"🤖 GGUF YANITI: '{ai_response}'")
                    
                    # AI düşünce süreci analizi
                    logger.info("🧠 AI DÜŞÜNCE ANALİZİ:")
                    if "check_network_status" in ai_response.lower():
                        logger.info("   ✅ Ağ durumu aracı seçildi")
                    if "get_past_bills" in ai_response.lower():
                        logger.info("   ✅ Geçmiş faturalar aracı seçildi")
                    if "get_available_packages" in ai_response.lower():
                        logger.info("   ✅ Kullanılabilir paketler aracı seçildi")
                    if "get_remaining_quotas" in ai_response.lower():
                        logger.info("   ✅ Kalan kotalar aracı seçildi")
                    
                    logger.info("🎯 AI DÜŞÜNCE SÜRECİ TAMAMLANDI")
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
                        loop.run_in_executor(None, self.langchain_chain.invoke, {"user_input": processed_message}),
                        timeout=30.0  # 30 saniye timeout (artırıldı)
                    )
                    logger.info(f"LangChain yanıtı: {response}")
                    return str(response).strip()
                except asyncio.TimeoutError:
                    logger.warning("LangChain timeout, AI doğal yanıt veriyor")
                except Exception as e:
                    logger.warning(f"LangChain hatası, AI doğal yanıt veriyor: {e}")
            
            # AI'nin kendi karar vermesi - gelişmiş keyword detection
            logger.info("AI kendi kararını veriyor...")
            
            # AI sadece LangChain ile karar verir, keyword detection yok
            # Eğer LangChain timeout olursa, AI doğal yanıt verir
            return "Anlıyorum. Size en uygun hizmeti bulmak için düşünüyorum. Hangi konuda yardım istiyorsunuz?"
            
        except Exception as e:
            logger.error(f"AI yanıt üretme hatası: {e}")
            return "AI şu anda düşünüyor, lütfen tekrar deneyin."
    
    async def _parse_tool_calls(self, text: str, session_token: str = None) -> List[AracCagrisi]:
        """AI yanıtından araç çağrılarını parse et"""
        arac_cagrilari = []
        
        try:
            # AI yanıtını temizle
            cleaned_text = text.strip().lower()
            logger.info(f"Parse edilecek metin: {cleaned_text}")
            
            # AI sadece LangChain yanıtını parse eder
            # Keyword detection yok - AI kendi kararını verir
            
            # Eğer AI araç adı döndürdüyse, onu kullan
            # Format: "Açıklama. [get_past_bills]" veya sadece "get_past_bills"
            if "get_past_bills" in cleaned_text:
                arac_adi = "get_past_bills"
                parametreler = {"session_token": session_token} if session_token else {}
                arac_cagrilari.append(AracCagrisi(arac_adi, parametreler))
                logger.info(f"AI araç seçti: {arac_adi}")
                
            elif "get_current_bill" in cleaned_text:
                arac_adi = "get_current_bill"
                parametreler = {"session_token": session_token} if session_token else {}
                arac_cagrilari.append(AracCagrisi(arac_adi, parametreler))
                logger.info(f"AI araç seçti: {arac_adi}")
                
            elif "get_available_packages" in cleaned_text:
                arac_adi = "get_available_packages"
                parametreler = {}
                arac_cagrilari.append(AracCagrisi(arac_adi, parametreler))
                logger.info(f"AI araç seçti: {arac_adi}")
                
            elif "get_remaining_quotas" in cleaned_text:
                arac_adi = "get_remaining_quotas"
                parametreler = {"session_token": session_token} if session_token else {}
                arac_cagrilari.append(AracCagrisi(arac_adi, parametreler))
                logger.info(f"AI araç seçti: {arac_adi}")
                
            elif "check_network_status" in cleaned_text:
                arac_adi = "check_network_status"
                parametreler = {"session_token": session_token} if session_token else {}
                arac_cagrilari.append(AracCagrisi(arac_adi, parametreler))
                logger.info(f"AI araç seçti: {arac_adi}")
                
            elif "test_internet_speed" in cleaned_text:
                arac_adi = "test_internet_speed"
                parametreler = {}
                arac_cagrilari.append(AracCagrisi(arac_adi, parametreler))
                logger.info(f"AI araç seçti: {arac_adi}")
            
            logger.info(f"AI toplam {len(arac_cagrilari)} araç seçti")
            
        except Exception as e:
            logger.error(f"Araç parse hatası: {e}")
        
        return arac_cagrilari
    
    async def kullanici_mesaj_isle(self, mesaj: str, kullanici_id: str, oturum_id: str, session_token: str = None) -> Dict[str, Any]:
        """Ana mesaj işleme fonksiyonu"""
        logger.info(f"AI Orchestrator'a iletilen session_token: {session_token}")
        
        try:
            logger.info(f"Kullanıcı mesajı işleniyor: {kullanici_id} - {mesaj[:50]}...")
            
            # Mesajı ön işle
            islenmis_mesaj = self._turkish_preprocessing(mesaj)
            logger.info(f"İşlenmiş mesaj: {islenmis_mesaj}")
            
            # Konuşma bağlamını hazırla
            dialogue = [{"role": "user", "content": islenmis_mesaj}]
            logger.info(f"Bağlam mesaj sayısı: {len(dialogue)}")
            
            # Mevcut araçları hazırla
            mevcut_araclar = {
                "get_past_bills": "Geçmiş faturalar",
                "get_current_bill": "Mevcut fatura",
                "get_available_packages": "Kullanılabilir paketler",
                "get_remaining_quotas": "Kalan kotas",
                "check_network_status": "Ağ durumu",
                "test_internet_speed": "İnternet hızı testi"
            }
            logger.info(f"Mevcut araç sayısı: {len(mevcut_araclar)}")
            
            # AI yanıtı üret (model yüklenmese bile)
            logger.info("AI yanıtı üretiliyor...")
            ai_response = await self._generate_response(dialogue)
            logger.info(f"AI yanıtı üretildi: {ai_response[:100]}...")
            
            # Araç çağrılarını parse et
            logger.info("🔧 ARAÇ PARSE SÜRECİ:")
            arac_cagrilari = await self._parse_tool_calls(ai_response, session_token)
            logger.info(f"📊 Araç çağrısı sayısı: {len(arac_cagrilari)}")
            
            for i, arac in enumerate(arac_cagrilari):
                logger.info(f"   🛠️ Araç {i+1}: {arac.arac_adi}")
                logger.info(f"   📋 Parametreler: {arac.parametreler}")
            
            # Araç çağrılarını yürüt
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
            
            # Final yanıt üret
            logger.info("Final yanıt üretiliyor...")
            final_yanit = self._arac_sonuclarini_entegre_et(ai_response, arac_cagrilari)
            logger.info(f"Final yanıt: {final_yanit[:100]}...")
            
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
                "get_current_bill": ai_endpoint_functions.telekom_get_current_bill,
                "get_past_bills": ai_endpoint_functions.telekom_get_bill_history,
                "get_available_packages": ai_endpoint_functions.telekom_get_available_packages,
                "get_remaining_quotas": ai_endpoint_functions.telekom_get_remaining_quotas,
                "check_network_status": ai_endpoint_functions.telekom_check_network_status,
                "test_internet_speed": ai_endpoint_functions.telekom_test_internet_speed,
            }
            
            if arac_adi not in function_mapping:
                logger.warning(f"Bilinmeyen araç: {arac_adi}")
                return None
            
            # Fonksiyonu çağır
            function = function_mapping[arac_adi]
            logger.info(f"Araç çağrısı: {arac_adi} -> {function.__name__}")
            result = await function(**parametreler)
            
            logger.info(f"AI Telekom API yanıtı: {result}")
            return result
            
        except Exception as e:
            logger.error(f"AI Telekom araç çağrısı hatası: {e}")
            raise
    
    def _arac_sonuclarini_entegre_et(self, temel_yanit: str, arac_sonuclari: List[AracCagrisi]) -> str:
        """Araç sonuçlarını yanıta entegre et"""
        if not arac_sonuclari:
            return temel_yanit
        
        # Basit entegrasyon
        basarili_sonuclar = [arac for arac in arac_sonuclari if arac.durum == "tamamlandi"]
        
        if basarili_sonuclar:
            return f"İşleminiz tamamlandı. {len(basarili_sonuclar)} araç başarıyla çalıştırıldı."
        else:
            return "Üzgünüm, işleminiz sırasında bir hata oluştu."
    
    async def sistem_durumu_getir(self) -> Dict[str, Any]:
        """Sistem durumu bilgilerini getir"""
        return {
            "status": "healthy",
            "model_loaded": self._model_loaded,
            "model_name": self.model_name,
            "turkish_nlp": ZEMBEREK_AVAILABLE,
            "langchain_available": LANGCHAIN_AVAILABLE,
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        }

# Global orkestratör örneği
ai_orchestrator = YapayZekaOrkestratori() 