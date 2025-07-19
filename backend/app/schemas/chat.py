"""
Chat endpoint'i için Pydantic şemaları
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ChatMessage(BaseModel):
    """Kullanıcı mesajı şeması"""
    message: str = Field(..., description="Kullanıcının gönderdiği mesaj", min_length=1, max_length=1000)
    user_id: str = Field(..., description="Kullanıcı ID'si")
    session_id: Optional[str] = Field(None, description="Oturum ID'si (opsiyonel)")

class ChatResponse(BaseModel):
    """Chat endpoint yanıt şeması"""
    success: bool = Field(..., description="İşlem başarı durumu")
    message: str = Field(..., description="Yanıt mesajı")
    data: Optional[Dict[str, Any]] = Field(None, description="Yanıt verisi")
    timestamp: datetime = Field(default_factory=datetime.now, description="Yanıt zamanı")

class ErrorResponse(BaseModel):
    """Hata yanıt şeması"""
    success: bool = Field(False, description="İşlem başarı durumu")
    error: str = Field(..., description="Hata türü")
    message: str = Field(..., description="Hata mesajı")
    timestamp: datetime = Field(default_factory=datetime.now, description="Hata zamanı")

class AracCagrisi(BaseModel):
    """Araç çağrısı şeması"""
    arac_adi: str = Field(..., description="Çağrılacak araç adı")
    parametreler: Dict[str, Any] = Field(default_factory=dict, description="Araç parametreleri")
    sonuc: Optional[Any] = Field(None, description="Araç sonucu")
    durum: str = Field(..., description="Araç durumu")

class AIYanit(BaseModel):
    """AI yanıt şeması"""
    yanit_id: str = Field(..., description="Yanıt ID'si")
    yanit: str = Field(..., description="AI'nın yanıtı")
    guven_puani: float = Field(..., description="Yanıt güvenilirliği (0-1)")
    arac_cagrilari: int = Field(..., description="Kullanılan araç sayısı")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Yanıt metadata'sı")

class SistemDurumu(BaseModel):
    """Sistem durumu şeması"""
    model_hizmeti: Dict[str, Any] = Field(..., description="Model hizmeti durumu")
    arac_kaydi: Dict[str, Any] = Field(..., description="Araç kaydı durumu")
    konusma_yoneticisi: Dict[str, Any] = Field(..., description="Konuşma yöneticisi durumu")
    telekom_api: Dict[str, Any] = Field(..., description="Telekom API durumu")

class OturumTemizleme(BaseModel):
    """Oturum temizleme şeması"""
    session_id: str = Field(..., description="Temizlenecek oturum ID'si")

class OturumTemizlemeYanit(BaseModel):
    """Oturum temizleme yanıt şeması"""
    success: bool = Field(..., description="İşlem başarı durumu")
    message: str = Field(..., description="Yanıt mesajı")
    session_id: str = Field(..., description="Temizlenen oturum ID'si") 