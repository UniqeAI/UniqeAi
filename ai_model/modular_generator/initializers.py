# -*- coding: utf-8 -*-
"""
🚀 INITIALIZATION METHODS - V3 ENHANCEMENT
=========================================

Bu modül, SupremeHumanLevelDatasetGenerator için tüm initialize metodlarını içerir.
V3 Enhancement özelliklerini destekler.
"""

from typing import Dict, List, Any
from .models import PersonalityProfile, CulturalContext

def initialize_enhanced_personality_profiles():
    """Gelişmiş kişilik profilleri - 20+ arketip"""
    return {
        # Mevcut profiller
        "tech_savvy_millennial": PersonalityProfile(
            patience_level=0.6, tech_literacy=0.9, emotional_stability=0.7,
            communication_style="casual", problem_solving_approach="digital_first",
            trust_level=0.7, cultural_background="digital_native",
            learning_style="interactive", stress_response="problem_solving",
            social_orientation="collaborative", risk_tolerance=0.7, innovation_openness=0.9
        ),
        
        "cautious_senior": PersonalityProfile(
            patience_level=0.9, tech_literacy=0.3, emotional_stability=0.8,
            communication_style="formal", problem_solving_approach="traditional",
            trust_level=0.5, cultural_background="traditional",
            learning_style="step_by_step", stress_response="seek_help",
            social_orientation="family_focused", risk_tolerance=0.2, innovation_openness=0.3
        ),
        
        "busy_working_parent": PersonalityProfile(
            patience_level=0.4, tech_literacy=0.6, emotional_stability=0.6,
            communication_style="efficient", problem_solving_approach="practical",
            trust_level=0.8, cultural_background="family_oriented",
            learning_style="solution_focused", stress_response="time_pressure",
            social_orientation="family_first", risk_tolerance=0.4, innovation_openness=0.5
        ),
        
        # YENİ GELİŞMİŞ PROFİLLER
        "innovative_entrepreneur": PersonalityProfile(
            patience_level=0.5, tech_literacy=0.8, emotional_stability=0.7,
            communication_style="visionary", problem_solving_approach="disruptive",
            trust_level=0.6, cultural_background="global",
            learning_style="experimental", stress_response="opportunity_seeking",
            social_orientation="network_builder", risk_tolerance=0.9, innovation_openness=1.0
        ),
        
        "security_paranoid_executive": PersonalityProfile(
            patience_level=0.3, tech_literacy=0.7, emotional_stability=0.5,
            communication_style="authoritative", problem_solving_approach="risk_averse",
            trust_level=0.2, cultural_background="corporate",
            learning_style="verified_sources", stress_response="control_seeking",
            social_orientation="hierarchical", risk_tolerance=0.1, innovation_openness=0.3
        ),
        
        "creative_artist_freelancer": PersonalityProfile(
            patience_level=0.7, tech_literacy=0.6, emotional_stability=0.6,
            communication_style="expressive", problem_solving_approach="creative",
            trust_level=0.8, cultural_background="artistic",
            learning_style="inspirational", stress_response="creative_outlet",
            social_orientation="community_minded", risk_tolerance=0.6, innovation_openness=0.9
        ),
        
        "data_driven_analyst": PersonalityProfile(
            patience_level=0.8, tech_literacy=0.9, emotional_stability=0.8,
            communication_style="precise", problem_solving_approach="evidence_based",
            trust_level=0.7, cultural_background="academic",
            learning_style="data_driven", stress_response="research_more",
            social_orientation="professional", risk_tolerance=0.4, innovation_openness=0.7
        ),
        
        "empathetic_healthcare_worker": PersonalityProfile(
            patience_level=0.9, tech_literacy=0.5, emotional_stability=0.7,
            communication_style="caring", problem_solving_approach="human_centered",
            trust_level=0.9, cultural_background="service_oriented",
            learning_style="practical_application", stress_response="support_others",
            social_orientation="community_service", risk_tolerance=0.3, innovation_openness=0.6
        ),
        
        "competitive_sales_professional": PersonalityProfile(
            patience_level=0.4, tech_literacy=0.7, emotional_stability=0.6,
            communication_style="persuasive", problem_solving_approach="win_win",
            trust_level=0.6, cultural_background="competitive",
            learning_style="results_oriented", stress_response="goal_focused",
            social_orientation="network_leveraging", risk_tolerance=0.7, innovation_openness=0.8
        ),
        
        "philosophical_academic": PersonalityProfile(
            patience_level=0.9, tech_literacy=0.6, emotional_stability=0.8,
            communication_style="contemplative", problem_solving_approach="systematic_inquiry",
            trust_level=0.7, cultural_background="intellectual",
            learning_style="deep_understanding", stress_response="reflection",
            social_orientation="knowledge_sharing", risk_tolerance=0.5, innovation_openness=0.8
        )
    }

def initialize_advanced_cognitive_patterns():
    """Gelişmiş bilişsel düşünme kalıpları"""
    return {
        # Mevcut kalıplar korunuyor...
        "analogical_reasoning": [
            "Bu durum tıpkı... gibi, şöyle düşünelim:",
            "Bunu başka bir örnekle açıklayacak olursam:",
            "Benzer deneyimlerden yola çıkarak:"
        ],
        
        # YENİ GELİŞMİŞ KALIPLAR
        "negotiation_strategy": [
            "Her iki tarafın da kazanacağı bir çözüm bulalım:",
            "Önceliklerinizi anlayarak en iyi dengeyi kuralım:",
            "Bu noktada karşılıklı değer yaratma fırsatı var:"
        ],
        
        "teaching_methodology": [
            "Adım adım öğrenmenizi destekleyeyim:",
            "Bu konuyu daha iyi anlamanız için farklı açılardan bakalım:",
            "Öğrenme sürecinizi kişiselleştireyim:"
        ],
        
        "innovation_thinking": [
            "Geleneksel sınırları aşan bir yaklaşım deneyelim:",
            "Bu problemi bambaşka bir perspektiften değerlendirelim:",
            "Yıkıcı yenilik potansiyeli olan çözümler araştıralım:"
        ],
        
        "temporal_reasoning": [
            "Geçmiş deneyimlerinizden çıkarılan derslerle:",
            "Gelecekteki ihtiyaçlarınızı öngörerek:",
            "Zamansal bağlamda değerlendirdiğimizde:"
        ],
        
        "predictive_analysis": [
            "Mevcut eğilimleri analiz ettiğimizde:",
            "Gelecek senaryolarını modelleyecek olursak:",
            "Öngörüsel verilerle desteklersek:"
        ],
        
        "cross_cultural_bridge": [
            "Farklı kültürel perspektifleri harmanlayarak:",
            "Kültürler arası ortak noktaları bularak:",
            "Çok-kültürlü bir yaklaşımla:"
        ]
    }

def initialize_comprehensive_meta_templates():
    """Kapsamlı meta-konuşma şablonları"""
    return {
        # Mevcut şablonlar korunuyor + yeniler ekleniyor
        "self_correction": [
            "Aslında az önce söylediklerimi düzeltelim:",
            "Pardon, daha doğru bir ifadeyle:",
            "Yanlış anladım, tekrar değerlendireyim:"
        ],
        
        "confidence_calibration": [
            "Bu konuda %{confidence} emin olduğumu söyleyebilirim:",
            "Elimdeki bilgilere göre, güven seviyem %{confidence}:",
            "Belirsizlik payıyla birlikte, %{confidence} olasılıkla:"
        ],
        
        # YENİ META-ŞABLONlar
        "learning_acknowledgment": [
            "Bu konuşmamızdan şunu öğrendim:",
            "Tarzınızı öğrenerek ileride daha iyi yardım edebilirim:",
            "Bu deneyim sayesinde yaklaşımımı şöyle geliştiriyorum:"
        ],
        
        "relationship_building": [
            "Birlikte çalışırken fark ettiğim şey:",
            "İlişkimizin gelişimiyle birlikte:",
            "Güveninizi kazandıkça daha iyi hizmet verebiliyorum:"
        ],
        
        "adaptive_communication": [
            "Iletişim tarzınıza uyum sağlayarak:",
            "Size en uygun şekilde anlatmak için:",
            "Tercih ettiğiniz yaklaşımı kullanarak:"
        ],
        
        "innovation_brainstorming": [
            "Yaratıcı beyin fırtınası yaparsak:",
            "Sıra dışı fikirler üretmeye odaklanalım:",
            "İnovasyon odaklı düşünce egzersizi yapalım:"
        ]
    }

def initialize_cultural_contexts():
    """Kültürel bağlamlar"""
    return {
        "traditional_turkish": CulturalContext(
            region="Türkiye", communication_style="respectful_formal",
            decision_making_pattern="family_consultation", technology_adoption="gradual",
            family_influence="high", time_orientation="relationship_first",
            authority_respect="high", collective_vs_individual="collective"
        ),
        
        "modern_urban_turkish": CulturalContext(
            region="İstanbul/Ankara", communication_style="efficient_friendly",
            decision_making_pattern="individual_informed", technology_adoption="early_adopter",
            family_influence="balanced", time_orientation="efficiency_focused",
            authority_respect="moderate", collective_vs_individual="balanced"
        ),
        
        "global_expat": CulturalContext(
            region="International", communication_style="direct_multicultural",
            decision_making_pattern="data_driven", technology_adoption="cutting_edge",
            family_influence="low", time_orientation="time_sensitive",
            authority_respect="performance_based", collective_vs_individual="individual"
        )
    }

def initialize_temporal_patterns():
    """Zamansal akıl yürütme kalıpları"""
    return {
        "past_analysis": [
            "Geçmiş deneyimlerinizi analiz ettiğimizde:",
            "Önceki etkileşimlerimizden çıkardığımız sonuçlar:",
            "Tarihsel verileriniz şunu gösteriyor:"
        ],
        
        "present_awareness": [
            "Şu anki durumunuzu değerlendirdiğimizde:",
            "Mevcut ihtiyaçlarınız ve kapasiteleriniz:",
            "Bugünkü koşullarda en uygun yaklaşım:"
        ],
        
        "future_projection": [
            "Gelecekteki ihtiyaçlarınızı öngördüğümüzde:",
            "İlerleyen süreçte karşılaşabileceğiniz durumlar:",
            "Uzun vadeli hedeflerinize uygun stratejiler:"
        ],
        
        "seasonal_awareness": [
            "Yılın bu döneminde genellikle:",
            "Mevsimsel ihtiyaçlarınızı düşünürsek:",
            "Bu zamanlamanın getirdiği özel durumlar:"
        ]
    }

def initialize_innovation_frameworks():
    """İnovasyon çerçeveleri"""
    return {
        "design_thinking": [
            "Kullanıcı deneyimi odaklı düşünürsek:",
            "Empati kurarak problem tanımını netleştirirelim:",
            "Prototip yaklaşımıyla hızlı test edelim:"
        ],
        
        "disruptive_innovation": [
            "Sektördeki geleneksel yaklaşımları sorgulayalım:",
            "Yıkıcı değişim potansiyeli olan çözümler:",
            "Paradigma değiştiren yaklaşımlar:"
        ],
        
        "lean_methodology": [
            "Minimum viable product mantığıyla:",
            "Hızlı öğrenme döngüleriyle:",
            "Sürekli iyileştirme odaklı:"
        ]
    } 