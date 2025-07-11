# -*- coding: utf-8 -*-
"""
Telekom AI Projesi için Merkezi API Şeması ve Modelleri (Pydantic)

Bu dosya, yapay zeka ajanının kullanabileceği tüm araçların (backend fonksiyonları)
ve bu fonksiyonların DÖNÜŞ DEĞERLERİNİN (response) yapılarını tanımlar.
Bu, projenin "kabiliyetlerinin" ve "veri yapılarının" tek ve doğru kaynağıdır (Single Source of Truth).
Veri üretimi, backend geliştirmesi ve modelin kendisi bu şemalara %100 uymalıdır.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ==============================================================================
# 1. FATURA & ÖDEME İŞLEMLERİ İÇİN VERİ MODELLERİ
# ==============================================================================

class ServiceItem(BaseModel):
    service_name: str
    amount: float

class GetCurrentBillResponse(BaseModel):
    bill_id: str
    user_id: int
    amount: float
    currency: str
    due_date: str
    bill_date: str
    status: str
    services: List[ServiceItem]

class PastBillItem(BaseModel):
    bill_id: str
    amount: float
    bill_date: str
    status: str
    paid_date: Optional[str] = None

class GetPastBillsResponse(BaseModel):
    bills: List[PastBillItem]
    total_count: int
    total_amount_paid: float

class PayBillResponse(BaseModel):
    transaction_id: str
    bill_id: str
    amount: float
    method: str
    status: str
    timestamp: str

class PaymentHistoryItem(BaseModel):
    transaction_id: str
    amount: float
    method: str
    date: str
    bill_id: str

class GetPaymentHistoryResponse(BaseModel):
    payments: List[PaymentHistoryItem]
    total_payments: int
    total_amount: float

class SetupAutopayResponse(BaseModel):
    user_id: int
    autopay_enabled: bool
    payment_method: str
    next_payment_date: str

# ==============================================================================
# 2. PAKET & TARİFE YÖNETİMİ İÇİN VERİ MODELLERİ
# ==============================================================================

class PackageFeatures(BaseModel):
    internet_gb: int
    voice_minutes: int
    sms_count: int
    roaming_enabled: Optional[bool] = None
    international_minutes: Optional[int] = None

class GetCustomerPackageResponse(BaseModel):
    package_name: str
    monthly_fee: float
    features: PackageFeatures
    activation_date: str
    renewal_date: str
    
class UsagePercentage(BaseModel):
    internet: int
    voice: int
    sms: int

class GetRemainingQuotasResponse(BaseModel):
    internet_remaining_gb: float
    voice_remaining_minutes: int
    sms_remaining: int
    period_end: str
    usage_percentage: UsagePercentage

class ChangePackageResponse(BaseModel):
    change_id: str
    from_package: str
    to_package: str
    effective_date: str
    fee_difference: float
    status: str

class AvailablePackageFeatures(BaseModel):
    internet_gb: int
    voice_minutes: int
    sms_count: int

class AvailablePackageItem(BaseModel):
    name: str
    monthly_fee: float
    features: AvailablePackageFeatures
    target_audience: Optional[str] = None

class GetAvailablePackagesResponse(BaseModel):
    packages: List[AvailablePackageItem]

class PackageDetailsFeatures(BaseModel):
    internet_gb: int
    voice_minutes: int
    sms_count: int
    international_minutes: int

class GetPackageDetailsResponse(BaseModel):
    name: str
    monthly_fee: float
    setup_fee: float
    features: PackageDetailsFeatures
    contract_duration: int
    cancellation_fee: float

class EnableRoamingResponse(BaseModel):
    user_id: int
    roaming_enabled: bool
    activation_time: str
    daily_fee: float
    data_package: str

# ==============================================================================
# 3. TEKNİK DESTEK & ARIZA İÇİN VERİ MODELLERİ
# ==============================================================================

class ActiveOutageItem(BaseModel):
    area: str
    issue: str
    start_time: str
    estimated_end: str

class CheckNetworkStatusResponse(BaseModel):
    region: str
    status: str
    coverage_percentage: int
    active_outages: List[ActiveOutageItem]
    last_updated: str

class CloseFaultTicketResponse(BaseModel):
    ticket_id: str
    user_id: int
    issue_description: str
    category: str
    priority: str
    status: str
    created_at: str
    estimated_resolution: str

class CreateFaultTicketResponse(BaseModel):
    ticket_id: str
    user_id: int
    issue_description: str
    category: str
    priority: str
    status: str
    created_at: str
    estimated_resolution: str

class UserTicketItem(BaseModel):
    ticket_id: str
    issue_description: str
    category: str
    priority: str
    status: str
    created_at: str
    estimated_resolution: str

class GetUsersTicketsResponse(BaseModel):
    user_id: str
    tickets: List[UserTicketItem]

class GetFaultTicketStatusResponse(BaseModel):
    ticket_id: str
    status: str
    resolution: Optional[str]
    created_at: str
    resolved_at: Optional[str]
    technician_notes: str

class TestInternetSpeedResponse(BaseModel):
    user_id: int
    download_speed_mbps: float
    upload_speed_mbps: float
    ping_ms: int
    test_timestamp: str
    test_server: str
    quality_rating: str

# ==============================================================================
# 4. HESAP YÖNETİMİ İÇİN VERİ MODELLERİ
# ==============================================================================

class PhoneNumberItem(BaseModel):
    number: str
    type: str
    status: str

class GetCustomerProfileResponse(BaseModel):
    user_id: int
    name: str
    phone_numbers: List[PhoneNumberItem]
    email: str
    address: str
    registration_date: str
    customer_tier: str

class UpdateCustomerContactResponse(BaseModel):
    user_id: int
    contact_type: str
    old_value: str
    new_value: str
    updated_at: str
    verification_required: bool

class SuspendLineResponse(BaseModel):
    user_id: int
    line_number: str
    suspension_reason: str
    suspended_at: str
    reactivation_fee: float
    max_suspension_days: int

class ReactivateLineResponse(BaseModel):
    user_id: int
    line_number: str
    reactivated_at: str
    suspension_duration_days: int
    reactivation_fee: float

# ==============================================================================
# API HARİTASI VE YARDIMCI FONKSİYONLAR
# ==============================================================================

# API_MAP artık sadece isimleri değil, Pydantic modellerini de referans alabilir
# Ancak şimdilik eski yapıyı koruyoruz, scriptler bunu kullanıyor.
API_MAP = {
    # --- Paket ve Tarife Yönetimi ---
    "get_customer_package": "backend_api.get_customer_package",
    "get_available_packages": "backend_api.get_available_packages",
    "change_package": "backend_api.change_package",
    "get_remaining_quotas": "backend_api.get_remaining_quotas",
    "get_package_details": "backend_api.get_package_details",
    "enable_roaming": "backend_api.enable_roaming",

    # --- Fatura ve Ödeme İşlemleri ---
    "get_current_bill": "backend_api.get_current_bill",
    "get_past_bills": "backend_api.get_past_bills",
    "pay_bill": "backend_api.pay_bill",
    "get_payment_history": "backend_api.get_payment_history",
    "setup_autopay": "backend_api.setup_autopay",

    # --- Teknik Destek ve Arıza Kaydı ---
    "check_network_status": "backend_api.check_network_status",
    "create_fault_ticket": "backend_api.create_fault_ticket",
    "close_fault_ticket": "backend_api.close_fault_ticket",
    "get_users_tickets": "backend_api.get_users_tickets",
    "get_fault_ticket_status": "backend_api.get_fault_ticket_status",
    "test_internet_speed": "backend_api.test_internet_speed",

    # --- Hat ve Abonelik İşlemleri ---
    "get_customer_profile": "backend_api.get_customer_profile",
    "update_customer_contact": "backend_api.update_customer_contact",
    "suspend_line": "backend_api.suspend_line",
    "reactivate_line": "backend_api.reactivate_line",
}

VERSION = "2.0-Pydantic"
TOTAL_APIS = len(API_MAP)