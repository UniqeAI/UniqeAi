"""
Telekom API endpoint'leri - Spesifikasyonda belirtilen tüm endpoint'ler
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import logging

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telekom", tags=["Telekom API"])

# Müşteri verisi merkezi olarak burada tanımlanacak
CUSTOMERS = {
    0: {
        "name": "Enes Faruk Aydın",
        "phone_numbers": [{"number": "+905551234567", "type": "mobile", "status": "active"}],
        "email": "enes.faruk.aydin@email.com",
        "address": "Ankara, Çankaya",
        "registration_date": "2022-06-15",
        "customer_tier": "premium"
    },
    1: {
        "name": "Nisa Nur Özkal",
        "phone_numbers": [{"number": "+905559876543", "type": "mobile", "status": "active"}],
        "email": "nisa.nur.ozkal@email.com",
        "address": "İstanbul, Beşiktaş",
        "registration_date": "2023-03-20",
        "customer_tier": "gold"
    },
    2: {
        "name": "Sedat Kılıçoğlu",
        "phone_numbers": [{"number": "+905551112223", "type": "mobile", "status": "active"}],
        "email": "sedat.kilicoglu@email.com",
        "address": "İzmir, Konak",
        "registration_date": "2021-11-10",
        "customer_tier": "silver"
    },
    3: {
        "name": "Erkan Tanrıöver",
        "phone_numbers": [{"number": "+905554445556", "type": "mobile", "status": "active"}],
        "email": "erkan.tanriover@email.com",
        "address": "Bursa, Nilüfer",
        "registration_date": "2023-08-05",
        "customer_tier": "gold"
    },
    4: {
        "name": "Ahmet Nazif Gemalmaz",
        "phone_numbers": [{"number": "+905557778889", "type": "mobile", "status": "active"}],
        "email": "ahmet.nazif.gemalmaz@email.com",
        "address": "Antalya, Muratpaşa",
        "registration_date": "2022-12-01",
        "customer_tier": "premium"
    },
    5: {
        "name": "Ziişan Şahin",
        "phone_numbers": [{"number": "+905557771234", "type": "mobile", "status": "active"}],
        "email": "ziisan.sahin@email.com",
        "address": "istanbul, eminönü",
        "registration_date": "2024-12-01",
        "customer_tier": "diomand"
    }
}

# Kayıtlı kullanıcılar (email -> user info)
REGISTERED_USERS = {
    "enes.faruk.aydin@email.com": {
        "user_id": 0,
        "email": "enes.faruk.aydin@email.com",
        "password": "enes123",  # Gerçek uygulamada hashlenmeli!
        "name": "Enes Faruk Aydın"
    },
    "nisa.nur.ozkal@email.com": {
        "user_id": 1,
        "email": "nisa.nur.ozkal@email.com",
        "password": "nisa123",
        "name": "Nisa Nur Özkal"
    },
    "sedat.kilicoglu@email.com": {
        "user_id": 2,
        "email": "sedat.kilicoglu@email.com",
        "password": "sedat123",
        "name": "Sedat Kılıçoğlu"
    },
    "erkan.tanriover@email.com": {
        "user_id": 3,
        "email": "erkan.tanriover@email.com",
        "password": "erkan123",
        "name": "Erkan Tanrıöver"
    },
    "ahmet.nazif.gemalmaz@email.com": {
        "user_id": 4,
        "email": "ahmet.nazif.gemalmaz@email.com",
        "password": "ahmet123",
        "name": "Ahmet Nazif Gemalmaz"
    },
    "ziisan.sahin@email.com": {
        "user_id": 5,
        "email": "ziisan.sahin@email.com",
        "password": "ziisan123",
        "name": "Ziişan Şahin"
    }
}

# Kullanıcı paketleri (user_id -> package info veya None)
USER_PACKAGES = {
    0: {
        "package_name": "Premium Paket", 
        "monthly_fee": 89.90, 
        "package_type": "Premium",
        "features": ["Unlimited Data", "Premium Support", "Roaming Included"],
        "internet_speed": "100 Mbps",
        "voice_minutes": "Unlimited",
        "sms_count": "Unlimited",
        "contract_duration": "24 ay"
    },
    1: {
        "package_name": "Öğrenci Dostu", 
        "monthly_fee": 49.90, 
        "package_type": "Student",
        "features": ["10GB Data", "Student Discount", "Basic Support"],
        "internet_speed": "50 Mbps",
        "voice_minutes": "500 dakika",
        "sms_count": "250 SMS",
        "contract_duration": "12 ay"
    },
    2: {
        "package_name": "Süper Konuşma", 
        "monthly_fee": 59.90, 
        "package_type": "Voice",
        "features": ["Unlimited Calls", "5GB Data", "Voice Priority"],
        "internet_speed": "25 Mbps",
        "voice_minutes": "Unlimited",
        "sms_count": "1000 SMS",
        "contract_duration": "12 ay"
    },
    3: {
        "package_name": "Premium Paket", 
        "monthly_fee": 89.90, 
        "package_type": "Premium",
        "features": ["Unlimited Data", "Premium Support", "Roaming Included"],
        "internet_speed": "100 Mbps",
        "voice_minutes": "Unlimited",
        "sms_count": "Unlimited",
        "contract_duration": "24 ay"
    },
    4: {
        "package_name": "Mega İnternet", 
        "monthly_fee": 69.90, 
        "package_type": "Internet",
        "features": ["50GB Data", "High Speed", "Basic Support"],
        "internet_speed": "75 Mbps",
        "voice_minutes": "1000 dakika",
        "sms_count": "500 SMS",
        "contract_duration": "12 ay"
    },
    5: {
        "package_name": "Öğrenci Dostu", 
        "monthly_fee": 49.90, 
        "package_type": "Student",
        "features": ["10GB Data", "Student Discount", "Basic Support"],
        "internet_speed": "50 Mbps",
        "voice_minutes": "500 dakika",
        "sms_count": "250 SMS",
        "contract_duration": "12 ay"
    }
}

# Aktif oturumlar (session_token -> user_id)
ACTIVE_SESSIONS = {}

# ============================================================================
# EKSİK VERİLER - TÜM ENDPOINT'LER İÇİN
# ============================================================================

# Ödeme Geçmişi Verileri
PAYMENT_HISTORY = {
    0: [  # Enes Faruk Aydın
        {"payment_id": "PAY-0001", "bill_id": "F-2024-0000-01", "amount": 65.00, "method": "credit_card", "status": "completed", "date": "2024-01-05"},
        {"payment_id": "PAY-0002", "bill_id": "F-2024-0000-02", "amount": 67.00, "method": "bank_transfer", "status": "completed", "date": "2024-02-05"},
        {"payment_id": "PAY-0003", "bill_id": "F-2024-0000-03", "amount": 69.00, "method": "auto_pay", "status": "completed", "date": "2024-03-05"},
        {"payment_id": "PAY-0004", "bill_id": "F-2024-0000-04", "amount": 71.00, "method": "credit_card", "status": "completed", "date": "2024-04-05"},
        {"payment_id": "PAY-0005", "bill_id": "F-2024-0000-05", "amount": 73.00, "method": "bank_transfer", "status": "completed", "date": "2024-05-05"},
        {"payment_id": "PAY-0006", "bill_id": "F-2024-0000-06", "amount": 75.00, "method": "auto_pay", "status": "completed", "date": "2024-06-05"}
    ],
    1: [  # Nisa Nur Özkal
        {"payment_id": "PAY-0007", "bill_id": "F-2024-0001-01", "amount": 66.00, "method": "credit_card", "status": "completed", "date": "2024-01-05"},
        {"payment_id": "PAY-0008", "bill_id": "F-2024-0001-02", "amount": 68.00, "method": "bank_transfer", "status": "completed", "date": "2024-02-05"},
        {"payment_id": "PAY-0009", "bill_id": "F-2024-0001-03", "amount": 70.00, "method": "auto_pay", "status": "completed", "date": "2024-03-05"},
        {"payment_id": "PAY-0010", "bill_id": "F-2024-0001-04", "amount": 72.00, "method": "credit_card", "status": "completed", "date": "2024-04-05"},
        {"payment_id": "PAY-0011", "bill_id": "F-2024-0001-05", "amount": 74.00, "method": "bank_transfer", "status": "completed", "date": "2024-05-05"},
        {"payment_id": "PAY-0012", "bill_id": "F-2024-0001-06", "amount": 76.00, "method": "auto_pay", "status": "completed", "date": "2024-06-05"}
    ],
    2: [  # Sedat Kılıçoğlu
        {"payment_id": "PAY-0013", "bill_id": "F-2024-0002-01", "amount": 67.00, "method": "credit_card", "status": "completed", "date": "2024-01-05"},
        {"payment_id": "PAY-0014", "bill_id": "F-2024-0002-02", "amount": 69.00, "method": "bank_transfer", "status": "completed", "date": "2024-02-05"},
        {"payment_id": "PAY-0015", "bill_id": "F-2024-0002-03", "amount": 71.00, "method": "auto_pay", "status": "completed", "date": "2024-03-05"},
        {"payment_id": "PAY-0016", "bill_id": "F-2024-0002-04", "amount": 73.00, "method": "credit_card", "status": "completed", "date": "2024-04-05"},
        {"payment_id": "PAY-0017", "bill_id": "F-2024-0002-05", "amount": 75.00, "method": "bank_transfer", "status": "completed", "date": "2024-05-05"},
        {"payment_id": "PAY-0018", "bill_id": "F-2024-0002-06", "amount": 77.00, "method": "auto_pay", "status": "completed", "date": "2024-06-05"}
    ],
    3: [  # Erkan Tanrıöver
        {"payment_id": "PAY-0019", "bill_id": "F-2024-0003-01", "amount": 68.00, "method": "credit_card", "status": "completed", "date": "2024-01-05"},
        {"payment_id": "PAY-0020", "bill_id": "F-2024-0003-02", "amount": 70.00, "method": "bank_transfer", "status": "completed", "date": "2024-02-05"},
        {"payment_id": "PAY-0021", "bill_id": "F-2024-0003-03", "amount": 72.00, "method": "auto_pay", "status": "completed", "date": "2024-03-05"},
        {"payment_id": "PAY-0022", "bill_id": "F-2024-0003-04", "amount": 74.00, "method": "credit_card", "status": "completed", "date": "2024-04-05"},
        {"payment_id": "PAY-0023", "bill_id": "F-2024-0003-05", "amount": 76.00, "method": "bank_transfer", "status": "completed", "date": "2024-05-05"},
        {"payment_id": "PAY-0024", "bill_id": "F-2024-0003-06", "amount": 78.00, "method": "auto_pay", "status": "completed", "date": "2024-06-05"}
    ],
    4: [  # Ahmet Nazif Gemalmaz
        {"payment_id": "PAY-0025", "bill_id": "F-2024-0004-01", "amount": 69.00, "method": "credit_card", "status": "completed", "date": "2024-01-05"},
        {"payment_id": "PAY-0026", "bill_id": "F-2024-0004-02", "amount": 71.00, "method": "bank_transfer", "status": "completed", "date": "2024-02-05"},
        {"payment_id": "PAY-0027", "bill_id": "F-2024-0004-03", "amount": 73.00, "method": "auto_pay", "status": "completed", "date": "2024-03-05"},
        {"payment_id": "PAY-0028", "bill_id": "F-2024-0004-04", "amount": 75.00, "method": "credit_card", "status": "completed", "date": "2024-04-05"},
        {"payment_id": "PAY-0029", "bill_id": "F-2024-0004-05", "amount": 77.00, "method": "bank_transfer", "status": "completed", "date": "2024-05-05"},
        {"payment_id": "PAY-0030", "bill_id": "F-2024-0004-06", "amount": 79.00, "method": "auto_pay", "status": "completed", "date": "2024-06-05"}
    ],
    5: [  # Ziişan Şahin
        {"payment_id": "PAY-0031", "bill_id": "F-2024-0005-01", "amount": 114.00, "method": "credit_card", "status": "completed", "date": "2024-01-05"},
        {"payment_id": "PAY-0032", "bill_id": "F-2024-0005-02", "amount": 116.00, "method": "bank_transfer", "status": "completed", "date": "2024-02-05"},
        {"payment_id": "PAY-0033", "bill_id": "F-2024-0005-03", "amount": 118.00, "method": "auto_pay", "status": "completed", "date": "2024-03-05"},
        {"payment_id": "PAY-0034", "bill_id": "F-2024-0005-04", "amount": 120.00, "method": "credit_card", "status": "completed", "date": "2024-04-05"},
        {"payment_id": "PAY-0035", "bill_id": "F-2024-0005-05", "amount": 122.00, "method": "bank_transfer", "status": "completed", "date": "2024-05-05"},
        {"payment_id": "PAY-0036", "bill_id": "F-2024-0005-06", "amount": 124.00, "method": "auto_pay", "status": "completed", "date": "2024-06-05"}
    ]
}

# Destek Talepleri Verileri
SUPPORT_TICKETS = {
    0: [  # Enes Faruk Aydın
        {"ticket_id": "TICKET-0001", "issue": "İnternet hızı yavaş", "category": "technical", "priority": "medium", "status": "resolved", "created": "2024-01-15"},
        {"ticket_id": "TICKET-0002", "issue": "Fatura sorusu", "category": "billing", "priority": "low", "status": "resolved", "created": "2024-02-20"},
        {"ticket_id": "TICKET-0003", "issue": "Paket değişikliği", "category": "service", "priority": "medium", "status": "open", "created": "2024-03-10"}
    ],
    1: [  # Nisa Nur Özkal
        {"ticket_id": "TICKET-0004", "issue": "SMS gönderemiyorum", "category": "technical", "priority": "high", "status": "resolved", "created": "2024-01-10"},
        {"ticket_id": "TICKET-0005", "issue": "Roaming aktifleştirme", "category": "service", "priority": "medium", "status": "open", "created": "2024-02-25"}
    ],
    2: [  # Sedat Kılıçoğlu
        {"ticket_id": "TICKET-0006", "issue": "Konuşma kesintisi", "category": "technical", "priority": "high", "status": "resolved", "created": "2024-01-20"},
        {"ticket_id": "TICKET-0007", "issue": "Paket bilgisi", "category": "service", "priority": "low", "status": "resolved", "created": "2024-02-15"}
    ],
    3: [  # Erkan Tanrıöver
        {"ticket_id": "TICKET-0008", "issue": "İnternet bağlantı sorunu", "category": "technical", "priority": "medium", "status": "open", "created": "2024-03-05"}
    ],
    4: [  # Ahmet Nazif Gemalmaz
        {"ticket_id": "TICKET-0009", "issue": "Fatura ödeme sorunu", "category": "billing", "priority": "high", "status": "resolved", "created": "2024-01-25"},
        {"ticket_id": "TICKET-0010", "issue": "Premium hizmet aktivasyonu", "category": "service", "priority": "medium", "status": "open", "created": "2024-02-28"}
    ],
    5: [  # Ziişan Şahin
        {"ticket_id": "TICKET-0011", "issue": "Kota aşımı sorusu", "category": "billing", "priority": "low", "status": "resolved", "created": "2024-01-30"},
        {"ticket_id": "TICKET-0012", "issue": "Roaming kullanımı", "category": "service", "priority": "medium", "status": "open", "created": "2024-03-01"}
    ]
}

# Ağ Durumu Verileri
NETWORK_STATUS = {
    "istanbul": {
        "status": "excellent",
        "coverage": 95,
        "speed": "100 Mbps",
        "issues": [],
        "last_update": "2024-03-01T10:00:00Z"
    },
    "ankara": {
        "status": "good",
        "coverage": 90,
        "speed": "85 Mbps",
        "issues": ["Minor maintenance in Çankaya"],
        "last_update": "2024-03-01T10:00:00Z"
    },
    "izmir": {
        "status": "fair",
        "coverage": 85,
        "speed": "75 Mbps",
        "issues": ["Network upgrade in progress"],
        "last_update": "2024-03-01T10:00:00Z"
    },
    "bursa": {
        "status": "good",
        "coverage": 88,
        "speed": "80 Mbps",
        "issues": [],
        "last_update": "2024-03-01T10:00:00Z"
    },
    "antalya": {
        "status": "excellent",
        "coverage": 92,
        "speed": "95 Mbps",
        "issues": [],
        "last_update": "2024-03-01T10:00:00Z"
    }
}

# Hız Testi Verileri
SPEED_TEST_DATA = {
    0: {"download": 100, "upload": 50, "ping": 15, "jitter": 5},
    1: {"download": 95, "upload": 48, "ping": 18, "jitter": 6},
    2: {"download": 90, "upload": 45, "ping": 20, "jitter": 7},
    3: {"download": 85, "upload": 42, "ping": 22, "jitter": 8},
    4: {"download": 80, "upload": 40, "ping": 25, "jitter": 9},
    5: {"download": 75, "upload": 37, "ping": 28, "jitter": 10}
}

# Roaming Verileri
ROAMING_DATA = {
    0: {"enabled": True, "countries": ["Türkiye", "Almanya", "Fransa"], "usage": 2.5, "cost": 15.00},
    1: {"enabled": False, "countries": [], "usage": 0, "cost": 0},
    2: {"enabled": True, "countries": ["Türkiye", "İtalya"], "usage": 1.8, "cost": 12.00},
    3: {"enabled": True, "countries": ["Türkiye", "İspanya", "Portekiz"], "usage": 3.2, "cost": 18.50},
    4: {"enabled": False, "countries": [], "usage": 0, "cost": 0},
    5: {"enabled": True, "countries": ["Türkiye", "Hollanda", "Belçika"], "usage": 4.1, "cost": 22.00}
}

# Paket Değişiklik Geçmişi
PACKAGE_CHANGE_HISTORY = {
    0: [
        {"old_package": "Öğrenci Dostu", "new_package": "Mega İnternet", "date": "2023-06-15", "reason": "İnternet ihtiyacı arttı"},
        {"old_package": "Mega İnternet", "new_package": "Premium Paket", "date": "2024-01-10", "reason": "Premium hizmetler istendi"}
    ],
    1: [
        {"old_package": "Süper Konuşma", "new_package": "Öğrenci Dostu", "date": "2023-09-20", "reason": "Bütçe tasarrufu"}
    ],
    2: [
        {"old_package": "Mega İnternet", "new_package": "Süper Konuşma", "date": "2023-12-05", "reason": "Konuşma ihtiyacı arttı"}
    ],
    3: [
        {"old_package": "Öğrenci Dostu", "new_package": "Premium Paket", "date": "2024-02-15", "reason": "Premium hizmetler istendi"}
    ],
    4: [
        {"old_package": "Süper Konuşma", "new_package": "Mega İnternet", "date": "2023-08-10", "reason": "İnternet ihtiyacı arttı"}
    ],
    5: [
        {"old_package": "Premium Paket", "new_package": "Öğrenci Dostu", "date": "2024-01-25", "reason": "Bütçe tasarrufu"}
    ]
}

# Otomatik Ödeme Verileri
AUTOPAY_DATA = {
    0: {"enabled": True, "method": "credit_card", "card_last4": "1234", "next_payment": "2024-04-15"},
    1: {"enabled": False, "method": None, "card_last4": None, "next_payment": None},
    2: {"enabled": True, "method": "bank_transfer", "account_last4": "5678", "next_payment": "2024-04-15"},
    3: {"enabled": True, "method": "credit_card", "card_last4": "9012", "next_payment": "2024-04-15"},
    4: {"enabled": False, "method": None, "card_last4": None, "next_payment": None},
    5: {"enabled": True, "method": "bank_transfer", "account_last4": "3456", "next_payment": "2024-04-15"}
}

# Hat Askıya Alma Verileri
LINE_SUSPENSION_DATA = {
    0: {"suspended": False, "reason": None, "suspension_date": None},
    1: {"suspended": True, "reason": "Ödeme gecikmesi", "suspension_date": "2024-02-15"},
    2: {"suspended": False, "reason": None, "suspension_date": None},
    3: {"suspended": False, "reason": None, "suspension_date": None},
    4: {"suspended": True, "reason": "Talep üzerine", "suspension_date": "2024-03-01"},
    5: {"suspended": False, "reason": None, "suspension_date": None}
}

def get_mock_customer_data(user_id: int):
    """User ID'ye göre mock müşteri verisi döner"""
    return CUSTOMERS.get(user_id, CUSTOMERS[0])

def get_mock_bill_data(user_id: int):
    """User ID'ye göre mock fatura verisi döner"""
    base_amount = 50 + (user_id % 50)  # 50-99 arası
    return {
        "bill_id": f"F-2024-{user_id:04d}",
        "user_id": user_id,
        "amount": base_amount,
        "currency": "TRY",
        "due_date": "2024-03-15",
        "bill_date": "2024-02-28",
        "status": "unpaid" if user_id % 3 == 0 else "paid",
        "services": [
            {
                "service_name": "Mega İnternet",
                "amount": base_amount * 0.7
            },
            {
                "service_name": "Sesli Arama", 
                "amount": base_amount * 0.3
            }
        ]
    }

def get_mock_package_data(user_id: int):
    """User ID'ye göre mock paket verisi döner"""
    packages = [
        {
            "package_name": "Mega İnternet",
            "monthly_fee": 69.50,
            "features": {"internet_gb": 50, "voice_minutes": 1000, "sms_count": 500, "roaming_enabled": False}
        },
        {
            "package_name": "Öğrenci Dostu Tarife",
            "monthly_fee": 49.90,
            "features": {"internet_gb": 30, "voice_minutes": 500, "sms_count": 250, "roaming_enabled": False}
        },
        {
            "package_name": "Süper Konuşma",
            "monthly_fee": 59.90,
            "features": {"internet_gb": 25, "voice_minutes": 2000, "sms_count": 1000, "roaming_enabled": True}
        },
        {
            "package_name": "Premium Paket",
            "monthly_fee": 89.90,
            "features": {"internet_gb": 100, "voice_minutes": 3000, "sms_count": 1000, "roaming_enabled": True}
        }
    ]
    package = packages[user_id % len(packages)]
    return {
        **package,
        "activation_date": "2024-01-01",
        "renewal_date": "2024-04-01"
    }

def get_mock_quotas_data(user_id: int):
    """User ID'ye göre mock kota verisi döner"""
    base_internet = 50 - (user_id % 30)  # 20-50 GB arası
    base_voice = 1000 - (user_id % 400)  # 600-1000 dakika arası
    base_sms = 500 - (user_id % 200)     # 300-500 SMS arası
    
    return {
        "internet_remaining_gb": base_internet,
        "voice_remaining_minutes": base_voice,
        "sms_remaining": base_sms,
        "period_end": "2024-03-31",
        "usage_percentage": {
            "internet": (user_id % 30) + 10,
            "voice": (user_id % 40) + 5,
            "sms": (user_id % 20) + 5
        }
    }

# ============================================================================
# TEST ENDPOINT'LERİ (GET)
# ============================================================================

@router.get("/test")
async def test_endpoint():
    """Test endpoint'i - tarayıcıda test etmek için"""
    return {
        "success": True,
        "message": "Telekom API çalışıyor! 🎉",
        "mock_data_info": "Her user_id için farklı mock veriler döner",
        "example_user_ids": [0, 1, 2, 3, 4],
        "endpoints": [
            "POST /api/v1/telekom/billing/current",
            "POST /api/v1/telekom/billing/history", 
            "POST /api/v1/telekom/billing/payments",
            "POST /api/v1/telekom/packages/current",
            "POST /api/v1/telekom/packages/quotas",
            "POST /api/v1/telekom/customers/profile",
            "POST /api/v1/telekom/diagnostics/speed-test",
            "POST /api/v1/telekom/support/tickets"
        ],
        "test_examples": {
            "user_0": "Mehmet Demir (Premium)",
            "user_1": "Ayşe Kaya (Gold)", 
            "user_2": "Ali Özkan (Silver)",
            "user_3": "Fatma Şahin (Gold)",
            "user_4": "Mustafa Yılmaz (Premium)"
        }
    }

@router.get("/billing/current/{user_id}")
async def get_current_bill_test(user_id: int):
    """Mevcut fatura bilgilerini getir (GET test için)"""
    try:
        logger.info(f"Mevcut fatura sorgulanıyor: User ID {user_id}")
        
        # Mock veri - gerçek uygulamada veritabanından alınır
        bill_data = {
            "bill_id": f"F-2024-{user_id}",
            "user_id": user_id,
            "amount": 75.50,
            "currency": "TRY",
            "due_date": "2024-03-15",
            "bill_date": "2024-02-28",
            "status": "unpaid" if user_id % 3 == 0 else "paid",
            "services": [
                {
                    "service_name": "Mega İnternet",
                    "amount": 52.85
                },
                {
                    "service_name": "Sesli Arama", 
                    "amount": 22.65
                }
            ]
        }
        
        return {
            "success": True,
            "data": bill_data
        }
        
    except Exception as e:
        logger.error(f"Mevcut fatura getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Mevcut fatura getirme hatası: {str(e)}")

@router.get("/packages/current/{user_id}")
async def get_customer_package_test(user_id: int):
    """Müşterinin mevcut paketini getir (GET test için)"""
    try:
        logger.info(f"Mevcut paket sorgulanıyor: User ID {user_id}")
        
        package_data = get_mock_package_data(user_id)
        
        return {
            "success": True,
            "data": package_data
        }
        
    except Exception as e:
        logger.error(f"Mevcut paket getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Mevcut paket getirme hatası: {str(e)}")

@router.get("/customers/profile/{user_id}")
async def get_customer_profile_test(user_id: int):
    """Müşteri profilini getir (GET test için)"""
    try:
        logger.info(f"Müşteri profili sorgulanıyor: User ID {user_id}")
        
        customer_data = get_mock_customer_data(user_id)
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                **customer_data
            }
        }
        
    except Exception as e:
        logger.error(f"Müşteri profili getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Müşteri profili getirme hatası: {str(e)}")

# ============================================================================
# REQUEST MODELS
# ============================================================================

class UserIdRequest(BaseModel):
    user_id: int

class BillIdRequest(BaseModel):
    bill_id: str

class PaymentRequest(BaseModel):
    session_token: str
    bill_id: str
    method: str

class PastBillsRequest(BaseModel):
    session_token: str
    limit: int

class AutopayRequest(BaseModel):
    session_token: str
    status: bool

class PackageChangeRequest(BaseModel):
    session_token: str
    new_package_name: str

class PackageDetailsRequest(BaseModel):
    package_name: str

class RoamingRequest(BaseModel):
    session_token: str
    status: bool

class NetworkStatusRequest(BaseModel):
    region: str

class FaultTicketRequest(BaseModel):
    session_token: str
    issue_description: str
    category: str  # Yeni eklendi
    priority: str  # Yeni eklendi

class TicketStatusRequest(BaseModel):
    ticket_id: str

class ContactUpdateRequest(BaseModel):
    session_token: str
    contact_type: str
    new_value: str

class LineSuspendRequest(BaseModel):
    session_token: str
    reason: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SessionRequest(BaseModel):
    session_token: str

class AuthenticatedUserIdRequest(BaseModel):
    session_token: str

# ============================================================================
# BILLING ENDPOINT'LERİ
# ============================================================================

@router.post("/billing/current")
async def get_current_bill(request: AuthenticatedUserIdRequest):
    """Mevcut fatura bilgilerini getir"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Mevcut fatura sorgulanıyor: User ID {user_id}")
        
        bill_data = get_mock_bill_data(user_id)
        
        return {
            "success": True,
            "data": bill_data
        }
        
    except Exception as e:
        logger.error(f"Mevcut fatura getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Mevcut fatura getirme hatası: {str(e)}")

@router.post("/billing/history")
async def get_past_bills(request: PastBillsRequest):
    """Geçmiş faturaları getir"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Fatura geçmişi sorgulanıyor: User ID {user_id}, Limit: {request.limit}")
        
        bills = []
        base_amount = 50 + (user_id % 50)
        
        # Daha detaylı geçmiş faturalar
        for i in range(min(request.limit, 24)):  # 24 adet fatura (2 yıl)
            # Farklı aylar için farklı tutarlar
            month_variation = (i % 12) * 2  # 0-22 arası
            seasonal_adjustment = 0
            
            # Yaz aylarında (6-8) daha yüksek fatura
            if i % 12 in [5, 6, 7]:  # Haziran, Temmuz, Ağustos
                seasonal_adjustment = 15
            
            # Kış aylarında (12-2) orta fatura
            elif i % 12 in [11, 0, 1]:  # Aralık, Ocak, Şubat
                seasonal_adjustment = 10
            
            # Diğer aylarda normal fatura
            else:
                seasonal_adjustment = 5
            
            bill_amount = base_amount + month_variation + seasonal_adjustment
            
            # Fatura durumu: Son 3 fatura ödenmemiş olabilir
            bill_status = "paid" if i < 21 else "unpaid"
            
            # Farklı hizmet kombinasyonları
            services = []
            if i % 4 == 0:  # Her 4. fatura sadece internet
                services = [
                    {
                        "service_name": "Mega İnternet",
                        "amount": bill_amount * 0.8
                    },
                    {
                        "service_name": "Sesli Arama",
                        "amount": bill_amount * 0.2
                    }
                ]
            elif i % 4 == 1:  # Her 4. fatura + SMS
                services = [
                    {
                        "service_name": "Mega İnternet",
                        "amount": bill_amount * 0.7
                    },
                    {
                        "service_name": "Sesli Arama",
                        "amount": bill_amount * 0.2
                    },
                    {
                        "service_name": "SMS Paketi",
                        "amount": bill_amount * 0.1
                    }
                ]
            elif i % 4 == 2:  # Her 4. fatura + roaming
                services = [
                    {
                        "service_name": "Mega İnternet",
                        "amount": bill_amount * 0.6
                    },
                    {
                        "service_name": "Sesli Arama",
                        "amount": bill_amount * 0.2
                    },
                    {
                        "service_name": "Roaming Servisi",
                        "amount": bill_amount * 0.2
                    }
                ]
            else:  # Her 4. fatura premium hizmetler
                services = [
                    {
                        "service_name": "Mega İnternet",
                        "amount": bill_amount * 0.5
                    },
                    {
                        "service_name": "Sesli Arama",
                        "amount": bill_amount * 0.2
                    },
                    {
                        "service_name": "Premium Hizmetler",
                        "amount": bill_amount * 0.3
                    }
                ]
            
            # Gerçekçi tarihler (2023-2024)
            year = 2023 if i < 12 else 2024
            month = (i % 12) + 1
            
            bill_data = {
                "bill_id": f"F-{year}-{user_id:04d}-{month:02d}",
                "user_id": user_id,
                "amount": bill_amount,
                "currency": "TRY",
                "bill_date": f"{year}-{month:02d}-28",
                "due_date": f"{year}-{month+1:02d}-15",
                "status": bill_status,
                "services": services,
                "payment_method": "credit_card" if i % 3 == 0 else "bank_transfer" if i % 3 == 1 else "auto_pay",
                "late_fee": 0 if bill_status == "paid" else 15.50,
                "discount_applied": 5.00 if i % 6 == 0 else 0.00  # Her 6. faturada indirim
            }
            bills.append(bill_data)
        
        return {
            "success": True,
            "data": {
                "bills": bills,
                "total_count": len(bills),
                "user_id": user_id,
                "total_paid": sum(bill["amount"] for bill in bills if bill["status"] == "paid"),
                "total_unpaid": sum(bill["amount"] for bill in bills if bill["status"] == "unpaid"),
                "average_amount": sum(bill["amount"] for bill in bills) / len(bills)
            }
        }
        
    except Exception as e:
        logger.error(f"Fatura geçmişi getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Fatura geçmişi getirme hatası: {str(e)}")

@router.post("/billing/pay")
async def pay_bill(request: PaymentRequest):
    """Fatura ödemesi yap"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Fatura ödemesi yapılıyor: User ID {user_id}, Bill ID {request.bill_id}, Method: {request.method}")
        
        payment_data = {
            "payment_id": f"PAY-{request.bill_id}",
            "bill_id": request.bill_id,
            "user_id": user_id,
            "amount": 75.50,
            "method": request.method,
            "status": "completed",
            "transaction_date": "2024-03-01T14:30:00Z",
            "confirmation_code": f"CONF-{request.bill_id}"
        }
        
        return {
            "success": True,
            "data": payment_data
        }
        
    except Exception as e:
        logger.error(f"Fatura ödeme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Fatura ödeme hatası: {str(e)}")

@router.post("/billing/payments")
async def get_payment_history(request: AuthenticatedUserIdRequest):
    """Ödeme geçmişini getir"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Ödeme geçmişi sorgulanıyor: User ID {user_id}")
        
        # Yeni detaylı ödeme verilerini kullan
        payments = PAYMENT_HISTORY.get(user_id, [])
        
        return {
            "success": True,
            "data": {
                "payments": payments,
                "total_count": len(payments),
                "user_id": user_id,
                "total_amount": sum(payment["amount"] for payment in payments),
                "payment_methods": list(set(payment["method"] for payment in payments))
            }
        }
        
    except Exception as e:
        logger.error(f"Ödeme geçmişi getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Ödeme geçmişi getirme hatası: {str(e)}")

@router.post("/billing/autopay")
async def setup_autopay(request: AutopayRequest):
    """Otomatik ödeme ayarlar"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Otomatik ödeme ayarlanıyor: User ID {user_id}, Status: {request.status}")
        
        # Yeni detaylı otomatik ödeme verilerini kullan
        autopay_data = AUTOPAY_DATA.get(user_id, {
            "enabled": False,
            "method": None,
            "card_last4": None,
            "next_payment": None
        })
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "autopay_enabled": request.status,
                "payment_method": autopay_data["method"] if request.status else None,
                "card_last4": autopay_data["card_last4"] if request.status else None,
                "next_payment_date": autopay_data["next_payment"] if request.status else None,
                "last_updated": "2024-03-01T14:30:00Z"
            }
        }
        
    except Exception as e:
        logger.error(f"Otomatik ödeme ayarlama hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Otomatik ödeme ayarlama hatası: {str(e)}")

# ============================================================================
# PACKAGE ENDPOINT'LERİ
# ============================================================================

@router.post("/packages/current")
async def get_customer_package(request: AuthenticatedUserIdRequest):
    """Müşterinin mevcut paketini getir"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Mevcut paket sorgulanıyor: User ID {user_id}")
        
        # Önce USER_PACKAGES dict'ine bak
        package_data = USER_PACKAGES.get(user_id)
        if package_data is None:
            return {
                "success": False,
                "message": "Kullanıcının aktif bir paketi yok.",
                "data": None
            }
        return {
            "success": True,
            "data": package_data
        }
    except Exception as e:
        logger.error(f"Mevcut paket getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Mevcut paket getirme hatası: {str(e)}")

@router.post("/packages/quotas")
async def get_remaining_quotas(request: AuthenticatedUserIdRequest):
    """Müşterinin kalan kotalarını getir"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Kalan kotalar sorgulanıyor: User ID {user_id}")
        
        quota_data = get_mock_quotas_data(user_id)
        
        return {
            "success": True,
            "data": quota_data
        }
        
    except Exception as e:
        logger.error(f"Kalan kotalar getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Kalan kotalar getirme hatası: {str(e)}")

@router.post("/packages/change")
async def change_package(request: PackageChangeRequest):
    """Paket değişikliği başlat"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Paket değişikliği başlatılıyor: User ID {user_id}, New Package: {request.new_package_name}")
        
        change_data = {
            "change_id": f"CHG-{user_id:04d}",
            "user_id": user_id,
            "current_package": "Mega İnternet",
            "new_package": request.new_package_name,
            "status": "pending",
            "effective_date": "2024-04-01T00:00:00Z",
            "estimated_cost": 89.90
        }
        
        return {
            "success": True,
            "data": change_data
        }
        
    except Exception as e:
        logger.error(f"Paket değişikliği hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Paket değişikliği hatası: {str(e)}")

@router.post("/packages/available")
async def get_available_packages():
    """Kullanılabilir paketleri listele"""
    try:
        logger.info("Kullanılabilir paketler sorgulanıyor")
        
        packages = [
            {
                "package_name": "Mega İnternet",
                "monthly_fee": 69.50,
                "features": {"internet_gb": 50, "voice_minutes": 1000, "sms_count": 500, "roaming_enabled": False},
                "description": "Hızlı internet ve bol dakika"
            },
            {
                "package_name": "Öğrenci Dostu Tarife",
                "monthly_fee": 49.90,
                "features": {"internet_gb": 30, "voice_minutes": 500, "sms_count": 250, "roaming_enabled": False},
                "description": "Öğrenciler için özel tarife"
            },
            {
                "package_name": "Süper Konuşma",
                "monthly_fee": 59.90,
                "features": {"internet_gb": 25, "voice_minutes": 2000, "sms_count": 1000, "roaming_enabled": True},
                "description": "Bol dakika ve SMS"
            },
            {
                "package_name": "Premium Paket",
                "monthly_fee": 89.90,
                "features": {"internet_gb": 100, "voice_minutes": 3000, "sms_count": 1000, "roaming_enabled": True},
                "description": "Premium hizmetler"
            }
        ]
        
        return {
            "success": True,
            "data": {
                "packages": packages,
                "total_count": len(packages)
            }
        }
        
    except Exception as e:
        logger.error(f"Kullanılabilir paketler getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Kullanılabilir paketler getirme hatası: {str(e)}")

@router.post("/packages/details")
async def get_package_details(request: PackageDetailsRequest):
    """Paket detaylarını getir"""
    try:
        logger.info(f"Paket detayları sorgulanıyor: Package {request.package_name}")
        
        package_details = {
            "package_name": request.package_name,
            "monthly_fee": 69.50,
            "features": {
                "internet_gb": 50,
                "voice_minutes": 1000,
                "sms_count": 500,
                "roaming_enabled": False
            },
            "description": "Hızlı internet ve bol dakika",
            "contract_duration": "12 ay",
            "early_termination_fee": 200.00,
            "activation_fee": 0.00
        }
        
        return {
            "success": True,
            "data": package_details
        }
        
    except Exception as e:
        logger.error(f"Paket detayları getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Paket detayları getirme hatası: {str(e)}")

@router.post("/services/roaming")
async def enable_roaming(request: RoamingRequest):
    """Roaming hizmetini etkinleştir/devre dışı bırak"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Roaming ayarlanıyor: User ID {user_id}, Status: {request.status}")
        
        # Yeni detaylı roaming verilerini kullan
        roaming_data = ROAMING_DATA.get(user_id, {
            "enabled": False,
            "countries": [],
            "usage": 0,
            "cost": 0
        })
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
            "roaming_enabled": request.status,
            "effective_date": "2024-03-01T14:30:00Z",
                "supported_countries": roaming_data["countries"],
                "current_usage": roaming_data["usage"],
                "current_cost": roaming_data["cost"],
            "daily_fee": 15.00 if request.status else 0.00
        }
        }
        
    except Exception as e:
        logger.error(f"Roaming ayarlama hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Roaming ayarlama hatası: {str(e)}")

# ============================================================================
# NETWORK & DIAGNOSTICS ENDPOINT'LERİ
# ============================================================================

@router.post("/network/status")
async def check_network_status(request: NetworkStatusRequest):
    """Ağ durumunu kontrol et"""
    try:
        logger.info(f"Ağ durumu kontrol ediliyor: Region {request.region}")
        
        # Yeni detaylı ağ verilerini kullan
        network_status = NETWORK_STATUS.get(request.region.lower(), {
            "status": "unknown",
            "coverage": 0,
            "speed": "0 Mbps",
            "issues": ["Region not found"],
            "last_update": "2024-03-01T10:00:00Z"
        })
        
        return {
            "success": True,
            "data": {
                "region": request.region,
                **network_status
            }
        }
        
    except Exception as e:
        logger.error(f"Ağ durumu kontrol hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Ağ durumu kontrol hatası: {str(e)}")

@router.post("/support/tickets")
async def create_fault_ticket(request: FaultTicketRequest):
    """Destek talebi oluştur"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Destek talebi oluşturuluyor: User ID {user_id}")
        
        ticket_data = {
            "ticket_id": f"T-{user_id:04d}",
            "user_id": user_id,
            "issue_description": request.issue_description,
            "category": request.category,
            "priority": request.priority,
            "status": "open",
            "created_date": "2024-03-01T14:30:00Z",
            "estimated_resolution": "2024-03-04T14:30:00Z",
            "assigned_to": "Technical Support Team"
        }
        
        return {
            "success": True,
            "data": ticket_data
        }
        
    except Exception as e:
        logger.error(f"Destek talebi oluşturma hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Destek talebi oluşturma hatası: {str(e)}")

@router.post("/support/tickets/close")
async def close_fault_ticket(request: TicketStatusRequest):
    """Destek talebini kapat"""
    try:
        logger.info(f"Destek talebi kapatılıyor: Ticket ID {request.ticket_id}")
        
        def normalize_ticket_id(ticket_id):
            # Sondaki rakamları al
            import re
            digits = re.findall(r'\d+', ticket_id)
            return '-'.join(digits) if digits else ticket_id

        req_norm = normalize_ticket_id(request.ticket_id)
        found_ticket = None
        found_user_id = None
        for user_id, tickets in SUPPORT_TICKETS.items():
            for ticket in tickets:
                t_norm = normalize_ticket_id(ticket["ticket_id"])
                if req_norm == t_norm:
                    found_ticket = ticket
                    found_user_id = user_id
                    break
            if found_ticket:
                break

        close_data = {
            "ticket_id": request.ticket_id,
            "status": "closed",
            "closed_date": "2024-03-01T15:30:00Z",
            "resolution": "Sorun çözüldü",
            "satisfaction_rating": 5,
            "user_id": found_user_id if found_user_id is not None else "N/A",
            "issue_description": found_ticket["issue"] if found_ticket else "Açıklama bulunamadı"
        }
        
        return {
            "success": True,
            "data": close_data
        }
        
    except Exception as e:
        logger.error(f"Destek talebi kapatma hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Destek talebi kapatma hatası: {str(e)}")

@router.post("/support/tickets/status")
async def get_fault_ticket_status(request: TicketStatusRequest):
    """Destek talebi durumunu getir"""
    try:
        logger.info(f"Destek talebi durumu sorgulanıyor: Ticket ID {request.ticket_id}")
        
        status_data = {
            "ticket_id": request.ticket_id,
            "status": "in_progress",
            "last_updated": "2024-03-01T16:30:00Z",
            "progress": 75,
            "estimated_completion": "2024-03-02T14:30:00Z",
            "assigned_technician": "Ahmet Yılmaz",
            "notes": "Teknik ekip sorunu inceliyor"
        }
        
        return {
            "success": True,
            "data": status_data
        }
        
    except Exception as e:
        logger.error(f"Destek talebi durumu getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Destek talebi durumu getirme hatası: {str(e)}")

@router.post("/diagnostics/speed-test")
async def test_internet_speed(request: AuthenticatedUserIdRequest):
    """İnternet hız testi yap"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"İnternet hız testi yapılıyor: User ID {user_id}")
        
        # Yeni detaylı hız verilerini kullan
        speed_data = SPEED_TEST_DATA.get(user_id, {
            "download": 75,
            "upload": 37,
            "ping": 28,
            "jitter": 10
        })
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
            "test_date": "2024-03-01T14:30:00Z",
                "download_speed_mbps": speed_data["download"],
                "upload_speed_mbps": speed_data["upload"],
                "ping_ms": speed_data["ping"],
                "jitter_ms": speed_data["jitter"],
            "packet_loss_percent": 0.1,
            "connection_quality": "excellent",
            "server_location": "Istanbul"
        }
        }
        
    except Exception as e:
        logger.error(f"İnternet hız testi hatası: {e}")
        raise HTTPException(status_code=500, detail=f"İnternet hız testi hatası: {str(e)}")

# ============================================================================
# CUSTOMER MANAGEMENT ENDPOINT'LERİ
# ============================================================================

@router.post("/customers/profile")
async def get_customer_profile(request: AuthenticatedUserIdRequest):
    """Müşteri profilini getir"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Müşteri profili sorgulanıyor: User ID {user_id}")
        
        customer_data = get_mock_customer_data(user_id)
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                **customer_data
            }
        }
        
    except Exception as e:
        logger.error(f"Müşteri profili getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Müşteri profili getirme hatası: {str(e)}")

@router.post("/customers/contact")
async def update_customer_contact(request: ContactUpdateRequest):
    """Müşteri iletişim bilgilerini güncelle"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"İletişim bilgisi güncelleniyor: User ID {user_id}, Type: {request.contact_type}")
        
        update_data = {
            "user_id": user_id,
            "contact_type": request.contact_type,
            "old_value": "eski_değer",
            "new_value": request.new_value,
            "updated_date": "2024-03-01T14:30:00Z",
            "status": "updated"
        }
        
        return {
            "success": True,
            "data": update_data
        }
        
    except Exception as e:
        logger.error(f"İletişim bilgisi güncelleme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"İletişim bilgisi güncelleme hatası: {str(e)}")

@router.post("/lines/suspend")
async def suspend_line(request: LineSuspendRequest):
    """Hatı askıya al"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Hat askıya alınıyor: User ID {user_id}, Reason: {request.reason}")
        
        # Yeni detaylı hat askıya alma verilerini kullan
        suspension_data = LINE_SUSPENSION_DATA.get(user_id, {
            "suspended": False,
            "reason": None,
            "suspension_date": None
        })
        
        suspend_data = {
            "user_id": user_id,
            "status": "suspended" if request.reason else "active",
            "reason": request.reason,
            "suspended_date": "2024-03-01T14:30:00Z",
            "reactivation_fee": 25.00,
            "estimated_reactivation_date": "2024-03-08T14:30:00Z",
            "current_suspension": suspension_data
        }
        
        return {
            "success": True,
            "data": suspend_data
        }
        
    except Exception as e:
        logger.error(f"Hat askıya alma hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Hat askıya alma hatası: {str(e)}")

@router.post("/lines/reactivate")
async def reactivate_line(request: AuthenticatedUserIdRequest):
    """Hatı yeniden etkinleştir"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Hat yeniden etkinleştiriliyor: User ID {user_id}")
        
        reactivate_data = {
            "user_id": user_id,
            "status": "active",
            "reactivated_date": "2024-03-01T15:30:00Z",
            "reactivation_fee_paid": True,
            "services_restored": ["voice", "data", "sms"]
        }
        
        return {
            "success": True,
            "data": reactivate_data
        }
        
    except Exception as e:
        logger.error(f"Hat yeniden etkinleştirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Hat yeniden etkinleştirme hatası: {str(e)}")

@router.post("/support/tickets/list")
async def get_users_tickets(request: AuthenticatedUserIdRequest):
    """Kullanıcının tüm destek taleplerini getirir"""
    try:
        # Session doğrulaması
        user_id = get_current_user_from_token(request.session_token)
        logger.info(f"Kullanıcı destek talepleri sorgulanıyor: User ID {user_id}")
        
        # Yeni detaylı destek verilerini kullan
        tickets = SUPPORT_TICKETS.get(user_id, [])
        
        return {
            "success": True,
            "data": {
                "tickets": tickets,
                "user_id": user_id,
                "total_count": len(tickets),
                "open_tickets": len([t for t in tickets if t["status"] == "open"]),
                "resolved_tickets": len([t for t in tickets if t["status"] == "resolved"])
            }
        }
    except Exception as e:
        logger.error(f"Kullanıcı destek talepleri getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Kullanıcı destek talepleri getirme hatası: {str(e)}")

@router.post("/auth/register")
async def register_user(request: RegisterRequest):
    """Kullanıcı kaydı endpointi"""
    if request.email in REGISTERED_USERS:
        raise HTTPException(status_code=400, detail="Bu email ile zaten bir kullanıcı var.")
    
    # Yeni user_id ata (mevcut kullanıcılardan sonra)
    max_user_id = max([user["user_id"] for user in REGISTERED_USERS.values()]) if REGISTERED_USERS else -1
    user_id = max_user_id + 1
    
    user_info = {
        "user_id": user_id,
        "email": request.email,
        "password": request.password,  # Not: Gerçek uygulamada hashlenmeli!
        "name": request.name
    }
    REGISTERED_USERS[request.email] = user_info
    USER_PACKAGES[user_id] = None  # Başlangıçta paketi yok
    
    # Session oluştur
    session_token = create_session(user_id)
    
    return {
        "success": True, 
        "message": "Kayıt başarılı.", 
        "user_id": user_id,
        "session_token": session_token,
        "user_name": request.name
    }

@router.post("/auth/login")
async def login_user(request: LoginRequest):
    """Kullanıcı girişi endpointi"""
    try:
        user = authenticate_user(request.email, request.password)
        
        # Session oluştur
        session_token = create_session(user["user_id"])
        
        return {
            "success": True, 
            "message": "Giriş başarılı.", 
            "user_id": user["user_id"],
            "session_token": session_token,
            "user_name": user["name"]
        }
    except HTTPException:
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı.")

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

import secrets
import time

def generate_session_token() -> str:
    """Güvenli session token oluşturur"""
    return secrets.token_urlsafe(32)

def create_session(user_id: int) -> str:
    """Kullanıcı için session oluşturur"""
    token = generate_session_token()
    ACTIVE_SESSIONS[token] = {
        "user_id": user_id,
        "created_at": time.time(),
        "expires_at": time.time() + (24 * 60 * 60)  # 24 saat
    }
    return token

def validate_session(token: str) -> int:
    """Session token'ı doğrular ve user_id döner"""
    if token not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=401, detail="Geçersiz session token")
    
    session = ACTIVE_SESSIONS[token]
    if time.time() > session["expires_at"]:
        del ACTIVE_SESSIONS[token]
        raise HTTPException(status_code=401, detail="Session süresi dolmuş")
    
    return session["user_id"]

def get_user_from_email(email: str) -> dict:
    """Email ile kullanıcı bilgilerini getirir"""
    if email not in REGISTERED_USERS:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return REGISTERED_USERS[email]

def authenticate_user(email: str, password: str) -> dict:
    """Kullanıcı kimlik doğrulaması yapar"""
    user = get_user_from_email(email)
    if user["password"] != password:
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı")
    return user

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_all_customer_ids() -> set:
    """Tüm müşteri ID'lerini döner"""
    return set(CUSTOMERS.keys())

def is_valid_user_id(user_id: int) -> bool:
    """User ID'nin geçerli olup olmadığını kontrol eder"""
    return user_id in CUSTOMERS

def validate_user_id(user_id: int):
    """User ID'yi doğrular, geçersizse HTTPException fırlatır"""
    if not is_valid_user_id(user_id):
        raise HTTPException(status_code=404, detail=f"User ID {user_id} bulunamadı") 

def get_current_user_from_token(token: str) -> int:
    """Session token'dan current user'ı getirir"""
    return validate_session(token) 