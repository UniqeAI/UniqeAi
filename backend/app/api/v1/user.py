"""
Kullanıcı yönetimi endpoint'leri
"""

from fastapi import APIRouter, HTTPException
from app.schemas.user import UserLogin, UserResponse, UserUpdateRequest, UserRegister
from app.services.user_service import user_service
from typing import Dict, Any

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", response_model=UserResponse)
async def register_user(user_register: UserRegister):
    """
    Kullanıcı kayıt endpoint'i - yeni kullanıcı oluşturur
    
    Args:
        user_register: Kullanıcı kayıt bilgileri
        
    Returns:
        Kullanıcı bilgileri ve kayıt durumu
    """
    try:
        user_info = await user_service.register_user(user_register)
        
        return UserResponse(
            success=True,
            message="Kullanıcı başarıyla kayıt oldu",
            data=user_info
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kullanıcı kayıt işlemi sırasında hata oluştu: {str(e)}"
        )

@router.post("/login", response_model=UserResponse)
async def login_user(user_login: UserLogin):
    """
    Kullanıcı giriş endpoint'i - kullanıcı bilgilerini sisteme kaydeder
    
    Args:
        user_login: Kullanıcı giriş bilgileri
        
    Returns:
        Kullanıcı bilgileri ve giriş durumu
    """
    try:
        user_info = await user_service.login_user(user_login)
        
        return UserResponse(
            success=True,
            message="Kullanıcı başarıyla giriş yaptı",
            data=user_info
        )
        
    except ValueError as ve:
        raise HTTPException(
            status_code=401,
            detail=f"Kullanıcı kaydı yok veya şifre hatalı: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kullanıcı giriş işlemi sırasında hata oluştu: {str(e)}"
        )

@router.get("/current", response_model=UserResponse)
async def get_current_user():
    """
    Geçerli kullanıcı bilgilerini getirir - AI bu endpoint'i kullanacak
    
    Returns:
        Geçerli kullanıcı bilgileri
    """
    try:
        user_info = await user_service.get_current_user()
        
        if not user_info:
            return UserResponse(
                success=False,
                message="Aktif kullanıcı bulunamadı",
                data=None
            )
        
        return UserResponse(
            success=True,
            message="Geçerli kullanıcı bilgileri başarıyla getirildi",
            data=user_info
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kullanıcı bilgilerini getirme sırasında hata oluştu: {str(e)}"
        )

@router.get("/profile", response_model=UserResponse)
async def get_user_profile():
    """
    Geçerli kullanıcı profilini getirir - Frontend için alias
    
    Returns:
        Geçerli kullanıcı bilgileri
    """
    try:
        user_info = await user_service.get_current_user()
        
        if not user_info:
            return UserResponse(
                success=False,
                message="Aktif kullanıcı bulunamadı",
                data=None
            )
        
        return UserResponse(
            success=True,
            message="Kullanıcı profili başarıyla getirildi",
            data=user_info
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kullanıcı profili getirme sırasında hata oluştu: {str(e)}"
        )

@router.get("/by-id/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str):
    """
    Belirtilen ID'ye sahip kullanıcı bilgilerini getirir
    
    Args:
        user_id: Kullanıcı ID'si
        
    Returns:
        Kullanıcı bilgileri
    """
    try:
        user_info = await user_service.get_user_by_id(user_id)
        
        if not user_info:
            return UserResponse(
                success=False,
                message=f"ID '{user_id}' ile kullanıcı bulunamadı",
                data=None
            )
        
        return UserResponse(
            success=True,
            message="Kullanıcı bilgileri başarıyla getirildi",
            data=user_info
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kullanıcı bilgilerini getirme sırasında hata oluştu: {str(e)}"
        )

@router.put("/current", response_model=UserResponse)
async def update_current_user(update_request: UserUpdateRequest):
    """
    Geçerli kullanıcının bilgilerini günceller
    
    Args:
        update_request: Güncelleme bilgileri
        
    Returns:
        Güncellenmiş kullanıcı bilgileri
    """
    try:
        user_info = await user_service.update_current_user(update_request)
        
        if not user_info:
            return UserResponse(
                success=False,
                message="Güncellenecek aktif kullanıcı bulunamadı",
                data=None
            )
        
        return UserResponse(
            success=True,
            message="Kullanıcı bilgileri başarıyla güncellendi",
            data=user_info
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kullanıcı bilgilerini güncelleme sırasında hata oluştu: {str(e)}"
        )

@router.post("/logout")
async def logout_current_user():
    """
    Geçerli kullanıcıyı çıkış yapar
    
    Returns:
        Çıkış durumu
    """
    try:
        result = await user_service.logout_current_user()
        
        if result:
            return {
                "success": True,
                "message": "Kullanıcı başarıyla çıkış yaptı"
            }
        else:
            return {
                "success": False,
                "message": "Çıkış yapacak aktif kullanıcı bulunamadı"
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kullanıcı çıkışı sırasında hata oluştu: {str(e)}"
        )

@router.get("/all-active")
async def get_all_active_users():
    """
    Tüm aktif kullanıcıları getirir
    
    Returns:
        Aktif kullanıcılar listesi
    """
    try:
        active_users = await user_service.get_all_active_users()
        
        return {
            "success": True,
            "message": "Aktif kullanıcılar başarıyla getirildi",
            "data": active_users,
            "count": len(active_users)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Aktif kullanıcıları getirme sırasında hata oluştu: {str(e)}"
        ) 