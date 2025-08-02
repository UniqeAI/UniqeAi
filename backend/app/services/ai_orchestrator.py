import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import uuid

from .telekom_api import telekom_api
from .ai_endpoint_functions import ai_endpoint_functions
from .user_service import user_service

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
class AracCagrisiLegacy:
    """Araç çağrısı yapısı (legacy)"""
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
    arac_cagrilari: List[AracCagrisiLegacy]
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
            
            # PAKET & TARİFE İŞLEMLERİ
            "get_customer_package": {
                "aciklama": "Müşterinin mevcut paket bilgilerini getirir",
                "parametreler": ["user_id"]
            },
            "get_remaining_quotas": {
                "aciklama": "Kalan kotaları getirir",
                "parametreler": ["user_id"]
            },
            "change_package": {
                "aciklama": "Paket değiştirme işlemi",
                "parametreler": ["user_id", "new_package_id"]
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
                "aciklama": "Yurt dışı kullanım ayarları",
                "parametreler": ["user_id", "status"]
            },
            
            # TEKNİK DESTEK İŞLEMLERİ
            "check_network_status": {
                "aciklama": "Ağ durumu kontrolü",
                "parametreler": ["region"]
            },
            "create_fault_ticket": {
                "aciklama": "Arıza kaydı oluşturur",
                "parametreler": ["user_id", "issue_description", "category"]
            },
            "get_fault_ticket_status": {
                "aciklama": "Arıza kaydı durumu",
                "parametreler": ["ticket_id"]
            },
            "test_internet_speed": {
                "aciklama": "İnternet hız testi",
                "parametreler": ["user_id"]
            },
            
            # HESAP YÖNETİMİ
            "get_customer_profile": {
                "aciklama": "Müşteri profili bilgileri",
                "parametreler": ["user_id"]
            },
            "update_customer_contact": {
                "aciklama": "İletişim bilgilerini güncelle",
                "parametreler": ["user_id", "contact_info"]
            },
            "suspend_line": {
                "aciklama": "Hat askıya alma",
                "parametreler": ["user_id", "reason"]
            },
            "reactivate_line": {
                "aciklama": "Hat yeniden aktifleştirme",
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
        """Mevcut araçları getir"""
        return self.kayitli_araclar
    
    def arac_var_mi(self, arac_adi: str) -> bool:
        """Araç kayıtlı mı kontrol et"""
        return arac_adi in self.kayitli_araclar
    
    def arac_bilgisi_getir(self, arac_adi: str) -> Optional[Dict[str, Any]]:
        """Araç bilgilerini getir"""
        return self.kayitli_araclar.get(arac_adi)

class MockInferenceService:
    """Mock AI inference servisi"""
    
    def __init__(self):
        self.function_mapping = self._create_function_mapping()
    
    def _create_function_mapping(self) -> Dict[str, callable]:
        """Mock fonksiyon mapping'i oluştur"""
        def mock_get_current_bill(user_id: int):
            return {
                "success": True,
                "data": {
                    "amount": 150.0,
                    "due_date": "2024-03-15",
                    "status": "unpaid",
                    "bill_id": f"F-2024-{user_id:04d}-01"
                }
            }
        
        def mock_get_bill_history(user_id: int, limit: int = 12):
            return {
                "success": True,
                "data": {
                    "bills": [
                        {
                            "bill_id": f"F-2024-{user_id:04d}-{i:02d}",
                            "amount": 150 + (i * 5),
                            "status": "paid" if i < 11 else "unpaid"
                        } for i in range(limit)
                    ]
                }
            }
        
        def mock_pay_bill(bill_id: str, method: str = "kredi_karti"):
            return {
                "success": True,
                "data": {
                    "payment_id": f"PAY-{bill_id}",
                    "status": "completed",
                    "method": method
                }
            }
        
        def mock_get_current_package(user_id: int):
            return {
                "success": True,
                "data": {
                    "package_name": "Mega İnternet",
                    "monthly_fee": 150.0,
                    "data_limit": "50 GB",
                    "voice_limit": "1000 dakika"
                }
            }
        
        def mock_get_remaining_quotas(user_id: int):
            return {
                "success": True,
                "data": {
                    "data_remaining": "25.5 GB",
                    "voice_remaining": "750 dakika",
                    "sms_remaining": "250 SMS"
                }
            }
        
        def mock_change_package(user_id: int, new_package_id: str):
            return {
                "success": True,
                "data": {
                    "old_package": "Mega İnternet",
                    "new_package": new_package_id,
                    "change_date": "2024-03-01"
                }
            }
        
        def mock_create_support_ticket(user_id: int, issue_description: str, category: str = "technical"):
            return {
                "success": True,
                "data": {
                    "ticket_id": f"T-2024-{user_id:04d}-001",
                    "status": "open",
                    "category": category,
                    "description": issue_description
                }
            }
        
        def mock_get_support_ticket_status(ticket_id: str):
            return {
                "success": True,
                "data": {
                    "ticket_id": ticket_id,
                    "status": "in_progress",
                    "estimated_resolution": "24 saat"
                }
            }
        
        def mock_get_customer_profile(user_id: int):
            return {
                "success": True,
                "data": {
                    "name": "Ahmet Yılmaz",
                    "phone": "05321234567",
                    "email": "ahmet.yilmaz@email.com",
                    "customer_level": "premium"
                }
            }
        
        def mock_update_customer_contact(user_id: int, contact_info: dict):
            return {
                "success": True,
                "data": {
                    "updated_fields": list(contact_info.keys()),
                    "update_date": "2024-03-01"
                }
            }
        
        return {
            # FATURA & ÖDEME
            "get_current_bill": mock_get_current_bill,
            "get_past_bills": mock_get_bill_history,
            "pay_bill": mock_pay_bill,
            "get_payment_history": lambda user_id: {"success": True, "data": {"payments": []}},
            "setup_autopay": lambda user_id, status: {"success": True, "data": {"autopay_enabled": status}},
            
            # PAKET & TARİFE
            "get_customer_package": mock_get_current_package,
            "get_remaining_quotas": mock_get_remaining_quotas,
            "change_package": mock_change_package,
            "get_available_packages": lambda: {"success": True, "data": {"packages": []}},
            "get_package_details": lambda package_name: {"success": True, "data": {}},
            "enable_roaming": lambda user_id, status: {"success": True, "data": {"roaming_enabled": status}},
            
            # TEKNİK DESTEK
            "check_network_status": lambda region: {"success": True, "data": {"status": "operational"}},
            "create_fault_ticket": mock_create_support_ticket,
            "get_fault_ticket_status": mock_get_support_ticket_status,
            "test_internet_speed": lambda user_id: {"success": True, "data": {"speed": "50 Mbps"}},
            
            # HESAP YÖNETİMİ
            "get_customer_profile": mock_get_customer_profile,
            "update_customer_contact": mock_update_customer_contact,
            "suspend_line": lambda user_id, reason: {"success": True, "data": {"status": "suspended"}},
            "reactivate_line": lambda user_id: {"success": True, "data": {"status": "active"}},
            
            # KULLANICI YÖNETİMİ
            "register_user": lambda email, password, name: {"success": True, "data": {"user_id": 123, "email": email, "name": name}},
            "login_user": lambda email, password: {"success": True, "data": {"user_id": 123, "email": email}},
            "get_user_by_id": lambda user_id: {"success": True, "data": {"user_id": user_id, "email": "user@example.com"}},
            "update_user": lambda user_id, update_data: {"success": True, "data": {"user_id": user_id, "updated": True}},
            "logout_user": lambda: {"success": True, "data": {"logged_out": True}},
            "get_all_active_users": lambda: {"success": True, "data": {"users": [{"user_id": 1, "email": "user1@example.com"}]}},
            
            # TELEKOM AUTH
            "telekom_register": lambda email, password, name: {"success": True, "data": {"user_id": 456, "email": email, "name": name}},
            "telekom_login": lambda email, password: {"success": True, "data": {"user_id": 456, "email": email}},
            
            # TELEKOM DESTEK EK
            "close_support_ticket": lambda ticket_id: {"success": True, "data": {"ticket_id": ticket_id, "status": "closed"}},
            "get_user_support_tickets": lambda user_id: {"success": True, "data": {"tickets": [{"ticket_id": f"T-{user_id}-001", "status": "open"}]}},
            
            # MOCK TEST ENDPOINT'LERİ
            "mock_get_user_info": lambda user_id: {"success": True, "data": {"user_id": user_id, "name": f"Mock User {user_id}"}},
            "mock_get_available_packages": lambda: {"success": True, "data": {"packages": [{"name": "Basic", "price": 29.99}]}},
            "mock_get_invoice": lambda user_id: {"success": True, "data": {"invoice_id": f"INV-{user_id}", "amount": 49.99}},
            "mock_get_customer_info": lambda user_id: {"success": True, "data": {"user_id": user_id, "name": f"Mock Customer {user_id}"}},
            "mock_get_payment_history": lambda user_id: {"success": True, "data": {"payments": [{"payment_id": f"PAY-{user_id}-1", "amount": 49.99}]}},
            "mock_get_subscription_status": lambda user_id: {"success": True, "data": {"user_id": user_id, "status": "active"}},
            "mock_get_support_tickets": lambda user_id: {"success": True, "data": {"tickets": [{"ticket_id": f"TICKET-{user_id}-1", "status": "open"}]}},
            "mock_get_address": lambda user_id: {"success": True, "data": {"user_id": user_id, "street": f"Mock Street {user_id}"}},
            "mock_get_campaigns": lambda: {"success": True, "data": {"campaigns": [{"id": 1, "name": "Mock Campaign"}]}},
            
            # SİSTEM ENDPOINT'LERİ
            "get_system_health": lambda: {"success": True, "data": {"status": "ok", "timestamp": "2024-03-01T10:00:00Z"}},
            "get_ai_model_info": lambda: {"success": True, "data": {"model_type": "Mock AI Model", "is_mock_mode": True}}
        }
    
    async def yanit_uret(self, mesaj: str, baglam: List[KonusmaMesaji], mevcut_araclar: Dict[str, Any]) -> AIYaniti:
        """Mock AI yanıtı üret"""
        try:
            # Basit anahtar kelime tabanlı yanıt üretimi
            mesaj_lower = mesaj.lower()
            
            if "fatura" in mesaj_lower:
                yanit = "Mevcut faturanızı kontrol ediyorum. Fatura bilgileriniz: 150 TL, son ödeme tarihi: 15 Mart 2024."
                arac_cagrilari = [AracCagrisiLegacy(
                    arac_adi="get_current_bill",
                    parametreler={"user_id": 1},
                    durum="beklemede"
                )]
            elif "paket" in mesaj_lower:
                yanit = "Paket bilgilerinizi kontrol ediyorum. Aktif paketiniz: Mega İnternet, aylık ücret: 150 TL."
                arac_cagrilari = [AracCagrisiLegacy(
                    arac_adi="get_customer_package",
                    parametreler={"user_id": 1},
                    durum="beklemede"
                )]
            elif "arıza" in mesaj_lower or "sorun" in mesaj_lower:
                yanit = "Teknik sorununuzu anlıyorum. Arıza kaydı oluşturuyorum."
                arac_cagrilari = [AracCagrisiLegacy(
                    arac_adi="create_fault_ticket",
                    parametreler={
                        "user_id": 1,
                        "issue_description": "Kullanıcı arıza bildirdi",
                        "category": "technical"
                    },
                    durum="beklemede"
                )]
            elif "kota" in mesaj_lower or "kalan" in mesaj_lower:
                yanit = "Kalan kotalarınızı kontrol ediyorum. Veri: 25.5 GB, Dakika: 750, SMS: 250 kaldı."
                arac_cagrilari = [AracCagrisiLegacy(
                    arac_adi="get_remaining_quotas",
                    parametreler={"user_id": 1},
                    durum="beklemede"
                )]
            else:
                yanit = "Merhaba! Size nasıl yardımcı olabilirim? Fatura, paket, teknik destek konularında yardım edebilirim."
                arac_cagrilari = []
            
            return AIYaniti(
                yanit_id=str(uuid.uuid4()),
                orijinal_mesaj=mesaj,
                islenmis_yanit=yanit,
                arac_cagrilari=arac_cagrilari,
                guven_puani=0.95
            )
            
        except Exception as e:
            logger.error(f"Mock AI yanıt üretme hatası: {e}")
            return AIYaniti(
                yanit_id=str(uuid.uuid4()),
                orijinal_mesaj=mesaj,
                islenmis_yanit="Anlayamadım, lütfen tekrar açıklar mısınız?",
                arac_cagrilari=[],
                guven_puani=0.3
            )
    
    async def final_yanit_uret(self, orijinal_yanit: AIYaniti, arac_sonuclari: List[AracCagrisiLegacy]) -> str:
        """Araç sonuçlarını kullanarak final yanıt oluştur"""
        
        if not arac_sonuclari:
            return orijinal_yanit.islenmis_yanit
        
        # Araç sonuçlarını analiz et
        basarili_sonuclar = [r for r in arac_sonuclari if r.durum == "tamamlandi"]
        
        if not basarili_sonuclar:
            return "Üzgünüm, şu anda bu bilgilere ulaşamıyorum. Lütfen daha sonra tekrar deneyin."
        
        # Sonuçları formatla
        yanit_parcalari = [orijinal_yanit.islenmis_yanit]
        
        for sonuc in basarili_sonuclar:
            if sonuc.arac_adi == "get_current_bill":
                data = sonuc.sonuc.get("data", {})
                yanit_parcalari.append(
                    f"\n💰 Mevcut faturanız: {data.get('amount', 'N/A')} TL\n"
                    f"📅 Son ödeme tarihi: {data.get('due_date', 'N/A')}\n"
                    f"📊 Durum: {data.get('status', 'N/A')}"
                )
            elif sonuc.arac_adi == "get_customer_package":
                data = sonuc.sonuc.get("data", {})
                yanit_parcalari.append(
                    f"\n📦 Paketiniz: {data.get('package_name', 'N/A')}\n"
                    f"💵 Aylık ücret: {data.get('monthly_fee', 'N/A')} TL"
                )
        
        return "\n".join(yanit_parcalari)

class YapayZekaOrkestratori:
    """Ana AI orkestratör sınıfı"""
    
    def __init__(self):
        self.konusma_yoneticisi = KonusmaYoneticisi()
        self.telekom_arac_kaydi = TelekomAracKaydi()
        self.mock_inference = MockInferenceService()
    
    async def kullanici_mesaj_isle(self, mesaj: str, kullanici_id: str, oturum_id: str) -> Dict[str, Any]:
        """Kullanıcı mesajını işle ve uygun yanıtı döndür"""
        try:
            # 1. Mesajı konuşma geçmişine ekle
            kullanici_mesaji = KonusmaMesaji(
                mesaj_id=str(uuid.uuid4()),
                kullanici_id=kullanici_id,
                icerik=mesaj,
                zaman_damgasi=datetime.now().isoformat(),
                mesaj_tipi="kullanici"
            )
            
            await self.konusma_yoneticisi.mesaj_ekle(oturum_id, kullanici_mesaji)
            
            # 2. Konuşma bağlamını al
            baglam = await self.konusma_yoneticisi.baglam_getir(oturum_id)
            
            # 3. Mevcut araçları al
            mevcut_araclar = self.telekom_arac_kaydi.mevcut_araclari_getir()
            
            # 4. AI yanıtını al
            ai_yaniti = await self.mock_inference.yanit_uret(mesaj, baglam, mevcut_araclar)
            
            # 5. Araç çağrılarını çalıştır
            arac_sonuclari = await self.arac_cagrilari_yurut(ai_yaniti.arac_cagrilari)
                
            # 6. Final yanıtı oluştur
            final_yanit = await self.mock_inference.final_yanit_uret(ai_yaniti, arac_sonuclari)
            
            # 7. AI yanıtını konuşma geçmişine ekle
            ai_mesaji = KonusmaMesaji(
                mesaj_id=str(uuid.uuid4()),
                kullanici_id="ai",
                icerik=final_yanit,
                zaman_damgasi=datetime.now().isoformat(),
                mesaj_tipi="ai"
            )
            
            await self.konusma_yoneticisi.mesaj_ekle(oturum_id, ai_mesaji)
            
            return {
                "yanit_id": ai_yaniti.yanit_id,
                "yanit": final_yanit,
                "guven_puani": ai_yaniti.guven_puani,
                "arac_cagrilari": [
                    {
                        "arac_adi": arac.arac_adi,
                        "parametreler": arac.parametreler,
                        "durum": arac.durum,
                        "sonuc": arac.sonuc
                    } for arac in arac_sonuclari
                ],
                "metadata": {
                    "oturum_id": oturum_id,
                    "kullanici_id": kullanici_id,
                    "islem_zamani": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Mesaj işleme hatası: {e}")
            return {
                "yanit_id": str(uuid.uuid4()),
                "yanit": "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.",
                "guven_puani": 0.0,
                "arac_cagrilari": [],
                "metadata": {
                    "hata": str(e),
                    "oturum_id": oturum_id,
                    "kullanici_id": kullanici_id
                }
            }
    
    def turkce_on_isle(self, mesaj: str) -> str:
        """Türkçe mesaj ön işleme"""
        # Basit temizlik işlemleri
        mesaj = mesaj.strip()
        mesaj = mesaj.lower()
        
        # Yaygın kısaltmaları genişlet
        kisaltmalar = {
            "fatura": "fatura",
            "paket": "paket",
            "arıza": "arıza",
            "destek": "destek",
            "yardım": "yardım"
        }
        
        for kisa, uzun in kisaltmalar.items():
            mesaj = mesaj.replace(kisa, uzun)
        
        return mesaj
    
    async def arac_cagrilari_yurut(self, arac_cagrilari: List[AracCagrisiLegacy]) -> List[AracCagrisiLegacy]:
        """Araç çağrılarını çalıştır"""
        sonuclar = []
        
        for arac_cagrisi in arac_cagrilari:
            try:
                arac_cagrisi.durum = "calisiyor"
                
                # Mock fonksiyon çağır
                if arac_cagrisi.arac_adi in self.mock_inference.function_mapping:
                    func = self.mock_inference.function_mapping[arac_cagrisi.arac_adi]
                    sonuc = func(**arac_cagrisi.parametreler)
                    arac_cagrisi.sonuc = sonuc
                    arac_cagrisi.durum = "tamamlandi"
                else:
                    arac_cagrisi.durum = "hata"
                    arac_cagrisi.hata_mesaji = f"Araç bulunamadı: {arac_cagrisi.arac_adi}"
                
            except Exception as e:
                logger.error(f"Araç çalıştırma hatası: {e}")
                arac_cagrisi.durum = "hata"
                arac_cagrisi.hata_mesaji = str(e)
            
            sonuclar.append(arac_cagrisi)
        
        return sonuclar
    
    async def _get_current_user(self, **kwargs) -> Dict[str, Any]:
        """Mevcut kullanıcı bilgilerini getir"""
        try:
            user_id = kwargs.get("user_id", 1)
            
            # Kullanıcı servisinden bilgi al
            kullanici_bilgisi = await user_service.get_user_by_id(user_id)
            
            if kullanici_bilgisi:
                return {
                    "success": True,
                    "data": kullanici_bilgisi
                }
            else:
                return {
                    "success": False,
                    "error": "Kullanıcı bulunamadı",
                    "data": {}
                }
            
        except Exception as e:
            logger.error(f"Kullanıcı bilgisi getirme hatası: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": {}
            }
    
    async def oturum_temizle(self, oturum_id: str):
        """Oturum konuşma geçmişini temizle"""
        await self.konusma_yoneticisi.konusma_temizle(oturum_id)
    
    async def sistem_durumu_getir(self) -> Dict[str, Any]:
        """Sistem durumu bilgilerini getir"""
        try:
            return {
                "model_yuklu": True,  # Mock model her zaman yüklü
                "model_adi": "Mock AI Model",
                "aktif_oturum_sayisi": len(self.konusma_yoneticisi.aktif_konusmalar),
                "kayitli_arac_sayisi": len(self.telekom_arac_kaydi.kayitli_araclar),
                "sistem_durumu": "aktif"
            }
            
        except Exception as e:
            logger.error(f"Sistem durumu getirme hatası: {e}")
            return {
                "sistem_durumu": "hata",
                "hata": str(e)
            }

# Global AI orchestrator instance
# Mock AI (varsayılan):
ai_orchestrator = YapayZekaOrkestratori()

# Gerçek AI entegrasyonu için:
# from .ai_orchestrator_real import HuggingFaceInferenceService, YapayZekaOrkestratori as RealYapayZekaOrkestratori
# ai_orchestrator = RealYapayZekaOrkestratori() 