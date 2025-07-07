import asyncio
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MusteriProfil:
    musteri_id: str
    telefon_numarasi: str
    ad_soyad: str
    email: str
    dogum_tarihi: str
    musteri_seviyesi: str  # standart, premium, vip
    kayit_tarihi: str
    son_odeme_tarihi: str
    toplam_borc: float
    aktif_paket: str
    kalan_veri: float  # GB
    kalan_dakika: int
    kalan_sms: int

@dataclass
class PaketDetay:
    paket_id: str
    paket_adi: str
    aylik_ucret: float
    veri_miktari: float  # GB
    dakika_miktari: int
    sms_miktari: int
    ozellikler: List[str]
    uygunluk: str  # standart, premium, vip

@dataclass
class FaturaDetay:
    fatura_id: str
    donem: str
    toplam_tutar: float
    odeme_durumu: str
    son_odeme_tarihi: str
    kalemler: List[Dict[str, Any]]

class TelekomAPIService:
    def __init__(self):
        self.musteri_veritabani = self._musteri_veritabanini_olustur()
        self.paket_veritabani = self._paket_veritabanini_olustur()
        self.fatura_veritabani = self._fatura_veritabanini_olustur()
        self.destek_talepleri = []
        
    def _musteri_veritabanini_olustur(self) -> Dict[str, MusteriProfil]:
        """Gerçekçi müşteri profilleri oluştur"""
        musteriler = {}
        
        # Örnek müşteri verileri
        ornek_musteriler = [
            {
                "telefon": "05321234567",
                "ad": "Ahmet Yılmaz",
                "email": "ahmet.yilmaz@email.com",
                "seviye": "premium"
            },
            {
                "telefon": "05339876543",
                "ad": "Ayşe Demir",
                "email": "ayse.demir@email.com", 
                "seviye": "standart"
            },
            {
                "telefon": "05355556666",
                "ad": "Mehmet Kaya",
                "email": "mehmet.kaya@email.com",
                "seviye": "vip"
            }
        ]
        
        for i, musteri in enumerate(ornek_musteriler):
            musteri_id = f"MUSTERI_{i+1:04d}"
            musteriler[musteri_id] = MusteriProfil(
                musteri_id=musteri_id,
                telefon_numarasi=musteri["telefon"],
                ad_soyad=musteri["ad"],
                email=musteri["email"],
                dogum_tarihi=f"19{random.randint(70, 90)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                musteri_seviyesi=musteri["seviye"],
                kayit_tarihi=f"202{random.randint(0, 3)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                son_odeme_tarihi=(datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                toplam_borc=random.uniform(0, 500),
                aktif_paket=f"Paket_{musteri['seviye'].upper()}",
                kalan_veri=random.uniform(0, 50),
                kalan_dakika=random.randint(0, 1000),
                kalan_sms=random.randint(0, 500)
            )
            
        return musteriler
    
    def _paket_veritabanini_olustur(self) -> Dict[str, PaketDetay]:
        """Kullanılabilir paketleri oluştur"""
        paketler = {
            "Paket_STANDART": PaketDetay(
                paket_id="PAKET_001",
                paket_adi="Standart Paket",
                aylik_ucret=89.90,
                veri_miktari=10.0,
                dakika_miktari=1000,
                sms_miktari=1000,
                ozellikler=["Sınırsız WhatsApp", "Sosyal Medya Paketi"],
                uygunluk="standart"
            ),
            "Paket_PREMIUM": PaketDetay(
                paket_id="PAKET_002", 
                paket_adi="Premium Paket",
                aylik_ucret=149.90,
                veri_miktari=25.0,
                dakika_miktari=2000,
                sms_miktari=2000,
                ozellikler=["Sınırsız WhatsApp", "Sosyal Medya Paketi", "Netflix Premium"],
                uygunluk="premium"
            ),
            "Paket_VIP": PaketDetay(
                paket_id="PAKET_003",
                paket_adi="VIP Paket", 
                aylik_ucret=299.90,
                veri_miktari=50.0,
                dakika_miktari=5000,
                sms_miktari=5000,
                ozellikler=["Sınırsız WhatsApp", "Sosyal Medya Paketi", "Netflix Premium", "HBO Max"],
                uygunluk="vip"
            )
        }
        return paketler
    
    def _fatura_veritabanini_olustur(self) -> Dict[str, List[FaturaDetay]]:
        """Fatura veritabanını oluştur"""
        fatura_veritabani = {}
        
        for musteri_id in self.musteri_veritabani.keys():
            fatura_listesi = []
            for ay in range(1, 13):
                fatura = FaturaDetay(
                    fatura_id=f"FATURA_{musteri_id}_{ay:02d}",
                    donem=f"2024-{ay:02d}",
                    toplam_tutar=random.uniform(80, 350),
                    odeme_durumu="odendi" if random.random() > 0.2 else "beklemede",
                    son_odeme_tarihi=f"2024-{ay:02d}-15",
                    kalemler=[
                        {"aciklama": "Aylık Paket Ücreti", "tutar": random.uniform(80, 300)},
                        {"aciklama": "Ek Veri Kullanımı", "tutar": random.uniform(0, 50)},
                        {"aciklama": "Ek Hizmetler", "tutar": random.uniform(0, 20)}
                    ]
                )
                fatura_listesi.append(fatura)
            fatura_veritabani[musteri_id] = fatura_listesi
            
        return fatura_veritabani

    async def get_customer_profile(self, telefon_numarasi: str) -> Optional[MusteriProfil]:
        """Müşteri profil bilgilerini getirir"""
        try:
            logger.info(f"Müşteri profili sorgulanıyor: {telefon_numarasi}")
            
            # Telefon numarasına göre müşteri bul
            for musteri in self.musteri_veritabani.values():
                if musteri.telefon_numarasi == telefon_numarasi:
                    logger.info(f"Müşteri bulundu: {musteri.ad_soyad}")
                    return musteri
            
            logger.warning(f"Müşteri bulunamadı: {telefon_numarasi}")
            return None
            
        except Exception as e:
            logger.error(f"Müşteri profili getirme hatası: {e}")
            raise

    async def get_customer_package(self, musteri_id: str) -> Optional[Dict[str, Any]]:
        """Müşterinin mevcut paket detaylarını getirir"""
        try:
            logger.info(f"Paket detayları sorgulanıyor: {musteri_id}")
            
            if musteri_id not in self.musteri_veritabani:
                logger.warning(f"Müşteri bulunamadı: {musteri_id}")
                return None
                
            musteri = self.musteri_veritabani[musteri_id]
            paket = self.paket_veritabani.get(musteri.aktif_paket)
            
            if not paket:
                logger.warning(f"Paket bulunamadı: {musteri.aktif_paket}")
                return None
                
            paket_detaylari = {
                "musteri_bilgileri": {
                    "ad_soyad": musteri.ad_soyad,
                    "telefon": musteri.telefon_numarasi,
                    "musteri_seviyesi": musteri.musteri_seviyesi
                },
                "aktif_paket": {
                    "paket_adi": paket.paket_adi,
                    "aylik_ucret": paket.aylik_ucret,
                    "veri_miktari": paket.veri_miktari,
                    "dakika_miktari": paket.dakika_miktari,
                    "sms_miktari": paket.sms_miktari,
                    "ozellikler": paket.ozellikler
                },
                "kullanim_durumu": {
                    "kalan_veri": musteri.kalan_veri,
                    "kalan_dakika": musteri.kalan_dakika,
                    "kalan_sms": musteri.kalan_sms,
                    "veri_kullanimi_yuzdesi": ((paket.veri_miktari - musteri.kalan_veri) / paket.veri_miktari) * 100
                },
                "fatura_durumu": {
                    "toplam_borc": musteri.toplam_borc,
                    "son_odeme_tarihi": musteri.son_odeme_tarihi
                }
            }
            
            logger.info(f"Paket detayları başarıyla getirildi: {musteri_id}")
            return paket_detaylari
            
        except Exception as e:
            logger.error(f"Paket detayları getirme hatası: {e}")
            raise

    async def get_available_packages(self, musteri_seviyesi: str = "standart") -> List[Dict[str, Any]]:
        """Kullanılabilir paketleri listeler"""
        try:
            logger.info(f"Kullanılabilir paketler sorgulanıyor: {musteri_seviyesi}")
            
            uygun_paketler = []
            
            for paket in self.paket_veritabani.values():
                if paket.uygunluk == musteri_seviyesi or musteri_seviyesi == "vip":
                    paket_bilgisi = {
                        "paket_id": paket.paket_id,
                        "paket_adi": paket.paket_adi,
                        "aylik_ucret": paket.aylik_ucret,
                        "veri_miktari": paket.veri_miktari,
                        "dakika_miktari": paket.dakika_miktari,
                        "sms_miktari": paket.sms_miktari,
                        "ozellikler": paket.ozellikler,
                        "uygunluk": paket.uygunluk,
                        "oneri_puani": random.randint(70, 100)  # Simüle edilmiş öneri puanı
                    }
                    uygun_paketler.append(paket_bilgisi)
            
            # Fiyata göre sırala
            uygun_paketler.sort(key=lambda x: x["aylik_ucret"])
            
            logger.info(f"{len(uygun_paketler)} paket bulundu: {musteri_seviyesi}")
            return uygun_paketler
            
        except Exception as e:
            logger.error(f"Kullanılabilir paketler getirme hatası: {e}")
            raise

    async def change_package(self, musteri_id: str, hedef_paket: str) -> Dict[str, Any]:
        """Çok adımlı paket değişikliği ve doğrulama"""
        try:
            logger.info(f"Paket değişikliği başlatılıyor: {musteri_id} -> {hedef_paket}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            if hedef_paket not in self.paket_veritabani:
                raise ValueError("Hedef paket bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            yeni_paket = self.paket_veritabani[hedef_paket]
            mevcut_paket = self.paket_veritabani[musteri.aktif_paket]
            
            # Paket değişikliği doğrulama
            if yeni_paket.aylik_ucret < mevcut_paket.aylik_ucret:
                # Düşük pakete geçiş için ek doğrulama
                if musteri.toplam_borc > 0:
                    raise ValueError("Borçlu müşteri düşük pakete geçemez")
            
            # Simüle edilmiş işlem süresi
            await asyncio.sleep(0.5)
            
            # Paket değişikliği başarılı
            musteri.aktif_paket = hedef_paket
            musteri.kalan_veri = yeni_paket.veri_miktari
            musteri.kalan_dakika = yeni_paket.dakika_miktari
            musteri.kalan_sms = yeni_paket.sms_miktari
            
            sonuc = {
                "durum": "basarili",
                "mesaj": f"Paket değişikliği başarıyla tamamlandı: {yeni_paket.paket_adi}",
                "eski_paket": mevcut_paket.paket_adi,
                "yeni_paket": yeni_paket.paket_adi,
                "yeni_aylik_ucret": yeni_paket.aylik_ucret,
                "gecerlilik_tarihi": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "islem_id": f"ISLEM_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            logger.info(f"Paket değişikliği başarılı: {sonuc['islem_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Paket değişikliği hatası: {e}")
            raise

    async def get_package_details(self, musteri_id: str) -> Optional[Dict[str, Any]]:
        """Paket detaylarını getirir (mevcut_paket_detaylari ile aynı)"""
        return await self.get_customer_package(musteri_id)

    async def get_current_bill(self, musteri_id: str, ay: int) -> Optional[Dict[str, Any]]:
        """Detaylı fatura ve döküm"""
        try:
            logger.info(f"Fatura detayları sorgulanıyor: {musteri_id} - {ay}. ay")
            if musteri_id not in self.fatura_veritabani:
                logger.warning(f"Müşteri faturaları bulunamadı: {musteri_id}")
                return None
            fatura_listesi = self.fatura_veritabani[musteri_id]
            if ay < 1 or ay > len(fatura_listesi):
                logger.warning(f"Geçersiz ay: {ay}")
                return None
            fatura = fatura_listesi[ay - 1]
            musteri = self.musteri_veritabani[musteri_id]
            fatura_detaylari = {
                "fatura_bilgileri": {
                    "fatura_id": fatura.fatura_id,
                    "donem": fatura.donem,
                    "toplam_tutar": fatura.toplam_tutar,
                    "odeme_durumu": fatura.odeme_durumu,
                    "son_odeme_tarihi": fatura.son_odeme_tarihi
                },
                "musteri_bilgileri": {
                    "ad_soyad": musteri.ad_soyad,
                    "telefon": musteri.telefon_numarasi,
                    "email": musteri.email
                },
                "fatura_kalemleri": fatura.kalemler,
                "ozet": {
                    "toplam_kalem": len(fatura.kalemler),
                    "en_yuksek_kalem": max(fatura.kalemler, key=lambda x: x["tutar"]),
                    "odeme_gecmisi": "Düzenli" if fatura.odeme_durumu == "odendi" else "Gecikmeli"
                }
            }
            logger.info(f"Fatura detayları başarıyla getirildi: {fatura.fatura_id}")
            return fatura_detaylari
        except Exception as e:
            logger.error(f"Fatura detayları getirme hatası: {e}")
            raise

    async def create_fault_ticket(self, musteri_id: str, sorun_kategorisi: str, aciklama: str) -> Dict[str, Any]:
        """Teknik destek talebi oluşturma"""
        try:
            logger.info(f"Destek talebi oluşturuluyor: {musteri_id} - {sorun_kategorisi}")
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
            musteri = self.musteri_veritabani[musteri_id]
            # Destek talebi oluştur
            talep_id = f"TALEP_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            destek_talebi = {
                "talep_id": talep_id,
                "musteri_id": musteri_id,
                "musteri_adi": musteri.ad_soyad,
                "telefon": musteri.telefon_numarasi,
                "sorun_kategorisi": sorun_kategorisi,
                "aciklama": aciklama,
                "olusturma_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "durum": "beklemede",
                "oncelik": "normal" if musteri.musteri_seviyesi == "standart" else "yuksek",
                "tahmini_cozum_suresi": "24 saat" if musteri.musteri_seviyesi == "standart" else "4 saat"
            }
            self.destek_talepleri.append(destek_talebi)
            sonuc = {
                "durum": "basarili",
                "mesaj": "Destek talebi başarıyla oluşturuldu",
                "talep_id": talep_id,
                "tahmini_cozum_suresi": destek_talebi["tahmini_cozum_suresi"],
                "oncelik": destek_talebi["oncelik"]
            }
            logger.info(f"Destek talebi oluşturuldu: {talep_id}")
            return sonuc
        except Exception as e:
            logger.error(f"Destek talebi oluşturma hatası: {e}")
            raise

    async def get_remaining_quotas(self, musteri_id: str) -> Optional[Dict[str, Any]]:
        """Kalan veri, dakika ve SMS kotasını getirir"""
        try:
            logger.info(f"Kalan kotalar sorgulanıyor: {musteri_id}")
            
            if musteri_id not in self.musteri_veritabani:
                logger.warning(f"Müşteri bulunamadı: {musteri_id}")
                return None
                
            musteri = self.musteri_veritabani[musteri_id]
            paket = self.paket_veritabani.get(musteri.aktif_paket)
            
            if not paket:
                logger.warning(f"Paket bulunamadı: {musteri.aktif_paket}")
                return None
                
            kalan_kotalar = {
                "musteri_id": musteri_id,
                "paket_adi": paket.paket_adi,
                "kotalar": {
                    "veri": {
                        "kalan": musteri.kalan_veri,
                        "toplam": paket.veri_miktari,
                        "kullanilan": paket.veri_miktari - musteri.kalan_veri,
                        "kullanim_yuzdesi": ((paket.veri_miktari - musteri.kalan_veri) / paket.veri_miktari) * 100
                    },
                    "dakika": {
                        "kalan": musteri.kalan_dakika,
                        "toplam": paket.dakika_miktari,
                        "kullanilan": paket.dakika_miktari - musteri.kalan_dakika,
                        "kullanim_yuzdesi": ((paket.dakika_miktari - musteri.kalan_dakika) / paket.dakika_miktari) * 100
                    },
                    "sms": {
                        "kalan": musteri.kalan_sms,
                        "toplam": paket.sms_miktari,
                        "kullanilan": paket.sms_miktari - musteri.kalan_sms,
                        "kullanim_yuzdesi": ((paket.sms_miktari - musteri.kalan_sms) / paket.sms_miktari) * 100
                    }
                },
                "son_guncelleme": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info(f"Kalan kotalar başarıyla getirildi: {musteri_id}")
            return kalan_kotalar
            
        except Exception as e:
            logger.error(f"Kalan kotalar getirme hatası: {e}")
            raise

    async def enable_roaming(self, musteri_id: str, ulke_kodu: str = "TR") -> Dict[str, Any]:
        """Roaming hizmetini aktifleştirir"""
        try:
            logger.info(f"Roaming aktifleştiriliyor: {musteri_id} - {ulke_kodu}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            
            # Roaming ücretleri (simüle edilmiş)
            roaming_ucretleri = {
                "TR": {"veri": 0.05, "dakika": 0.15, "sms": 0.10},
                "EU": {"veri": 0.10, "dakika": 0.25, "sms": 0.15},
                "US": {"veri": 0.20, "dakika": 0.50, "sms": 0.25}
            }
            
            ucret = roaming_ucretleri.get(ulke_kodu, roaming_ucretleri["TR"])
            
            sonuc = {
                "durum": "basarili",
                "mesaj": f"Roaming hizmeti {ulke_kodu} için aktifleştirildi",
                "musteri_id": musteri_id,
                "ulke_kodu": ulke_kodu,
                "aktifleştirme_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ucretler": ucret,
                "gecerlilik_suresi": "30 gün",
                "islem_id": f"ROAMING_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            logger.info(f"Roaming aktifleştirildi: {sonuc['islem_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Roaming aktifleştirme hatası: {e}")
            raise

    async def get_past_bills(self, musteri_id: str, ay_sayisi: int = 6) -> Optional[Dict[str, Any]]:
        """Geçmiş faturaları getirir"""
        try:
            logger.info(f"Geçmiş faturalar sorgulanıyor: {musteri_id} - Son {ay_sayisi} ay")
            
            if musteri_id not in self.fatura_veritabani:
                logger.warning(f"Müşteri faturaları bulunamadı: {musteri_id}")
                return None
                
            fatura_listesi = self.fatura_veritabani[musteri_id]
            musteri = self.musteri_veritabani[musteri_id]
            
            # Son N ayın faturalarını al
            son_faturalar = fatura_listesi[-ay_sayisi:] if len(fatura_listesi) >= ay_sayisi else fatura_listesi
            
            gecmis_faturalar = {
                "musteri_id": musteri_id,
                "musteri_adi": musteri.ad_soyad,
                "toplam_fatura_sayisi": len(son_faturalar),
                "toplam_tutar": sum(fatura.toplam_tutar for fatura in son_faturalar),
                "odenen_tutar": sum(fatura.toplam_tutar for fatura in son_faturalar if fatura.odeme_durumu == "odendi"),
                "bekleyen_tutar": sum(fatura.toplam_tutar for fatura in son_faturalar if fatura.odeme_durumu == "beklemede"),
                "faturalar": [
                    {
                        "fatura_id": fatura.fatura_id,
                        "donem": fatura.donem,
                        "tutar": fatura.toplam_tutar,
                        "odeme_durumu": fatura.odeme_durumu,
                        "son_odeme_tarihi": fatura.son_odeme_tarihi
                    }
                    for fatura in son_faturalar
                ]
            }
            
            logger.info(f"Geçmiş faturalar başarıyla getirildi: {len(son_faturalar)} fatura")
            return gecmis_faturalar
            
        except Exception as e:
            logger.error(f"Geçmiş faturalar getirme hatası: {e}")
            raise

    async def pay_bill(self, musteri_id: str, fatura_id: str, odeme_yontemi: str = "kredi_karti") -> Dict[str, Any]:
        """Fatura ödeme işlemi"""
        try:
            logger.info(f"Fatura ödeme işlemi başlatılıyor: {fatura_id} - {odeme_yontemi}")
            
            if musteri_id not in self.fatura_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            fatura_listesi = self.fatura_veritabani[musteri_id]
            musteri = self.musteri_veritabani[musteri_id]
            
            # Faturayı bul
            fatura = None
            for f in fatura_listesi:
                if f.fatura_id == fatura_id:
                    fatura = f
                    break
                    
            if not fatura:
                raise ValueError("Fatura bulunamadı")
                
            if fatura.odeme_durumu == "odendi":
                raise ValueError("Bu fatura zaten ödenmiş")
                
            # Simüle edilmiş ödeme işlemi
            await asyncio.sleep(1)
            
            # Ödeme başarılı
            fatura.odeme_durumu = "odendi"
            musteri.toplam_borc -= fatura.toplam_tutar
            
            sonuc = {
                "durum": "basarili",
                "mesaj": "Fatura başarıyla ödendi",
                "fatura_id": fatura_id,
                "odenen_tutar": fatura.toplam_tutar,
                "odeme_yontemi": odeme_yontemi,
                "odeme_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "kalan_borc": musteri.toplam_borc,
                "islem_id": f"ODEME_{fatura_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            logger.info(f"Fatura ödendi: {sonuc['islem_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Fatura ödeme hatası: {e}")
            raise

    async def setup_autopay(self, musteri_id: str, kart_bilgileri: Dict[str, str]) -> Dict[str, Any]:
        """Otomatik ödeme kurulumu"""
        try:
            logger.info(f"Otomatik ödeme kurulumu: {musteri_id}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            
            # Gerekli kart bilgilerini kontrol et
            gerekli_alanlar = ["kart_numarasi", "son_kullanma_tarihi", "cvv"]
            for alan in gerekli_alanlar:
                if alan not in kart_bilgileri:
                    raise ValueError(f"Eksik kart bilgisi: {alan}")
            
            # Simüle edilmiş kart doğrulama
            await asyncio.sleep(0.5)
            
            sonuc = {
                "durum": "basarili",
                "mesaj": "Otomatik ödeme başarıyla kuruldu",
                "musteri_id": musteri_id,
                "kart_son_4_hane": kart_bilgileri["kart_numarasi"][-4:],
                "kurulum_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "aktif": True,
                "sonraki_odeme_tarihi": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "islem_id": f"AUTOPAY_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            logger.info(f"Otomatik ödeme kuruldu: {sonuc['islem_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Otomatik ödeme kurulum hatası: {e}")
            raise

    async def check_network_status(self, musteri_id: str) -> Dict[str, Any]:
        """Ağ durumu kontrolü"""
        try:
            logger.info(f"Ağ durumu kontrol ediliyor: {musteri_id}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            
            # Simüle edilmiş ağ durumu
            ag_durumu = {
                "musteri_id": musteri_id,
                "telefon": musteri.telefon_numarasi,
                "ag_durumu": "aktif",
                "sinyal_gucu": random.randint(70, 100),
                "ag_tipi": "4G" if random.random() > 0.3 else "5G",
                "baz_istasyonu": f"BS_{random.randint(1000, 9999)}",
                "son_guncelleme": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "uyarilar": []
            }
            
            # Simüle edilmiş uyarılar
            if ag_durumu["sinyal_gucu"] < 80:
                ag_durumu["uyarilar"].append("Düşük sinyal gücü")
                
            if random.random() < 0.1:  # %10 ihtimalle bakım uyarısı
                ag_durumu["uyarilar"].append("Bölgenizde planlı bakım çalışması")
            
            logger.info(f"Ağ durumu kontrol edildi: {ag_durumu['ag_durumu']}")
            return ag_durumu
            
        except Exception as e:
            logger.error(f"Ağ durumu kontrol hatası: {e}")
            raise

    async def get_fault_ticket_status(self, talep_id: str) -> Optional[Dict[str, Any]]:
        """Arıza kaydı durumu sorgulama"""
        try:
            logger.info(f"Arıza kaydı durumu sorgulanıyor: {talep_id}")
            
            # Destek taleplerinde ara
            for talep in self.destek_talepleri:
                if talep["talep_id"] == talep_id:
                    durum_bilgisi = {
                        "talep_id": talep_id,
                        "durum": talep["durum"],
                        "oncelik": talep["oncelik"],
                        "olusturma_tarihi": talep["olusturma_tarihi"],
                        "tahmini_cozum_suresi": talep["tahmini_cozum_suresi"],
                        "sorun_kategorisi": talep["sorun_kategorisi"],
                        "aciklama": talep["aciklama"],
                        "son_guncelleme": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    logger.info(f"Arıza kaydı durumu getirildi: {talep_id} - {talep['durum']}")
                    return durum_bilgisi
            
            logger.warning(f"Arıza kaydı bulunamadı: {talep_id}")
            return None
            
        except Exception as e:
            logger.error(f"Arıza kaydı durumu getirme hatası: {e}")
            raise

    async def test_internet_speed(self, musteri_id: str) -> Dict[str, Any]:
        """İnternet hızı testi"""
        try:
            logger.info(f"İnternet hızı testi başlatılıyor: {musteri_id}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            paket = self.paket_veritabani.get(musteri.aktif_paket)
            
            # Simüle edilmiş hız testi
            await asyncio.sleep(2)
            
            # Paket hızına göre simüle edilmiş sonuçlar
            paket_hizlari = {
                "Paket_STANDART": {"download": 16, "upload": 2},
                "Paket_PREMIUM": {"download": 100, "upload": 10},
                "Paket_VIP": {"download": 500, "upload": 50}
            }
            
            hedef_hiz = paket_hizlari.get(musteri.aktif_paket, {"download": 16, "upload": 2})
            
            # Gerçekçi hız varyasyonu (±20%)
            download_hiz = hedef_hiz["download"] * random.uniform(0.8, 1.2)
            upload_hiz = hedef_hiz["upload"] * random.uniform(0.8, 1.2)
            
            hiz_testi_sonucu = {
                "musteri_id": musteri_id,
                "telefon": musteri.telefon_numarasi,
                "paket": musteri.aktif_paket,
                "hedef_hiz": hedef_hiz,
                "test_sonuclari": {
                    "download_hiz": round(download_hiz, 2),
                    "upload_hiz": round(upload_hiz, 2),
                    "ping": random.randint(10, 50),
                    "jitter": random.uniform(1, 5)
                },
                "test_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "degerlendirme": "iyi" if download_hiz >= hedef_hiz["download"] * 0.8 else "düşük"
            }
            
            logger.info(f"İnternet hızı testi tamamlandı: {hiz_testi_sonucu['degerlendirme']}")
            return hiz_testi_sonucu
            
        except Exception as e:
            logger.error(f"İnternet hızı testi hatası: {e}")
            raise

    async def update_customer_contact(self, musteri_id: str, yeni_bilgiler: Dict[str, str]) -> Dict[str, Any]:
        """Müşteri iletişim bilgilerini günceller"""
        try:
            logger.info(f"Müşteri iletişim bilgileri güncelleniyor: {musteri_id}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            
            # Güncellenebilir alanları kontrol et ve güncelle
            guncellenen_alanlar = []
            
            if "email" in yeni_bilgiler:
                musteri.email = yeni_bilgiler["email"]
                guncellenen_alanlar.append("email")
                
            if "telefon_numarasi" in yeni_bilgiler:
                musteri.telefon_numarasi = yeni_bilgiler["telefon_numarasi"]
                guncellenen_alanlar.append("telefon_numarasi")
                
            if "ad_soyad" in yeni_bilgiler:
                musteri.ad_soyad = yeni_bilgiler["ad_soyad"]
                guncellenen_alanlar.append("ad_soyad")
            
            if not guncellenen_alanlar:
                raise ValueError("Güncellenecek bilgi bulunamadı")
            
            sonuc = {
                "durum": "basarili",
                "mesaj": "Müşteri bilgileri başarıyla güncellendi",
                "musteri_id": musteri_id,
                "guncellenen_alanlar": guncellenen_alanlar,
                "guncelleme_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "yeni_bilgiler": {alan: getattr(musteri, alan) for alan in guncellenen_alanlar},
                "islem_id": f"UPDATE_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            logger.info(f"Müşteri bilgileri güncellendi: {guncellenen_alanlar}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Müşteri bilgileri güncelleme hatası: {e}")
            raise

    async def suspend_line(self, musteri_id: str, sebep: str = "müşteri_talebi") -> Dict[str, Any]:
        """Hattı askıya alır"""
        try:
            logger.info(f"Hat askıya alınıyor: {musteri_id} - {sebep}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            
            # Borç kontrolü
            if musteri.toplam_borc > 0:
                raise ValueError("Borçlu hattı askıya alınamaz")
            
            # Simüle edilmiş askıya alma işlemi
            await asyncio.sleep(1)
            
            sonuc = {
                "durum": "basarili",
                "mesaj": "Hat başarıyla askıya alındı",
                "musteri_id": musteri_id,
                "telefon": musteri.telefon_numarasi,
                "askiya_alma_sebebi": sebep,
                "askiya_alma_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "hat_durumu": "askiya_alindi",
                "geri_aktifleştirme_tarihi": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "islem_id": f"SUSPEND_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            logger.info(f"Hat askıya alındı: {sonuc['islem_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Hat askıya alma hatası: {e}")
            raise

    async def reactivate_line(self, musteri_id: str) -> Dict[str, Any]:
        """Hattı yeniden aktifleştirir"""
        try:
            logger.info(f"Hat yeniden aktifleştiriliyor: {musteri_id}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            
            # Simüle edilmiş aktifleştirme işlemi
            await asyncio.sleep(1)
            
            sonuc = {
                "durum": "basarili",
                "mesaj": "Hat başarıyla yeniden aktifleştirildi",
                "musteri_id": musteri_id,
                "telefon": musteri.telefon_numarasi,
                "aktifleştirme_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "hat_durumu": "aktif",
                "islem_id": f"REACTIVATE_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            logger.info(f"Hat yeniden aktifleştirildi: {sonuc['islem_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Hat yeniden aktifleştirme hatası: {e}")
            raise

    async def check_number_portability(self, telefon_numarasi: str) -> Dict[str, Any]:
        """Numara taşınabilirlik kontrolü"""
        try:
            logger.info(f"Numara taşınabilirlik kontrol ediliyor: {telefon_numarasi}")
            
            # Simüle edilmiş taşınabilirlik kontrolü
            await asyncio.sleep(0.5)
            
            # Basit kontrol: 0532 ile başlayan numaralar taşınabilir
            tasinabilir = telefon_numarasi.startswith("0532")
            
            sonuc = {
                "telefon_numarasi": telefon_numarasi,
                "tasinabilir": tasinabilir,
                "kontrol_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "aciklama": "Numara taşınabilir" if tasinabilir else "Numara taşınamaz",
                "gerekli_belgeler": [
                    "Kimlik fotokopisi",
                    "Adres belgesi",
                    "Mevcut operatör faturası"
                ] if tasinabilir else [],
                "tahmini_sure": "3-5 iş günü" if tasinabilir else "N/A"
            }
            
            logger.info(f"Numara taşınabilirlik kontrol edildi: {tasinabilir}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Numara taşınabilirlik kontrol hatası: {e}")
            raise

    async def get_payment_history(self, musteri_id: str) -> Optional[Dict[str, Any]]:
        """Müşterinin ödeme geçmişini getirir"""
        try:
            logger.info(f"Ödeme geçmişi sorgulanıyor: {musteri_id}")
            if musteri_id not in self.fatura_veritabani:
                logger.warning(f"Müşteri faturaları bulunamadı: {musteri_id}")
                return None
            fatura_listesi = self.fatura_veritabani[musteri_id]
            odeme_gecmisi = [
                {
                    "fatura_id": fatura.fatura_id,
                    "donem": fatura.donem,
                    "tutar": fatura.toplam_tutar,
                    "odeme_durumu": fatura.odeme_durumu,
                    "odeme_tarihi": fatura.son_odeme_tarihi if fatura.odeme_durumu == "odendi" else None
                }
                for fatura in fatura_listesi if fatura.odeme_durumu == "odendi"
            ]
            sonuc = {
                "musteri_id": musteri_id,
                "odeme_gecmisi": odeme_gecmisi,
                "toplam_odenen_fatura": len(odeme_gecmisi),
                "toplam_odenen_tutar": sum(f["tutar"] for f in odeme_gecmisi)
            }
            logger.info(f"Ödeme geçmişi getirildi: {len(odeme_gecmisi)} kayıt")
            return sonuc
        except Exception as e:
            logger.error(f"Ödeme geçmişi getirme hatası: {e}")
            raise

# Global servis örneği
telekom_api = TelekomAPIService() 