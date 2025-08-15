# -*- coding: utf-8 -*-
"""
🚀 Cerrahi Müdahale: Araç Kullanımını Zorlama Veri Seti Üreticisi v4.0 (Schema-Driven Professional)
=================================================================================================

Bu script, "Dahi Çocuk Sendromu" yaşayan modeli yeniden eğitmek için tasarlanmıştır.
Bu profesyonel sürüm, projenin "tek doğru kaynak" (`telekom_api_schema.py`) prensibine
%100 sadık kalarak çalışır ve önceki sürümlerdeki tüm mimari eksiklikleri giderir.

ÖZELLİKLER:
- **Tek Doğru Kaynak:** Kullanılabilir araçların listesini doğrudan `telekom_api_schema.py` dosyasındaki `API_MAP`'ten alır.
- **Senkronizasyon Kontrolü:** `telekom_api_schema.py` ve `tool_definitions.py` arasındaki tutarsızlıkları bularak uyarır.
- **Dinamik ve Kapsamlı:** `API_MAP`'teki TÜM araçlar için veri üretir.
- **Gerçekçi Parametreler:** `Faker` kütüphanesi ile her araç için mantıklı ve çeşitli sahte veriler üretir.
- **Odaklı Eğitim:** Sadece "Kullanıcı Komutu -> Anında Araç Çağrısı" formatına odaklanır.
"""

import json
import random
import uuid
import os
import argparse
from faker import Faker
import sys
from pathlib import Path

# --- Proje Kök Dizini ve Modül Yolu ---
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parents[3] 
except (NameError, IndexError):
    PROJECT_ROOT = Path(os.getcwd())

sys.path.insert(0, str(SCRIPT_DIR))

# --- İKİ ANA KAYNAĞI DA İÇE AKTARMA ---
try:
    from telekom_api_schema import API_MAP
    from tool_definitions import get_tool_definitions
    # Pydantic modelleri import et
    from telekom_api_schema import *
    from pydantic import ValidationError
except ImportError as e:
    print(f"HATA: Gerekli modüller yüklenemedi. 'telekom_api_schema.py' ve 'tool_definitions.py' dosyalarının varlığını kontrol edin.")
    print(f"Arama yolu: {SCRIPT_DIR}")
    print(f"Hata detayı: {e}")
    sys.exit(1)

fake = Faker("tr_TR")

def sync_and_get_tools():
    """
    İki ana kaynağı senkronize eder, tutarsızlıkları bildirir ve nihai araç haritasını döndürür.
    """
    print("🔄 Araç kaynakları senkronize ediliyor...")
    
    schema_functions = set(API_MAP.keys())
    definitions_data = get_tool_definitions()
    definitions_map = {tool['function']['name']: tool['function'] for tool in definitions_data}
    definitions_functions = set(definitions_map.keys())
    
    if schema_functions != definitions_functions:
        print("\n" + "="*80)
        print("⚠️ UYARI: `telekom_api_schema.py` ve `tool_definitions.py` arasında tutarsızlık tespit edildi!")
        
        in_schema_not_in_defs = schema_functions - definitions_functions
        if in_schema_not_in_defs:
            print(f"\n[+] `telekom_api_schema.py`'de olup `tool_definitions.py`'de EKSİK olanlar:")
            for func in in_schema_not_in_defs:
                print(f"  - {func}")
        
        in_defs_not_in_schema = definitions_functions - schema_functions
        if in_defs_not_in_schema:
            print(f"\n[-] `tool_definitions.py`'de olup `telekom_api_schema.py`'de OLMAYANLAR (fazlalık):")
            for func in in_defs_not_in_schema:
                print(f"  - {func}")
        
        print("\n" + "="*80)
        print("💡 Öneri: Lütfen bu iki dosyayı senkronize edin. Eğitim için `telekom_api_schema.py` TEK DOĞRU KAYNAK olarak kullanılacaktır.")
    else:
        print("✅ Senkronizasyon başarılı! İki dosya da birbiriyle uyumlu.")

    final_tool_map = {name: definitions_map[name] for name in schema_functions if name in definitions_map}
    
    if not final_tool_map:
        print("❌ HATA: Hiçbir ortak araç bulunamadı. Lütfen dosya içeriklerini kontrol edin.")
        sys.exit(1)
        
    return final_tool_map

def generate_realistic_param(param_name: str, param_schema: dict) -> any:
    p_name_lower = param_name.lower()
    p_type = param_schema.get("type", "string")

    if "user_id" in p_name_lower: return fake.random_int(min=10000, max=99999)
    if "ticket_id" in p_name_lower: return f"TKT-{fake.random_int(min=100000, max=999999)}"
    if "bill_id" in p_name_lower: return f"F-{fake.year()}-{fake.random_int(min=1000, max=9999)}"
    if "package_name" in p_name_lower or "to_package" in p_name_lower: return random.choice(["Süper İnternet", "Gamer Pro", "Aile Paketi"])
    if "amount" in p_name_lower: return round(random.uniform(50, 450), 2)
    if "description" in p_name_lower: return random.choice(["İnternetim çok yavaş.", "Hattımda kesinti var.", "TV yayınında donma."])
    if "email" in p_name_lower: return fake.email()
    if "new_value" in p_name_lower and p_type == "string": return fake.address() if 'address' in param_name else fake.phone_number()
    if "phone" in p_name_lower or "number" in p_name_lower: return fake.phone_number()
    if "address" in p_name_lower: return fake.address()
    if "reason" in p_name_lower: return random.choice(["Kullanıcı talebi", "Yurt dışı seyahati", "Fatura ödenmemesi"])
    if "priority" in p_name_lower: return random.choice(["low", "medium", "high"])
    if "category" in p_name_lower: return random.choice(["internet_speed", "billing_issue", "service_outage"])
    if p_type == "integer": return fake.random_int(min=1, max=100)
    if p_type == "number": return round(random.uniform(1, 100), 2)
    if p_type == "boolean": return random.choice([True, False])
    return f"test_degeri_{param_name}"

def create_prompt_templates(tool_map: dict) -> dict:
    templates = {}
    for name, schema in tool_map.items():
        desc = schema['description']
        prompts = [f"{name} fonksiyonunu çalıştır.", desc]
        name_parts = name.split('_')
        if len(name_parts) > 1:
            action, entity = name_parts[0], " ".join(name_parts[1:])
            if action in ["get", "check", "test", "show", "list", "find", "analyze"]:
                prompts.extend([f"{entity} göster.", f"{entity} nedir?", f"{entity} durumunu sorgula."])
            elif action in ["create", "generate", "add", "new"]:
                prompts.extend([f"Yeni bir {entity} oluştur.", f"{entity} ekle."])
            elif action in ["update", "change", "set", "modify", "enable", "suspend", "reactivate"]:
                prompts.extend([f"{entity} güncelle.", f"{entity} değiştir."])
        templates[name] = list(set(prompts))
    return templates

def generate_tool_forcing_dataset(num_samples: int, tool_map: dict, templates: dict):
    dataset = []
    tool_names = list(tool_map.keys())
    print(f"Toplam {len(tool_names)} adet doğrulanmış araç için veri üretilecek.")

    for i in range(num_samples):
        tool_name = random.choice(tool_names)
        tool_schema = tool_map[tool_name]
        user_prompt = random.choice(templates[tool_name])
        params = {}
        if 'parameters' in tool_schema and 'properties' in tool_schema['parameters']:
            for param_name, param_schema_def in tool_schema['parameters']['properties'].items():
                params[param_name] = generate_realistic_param(param_name, param_schema_def)

        dialogue = {
            "id": f"TF-V4-{uuid.uuid4().hex[:8]}",
            "senaryo": "Tool Forcing v4 - Schema-Driven, Direkt ve Kapsamlı Araç Çağrısı",
            "donguler": [
                {"rol": "kullanici", "icerik": user_prompt},
                {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": tool_name, "parametreler": params}]}
            ]
        }
        dataset.append(dialogue)
    return dataset

def save_dataset(dataset: list, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"✅ 'Araç Zorlama' v4 veri seti başarıyla kaydedildi: {path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='v4 - Schema-Driven ve Profesyonel Araç Zorlama Veri Seti Üreticisi.')
    parser.add_argument('--num', type=int, default=3000, help='Üretilecek toplam örnek sayısı.')
    parser.add_argument('--output', type=str, default=str(PROJECT_ROOT / 'UniqeAi' / 'ai_model' / 'data' / 'tool_forcing_dataset_v4_schema_driven.json'), help='Çıktı JSON dosyasının yolu.')
    
    args = parser.parse_args()
    
    tool_map = sync_and_get_tools()
    
    print("🚀 Komut şablonları oluşturuluyor...")
    prompt_templates = create_prompt_templates(tool_map)
    
    print(f"🚀 {args.num} adet 'Araç Zorlama v4' senaryosu üretiliyor...")
    final_dataset = generate_tool_forcing_dataset(args.num, tool_map, prompt_templates)
    
    save_dataset(final_dataset, args.output)
    
    print(f"🎉 Cerrahi müdahale için v4 veri seti hazır! Toplam {len(final_dataset)} örnek üretildi.")
