"""
Telekom API endpoint'leri - Spesifikasyonda belirtilen tüm endpoint'ler
"""

from fastapi import APIRouter, HTTPException
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
            "amount": 89.50,
            "currency": "TRY",
            "due_date": "2024-03-15",
            "bill_date": "2024-02-28",
            "status": "unpaid",
            "services": [
                {
                    "service_name": "Mega İnternet",
                    "amount": 69.50
                },
                {
                    "service_name": "Sesli Arama", 
                    "amount": 20.00
                }
            ]
        }
        
        return {
            "success": True,
            "data": bill_data
        }
        
    except Exception as e:
        logger.error(f"Fatura getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/packages/current/{user_id}")
async def get_customer_package_test(user_id: int):
    """Müşterinin mevcut paketini getir (GET test için)"""
    try:
        logger.info(f"Müşteri paketi sorgulanıyor: User ID {user_id}")
        
        return {
            "success": True,
            "data": {
                "package_name": "Mega İnternet",
                "monthly_fee": 69.50,
                "features": {
                    "internet_gb": 50,
                    "voice_minutes": 1000,
                    "sms_count": 500,
                    "roaming_enabled": False
                },
                "activation_date": "2024-01-01",
                "renewal_date": "2024-04-01"
            }
        }
        
    except Exception as e:
        logger.error(f"Paket getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers/profile/{user_id}")
async def get_customer_profile_test(user_id: int):
    """Müşteri profilini getir (GET test için)"""
    try:
        logger.info(f"Müşteri profili sorgulanıyor: User ID {user_id}")
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "name": "Ahmet Yılmaz",
                "phone_numbers": [
                    {
                        "number": "+905551234567",
                        "type": "mobile",
                        "status": "active"
                    }
                ],
                "email": "ahmet@example.com",
                "address": "İstanbul, Kadıköy",
                "registration_date": "2023-01-15",
                "customer_tier": "gold"
            }
        }
        
    except Exception as e:
        logger.error(f"Müşteri profili getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# REQUEST/RESPONSE MODELS
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

# ============================================================================
# FATURA & ÖDEME İŞLEMLERİ
# ============================================================================

@router.post("/billing/current")
async def get_current_bill(request: UserIdRequest):
    validate_user_id(request.user_id)
    """Mevcut fatura bilgilerini getir"""
    try:
        logger.info(f"Mevcut fatura sorgulanıyor: User ID {request.user_id}")
        
        bill_data = get_mock_bill_data(request.user_id)
        
        return {
            "success": True,
            "data": bill_data
        }
        
    except Exception as e:
        logger.error(f"Fatura getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/billing/history")
async def get_past_bills(request: PastBillsRequest):
    validate_user_id(request.user_id)
    """Geçmiş faturaları getir"""
    try:
        logger.info(f"Geçmiş faturalar sorgulanıyor: User ID {request.user_id}, Limit {request.limit}")
        
        # Mock veri - user ID'ye göre farklı faturalar
        bills = []
        base_amount = 50 + (request.user_id % 50)
        for i in range(min(request.limit, 12)):
            bill_amount = base_amount + (i * 5)  # Her ay biraz artıyor
            bills.append({
                "bill_id": f"F-2024-{request.user_id:04d}-{i+1:02d}",
                "amount": bill_amount,
                "bill_date": f"2024-{i+1:02d}-28",
                "status": "paid" if i < 11 else "unpaid",
                "paid_date": f"2024-{i+2:02d}-05" if i < 11 else None
            })
        
        total_amount = sum(bill["amount"] for bill in bills if bill["status"] == "paid")
        
        return {
            "success": True,
            "data": {
                "bills": bills,
                "total_count": len(bills),
                "total_amount_paid": total_amount
            }
        }
        
    except Exception as e:
        logger.error(f"Geçmiş faturalar getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/billing/pay")
async def pay_bill(request: PaymentRequest):
    """Fatura ödemesi yap"""
    try:
        logger.info(f"Fatura ödemesi: Bill ID {request.bill_id}, Method {request.method}")
        
        # Mock ödeme işlemi
        payment_data = {
            "transaction_id": f"TXN-2024-{request.bill_id.split('-')[-1]}",
            "bill_id": request.bill_id,
            "amount": 89.50,
            "method": request.method,
            "status": "completed",
            "timestamp": "2024-03-01T14:30:00Z"
        }
        
        return {
            "success": True,
            "data": payment_data
        }
        
    except Exception as e:
        logger.error(f"Fatura ödeme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/billing/payments")
async def get_payment_history(request: UserIdRequest):
    validate_user_id(request.user_id)
    """Ödeme geçmişini getir"""
    try:
        logger.info(f"Ödeme geçmişi sorgulanıyor: User ID {request.user_id}")
        
        # Mock veri - user ID'ye göre farklı ödemeler
        base_amount = 50 + (request.user_id % 50)
        payment_methods = ["credit_card", "bank_transfer", "mobile_payment", "cash"]
        
        payments = []
        for i in range(5):
            payment_amount = base_amount + (i * 3)
            payments.append({
                "transaction_id": f"TXN-{request.user_id:04d}-{i+1:03d}",
                "amount": payment_amount,
                "method": payment_methods[i % len(payment_methods)],
                "date": f"2024-{i+1:02d}-05T10:15:00Z",
                "bill_id": f"F-2024-{request.user_id:04d}-{i+1:02d}"
            })
        
        total_amount = sum(payment["amount"] for payment in payments)
        
        return {
            "success": True,
            "data": {
                "payments": payments,
                "total_payments": len(payments),
                "total_amount": total_amount
            }
        }
        
    except Exception as e:
        logger.error(f"Ödeme geçmişi getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/billing/autopay")
async def setup_autopay(request: AutopayRequest):
    validate_user_id(request.user_id)
    """Otomatik ödeme ayarla"""
    try:
        logger.info(f"Otomatik ödeme ayarlanıyor: User ID {request.user_id}, Status {request.status}")
        
        return {
            "success": True,
            "data": {
                "user_id": request.user_id,
                "autopay_enabled": request.status,
                "payment_method": "credit_card_ending_1234",
                "next_payment_date": "2024-03-15"
            }
        }
        
    except Exception as e:
        logger.error(f"Otomatik ödeme ayarlama hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PAKET & TARİFE YÖNETİMİ
# ============================================================================

@router.post("/packages/current")
async def get_customer_package(request: UserIdRequest):
    validate_user_id(request.user_id)
    """Müşterinin mevcut paketini getir"""
    try:
        logger.info(f"Müşteri paketi sorgulanıyor: User ID {request.user_id}")
        
        package_data = get_mock_package_data(request.user_id)
        
        return {
            "success": True,
            "data": package_data
        }
        
    except Exception as e:
        logger.error(f"Paket getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/packages/quotas")
async def get_remaining_quotas(request: UserIdRequest):
    validate_user_id(request.user_id)
    """Kalan kotaları getir"""
    try:
        logger.info(f"Kalan kotalar sorgulanıyor: User ID {request.user_id}")
        
        quotas_data = get_mock_quotas_data(request.user_id)
        
        return {
            "success": True,
            "data": quotas_data
        }
        
    except Exception as e:
        logger.error(f"Kota getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/packages/change")
async def change_package(request: PackageChangeRequest):
    validate_user_id(request.user_id)
    """Paket değişikliği başlat"""
    try:
        logger.info(f"Paket değişikliği: User ID {request.user_id}, New Package {request.new_package_name}")
        
        return {
            "success": True,
            "data": {
                "change_id": "CHG-2024-001",
                "from_package": "Mega İnternet",
                "to_package": request.new_package_name,
                "effective_date": "2024-04-01",
                "fee_difference": -20.00,
                "status": "scheduled"
            }
        }
        
    except Exception as e:
        logger.error(f"Paket değişikliği hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/packages/available")
async def get_available_packages():
    """Kullanılabilir paketleri getir"""
    try:
        logger.info("Kullanılabilir paketler sorgulanıyor")
        
        return {
            "success": True,
            "data": {
                "packages": [
                    {
                        "name": "Öğrenci Dostu Tarife",
                        "monthly_fee": 49.90,
                        "features": {
                            "internet_gb": 30,
                            "voice_minutes": 500,
                            "sms_count": 250
                        },
                        "target_audience": "students"
                    },
                    {
                        "name": "Mega İnternet",
                        "monthly_fee": 69.50,
                        "features": {
                            "internet_gb": 50,
                            "voice_minutes": 1000,
                            "sms_count": 500
                        }
                    }
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Kullanılabilir paketler getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/packages/details")
async def get_package_details(request: PackageDetailsRequest):
    """Paket detaylarını getir"""
    try:
        logger.info(f"Paket detayları sorgulanıyor: {request.package_name}")
        
        return {
            "success": True,
            "data": {
                "name": request.package_name,
                "monthly_fee": 59.90,
                "setup_fee": 0,
                "features": {
                    "internet_gb": 25,
                    "voice_minutes": 2000,
                    "sms_count": 1000,
                    "international_minutes": 100
                },
                "contract_duration": 24,
                "cancellation_fee": 50.00
            }
        }
        
    except Exception as e:
        logger.error(f"Paket detayları getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/services/roaming")
async def enable_roaming(request: RoamingRequest):
    validate_user_id(request.user_id)
    """Roaming hizmetini etkinleştir/devre dışı bırak"""
    try:
        logger.info(f"Roaming ayarlanıyor: User ID {request.user_id}, Status {request.status}")
        
        return {
            "success": True,
            "data": {
                "user_id": request.user_id,
                "roaming_enabled": request.status,
                "activation_time": "2024-03-01T15:00:00Z",
                "daily_fee": 25.00,
                "data_package": "1GB/day"
            }
        }
        
    except Exception as e:
        logger.error(f"Roaming ayarlama hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TEKNİK DESTEK & ARIZA
# ============================================================================

@router.post("/network/status")
async def check_network_status(request: NetworkStatusRequest):
    """Ağ durumunu kontrol et"""
    try:
        logger.info(f"Ağ durumu sorgulanıyor: Region {request.region}")
        
        return {
            "success": True,
            "data": {
                "region": request.region,
                "status": "operational",
                "coverage_percentage": 95,
                "active_outages": [
                    {
                        "area": "Diyarbakır Merkez",
                        "issue": "Planlı bakım",
                        "start_time": "2024-03-01T02:00:00Z",
                        "estimated_end": "2024-03-01T06:00:00Z"
                    }
                ],
                "last_updated": "2024-03-01T14:30:00Z"
            }
        }
        
    except Exception as e:
        logger.error(f"Ağ durumu getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/support/tickets")
async def create_fault_ticket(request: FaultTicketRequest):
    validate_user_id(request.user_id)
    """Arıza talebi oluştur"""
    try:
        logger.info(f"Arıza talebi oluşturuluyor: User ID {request.user_id}")
        return {
            "success": True,
            "data": {
                "ticket_id": f"T-2024-{request.user_id}",
                "user_id": request.user_id,
                "issue_description": request.issue_description,
                "category": request.category,
                "priority": request.priority,
                "status": "open",
                "created_at": "2024-03-01T14:30:00Z",
                "estimated_resolution": "2024-03-02T14:30:00Z"
            }
        }
    except Exception as e:
        logger.error(f"Arıza talebi oluşturma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/support/tickets/close")
async def close_fault_ticket(request: TicketStatusRequest):
    """Arıza talebini kapat"""
    # ticket_id kontrolü örnek (gerçek uygulamada DB'den kontrol edilir)
    if not request.ticket_id.startswith("T-2024-"):
        raise HTTPException(status_code=404, detail=f"Talep ID {request.ticket_id} bulunamadı.")
    try:
        logger.info(f"Arıza talebi kapatılıyor: Ticket ID {request.ticket_id}")
        return {
            "success": True,
            "data": {
                "ticket_id": request.ticket_id,
                "status": "closed",
                "closed_at": "2024-03-01T16:00:00Z",
                "close_reason": "Kullanıcı isteğiyle kapatıldı"
            }
        }
    except Exception as e:
        logger.error(f"Arıza talebi kapatma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/support/tickets/status")
async def get_fault_ticket_status(request: TicketStatusRequest):
    """Arıza talebi durumunu getir"""
    try:
        logger.info(f"Arıza talebi durumu sorgulanıyor: Ticket ID {request.ticket_id}")
        
        return {
            "success": True,
            "data": {
                "ticket_id": request.ticket_id,
                "status": "resolved",
                "resolution": "Bölgesel sinyal sorunu giderildi",
                "created_at": "2024-02-28T10:00:00Z",
                "resolved_at": "2024-03-01T09:15:00Z",
                "technician_notes": "Antenna ayarlaması yapıldı"
            }
        }
        
    except Exception as e:
        logger.error(f"Arıza talebi durumu getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/diagnostics/speed-test")
async def test_internet_speed(request: UserIdRequest):
    validate_user_id(request.user_id)
    """İnternet hız testi yap"""
    try:
        logger.info(f"İnternet hız testi: User ID {request.user_id}")
        
        # User ID'ye göre farklı hız sonuçları
        base_download = 30 + (request.user_id % 70)  # 30-100 Mbps arası
        base_upload = 10 + (request.user_id % 30)    # 10-40 Mbps arası
        base_ping = 10 + (request.user_id % 20)      # 10-30 ms arası
        
        # Kalite değerlendirmesi
        if base_download > 80:
            quality = "excellent"
        elif base_download > 50:
            quality = "good"
        elif base_download > 30:
            quality = "fair"
        else:
            quality = "poor"
        
        test_servers = ["Istanbul-1", "Ankara-1", "Izmir-1", "Bursa-1", "Antalya-1"]
        
        return {
            "success": True,
            "data": {
                "user_id": request.user_id,
                "download_speed_mbps": base_download,
                "upload_speed_mbps": base_upload,
                "ping_ms": base_ping,
                "test_timestamp": "2024-03-01T14:30:00Z",
                "test_server": test_servers[request.user_id % len(test_servers)],
                "quality_rating": quality
            }
        }
        
    except Exception as e:
        logger.error(f"Hız testi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# HESAP YÖNETİMİ
# ============================================================================

@router.post("/customers/profile")
async def get_customer_profile(request: UserIdRequest):
    validate_user_id(request.user_id)
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/customers/contact")
async def update_customer_contact(request: ContactUpdateRequest):
    validate_user_id(request.user_id)
    """Müşteri iletişim bilgilerini güncelle"""
    try:
        logger.info(f"İletişim bilgisi güncelleniyor: User ID {request.user_id}, Type {request.contact_type}")
        
        return {
            "success": True,
            "data": {
                "user_id": request.user_id,
                "contact_type": request.contact_type,
                "old_value": "+905551234567",
                "new_value": request.new_value,
                "updated_at": "2024-03-01T14:30:00Z",
                "verification_required": True
            }
        }
        
    except Exception as e:
        logger.error(f"İletişim bilgisi güncelleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lines/suspend")
async def suspend_line(request: LineSuspendRequest):
    validate_user_id(request.user_id)
    """Hatı askıya al"""
    try:
        logger.info(f"Hat askıya alınıyor: User ID {request.user_id}, Reason {request.reason}")
        
        return {
            "success": True,
            "data": {
                "user_id": request.user_id,
                "line_number": "+905551234567",
                "suspension_reason": request.reason,
                "suspended_at": "2024-03-01T14:30:00Z",
                "reactivation_fee": 0,
                "max_suspension_days": 90
            }
        }
        
    except Exception as e:
        logger.error(f"Hat askıya alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lines/reactivate")
async def reactivate_line(request: UserIdRequest):
    validate_user_id(request.user_id)
    """Hatı yeniden etkinleştir"""
    try:
        logger.info(f"Hat yeniden etkinleştiriliyor: User ID {request.user_id}")
        
        return {
            "success": True,
            "data": {
                "user_id": request.user_id,
                "line_number": "+905551234567",
                "reactivated_at": "2024-03-01T14:30:00Z",
                "suspension_duration_days": 15,
                "reactivation_fee": 0
            }
        }
        
    except Exception as e:
        logger.error(f"Hat yeniden etkinleştirme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 

# Dinamik user_id kontrolü için customers anahtarlarını kullanan fonksiyon

def get_all_customer_ids() -> set:
    return set(CUSTOMERS.keys())

def is_valid_user_id(user_id: int) -> bool:
    return user_id in get_all_customer_ids()

def validate_user_id(user_id: int):
    if not is_valid_user_id(user_id):
        raise HTTPException(status_code=404, detail={"Error": f"Kullanıcı ID {user_id} bulunamadı."}) 