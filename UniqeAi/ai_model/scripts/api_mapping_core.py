"""
BASIT API MAPPING - TELEKOM AI TRAINING DATASET
Sadece temel/core API endpoint'leri - Toplam: 39 API

Bu mapping'i kullanarak backend ekibiyle kolayca senkronize olabilirsiniz.
"""

# Temel API Mapping Dictionary
API_MAP = {

    # --- TELECOM APIs ---
    "get_customer_package": "backend_api.get_customer_package",
    "change_package": "backend_api.change_package",
    "get_remaining_quotas": "backend_api.get_remaining_quotas",
    "get_bill_details": "backend_api.get_bill_details",
    "pay_bill": "backend_api.pay_bill",
    "check_network_status": "backend_api.check_network_status",
    "create_fault_ticket": "backend_api.create_fault_ticket",
    "suspend_line": "backend_api.suspend_line",
    "reactivate_line": "backend_api.reactivate_line",
    "get_usage_statistics": "backend_api.get_usage_statistics",
    "enable_roaming": "backend_api.enable_roaming",
    "get_suitable_packages": "backend_api.get_suitable_packages",

    # --- ECOMMERCE APIs ---
    "search_products": "backend_api.search_products",
    "get_product_details": "backend_api.get_product_details",
    "create_order": "backend_api.create_order",
    "get_order_status": "backend_api.get_order_status",
    "cancel_order": "backend_api.cancel_order",
    "get_order_history": "backend_api.get_order_history",
    "update_product_price": "backend_api.update_product_price",
    "check_stock_status": "backend_api.check_stock_status",
    "add_stock": "backend_api.add_stock",
    "get_low_stock_products": "backend_api.get_low_stock_products",

    # --- CUSTOMER APIs ---
    "get_customer_profile": "backend_api.get_customer_profile",
    "register_customer": "backend_api.register_customer",
    "update_customer_preferences": "backend_api.update_customer_preferences",
    "get_customer_activity": "backend_api.get_customer_activity",
    "get_loyalty_points": "backend_api.get_loyalty_points",
    "update_customer_address": "backend_api.update_customer_address",

    # --- PAYMENT APIs ---
    "process_payment": "backend_api.process_payment",
    "process_refund": "backend_api.process_refund",
    "get_payment_history": "backend_api.get_payment_history",
    "setup_auto_payment": "backend_api.setup_auto_payment",

    # --- ANALYTICS APIs ---
    "generate_sales_report": "backend_api.generate_sales_report",
    "analyze_customer_behavior": "backend_api.analyze_customer_behavior",
    "get_product_performance_report": "backend_api.get_product_performance_report",

    # --- SUPPORT APIs ---
    "create_support_ticket": "backend_api.create_support_ticket",
    "get_ticket_status": "backend_api.get_ticket_status",
    "send_email": "backend_api.send_email",
    "start_live_chat": "backend_api.start_live_chat",

}

# Helper functions
def get_api_path(api_name: str) -> str:
    """API path'i al"""
    return API_MAP.get(api_name, f"backend_api.{api_name}")

def get_all_apis() -> list:
    """Tüm API'leri listele"""
    return list(API_MAP.keys())

def get_apis_by_category() -> dict:
    """Kategori bazlı API'leri döndür"""
    return {
        "telecom": ['get_customer_package', 'change_package', 'get_remaining_quotas', 'get_bill_details', 'pay_bill', 'check_network_status', 'create_fault_ticket', 'suspend_line', 'reactivate_line', 'get_usage_statistics', 'enable_roaming', 'get_suitable_packages'],
        "ecommerce": ['search_products', 'get_product_details', 'create_order', 'get_order_status', 'cancel_order', 'get_order_history', 'update_product_price', 'check_stock_status', 'add_stock', 'get_low_stock_products'],
        "customer": ['get_customer_profile', 'register_customer', 'update_customer_preferences', 'get_customer_activity', 'get_loyalty_points', 'update_customer_address'],
        "payment": ['process_payment', 'process_refund', 'get_payment_history', 'setup_auto_payment'],
        "analytics": ['generate_sales_report', 'analyze_customer_behavior', 'get_product_performance_report'],
        "support": ['create_support_ticket', 'get_ticket_status', 'send_email', 'start_live_chat'],
    }

# Versiyon bilgisi
VERSION = "2.0-SIMPLIFIED"
TOTAL_APIS = {total_apis}
