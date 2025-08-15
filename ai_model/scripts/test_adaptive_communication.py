#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script: Adaptive Communication Senaryoları
===============================================

Bu script, adaptive_communication.py dosyasındaki senaryoların 
core_generator.py ile doğru çalışıp çalışmadığını test eder.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modular_generator'))

from generators.advanced_scenarios.adaptive_communication import generate_adaptive_communication_scenarios

def test_adaptive_communication_scenarios():
    """Adaptive communication senaryolarını test eder"""
    
    print("🧪 Adaptive Communication Senaryoları Test Ediliyor...")
    print("=" * 60)
    
    try:
        # Tüm senaryoları al
        scenarios = generate_adaptive_communication_scenarios()
        
        print(f"✅ Toplam {len(scenarios)} senaryo başarıyla yüklendi!")
        print()
        
        # İlk 3 senaryoyu göster
        print("📋 İlk 3 Senaryo Örneği:")
        print("-" * 40)
        
        for i, scenario in enumerate(scenarios[:3], 1):
            print(f"\n{i}. Senaryo:")
            print(f"   ID: {scenario.get('id', 'N/A')}")
            print(f"   Tür: {scenario.get('scenario_type', 'N/A')}")
            print(f"   Kişilik: {scenario.get('personality_profile', 'N/A')}")
            print(f"   Döngü Sayısı: {len(scenario.get('donguler', []))}")
            
            # İlk döngüyü göster
            if scenario.get('donguler'):
                first_dialog = scenario['donguler'][0]
                print(f"   İlk Mesaj: {first_dialog.get('icerik', 'N/A')[:50]}...")
        
        print("\n" + "=" * 60)
        print("🎉 Test başarılı! Tüm senaryolar hazır.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test başarısız: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_adaptive_communication_scenarios()
    if success:
        print("\n✅ Test tamamlandı. Senaryolar core_generator.py ile kullanıma hazır!")
    else:
        print("\n❌ Test başarısız. Lütfen hataları düzeltin.") 