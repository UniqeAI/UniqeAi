# -*- coding: utf-8 -*-
"""
🚀 LAZY LOADING PROPERTY FONKSİYONLARI
======================================

Bu modül, SupremeHumanLevelDatasetGenerator için lazy loading property fonksiyonlarını içerir.
Memory optimization için cache sistemi ile çalışır.
"""

from typing import Dict, List, Any
from .models import CulturalContext, PersonalityProfile
from .initializers import (
    initialize_enhanced_personality_profiles,
    initialize_advanced_cognitive_patterns,
    initialize_comprehensive_meta_templates,
    initialize_cultural_contexts,
    initialize_temporal_patterns,
    initialize_innovation_frameworks
)

def personality_profiles_property(self) -> Dict[str, 'PersonalityProfile']:
    """Lazy loading personality profiles - memory optimization"""
    if self._personality_profiles_cache is None:
        self._personality_profiles_cache = initialize_enhanced_personality_profiles()
    return self._personality_profiles_cache

def cognitive_patterns_property(self) -> Dict[str, List[str]]:
    """Lazy loading cognitive patterns - memory optimization"""
    if self._cognitive_patterns_cache is None:
        self._cognitive_patterns_cache = initialize_advanced_cognitive_patterns()
    return self._cognitive_patterns_cache

def meta_templates_property(self) -> Dict[str, List[str]]:
    """Lazy loading meta templates - memory optimization"""
    if self._meta_templates_cache is None:
        self._meta_templates_cache = initialize_comprehensive_meta_templates()
    return self._meta_templates_cache

def cultural_contexts_property(self) -> Dict[str, 'CulturalContext']:
    """Lazy loading cultural contexts - memory optimization"""
    if self._cultural_contexts_cache is None:
        self._cultural_contexts_cache = initialize_cultural_contexts()
    return self._cultural_contexts_cache

def temporal_reasoning_patterns_property(self) -> Dict[str, List[str]]:
    """Lazy loading temporal patterns - memory optimization"""
    if self._temporal_patterns_cache is None:
        self._temporal_patterns_cache = initialize_temporal_patterns()
    return self._temporal_patterns_cache

def innovation_frameworks_property(self) -> Dict[str, List[str]]:
    """Lazy loading innovation frameworks - memory optimization"""
    if self._innovation_frameworks_cache is None:
        self._innovation_frameworks_cache = initialize_innovation_frameworks()
    return self._innovation_frameworks_cache 