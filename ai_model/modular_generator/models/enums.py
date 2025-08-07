# -*- coding: utf-8 -*-
"""
📊 GELİŞMİŞ FRAMEWORK TANIMLARI (Enhanced Framework)
====================================================

Bu modül, SupremeHumanLevelDatasetGenerator için tüm enum tanımlarını içerir.
"""

from enum import Enum


class ScenarioType(Enum):
    # Mevcut senaryolar
    STANDARD = "standard"
    MULTI_INTENT = "multi_intent"
    DISAMBIGUATION = "disambiguation"
    PROACTIVE = "proactive"
    TOOL_CHAINING = "tool_chaining"
    ETHICAL_DILEMMA = "ethical_dilemma"
    CREATIVE_PROBLEM_SOLVING = "creative_problem_solving"
    REAL_TIME_LEARNING = "real_time_learning"
    MULTI_MODAL_REASONING = "multi_modal_reasoning"
    CULTURAL_SENSITIVITY = "cultural_sensitivity"
    CRISIS_MANAGEMENT = "crisis_management"
    
    # YENİ EKLENEN 14 SENARYO
    NEGOTIATION_SKILLS = "negotiation_skills"
    TEACHING_MENTORING = "teaching_mentoring"
    INNOVATION_THINKING = "innovation_thinking"
    COLLABORATIVE_FILTERING = "collaborative_filtering"
    TEMPORAL_REASONING = "temporal_reasoning"
    CROSS_CULTURAL_COMMUNICATION = "cross_cultural_communication"
    ADVANCED_ERROR_RECOVERY = "advanced_error_recovery"
    PREDICTIVE_ANALYTICS = "predictive_analytics"
    SOCIAL_DYNAMICS = "social_dynamics"
    ADAPTIVE_COMMUNICATION = "adaptive_communication"
    CONFLICTING_INFORMATION = "conflicting_information"
    RESOURCE_OPTIMIZATION = "resource_optimization"
    STRATEGIC_PLANNING = "strategic_planning"
    EMPATHETIC_REASONING = "empathetic_reasoning"

    # --- UZMAN SEVİYE EKLEME: EKSİK API'LER İÇİN YENİ SENARYOLAR ---
    PAYMENT_HISTORY = "payment_history"
    SETUP_AUTOPAY = "setup_autopay"
    CHANGE_PACKAGE = "change_package"
    PACKAGE_DETAILS = "package_details"
    ENABLE_ROAMING = "enable_roaming"
    CLOSE_TICKET = "close_ticket"
    GET_USER_TICKETS = "get_user_tickets"
    GET_TICKET_STATUS = "get_ticket_status"
    UPDATE_CONTACT = "update_contact"
    SUSPEND_LINE = "suspend_line"
    REACTIVATE_LINE = "reactivate_line"
    EMERGENCY_SERVICE = "emergency_service"
    TEST_INTERNET_SPEED = "test_internet_speed"
    LEARNING_ADAPTATION = "learning_adaptation"
    ERROR_RESPONSE = "error_response"


class CognitiveState(Enum):
    FOCUSED = "focused"
    
    #
    ANALYTICAL = "analytical"
    EMPATHETIC = "empathetic"
    CREATIVE = "creative"
    SYSTEMATIC = "systematic"
    INTUITIVE = "intuitive"
    STRATEGIC = "strategic"
    COLLABORATIVE = "collaborative"
    INNOVATIVE = "innovative"
    NEGOTIATIVE = "negotiative"      # YENİ
    EDUCATIONAL = "educational"      # YENİ
    PREDICTIVE = "predictive"       # YENİ

class EmotionalContext(Enum):
    # Mevcut duygusal durumlar
    HOPEFUL = "hopeful"
    CALM = "calm"
    FRUSTRATED = "frustrated"
    EXCITED = "excited"
    WORRIED = "worried"
    CONFUSED = "confused"
    GRATEFUL = "grateful"
    URGENT = "urgent"
    SKEPTICAL = "skeptical"
    OVERWHELMED = "overwhelmed"
    CURIOUS = "curious"
    GRIEF = "grief"
    NOSTALGIA = "nostalgia"
    BETRAYAL = "betrayal"
    OVERWHELM = "overwhelm"
    ISOLATION = "isolation"
    EUPHORIA = "euphoria"
    REGRET = "regret"
    ANTICIPATION = "anticipation"
    MELANCHOLY = "melancholy"
    TRIUMPH = "triumph"
    
    # YENİ DUYGUSAL DURUMLAR
    COMPETITIVE = "competitive"      # Rekabetçi
    COLLABORATIVE_MOOD = "collaborative_mood"  # İş birlikçi
    INNOVATIVE_DRIVE = "innovative_drive"     # Yenilikçi itkisi
    PROTECTIVE = "protective"        # Koruyucu
    AMBITIOUS = "ambitious"          # Hırslı
    CONTEMPLATIVE = "contemplative"  # Düşünceli
    RESILIENT = "resilient"         # Dirençli