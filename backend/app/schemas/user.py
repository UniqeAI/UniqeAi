"""
Kullanıcı endpoint'i için Pydantic şemaları
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class UserInfo(BaseModel):
    """Kullanıcı bilgileri şeması"""
    user_id: str = Field(..., description="Kullanıcı ID'si")
    username: Optional[str] = Field(None, description="Kullanıcı adı")
    email: Optional[str] = Field(None, description="E-posta adresi")
    full_name: Optional[str] = Field(None, description="Tam ad")
    phone: Optional[str] = Field(None, description="Telefon numarası")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Kullanıcı tercihleri")
    last_login: Optional[datetime] = Field(None, description="Son giriş tarihi")
    is_active: bool = Field(True, description="Aktif durumu")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Ek bilgiler")

class UserRegister(BaseModel):
    """Kullanıcı kayıt şeması"""
    username: str = Field(..., description="Kullanıcı adı", min_length=3)
    email: str = Field(..., description="E-posta adresi")
    password: str = Field(..., description="Şifre", min_length=6)
    full_name: str = Field(..., description="Tam ad")
    phone: str = Field(..., description="Telefon numarası")
    birth_date: Optional[str] = Field(None, description="Doğum tarihi")
    gender: Optional[str] = Field(None, description="Cinsiyet")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Kullanıcı tercihleri")

class UserLogin(BaseModel):
    """Kullanıcı giriş şeması"""
    email: str = Field(..., description="E-posta adresi")
    password: str = Field(..., description="Şifre")

class UserResponse(BaseModel):
    """Kullanıcı yanıt şeması"""
    success: bool = Field(..., description="İşlem başarı durumu")
    message: str = Field(..., description="Yanıt mesajı")
    data: Optional[UserInfo] = Field(None, description="Kullanıcı bilgileri")
    timestamp: datetime = Field(default_factory=datetime.now, description="Yanıt zamanı")

class UserUpdateRequest(BaseModel):
    """Kullanıcı güncelleme şeması"""
    username: Optional[str] = Field(None, description="Kullanıcı adı")
    email: Optional[str] = Field(None, description="E-posta adresi")
    full_name: Optional[str] = Field(None, description="Tam ad")
    phone: Optional[str] = Field(None, description="Telefon numarası")
    preferences: Optional[Dict[str, Any]] = Field(None, description="Kullanıcı tercihleri") 