# -*- coding: utf-8 -*-
"""
⚙️ KONFİGÜRASYON AYARLARI
==========================

Bu modül, SupremeHumanLevelDatasetGenerator için tüm konfigürasyon ayarlarını içerir.
"""

import sys
from pathlib import Path

# === KRİTİK: PROJE YOLU TANIMLAMASI ===
# Proje kök dizinini sisteme tanıt
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # 4 seviye yukarı
sys.path.insert(0, str(PROJECT_ROOT))

# Mevcut script dizinini de ekle
SCRIPT_DIR = Path(__file__).resolve().parents[2]  # 2 seviye yukarı
sys.path.insert(0, str(SCRIPT_DIR))

# === API ŞEMASI KONFİGÜRASYONU ===
try:
    # telekom_api_schema.py'den TÜM modelleri import et
    try:
        from telekom_api_schema import *
        print(f"✅ telekom_api_schema başarıyla yüklendi (local import)")
    except ImportError:
        from UniqeAi.ai_model.scripts.telekom_api_schema import *
        print(f"✅ telekom_api_schema başarıyla yüklendi (full path import)")
    
    print("✅ Pydantic ve telekom_api_schema başarıyla yüklendi")
    print(f"✅ API Fonksiyon Sayısı: {TOTAL_APIS}")
    print(f"✅ Schema Versiyonu: {VERSION}")
    
except ImportError as e:
    print(f"❌ KRİTİK HATA: Pydantic veya telekom_api_schema yüklenemedi: {e}")
    print(f"🐍 Python yolu: {sys.path}")
    sys.exit(1)

# === DATASET KONFİGÜRASYONU ===
DEFAULT_NUM_SAMPLES = 10000
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "UniqeAi/ai_model/data"

# === VALIDASYON KONFİGÜRASYONU ===
MAX_VALIDATION_ERRORS = 100
MAX_SCHEMA_VIOLATIONS = 50
QUALITY_THRESHOLD = 0.95  # %95 kalite eşiği

# === MEMORY OPTIMIZATION ===
CACHE_SIZE = 128
LAZY_LOADING_ENABLED = True

# === LOGGING KONFİGÜRASYONU ===
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# === SCENARIO WEIGHTS ===
# Her senaryo için ağırlıklar (daha yüksek = daha sık üretilir)
SCENARIO_WEIGHTS = {
    # Temel Senaryolar
    "standard": 1.0,
    "tool_chaining": 2.0,
    "proactive": 2.5,
    "disambiguation": 2.0,
    "multi_intent": 2.5,
    "ethical_dilemma": 3.0,
    
    # Gelişmiş Senaryolar
    "negotiation_skills": 4.0,
    "teaching_mentoring": 4.0,
    "innovation_thinking": 4.0,
    "temporal_reasoning": 4.0,
    "cross_cultural_communication": 4.0,
    "advanced_error_recovery": 3.5,
    "social_dynamics": 3.5,
    "conflicting_information": 3.5,
    "strategic_planning": 4.0,
    "empathetic_reasoning": 5.0,  # En Yüksek Ağırlık!
    "adaptive_communication": 3.0,
    "predictive_analytics": 3.0,
    "resource_optimization": 3.0,
    "collaborative_filtering": 3.0,

    # Yeni Eklenen Senaryolar
    "payment_history": 2.0,
    "setup_autopay": 2.0,
    "change_package": 2.5,
    "suspend_line": 1.5,
    "error_response": 3.5,
    "package_details": 2.0,
    "enable_roaming": 2.0,
    "get_user_tickets": 2.0,
    "get_ticket_status": 2.0,
    "test_internet_speed": 2.0,
}

# === API RESPONSE MAPPING ===
# Bu mapping, API fonksiyonlarını response modellerine eşleştirir
API_RESPONSE_MAPPING = {
    # Fatura ve Ödeme İşlemleri
    "get_current_bill": "GetCurrentBillResponse",
    "get_past_bills": "GetPastBillsResponse",
    "pay_bill": "PayBillResponse",
    "get_payment_history": "GetPaymentHistoryResponse",
    "setup_autopay": "SetupAutopayResponse",
    
    # Paket ve Tarife Yönetimi
    "get_customer_package": "GetCustomerPackageResponse",
    "get_available_packages": "GetAvailablePackagesResponse",
    "change_package": "ChangePackageResponse",
    "get_remaining_quotas": "GetRemainingQuotasResponse",
    "get_package_details": "GetPackageDetailsResponse",
    "enable_roaming": "EnableRoamingResponse",
    
    # Teknik Destek ve Arıza
    "check_network_status": "CheckNetworkStatusResponse",
    "create_fault_ticket": "CreateFaultTicketResponse",
    "close_fault_ticket": "CloseFaultTicketResponse",
    "get_users_tickets": "GetUsersTicketsResponse",
    "get_fault_ticket_status": "GetFaultTicketStatusResponse",
    "test_internet_speed": "TestInternetSpeedResponse",
    
    # Hesap Yönetimi
    "get_customer_profile": "GetCustomerProfileResponse",
    "update_customer_contact": "UpdateCustomerContactResponse",
    "suspend_line": "SuspendLineResponse",
    "reactivate_line": "ReactivateLineResponse",
    
    # Acil Durum ve Gelişmiş Servisler
    "activate_emergency_service": "ActivateEmergencyServiceResponse",
    "check_5g_coverage": "Check5GCoverageResponse",
    "get_cultural_context": "CulturalContextResponse",
    "update_learning_adaptation": "LearningAdaptationResponse",
} 