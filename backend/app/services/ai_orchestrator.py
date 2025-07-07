import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import uuid

from .telekom_api import telekom_api

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
            "musteri_profil_getir": {
                "aciklama": "Müşteri profil bilgilerini getirir",
                "parametreler": ["telefon_numarasi"]
            },
            "mevcut_paket_detaylari": {
                "aciklama": "Müşterinin mevcut paket detaylarını getirir",
                "parametreler": ["musteri_id"]
            },
            "kullanilabilir_paketler": {
                "aciklama": "Kullanılabilir paketleri listeler",
                "parametreler": ["musteri_seviyesi"]
            },
            "fatura_detaylari_getir": {
                "aciklama": "Fatura detaylarını getirir",
                "parametreler": ["musteri_id", "ay"]
            },
            "destek_talep_olustur": {
                "aciklama": "Destek talebi oluşturur",
                "parametreler": ["musteri_id", "sorun_kategorisi", "aciklama"]
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
        
        if "profil" in mesaj_lower:
            # Telefon numarası tespit et (basit regex)
            import re
            telefon_match = re.search(r'0\d{10}', mesaj)
            if telefon_match:
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="musteri_profil_getir",
                    parametreler={"telefon_numarasi": telefon_match.group()}
                ))
        
        if "paket" in mesaj_lower:
            # Müşteri ID tespit et
            musteri_match = re.search(r'MUSTERI_\d+', mesaj)
            if musteri_match:
                arac_cagrilari.append(AracCagrisi(
                    arac_adi="mevcut_paket_detaylari",
                    parametreler={"musteri_id": musteri_match.group()}
                ))
        
        return arac_cagrilari
    
    def _yanit_uret(self, mesaj: str, arac_cagrilari: List[AracCagrisi]) -> str:
        """Temel yanıt üretimi"""
        if arac_cagrilari:
            return f"Anlıyorum, {len(arac_cagrilari)} araç çağrısı tespit ettim. Bilgileri getiriyorum..."
        else:
            return "Size nasıl yardımcı olabilirim? Müşteri profili, paket bilgileri veya fatura detayları sorgulayabilirim."
    
    def _arac_sonuclarini_entegre_et(self, temel_yanit: str, arac_sonuclari: List[AracCagrisi]) -> str:
        """Araç sonuçlarını yanıta entegre et"""
        if not arac_sonuclari:
            return temel_yanit
        
        entegre_yanit = temel_yanit + "\n\n"
        
        for arac_sonuc in arac_sonuclari:
            if arac_sonuc.durum == "tamamlandi":
                entegre_yanit += f"✅ {arac_sonuc.arac_adi}: İşlem başarılı\n"
                if arac_sonuc.sonuc:
                    entegre_yanit += f"   Sonuç: {str(arac_sonuc.sonuc)[:100]}...\n"
            elif arac_sonuc.durum == "hata":
                entegre_yanit += f"❌ {arac_sonuc.arac_adi}: Hata\n"
        
        return entegre_yanit

class YapayZekaOrkestratori:
    """Ana yapay zeka orkestratör sınıfı"""
    
    def __init__(self):
        self.model_hizmeti = LlamaInferenceService()
        self.arac_kaydi = TelekomAracKaydi()
        self.konusma_yoneticisi = KonusmaYoneticisi()
        self.telekom_api = telekom_api
    
    async def kullanici_mesaj_isle(self, mesaj: str, kullanici_id: str, oturum_id: str) -> Dict[str, Any]:
        """Kullanıcı mesajını işle ve yanıt üret"""
        try:
            logger.info(f"Kullanıcı mesajı işleniyor: {kullanici_id}")
            
            # 1. Türkçe doğal dil işleme ile ön işleme
            islenmis_mesaj = self.turkce_on_isle(mesaj)
            
            # 2. Konuşma bağlamını getir
            baglam = await self.konusma_yoneticisi.baglam_getir(oturum_id)
            
            # 3. Kullanıcı mesajını kaydet
            kullanici_mesaji = KonusmaMesaji(
                mesaj_id=f"MSG_{uuid.uuid4().hex[:8]}",
                kullanici_id=kullanici_id,
                icerik=islenmis_mesaj,
                zaman_damgasi=datetime.now().isoformat(),
                mesaj_tipi="kullanici"
            )
            await self.konusma_yoneticisi.mesaj_ekle(oturum_id, kullanici_mesaji)
            
            # 4. AI yanıtı üret
            ai_yaniti = await self.model_hizmeti.yanit_uret(
                mesaj=islenmis_mesaj,
                baglam=baglam,
                mevcut_araclar=self.arac_kaydi.mevcut_araclari_getir()
            )
            
            # 5. Araç çağrılarını yürüt
            arac_sonuclari = await self.arac_cagrilari_yurut(ai_yaniti.arac_cagrilari)
            
            # 6. Final yanıt üret
            final_yanit = await self.model_hizmeti.final_yanit_uret(
                orijinal_yanit=ai_yaniti,
                arac_sonuclari=arac_sonuclari
            )
            
            # 7. AI yanıtını kaydet
            ai_mesaji = KonusmaMesaji(
                mesaj_id=ai_yaniti.yanit_id,
                kullanici_id="AI_SYSTEM",
                icerik=final_yanit,
                zaman_damgasi=datetime.now().isoformat(),
                mesaj_tipi="ai"
            )
            await self.konusma_yoneticisi.mesaj_ekle(oturum_id, ai_mesaji)
            
            # 8. Sonuç döndür
            sonuc = {
                "yanit_id": ai_yaniti.yanit_id,
                "yanit": final_yanit,
                "guven_puani": ai_yaniti.guven_puani,
                "arac_cagrilari": len(ai_yaniti.arac_cagrilari),
                "metadata": {
                    "oturum_id": oturum_id,
                    "kullanici_id": kullanici_id
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
            
            sonuclar.append(arac_cagrisi)
        
        return sonuclar
    
    async def _telekom_arac_cagir(self, arac_adi: str, parametreler: Dict[str, Any]) -> Any:
        """Telekom API araç çağrısı"""
        if arac_adi == "musteri_profil_getir":
            return await self.telekom_api.musteri_profil_getir(parametreler["telefon_numarasi"])
        
        elif arac_adi == "mevcut_paket_detaylari":
            return await self.telekom_api.mevcut_paket_detaylari(parametreler["musteri_id"])
        
        elif arac_adi == "kullanilabilir_paketler":
            musteri_seviyesi = parametreler.get("musteri_seviyesi", "standart")
            return await self.telekom_api.kullanilabilir_paketler(musteri_seviyesi)
        
        elif arac_adi == "fatura_detaylari_getir":
            return await self.telekom_api.fatura_detaylari_getir(
                parametreler["musteri_id"], 
                parametreler["ay"]
            )
        
        elif arac_adi == "destek_talep_olustur":
            return await self.telekom_api.destek_talep_olustur(
                parametreler["musteri_id"],
                parametreler["sorun_kategorisi"],
                parametreler["aciklama"]
            )
        
        else:
            raise ValueError(f"Bilinmeyen araç: {arac_adi}")
    
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