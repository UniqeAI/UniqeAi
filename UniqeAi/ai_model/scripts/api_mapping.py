# Centralized mapping of logical tool names to backend API function calls
# This allows us to update function names/paths in a single file once the backend API is finalized.
# The data generators will import this file and construct tool_code dynamically as desired.

API_MAP = {
    # --- User Management ---
    "get_user_info": "backend_api.get_user_info",
    "create_user": "backend_api.create_user",
    "filter_users_by_email_domain": "backend_api.filter_users_by_email_domain",
    "get_user_statistics": "backend_api.get_user_statistics",
    "update_user_phone": "backend_api.update_user_phone",

    # --- Product Management ---
    "get_products_by_category": "backend_api.get_products_by_category",
    "update_product_price": "backend_api.update_product_price",
    "search_products": "backend_api.search_products",
    "get_product_variants": "backend_api.get_product_variants",
    "get_product_reviews": "backend_api.get_product_reviews",

    # --- Order Management ---
    "get_order_status": "backend_api.get_order_status",
    "create_order": "backend_api.create_order",
    "get_user_order_history": "backend_api.get_user_order_history",
    "cancel_order": "backend_api.cancel_order",
    "track_shipping": "backend_api.track_shipping",

    # --- Analytics / Reporting ---
    "generate_sales_report": "backend_api.generate_sales_report",
    "generate_daily_sales_report": "backend_api.generate_daily_sales_report",
    "analyze_category_performance": "backend_api.analyze_category_performance",
    "segment_customers_by_spending": "backend_api.segment_customers_by_spending",

    # --- Inventory ---
    "get_inventory_status": "backend_api.get_inventory_status",
    "get_low_stock_products": "backend_api.get_low_stock_products",
    "get_stock_movements_report": "backend_api.get_stock_movements_report",
    "add_stock": "backend_api.add_stock",

    # --- Promotion ---
    "get_active_promotions": "backend_api.get_active_promotions",
    "get_coupon_usage_stats": "backend_api.get_coupon_usage_stats",
    "create_promotion": "backend_api.create_promotion",

    # --- Customer Service ---
    "get_pending_support_tickets": "backend_api.get_pending_support_tickets",
    "create_support_ticket": "backend_api.create_support_ticket",
    "update_support_ticket": "backend_api.update_support_ticket",

    # --- Telecom Specific: Package & Tariff ---
    "get_customer_package": "backend_api.get_customer_package",
    "change_package": "backend_api.change_package",
    "get_suitable_packages": "backend_api.get_suitable_packages",
    "get_remaining_quotas": "backend_api.get_remaining_quotas",

    # --- Telecom Specific: Billing ---
    "get_bill_details": "backend_api.get_bill_details",
    "get_payment_status": "backend_api.get_payment_status",
    "setup_autopay": "backend_api.setup_autopay",

    # --- Telecom Specific: Technical Support ---
    "check_network_status": "backend_api.check_network_status",
    "create_fault_ticket": "backend_api.create_fault_ticket",
    "test_signal_strength": "backend_api.test_signal_strength",

    # --- Telecom Specific: Line Management ---
    "create_new_line_application": "backend_api.create_new_line_application",
    "suspend_line": "backend_api.suspend_line",
    "check_number_portability": "backend_api.check_number_portability",

    # --- Telecom Specific: Internet & TV ---
    "check_fiber_infrastructure": "backend_api.check_fiber_infrastructure",
    "add_tv_package": "backend_api.add_tv_package",
    "update_modem_wifi_password": "backend_api.update_modem_wifi_password",
}

# NOTE: Once the backend team finalizes the exact module & function paths, only this
# dictionary needs to be updated. Data generator scripts can then look up the path
# dynamically instead of hard-coding "backend_api." strings everywhere. 