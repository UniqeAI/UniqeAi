#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pydantic Doğrulama Test Script'i
===============================

Bu script, güncellenmiş tool_definitions.py ve fake_api_responses_pydantic.json
dosyalarının doğru çalıştığını test eder.
"""

import sys
import json
from pathlib import Path

# Proje yolunu ekle
sys.path.append(str(Path(__file__).parent))

try:
    from tool_definitions import get_tool_response, API_RESPONSE_MODELS, PYDANTIC_AVAILABLE
    from telekom_api_schema import API_MAP
except ImportError as e:
    print(f"❌ Import hatası: {e}")
    sys.exit(1)

def test_all_api_functions():
    """Tüm API fonksiyonlarını test eder."""
    print("🧪 Pydantic Doğrulama Testleri Başlıyor...")
    print(f"📊 Pydantic Mevcut: {PYDANTIC_AVAILABLE}")
    print(f"🔧 Toplam API Fonksiyonu: {len(API_MAP)}")
    print(f"✅ Pydantic Modeli Olan: {len(API_RESPONSE_MODELS)}")
    print("-" * 60)
    
    test_params = {
        "user_id": 8901,
        "bill_id": "F-2024-8901",
        "new_package_name": "Premium Unlimited",
        "issue_description": "Test sorunu",
        "ticket_id": "TKT-2024-001234",
        "problem_description": "Test problemi",
        "innovation_level": "basic",
        "limit": 3,
        "method": "credit_card",
        "payment_method": "credit_card",
        "line_number": "+905551234567",
        "contact_type": "email",
        "new_value": "test@example.com",
        "region": "İstanbul",
        "emergency_type": "natural_disaster",
        "location": "current_location",
        "cultural_profile": "turkish_urban",
        "learned_preferences": {"test": "value"}
    }
    
    success_count = 0
    error_count = 0
    
    for function_name in API_MAP.keys():
        print(f"\n🔍 Test: {function_name}")
        
        try:
            # API yanıtını al
            response_json = get_tool_response(function_name, test_params)
            response_data = json.loads(response_json)
            
            # Başarı durumunu kontrol et
            if response_data.get("success", True):
                if "_pydantic_validation_error" in response_data:
                    print(f"  ⚠️ Pydantic uyarısı var")
                    error_count += 1
                else:
                    print(f"  ✅ Başarılı")
                    success_count += 1
            else:
                print(f"  ℹ️ Hata yanıtı (normal): {response_data.get('error', {}).get('code', 'UNKNOWN')}")
                success_count += 1
                
        except Exception as e:
            print(f"  ❌ Test hatası: {e}")
            error_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 TEST SONUÇLARI:")
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Hatalı: {error_count}")
    print(f"📈 Başarı Oranı: {(success_count/(success_count+error_count)*100):.1f}%")
    
    return success_count, error_count

def test_specific_functions():
    """Belirli fonksiyonları detaylı test eder."""
    print("\n🔬 Detaylı Fonksiyon Testleri:")
    print("-" * 40)
    
    # Test 1: get_current_bill
    print("\n1️⃣ get_current_bill testi:")
    response = get_tool_response("get_current_bill", {"user_id": 8901})
    print(f"   Yanıt uzunluğu: {len(response)} karakter")
    
    # Test 2: get_cultural_context (yeni eklenen)
    print("\n2️⃣ get_cultural_context testi:")
    response = get_tool_response("get_cultural_context", {
        "user_id": 8901, 
        "cultural_profile": "turkish_urban"
    })
    print(f"   Yanıt uzunluğu: {len(response)} karakter")
    
    # Test 3: generate_creative_analysis (yeni eklenen)
    print("\n3️⃣ generate_creative_analysis testi:")
    response = get_tool_response("generate_creative_analysis", {
        "problem_description": "Müşteri memnuniyetsizliği",
        "innovation_level": "strategic"
    })
    print(f"   Yanıt uzunluğu: {len(response)} karakter")

def main():
    """Ana test fonksiyonu."""
    print("🚀 Pydantic Entegrasyon Testi v1.0")
    print("=" * 60)
    
    # Genel testler
    success_count, error_count = test_all_api_functions()
    
    # Detaylı testler
    test_specific_functions()
    
    print("\n🎯 TEST TAMAMLANDI!")
    
    if error_count == 0:
        print("🎉 Tüm testler başarılı! Pydantic entegrasyonu hazır.")
        return 0
    else:
        print(f"⚠️ {error_count} hata bulundu. Kontrol gerekli.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)