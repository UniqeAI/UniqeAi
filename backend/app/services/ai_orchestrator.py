import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import uuid

from .telekom_api import telekom_api
from .ai_endpoint_functions import ai_endpoint_functions

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class LlamaInferenceService:
    """Llama model hizmeti simülasyonu"""
    
    def __init__(self):
        self.model_adi = "llama-2-7b-chat"
    
    async def yanit_uret(self, mesaj: str, baglam: List[KonusmaMesaji], mevcut_araclar: Dict[str, Any]) -> AIYaniti:
        """Yapay zeka yanıtı üret"""
        logger.info(f"AI yanıtı üretiliyor: {mesaj[:50]}...")
        
        # Simüle edilmiş işlem süresi
        await asyncio.sleep(0.3)
        
        # Basit araç çağrısı tespiti (gerçek uygulamada daha gelişmiş NLP kullanılır)
        arac_cagrilari = self._arac_cagrilari_tespit_et(mesaj)
        
        # Yanıt üretimi
        islenmis_yanit = self._yanit_uret(mesaj, arac_cagrilari)
        
        return AIYaniti(
            yanit_id=f"YANIT_{uuid.uuid4().hex[:8]}",
            orijinal_mesaj=mesaj,
            islenmis_yanit=islenmis_yanit,
            arac_cagrilari=arac_cagrilari,
            guven_puani=0.85
        )
    
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
        import re
        
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
        
        if basarili_sonuclar:
            yanit_parcalari.append("İşlemler başarıyla tamamlandı.")
        
        if hatali_sonuclar:
            yanit_parcalari.append("Bazı işlemlerde sorun oluştu, lütfen tekrar deneyin.")
        
        return " ".join(yanit_parcalari)

class YapayZekaOrkestratori:
    """Ana yapay zeka orkestratörü"""
    
    def __init__(self):
        self.model_hizmeti = LlamaInferenceService()
        self.konusma_yoneticisi = KonusmaYoneticisi()
        self.arac_kaydi = TelekomAracKaydi()
        self.telekom_api = telekom_api
    
    async def kullanici_mesaj_isle(self, mesaj: str, kullanici_id: str, oturum_id: str) -> Dict[str, Any]:
        """Kullanıcı mesajını işle ve yanıt üret"""
        try:
            logger.info(f"Kullanıcı mesajı işleniyor: {kullanici_id} - {mesaj[:50]}...")
            
            # Mesajı ön işle
            islenmis_mesaj = self.turkce_on_isle(mesaj)
            
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
            
            # Mevcut araçları getir
            mevcut_araclar = self.arac_kaydi.mevcut_araclari_getir()
            
            # AI yanıtı üret
            ai_yaniti = await self.model_hizmeti.yanit_uret(islenmis_mesaj, baglam, mevcut_araclar)
            
            # Araç çağrılarını yürüt
            if ai_yaniti.arac_cagrilari:
                logger.info(f"{len(ai_yaniti.arac_cagrilari)} araç çağrısı yürütülüyor...")
                arac_sonuclari = await self.arac_cagrilari_yurut(ai_yaniti.arac_cagrilari)
                
                # Final yanıt üret
                final_yanit = await self.model_hizmeti.final_yanit_uret(ai_yaniti, arac_sonuclari)
            else:
                final_yanit = ai_yaniti.islenmis_yanit
                arac_sonuclari = []
            
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
                "reactivate_line": ai_endpoint_functions.telekom_reactivate_line
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
    
    async def oturum_temizle(self, oturum_id: str):
        """Oturum konuşma geçmişini temizle"""
        await self.konusma_yoneticisi.konusma_temizle(oturum_id)
        logger.info(f"Oturum temizlendi: {oturum_id}")
    
    async def sistem_durumu_getir(self) -> Dict[str, Any]:
        """Sistem durumu bilgilerini getir"""
        return {
            "model_hizmeti": {
                "model_adi": self.model_hizmeti.model_adi
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