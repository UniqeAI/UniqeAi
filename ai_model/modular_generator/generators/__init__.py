# -*- coding: utf-8 -*-
"""
🚀 SENARYO ÜRETİCİLERİ - MODÜL GİRİŞİ
=====================================

Bu modül, SupremeHumanLevelDatasetGenerator için tüm senaryo üreticilerini içerir.
"""

# Temel senaryolar (eski dosyadan)
from .basic_scenarios import (
    generate_standard_scenario,
    generate_tool_chaining_scenario,
    generate_proactive_scenario,
    generate_disambiguation_scenario,
    generate_multi_intent_scenario,
    generate_ethical_dilemma_scenario
)

# Gelişmiş senaryolar
from .advanced_scenarios import (
    generate_negotiation_skills_scenario,
)
from .advanced_scenarios import (
    generate_teaching_mentoring_scenario,
    generate_innovation_thinking_scenario,
    generate_temporal_reasoning_scenario,
    generate_cross_cultural_communication_scenario,
    generate_advanced_error_recovery_scenario,
    generate_social_dynamics_scenario,
    generate_conflicting_information_scenario,
    generate_strategic_planning_scenario,
    generate_empathetic_reasoning_scenario,
    generate_adaptive_communication_scenario,
    generate_predictive_analytics_scenario,
    generate_resource_optimization_scenario,
    generate_collaborative_filtering_scenario
)

# Yeni eklenen senaryolar
from .basic_scenarios import (
    generate_payment_history_scenario,
    generate_setup_autopay_scenario,
    generate_change_package_scenario,
    generate_suspend_line_scenario,
    generate_error_response_scenario,
    generate_package_details_scenario,
    generate_enable_roaming_scenario,
    generate_get_user_tickets_scenario,
    generate_get_ticket_status_scenario,
    generate_test_internet_speed_scenario
)

__all__ = [
    # Temel senaryolar
    'generate_standard_scenario',
    'generate_tool_chaining_scenario',
    'generate_proactive_scenario',
    'generate_disambiguation_scenario',
    'generate_multi_intent_scenario',
    'generate_ethical_dilemma_scenario',
    
    # Gelişmiş senaryolar
    'generate_negotiation_skills_scenario',
    'generate_teaching_mentoring_scenario',
    'generate_innovation_thinking_scenario',
    'generate_temporal_reasoning_scenario',
    'generate_cross_cultural_communication_scenario',
    'generate_advanced_error_recovery_scenario',
    'generate_social_dynamics_scenario',
    'generate_conflicting_information_scenario',
    'generate_strategic_planning_scenario',
    'generate_empathetic_reasoning_scenario',
    'generate_adaptive_communication_scenario',
    'generate_predictive_analytics_scenario',
    'generate_resource_optimization_scenario',
    'generate_collaborative_filtering_scenario',
    'generate_payment_history_scenario',
    'generate_setup_autopay_scenario',
    'generate_change_package_scenario',
    'generate_suspend_line_scenario',
    'generate_error_response_scenario',
    'generate_package_details_scenario',
    'generate_enable_roaming_scenario',
    'generate_get_user_tickets_scenario',
    'generate_get_ticket_status_scenario',
    'generate_test_internet_speed_scenario'
]
