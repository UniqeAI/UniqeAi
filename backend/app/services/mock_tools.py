"""
Mock API fonksiyonları - Telekom şirketi API'lerini simüle eden araçlar
Bu modül, gerçek bir telekom API'sine bağlanmadan test verileri döndürür.
"""

from typing import Dict, List, Any, Optional
from .user_service import user_service

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

# Mock fatura verileri
MOCK_INVOICES = {
    1: {
        "invoice_id": "INV-2024-001",
        "amount": 299.99,
        "due_date": "2024-06-30",
        "status": "Ödendi"
    },
    2: {
        "invoice_id": "INV-2024-002",
        "amount": 149.99,
        "due_date": "2024-06-30",
        "status": "Beklemede"
    }
}

# Mock müşteri bilgileri
MOCK_CUSTOMERS = {
    1: {
        "customer_id": 1,
        "name": "Ahmet Yılmaz",
        "address": "İstanbul, Türkiye",
        "email": "ahmet.yilmaz@email.com"
    },
    2: {
        "customer_id": 2,
        "name": "Fatma Demir",
        "address": "Ankara, Türkiye",
        "email": "fatma.demir@email.com"
    }
}

# Mock ödeme geçmişi
MOCK_PAYMENTS = {
    1: [
        {"payment_id": "PAY-001", "amount": 299.99, "date": "2024-05-30", "status": "Başarılı"}
    ],
    2: [
        {"payment_id": "PAY-002", "amount": 149.99, "date": "2024-05-30", "status": "Başarılı"}
    ]
}

# Mock abonelik durumu
MOCK_SUBSCRIPTIONS = {
    1: {"status": "Aktif", "start_date": "2023-01-01", "end_date": None},
    2: {"status": "Dondurulmuş", "start_date": "2022-06-01", "end_date": "2024-01-01"}
}

# Mock teknik destek kayıtları
MOCK_SUPPORT_TICKETS = {
    1: [
        {"ticket_id": "SUP-001", "subject": "İnternet bağlantı sorunu", "status": "Çözüldü"}
    ],
    2: [
        {"ticket_id": "SUP-002", "subject": "Fatura itirazı", "status": "Açık"}
    ]
}

# Mock adres bilgisi
MOCK_ADDRESSES = {
    1: {"address": "İstanbul, Türkiye"},
    2: {"address": "Ankara, Türkiye"}
}

# Mock kampanyalar
MOCK_CAMPAIGNS = [
    {"campaign_id": "CMP-001", "name": "Yaz İndirimi", "discount": "%20"},
    {"campaign_id": "CMP-002", "name": "Yeni Abone Fırsatı", "discount": "%15"}
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

def getInvoice(user_id: int) -> Dict[str, Any]:
    if user_id not in MOCK_INVOICES:
        return {"error": "Invoice not found", "message": f"Fatura bulunamadı: {user_id}"}
    return {"success": True, "data": MOCK_INVOICES[user_id]}

def getCustomerInfo(user_id: int) -> Dict[str, Any]:
    if user_id not in MOCK_CUSTOMERS:
        return {"error": "Customer not found", "message": f"Müşteri bulunamadı: {user_id}"}
    return {"success": True, "data": MOCK_CUSTOMERS[user_id]}

def getPaymentHistory(user_id: int) -> Dict[str, Any]:
    if user_id not in MOCK_PAYMENTS:
        return {"error": "Payment history not found", "message": f"Ödeme geçmişi bulunamadı: {user_id}"}
    return {"success": True, "data": MOCK_PAYMENTS[user_id]}

def getSubscriptionStatus(user_id: int) -> Dict[str, Any]:
    if user_id not in MOCK_SUBSCRIPTIONS:
        return {"error": "Subscription not found", "message": f"Abonelik durumu bulunamadı: {user_id}"}
    return {"success": True, "data": MOCK_SUBSCRIPTIONS[user_id]}

def getSupportTickets(user_id: int) -> Dict[str, Any]:
    if user_id not in MOCK_SUPPORT_TICKETS:
        return {"error": "Support tickets not found", "message": f"Destek kaydı bulunamadı: {user_id}"}
    return {"success": True, "data": MOCK_SUPPORT_TICKETS[user_id]}

def getAddress(user_id: int) -> Dict[str, Any]:
    if user_id not in MOCK_ADDRESSES:
        return {"error": "Address not found", "message": f"Adres bulunamadı: {user_id}"}
    return {"success": True, "data": MOCK_ADDRESSES[user_id]}

def getCampaigns() -> Dict[str, Any]:
    return {"success": True, "data": MOCK_CAMPAIGNS}

async def getCurrentUser() -> Dict[str, Any]:
    """
    Geçerli kullanıcı bilgilerini getir
    Bu fonksiyon AI tarafından mevcut kullanıcı bilgilerini almak için kullanılır
    """
    try:
        user_info = await user_service.get_current_user()
        
        if user_info:
            return {
                "success": True, 
                "message": "Geçerli kullanıcı bilgileri başarıyla getirildi",
                "data": {
                    "user_id": user_info.user_id,
                    "username": user_info.username,
                    "email": user_info.email,
                    "full_name": user_info.full_name,
                    "phone": user_info.phone,
                    "preferences": user_info.preferences,
                    "last_login": user_info.last_login.isoformat() if user_info.last_login else None,
                    "is_active": user_info.is_active,
                    "metadata": user_info.metadata
                }
            }
        else:
            return {
                "success": False,
                "message": "Aktif kullanıcı bulunamadı",
                "data": None
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Kullanıcı bilgilerini getirme hatası: {str(e)}",
            "data": None
        } 