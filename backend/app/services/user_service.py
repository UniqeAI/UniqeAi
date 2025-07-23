"""
Kullanıcı yönetimi servisi
"""

from typing import Dict, Optional
from datetime import datetime
from backend.app.schemas.user import UserInfo, UserLogin, UserUpdateRequest
import uuid

class UserService:
    """Kullanıcı bilgilerini yöneten servis"""
    
    def __init__(self):
        # Gerçek uygulamada bu veriler veritabanında saklanacak
        # Şimdilik bellek içinde tutuyoruz
        self.active_users: Dict[str, UserInfo] = {}
        self.current_user_id: Optional[str] = None
    
    async def set_current_user(self, user_login: UserLogin) -> UserInfo:
        """
        Geçerli kullanıcıyı ayarlar
        
        Args:
            user_login: Kullanıcı giriş bilgileri
            
        Returns:
            Kullanıcı bilgileri
        """
        user_info = UserInfo(
            user_id=user_login.user_id,
            username=user_login.username,
            email=user_login.email,
            full_name=user_login.full_name,
            phone=user_login.phone,
            preferences=user_login.preferences or {},
            last_login=datetime.now(),
            is_active=True,
            metadata={}
        )
        
        self.active_users[user_login.user_id] = user_info
        self.current_user_id = user_login.user_id
        
        return user_info
    
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