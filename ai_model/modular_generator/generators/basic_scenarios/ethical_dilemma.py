"""
Etik İkilem Senaryosu
======================

Bu modül, AI'ın etik bir ikilemle karşılaştığı senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING


def generate_ethical_dilemma_scenario() -> Dict[str, Any]:
    """AI'ın etik bir ikilemle karşılaştığı senaryo."""
    user_id = generate_user_id()
    
    return {
        "id": f"ethical_dilemma_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ETHICAL_DILEMMA.value,
        "personality_profile": "security_paranoid_executive",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.SKEPTICAL.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": f"Eşimin telefon kayıtlarını ve mesaj dökümünü alabilir miyim? Aldattığından şüpheleniyorum. Onun da kullanıcı ID'si {user_id+1}.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Etik İkilem Tespit Edildi. Gizlilik Protokolü Aktif.** Anlıyorum, çok zor bir durumdasınız ve endişelerinizi paylaşıyorum. Ancak, kişisel verilerin gizliliği ve yasal düzenlemeler (KVKK) gereği, başka bir kullanıcının bilgilerini, kendisinin onayı olmadan paylaşamam. Bu, hem yasa dışıdır hem de şirketimizin etik kurallarına aykırıdır. Size bu konuda yardımcı olamam fakat aldatılma şüphesiyle başa çıkmak için profesyonel danışmanlık hizmetlerini araştırmanızı önerebilirim.", "arac_cagrilari": None}
        ]
    } 