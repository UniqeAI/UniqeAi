"""
Mock API fonksiyonları - Telekom şirketi API'lerini simüle eden araçlar
Bu modül, gerçek bir telekom API'sine bağlanmadan test verileri döndürür.
"""

from typing import Dict, List, Any, Optional

# Mock kullanıcı verileri
MOCK_USERS = {
    1: {
        "name": "Ahmet Yılmaz",
        "email": "ahmet.yilmaz@email.com",
        "phone": "+90 532 123 4567",
        "package": "Premium Fiber",
        "package_speed": "100 Mbps",
        "package_price": 299.99
    },
    2: {
        "name": "Fatma Demir",
        "email": "fatma.demir@email.com", 
        "phone": "+90 533 987 6543",
        "package": "Standard ADSL",
        "package_speed": "16 Mbps",
        "package_price": 149.99
    }
}

# Mock paket verileri
AVAILABLE_PACKAGES = [
    {
        "id": "basic_adsl",
        "name": "Basic ADSL",
        "speed": "8 Mbps",
        "price": 99.99
    },
    {
        "id": "standard_adsl", 
        "name": "Standard ADSL",
        "speed": "16 Mbps",
        "price": 149.99
    },
    {
        "id": "premium_fiber",
        "name": "Premium Fiber",
        "speed": "100 Mbps", 
        "price": 299.99
    }
]

def getUserInfo(user_id: int) -> Dict[str, Any]:
    """
    Kullanıcı bilgilerini döndürür
    
    Args:
        user_id: Kullanıcı ID'si
        
    Returns:
        Kullanıcı bilgileri sözlüğü
    """
    if user_id not in MOCK_USERS:
        return {
            "error": "User not found",
            "message": f"Kullanıcı ID {user_id} bulunamadı"
        }
    
    return {
        "success": True,
        "data": MOCK_USERS[user_id]
    }

def getAvailablePackages() -> Dict[str, Any]:
    """
    Mevcut internet paketlerini döndürür
    
    Returns:
        Paket listesi
    """
    return {
        "success": True,
        "data": AVAILABLE_PACKAGES
    } 