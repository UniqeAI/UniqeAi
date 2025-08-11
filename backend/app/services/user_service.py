"""
Kullanıcı yönetimi servisi
"""

from typing import Dict, Optional
from datetime import datetime
from app.schemas.user import UserInfo, UserLogin, UserUpdateRequest, UserRegister
import uuid
import hashlib

class UserService:
    """Kullanıcı bilgilerini yöneten servis"""
    
    def __init__(self):
        # Gerçek uygulamada bu veriler veritabanında saklanacak
        # Şimdilik bellek içinde tutuyoruz
        self.active_users: Dict[str, UserInfo] = {}
        self.user_credentials: Dict[str, Dict[str, str]] = {}  # username -> {password_hash, user_id}
        self.current_user_id: Optional[str] = None

        # --- Varsayılan kullanıcı ekle ---
        default_user_id = str(uuid.uuid4())
        default_username = "Musteri Musteri"
        default_email = "musteri@choyrens.com"
        default_phone = "01234567890"
        default_password = "test123"
        default_gender = "erkek"
        default_birth_date = "01.01.2001"
        password_hash = self._hash_password(default_password)
        user_info = UserInfo(
            user_id=default_user_id,
            username=default_username,
            email=default_email,
            full_name=default_username,
            phone=default_phone,
            preferences={},
            last_login=datetime.now(),
            is_active=True,
            metadata={
                "birth_date": default_birth_date,
                "gender": default_gender,
                "registration_date": datetime.now().isoformat()
            }
        )
        self.active_users[default_user_id] = user_info
        self.user_credentials[default_username] = {
            "password_hash": password_hash,
            "user_id": default_user_id
        }
    
    def _hash_password(self, password: str) -> str:
        """Şifreyi hash'le"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Şifre doğrulaması"""
        return self._hash_password(password) == hashed_password
    
    async def register_user(self, user_register: UserRegister) -> UserInfo:
        """
        Yeni kullanıcı kaydı oluşturur
        
        Args:
            user_register: Kullanıcı kayıt bilgileri
            
        Returns:
            Kullanıcı bilgileri
        """
        # Kullanıcı adı kontrolü
        if user_register.username in self.user_credentials:
            raise ValueError("Bu kullanıcı adı zaten kullanılıyor")
        
        # E-posta kontrolü
        for user_id, user_info in self.active_users.items():
            if user_info.email == user_register.email:
                raise ValueError("Bu e-posta adresi zaten kullanılıyor")
        
        # Yeni kullanıcı ID'si oluştur
        user_id = str(uuid.uuid4())
        
        # Şifreyi hash'le
        password_hash = self._hash_password(user_register.password)
        
        # Kullanıcı bilgilerini oluştur
        user_info = UserInfo(
            user_id=user_id,
            username=user_register.username,
            email=user_register.email,
            full_name=user_register.full_name,
            phone=user_register.phone,
            preferences=user_register.preferences or {},
            last_login=datetime.now(),
            is_active=True,
            metadata={
                "birth_date": user_register.birth_date,
                "gender": user_register.gender,
                "registration_date": datetime.now().isoformat()
            }
        )
        
        # Kullanıcıyı kaydet
        self.active_users[user_id] = user_info
        self.user_credentials[user_register.username] = {
            "password_hash": password_hash,
            "user_id": user_id
        }
        
        # Geçerli kullanıcı olarak ayarla
        self.current_user_id = user_id
        
        return user_info
    
    async def login_user(self, user_login: UserLogin) -> UserInfo:
        """
        Kullanıcı girişi yapar (e-posta ile)
        
        Args:
            user_login: Kullanıcı giriş bilgileri
            
        Returns:
            Kullanıcı bilgileri
        """
        # E-posta ile kullanıcı arama
        user_found = None
        for user_id, user_info in self.active_users.items():
            if user_info.email == user_login.email:
                user_found = user_info
                break
        
        if not user_found:
            raise ValueError("E-posta adresi veya şifre hatalı")
        
        # Kullanıcı adı ile şifre kontrolü
        if user_found.username not in self.user_credentials:
            raise ValueError("E-posta adresi veya şifre hatalı")
        
        # Şifre kontrolü
        stored_credentials = self.user_credentials[user_found.username]
        if not self._verify_password(user_login.password, stored_credentials["password_hash"]):
            raise ValueError("E-posta adresi veya şifre hatalı")
        
        # Kullanıcı bilgilerini getir
        user_id = stored_credentials["user_id"]
        if user_id not in self.active_users:
            raise ValueError("Kullanıcı bulunamadı")
        
        user_info = self.active_users[user_id]
        
        # Son giriş tarihini güncelle
        user_info.last_login = datetime.now()
        self.active_users[user_id] = user_info
        
        # Geçerli kullanıcı olarak ayarla
        self.current_user_id = user_id
        
        return user_info
    
    async def set_current_user(self, user_login: UserLogin) -> UserInfo:
        """
        Geçerli kullanıcıyı ayarlar (legacy - geriye uyumluluk için)
        
        Args:
            user_login: Kullanıcı giriş bilgileri
            
        Returns:
            Kullanıcı bilgileri
        """
        return await self.login_user(user_login)
    
    async def get_current_user(self) -> Optional[UserInfo]:
        """
        Geçerli kullanıcı bilgilerini getirir
        
        Returns:
            Kullanıcı bilgileri veya None
        """
        if self.current_user_id and self.current_user_id in self.active_users:
            return self.active_users[self.current_user_id]
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserInfo]:
        """
        Belirtilen ID'ye sahip kullanıcı bilgilerini getirir
        
        Args:
            user_id: Kullanıcı ID'si
            
        Returns:
            Kullanıcı bilgileri veya None
        """
        return self.active_users.get(user_id)
    
    async def update_current_user(self, update_request: UserUpdateRequest) -> Optional[UserInfo]:
        """
        Geçerli kullanıcının bilgilerini günceller
        
        Args:
            update_request: Güncelleme bilgileri
            
        Returns:
            Güncellenmiş kullanıcı bilgileri veya None
        """
        if not self.current_user_id or self.current_user_id not in self.active_users:
            return None
        
        user_info = self.active_users[self.current_user_id]
        
        # Sadece None olmayan alanları güncelle
        if update_request.username is not None:
            user_info.username = update_request.username
        if update_request.email is not None:
            user_info.email = update_request.email
        if update_request.full_name is not None:
            user_info.full_name = update_request.full_name
        if update_request.phone is not None:
            user_info.phone = update_request.phone
        if update_request.preferences is not None:
            user_info.preferences = update_request.preferences
        
        self.active_users[self.current_user_id] = user_info
        
        return user_info
    
    async def logout_current_user(self) -> bool:
        """
        Geçerli kullanıcıyı çıkış yapıyor durumuna getirir
        
        Returns:
            Çıkış durumu
        """
        if self.current_user_id and self.current_user_id in self.active_users:
            self.active_users[self.current_user_id].is_active = False
            self.current_user_id = None
            return True
        return False
    
    async def get_all_active_users(self) -> Dict[str, UserInfo]:
        """
        Tüm aktif kullanıcıları getirir
        
        Returns:
            Aktif kullanıcılar sözlüğü
        """
        return {
            user_id: user_info 
            for user_id, user_info in self.active_users.items() 
            if user_info.is_active
        }

# Singleton instance
user_service = UserService() 