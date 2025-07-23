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
        "name": "Mehmet Demir",
        "phone_numbers": [{"number": "+905551234567", "type": "mobile", "status": "active"}],
        "email": "mehmet.demir@email.com",
        "address": "Ankara, Çankaya",
        "registration_date": "2022-06-15",
        "customer_tier": "premium"
    },
    1: {
        "name": "Ayşe Kaya",
        "phone_numbers": [{"number": "+905559876543", "type": "mobile", "status": "active"}],
        "email": "ayse.kaya@email.com",
        "address": "İstanbul, Beşiktaş",
        "registration_date": "2023-03-20",
        "customer_tier": "gold"
    },
    2: {
        "name": "Ali Özkan",
        "phone_numbers": [{"number": "+905551112223", "type": "mobile", "status": "active"}],
        "email": "ali.ozkan@email.com",
        "address": "İzmir, Konak",
        "registration_date": "2021-11-10",
        "customer_tier": "silver"
    },
    3: {
        "name": "Fatma Şahin",
        "phone_numbers": [{"number": "+905554445556", "type": "mobile", "status": "active"}],
        "email": "fatma.sahin@email.com",
        "address": "Bursa, Nilüfer",
        "registration_date": "2023-08-05",
        "customer_tier": "gold"
    },
    4: {
        "name": "Mustafa Yılmaz",
        "phone_numbers": [{"number": "+905557778889", "type": "mobile", "status": "active"}],
        "email": "mustafa.yilmaz@email.com",
        "address": "Antalya, Muratpaşa",
        "registration_date": "2022-12-01",
        "customer_tier": "premium"
    },
    5: {
        "name": "Sedat Kılıçoğlu",
        "phone_numbers": [{"number": "+905557771234", "type": "mobile", "status": "active"}],
        "email": "sedat.kilicoglu@email.com",
        "address": "istanbul, eminönü",
        "registration_date": "2024-12-01",
        "customer_tier": "diomand"
    },
    6: {
        "name": "Elon Musk",
        "phone_numbers": [{"number": "+905557776789", "type": "mobile", "status": "active"}],
        "email": "elon.musk@email.com",
        "address": "bursa, mudanya",
        "registration_date": "2025-12-01",
        "customer_tier": "elit"
    },
    7: {
        "name": "jeff bezos",
        "phone_numbers": [{"number": "+905557771122", "type": "mobile", "status": "active"}],
        "email": "jeff.bezos@email.com",
        "address": "ankara, anıtkabir",
        "registration_date": "2025-01-01",
        "customer_tier": "ultimate"
    }
}

# Kayıtlı kullanıcılar (örnek: email -> user info)
REGISTERED_USERS = {}
# Kullanıcı paketleri (örnek: user_id -> package info veya None)
USER_PACKAGES = {}

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
    bill_id: str
    method: str

class PastBillsRequest(BaseModel):
    user_id: int
    limit: int

class AutopayRequest(BaseModel):
    user_id: int
    status: bool

class PackageChangeRequest(BaseModel):
    user_id: int
    new_package_name: str

class PackageDetailsRequest(BaseModel):
    package_name: str

class RoamingRequest(BaseModel):
    user_id: int
    status: bool

class NetworkStatusRequest(BaseModel):
    region: str

class FaultTicketRequest(BaseModel):
    user_id: int
    issue_description: str
    category: str  # Yeni eklendi
    priority: str  # Yeni eklendi

class TicketStatusRequest(BaseModel):
    ticket_id: str

class ContactUpdateRequest(BaseModel):
    user_id: int
    contact_type: str
    new_value: str

class LineSuspendRequest(BaseModel):
    user_id: int
    reason: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

# ============================================================================
# BILLING ENDPOINT'LERİ
# ============================================================================

@router.post("/billing/current")
async def get_current_bill(request: UserIdRequest):
    """Mevcut fatura bilgilerini getir"""
    try:
        logger.info(f"Mevcut fatura sorgulanıyor: User ID {request.user_id}")
        
        bill_data = get_mock_bill_data(request.user_id)
        
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
        logger.info(f"Fatura geçmişi sorgulanıyor: User ID {request.user_id}, Limit: {request.limit}")
        
        bills = []
        base_amount = 50 + (request.user_id % 50)
        
        for i in range(min(request.limit, 12)):
            bill_data = {
                "bill_id": f"F-2024-{request.user_id:04d}-{i+1:02d}",
                "user_id": request.user_id,
                "amount": base_amount + (i * 5),
                "currency": "TRY",
                "bill_date": f"2024-{i+1:02d}-28",
                "due_date": f"2024-{i+2:02d}-15",
                "status": "paid" if i < 11 else "unpaid",
                "services": [
                    {
                        "service_name": "Mega İnternet",
                        "amount": (base_amount + (i * 5)) * 0.7
                    },
                    {
                        "service_name": "Sesli Arama",
                        "amount": (base_amount + (i * 5)) * 0.3
                    }
                ]
            }
            bills.append(bill_data)
        
        return {
            "success": True,
            "data": {
                "bills": bills,
                "total_count": len(bills),
                "user_id": request.user_id
            }
        }
        
    except Exception as e:
        logger.error(f"Fatura geçmişi getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Fatura geçmişi getirme hatası: {str(e)}")

@router.post("/billing/pay")
async def pay_bill(request: PaymentRequest):
    """Fatura ödemesi yap"""
    try:
        logger.info(f"Fatura ödemesi yapılıyor: Bill ID {request.bill_id}, Method: {request.method}")
        
        payment_data = {
            "payment_id": f"PAY-{request.bill_id}",
            "bill_id": request.bill_id,
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
async def get_payment_history(request: UserIdRequest):
    """Ödeme geçmişini getir"""
    try:
        logger.info(f"Ödeme geçmişi sorgulanıyor: User ID {request.user_id}")
        
        payments = []
        base_amount = 50 + (request.user_id % 50)
        
        for i in range(6):
            payment_data = {
                "payment_id": f"PAY-{request.user_id:04d}-{i+1:02d}",
                "bill_id": f"F-2024-{request.user_id:04d}-{i+1:02d}",
                "amount": base_amount + (i * 5),
                "method": "credit_card" if i % 2 == 0 else "bank_transfer",
                "status": "completed",
                "transaction_date": f"2024-{i+1:02d}-05T10:15:00Z"
            }
            payments.append(payment_data)
        
        return {
            "success": True,
            "data": {
                "payments": payments,
                "total_count": len(payments),
                "user_id": request.user_id
            }
        }
        
    except Exception as e:
        logger.error(f"Ödeme geçmişi getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Ödeme geçmişi getirme hatası: {str(e)}")

@router.post("/billing/autopay")
async def setup_autopay(request: AutopayRequest):
    """Otomatik ödeme ayarlar"""
    try:
        logger.info(f"Otomatik ödeme ayarlanıyor: User ID {request.user_id}, Status: {request.status}")
        
        autopay_data = {
            "user_id": request.user_id,
            "autopay_enabled": request.status,
            "payment_method": "credit_card",
            "last_updated": "2024-03-01T14:30:00Z",
            "next_payment_date": "2024-03-15T00:00:00Z"
        }
        
        return {
            "success": True,
            "data": autopay_data
        }
        
    except Exception as e:
        logger.error(f"Otomatik ödeme ayarlama hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Otomatik ödeme ayarlama hatası: {str(e)}")

# ============================================================================
# PACKAGE ENDPOINT'LERİ
# ============================================================================

@router.post("/packages/current")
async def get_customer_package(request: UserIdRequest):
    """Müşterinin mevcut paketini getir"""
    try:
        logger.info(f"Mevcut paket sorgulanıyor: User ID {request.user_id}")
        # Önce USER_PACKAGES dict'ine bak
        package_data = USER_PACKAGES.get(request.user_id)
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
async def get_remaining_quotas(request: UserIdRequest):
    """Müşterinin kalan kotalarını getir"""
    try:
        logger.info(f"Kalan kotalar sorgulanıyor: User ID {request.user_id}")
        
        quota_data = get_mock_quotas_data(request.user_id)
        
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
        logger.info(f"Paket değişikliği başlatılıyor: User ID {request.user_id}, New Package: {request.new_package_name}")
        
        change_data = {
            "change_id": f"CHG-{request.user_id:04d}",
            "user_id": request.user_id,
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
        logger.info(f"Roaming ayarlanıyor: User ID {request.user_id}, Status: {request.status}")
        
        roaming_data = {
            "user_id": request.user_id,
            "roaming_enabled": request.status,
            "effective_date": "2024-03-01T14:30:00Z",
            "supported_countries": ["EU", "USA", "Canada", "Australia"],
            "daily_fee": 15.00 if request.status else 0.00
        }
        
        return {
            "success": True,
            "data": roaming_data
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
        
        network_status = {
            "region": request.region,
            "status": "operational",
            "last_updated": "2024-03-01T14:30:00Z",
            "services": {
                "voice": "operational",
                "data": "operational",
                "sms": "operational"
            },
            "maintenance_scheduled": False,
            "outages": []
        }
        
        return {
            "success": True,
            "data": network_status
        }
        
    except Exception as e:
        logger.error(f"Ağ durumu kontrol hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Ağ durumu kontrol hatası: {str(e)}")

@router.post("/support/tickets")
async def create_fault_ticket(request: FaultTicketRequest):
    """Destek talebi oluştur"""
    try:
        logger.info(f"Destek talebi oluşturuluyor: User ID {request.user_id}")
        
        ticket_data = {
            "ticket_id": f"T-{request.user_id:04d}",
            "user_id": request.user_id,
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
        
        close_data = {
            "ticket_id": request.ticket_id,
            "status": "closed",
            "closed_date": "2024-03-01T15:30:00Z",
            "resolution": "Sorun çözüldü",
            "satisfaction_rating": 5
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
async def test_internet_speed(request: UserIdRequest):
    """İnternet hız testi yap"""
    try:
        logger.info(f"İnternet hız testi yapılıyor: User ID {request.user_id}")
        
        # Simüle edilmiş hız testi sonuçları
        speed_data = {
            "user_id": request.user_id,
            "test_date": "2024-03-01T14:30:00Z",
            "download_speed_mbps": 45.2,
            "upload_speed_mbps": 12.8,
            "ping_ms": 15,
            "jitter_ms": 2,
            "packet_loss_percent": 0.1,
            "connection_quality": "excellent",
            "server_location": "Istanbul"
        }
        
        return {
            "success": True,
            "data": speed_data
        }
        
    except Exception as e:
        logger.error(f"İnternet hız testi hatası: {e}")
        raise HTTPException(status_code=500, detail=f"İnternet hız testi hatası: {str(e)}")

# ============================================================================
# CUSTOMER MANAGEMENT ENDPOINT'LERİ
# ============================================================================

@router.post("/customers/profile")
async def get_customer_profile(request: UserIdRequest):
    """Müşteri profilini getir"""
    try:
        logger.info(f"Müşteri profili sorgulanıyor: User ID {request.user_id}")
        
        customer_data = get_mock_customer_data(request.user_id)
        
        return {
            "success": True,
            "data": {
                "user_id": request.user_id,
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
        logger.info(f"İletişim bilgisi güncelleniyor: User ID {request.user_id}, Type: {request.contact_type}")
        
        update_data = {
            "user_id": request.user_id,
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
        logger.info(f"Hat askıya alınıyor: User ID {request.user_id}, Reason: {request.reason}")
        
        suspend_data = {
            "user_id": request.user_id,
            "status": "suspended",
            "reason": request.reason,
            "suspended_date": "2024-03-01T14:30:00Z",
            "reactivation_fee": 25.00,
            "estimated_reactivation_date": "2024-03-08T14:30:00Z"
        }
        
        return {
            "success": True,
            "data": suspend_data
        }
        
    except Exception as e:
        logger.error(f"Hat askıya alma hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Hat askıya alma hatası: {str(e)}")

@router.post("/lines/reactivate")
async def reactivate_line(request: UserIdRequest):
    """Hatı yeniden etkinleştir"""
    try:
        logger.info(f"Hat yeniden etkinleştiriliyor: User ID {request.user_id}")
        
        reactivate_data = {
            "user_id": request.user_id,
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
async def get_users_tickets(request: UserIdRequest):
    """Kullanıcının tüm destek taleplerini getirir"""
    try:
        logger.info(f"Kullanıcı destek talepleri sorgulanıyor: User ID {request.user_id}")
        # Mock veri - gerçek uygulamada veritabanından alınır
        tickets = [
            {"ticket_id": f"T-{request.user_id:04d}-1", "status": "open", "subject": "Teknik sorun"},
            {"ticket_id": f"T-{request.user_id:04d}-2", "status": "closed", "subject": "Fatura sorunu"}
        ]
        return {
            "success": True,
            "data": {"tickets": tickets, "user_id": request.user_id}
        }
    except Exception as e:
        logger.error(f"Kullanıcı destek talepleri getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Kullanıcı destek talepleri getirme hatası: {str(e)}")

@router.post("/auth/register")
async def register_user(request: RegisterRequest):
    """Kullanıcı kaydı endpointi"""
    if request.email in REGISTERED_USERS:
        raise HTTPException(status_code=400, detail="Bu email ile zaten bir kullanıcı var.")
    # Yeni user_id ata
    user_id = len(REGISTERED_USERS) + 100  # 100'den başlat, çakışmasın
    user_info = {
        "user_id": user_id,
        "email": request.email,
        "password": request.password,  # Not: Gerçek uygulamada hashlenmeli!
        "name": request.name
    }
    REGISTERED_USERS[request.email] = user_info
    USER_PACKAGES[user_id] = None  # Başlangıçta paketi yok
    return {"success": True, "message": "Kayıt başarılı.", "user_id": user_id}

@router.post("/auth/login")
async def login_user(request: LoginRequest):
    """Kullanıcı girişi endpointi"""
    user = REGISTERED_USERS.get(request.email)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı.")
    return {"success": True, "message": "Giriş başarılı.", "user_id": user["user_id"]}

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