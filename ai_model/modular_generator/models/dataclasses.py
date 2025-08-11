# -*- coding: utf-8 -*-
"""
📊 VERİ MODELLERİ - DATACLASS TANIMLARI
=======================================

Bu modül, SupremeHumanLevelDatasetGenerator için tüm veri modellerini içerir.
Pydantic BaseModel'ler ile uyumlu dataclass tanımları.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class PersonalityProfile:
    patience_level: float = 0.5
    tech_literacy: float = 0.5
    emotional_stability: float = 0.5
    communication_style: str = "balanced"
    problem_solving_approach: str = "methodical"
    trust_level: float = 0.5
    cultural_background: str = "mixed"
    learning_style: str = "adaptive"
    stress_response: str = "moderate"
    social_orientation: str = "balanced"    # YENİ
    risk_tolerance: float = 0.5            # YENİ
    innovation_openness: float = 0.5       # YENİ

@dataclass
class ConversationMemory:
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    mentioned_topics: List[str] = field(default_factory=list)
    emotional_journey: List[str] = field(default_factory=list)
    learned_facts: Dict[str, str] = field(default_factory=dict)
    success_strategies: List[str] = field(default_factory=list)
    interaction_patterns: Dict[str, int] = field(default_factory=dict)
    relationship_depth: int = 0            # YENİ
    trust_evolution: List[float] = field(default_factory=list)  # YENİ

@dataclass 
class MultiModalData:
    data_type: str
    values: List[float]
    labels: List[str]
    insights: List[str]
    recommendations: List[str]
    temporal_patterns: List[str] = field(default_factory=list)  # YENİ
    predictive_insights: List[str] = field(default_factory=list)  # YENİ

@dataclass
class CulturalContext:
    region: str
    communication_style: str
    decision_making_pattern: str
    technology_adoption: str
    family_influence: str
    time_orientation: str
    authority_respect: str
    collective_vs_individual: str
