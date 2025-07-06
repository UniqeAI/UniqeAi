"""
Telekom AI Projesi için Merkezi API Şeması

Bu dosya, yapay zeka ajanının kullanabileceği tüm araçları (backend fonksiyonları)
merkezi bir yapıda tanımlar. Projenin "kabiliyetlerinin" tek ve doğru kaynağıdır.
Backend ekibiyle senkronizasyon için bu dosya temel alınmalıdır.
"""

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
    "get_fault_ticket_status": "backend_api.get_fault_ticket_status",
    "test_internet_speed": "backend_api.test_internet_speed",

    # --- Hat ve Abonelik İşlemleri ---
    "get_customer_profile": "backend_api.get_customer_profile",
    "update_customer_contact": "backend_api.update_customer_contact",
    "suspend_line": "backend_api.suspend_line",
    "reactivate_line": "backend_api.reactivate_line",
    "check_number_portability": "backend_api.check_number_portability",
}

# --- Yardımcı Fonksiyonlar ---

def get_api_path(tool_name: str) -> str | None:
    """Verilen araç isminin tam API yolunu döndürür."""
    return API_MAP.get(tool_name)

def get_all_tools() -> list[str]:
    """Mevcut tüm araçların listesini döndürür."""
    return list(API_MAP.keys())

def get_tools_by_category() -> dict[str, list[str]]:
    """Araçları kategorize edilmiş bir şekilde döndürür."""
    categories = {
        "Paket ve Tarife": [],
        "Fatura ve Ödeme": [],
        "Teknik Destek": [],
        "Hat İşlemleri": []
    }
    for tool in API_MAP.keys():
        if "package" in tool or "quota" in tool or "roaming" in tool:
            categories["Paket ve Tarife"].append(tool)
        elif "bill" in tool or "payment" in tool or "autopay" in tool:
            categories["Fatura ve Ödeme"].append(tool)
        elif "network" in tool or "fault" in tool or "speed" in tool:
            categories["Teknik Destek"].append(tool)
        elif "customer" in tool or "line" in tool or "portability" in tool:
            categories["Hat İşlemleri"].append(tool)
    return categories

VERSION = "1.0"
TOTAL_APIS = len(API_MAP) 