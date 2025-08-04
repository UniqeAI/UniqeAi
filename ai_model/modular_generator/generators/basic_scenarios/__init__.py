"""
Basic Scenarios Package
=======================

Bu paket, temel AI senaryolarını içerir. Her senaryo kendi dosyasında tanımlanmıştır.
"""

from .standard import generate_standard_scenario
from .tool_chaining import generate_tool_chaining_scenario
from .proactive import generate_proactive_scenario
from .disambiguation import generate_disambiguation_scenario
from .multi_intent import generate_multi_intent_scenario
from .ethical_dilemma import generate_ethical_dilemma_scenario
from .payment_history import generate_payment_history_scenario
from .setup_autopay import generate_setup_autopay_scenario
from .change_package import generate_change_package_scenario
from .suspend_line import generate_suspend_line_scenario
from .error_response import generate_error_response_scenario
from .package_details import generate_package_details_scenario
from .enable_roaming import generate_enable_roaming_scenario
from .get_user_tickets import generate_get_user_tickets_scenario
from .get_ticket_status import generate_get_ticket_status_scenario
from .test_internet_speed import generate_test_internet_speed_scenario

__all__ = [
    "generate_standard_scenario",
    "generate_tool_chaining_scenario",
    "generate_proactive_scenario",
    "generate_disambiguation_scenario",
    "generate_multi_intent_scenario",
    "generate_ethical_dilemma_scenario",
    "generate_payment_history_scenario",
    "generate_setup_autopay_scenario",
    "generate_change_package_scenario",
    "generate_suspend_line_scenario",
    "generate_error_response_scenario",
    "generate_package_details_scenario",
    "generate_enable_roaming_scenario",
    "generate_get_user_tickets_scenario",
    "generate_get_ticket_status_scenario",
    "generate_test_internet_speed_scenario",
] 