"""
Chat endpoint'i için Pydantic şemaları
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ChatMessage(BaseModel):
    """Kullanıcı mesajı şeması"""
    message: str = Field(..., description="Kullanıcının gönderdiği mesaj", min_length=1, max_length=1000)
    user_id: Optional[int] = Field(None, description="Kullanıcı ID'si (opsiyonel)")
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

class ToolCall(BaseModel):
    """Araç çağrısı şeması"""
    tool_name: str = Field(..., description="Çağrılacak araç adı")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Araç parametreleri")
    result: Optional[Any] = Field(None, description="Araç sonucu")

class AIResponse(BaseModel):
    """AI yanıt şeması"""
    response: str = Field(..., description="AI'nın yanıtı")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="Kullanılan araçlar")
    confidence: Optional[float] = Field(None, description="Yanıt güvenilirliği (0-1)") 