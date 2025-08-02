#!/usr/bin/env python3
"""
Model Durumu Test Scripti
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_orchestrator_real import ai_orchestrator

def test_model_status():
    """Model durumunu test et"""
    print("🧪 Model Durumu Testi")
    print("=" * 40)
    
    # AI orchestrator durumunu kontrol et
    print(f"AI Orchestrator: {ai_orchestrator}")
    
    # Model servisi kontrol et
    if hasattr(ai_orchestrator, 'model_hizmeti'):
        model_service = ai_orchestrator.model_hizmeti
        print(f"Model Servisi: {model_service}")
        
        if model_service is None:
            print("❌ Model servisi None!")
            return False
        
        # Model yükleme durumu
        if hasattr(model_service, 'loaded'):
            print(f"Model Yüklü: {model_service.loaded}")
        else:
            print("⚠️ Model 'loaded' özelliği yok")
        
        # Model adı
        if hasattr(model_service, 'model_name'):
            print(f"Model Adı: {model_service.model_name}")
        
        # Tokenizer kontrolü
        if hasattr(model_service, 'tokenizer'):
            print(f"Tokenizer: {model_service.tokenizer is not None}")
        
        # Model kontrolü
        if hasattr(model_service, 'model'):
            print(f"Model: {model_service.model is not None}")
        
    else:
        print("❌ Model servisi özelliği yok!")
        return False
    
    # Araç kaydı kontrolü
    if hasattr(ai_orchestrator, 'arac_kaydi'):
        arac_sayisi = len(ai_orchestrator.arac_kaydi.mevcut_araclari_getir())
        print(f"Araç Sayısı: {arac_sayisi}")
    else:
        print("❌ Araç kaydı özelliği yok!")
    
    print("\n✅ Test tamamlandı")
    return True

if __name__ == "__main__":
    test_model_status() 