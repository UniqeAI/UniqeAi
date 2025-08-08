# -*- coding: utf-8 -*-
"""
🚀 Cerrahi Müdahale: Araç Kullanımını Zorlama Veri Seti Üreticisi v3.0 (Profesyonel)
===================================================================================

Bu script, "Dahi Çocuk Sendromu" yaşayan modeli yeniden eğitmek için tasarlanmıştır.
Bu profesyonel sürüm, önceki denemelerdeki tüm eksiklikleri giderir:
- Dinamik olarak `tool_definitions.py`'den TÜM araçları okur, hiçbirini atlamaz.
- Her araç için gerekli parametreleri analiz eder ve `Faker` ile gerçekçi veriler üretir.
- Sadece "Kullanıcı Komutu -> Anında Araç Çağrısı" formatına odaklanır.
- Kod kalitesi ve sağlamlığı, projedeki diğer uzman seviye jeneratörlerle aynı seviyededir.
- Tek doğru kaynak prensibine sadık kalır.
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
    # Proje kök dizinine (tddi_proje_planlama) ulaşmak için 3 seviye yukarı çık
    PROJECT_ROOT = SCRIPT_DIR.parents[3] 
except (NameError, IndexError):
    PROJECT_ROOT = Path(os.getcwd())

# tool_definitions.py'nin bulunduğu yolu sys.path'e ekle
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from tool_definitions import get_tool_definitions
except ImportError as e:
    print(f"HATA: 'tool_definitions' modülü yüklenemedi. Lütfen UniqeAi/ai_model/scripts/ altında olduğundan emin olun.")
    print(f"Arama yolu: {SCRIPT_DIR}")
    print(f"Hata detayı: {e}")
    sys.exit(1)


fake = Faker("tr_TR")

def generate_realistic_param(param_name: str, param_schema: dict) -> any:
    """
    Parametre adına ve şemasına göre gerçekçi sahte veri üretir.
    """
    p_name_lower = param_name.lower()
    p_type = param_schema.get("type", "string")

    if "user_id" in p_name_lower:
        return fake.random_int(min=10000, max=99999)
    if "ticket_id" in p_name_lower:
        return f"TKT-{fake.random_int(min=100000, max=999999)}"
    if "bill_id" in p_name_lower:
        return f"F-{fake.year()}-{fake.random_int(min=1000, max=9999)}"
    if "package_name" in p_name_lower or "to_package" in p_name_lower:
        return random.choice(["Süper İnternet", "Gamer Pro", "Aile Paketi", "Limitsiz Sosyal"])
    if "amount" in p_name_lower:
        return round(random.uniform(50, 450), 2)
    if "description" in p_name_lower:
        return random.choice(["İnternetim çok yavaş.", "Hattımda kesinti var.", "TV yayınında donma sorunu."])
    if "email" in p_name_lower:
        return fake.email()
    if "new_value" in p_name_lower and p_type == "string": # Daha spesifik kontrol
        return fake.address() if 'address' in param_name else fake.phone_number()
    if "phone" in p_name_lower or "number" in p_name_lower:
        return fake.phone_number()
    if "address" in p_name_lower:
        return fake.address()
    if "reason" in p_name_lower:
        return random.choice(["Kullanıcı talebi", "Yurt dışı seyahati", "Fatura ödenmemesi"])
    if "priority" in p_name_lower:
        return random.choice(["low", "medium", "high"])
    if "category" in p_name_lower:
        return random.choice(["internet_speed", "billing_issue", "service_outage"])
    
    if p_type == "integer":
        return fake.random_int(min=1, max=100)
    if p_type == "number":
        return round(random.uniform(1, 100), 2)
    if p_type == "boolean":
        return random.choice([True, False])
    
    return f"test_degeri_{param_name}"


def create_prompt_templates() -> dict:
    """
    Tüm araçlar için dinamik olarak komut şablonları oluşturur.
    """
    templates = {}
    tool_definitions = get_tool_definitions()
    
    for tool in tool_definitions:
        name = tool['function']['name']
        desc = tool['function']['description']
        
        prompts = [
            f"{name} fonksiyonunu çalıştır.",
            f"{desc}",
        ]
        
        name_parts = name.split('_')
        if len(name_parts) > 1:
            action = name_parts[0]
            entity = " ".join(name_parts[1:])
            
            if action in ["get", "check", "test", "show", "list", "find", "analyze"]:
                prompts.extend([
                    f"{entity} göster.",
                    f"{entity} nedir?",
                    f"{entity} durumunu sorgula.",
                    f"{entity} alabilir miyim?",
                    f"Bana {entity} analizi yap."
                ])
            elif action in ["create", "generate", "add", "new"]:
                 prompts.extend([
                    f"Yeni bir {entity} oluştur.",
                    f"{entity} ekle.",
                ])
            elif action in ["update", "change", "set", "modify", "enable", "suspend", "reactivate"]:
                prompts.extend([
                    f"{entity} güncelle.",
                    f"{entity} değiştir.",
                    f"{entity} aktif et.",
                ])

        templates[name] = list(set(prompts))
        
    return templates


def generate_tool_forcing_dataset(num_samples: int, templates: dict):
    """
    Sadece 'Kullanıcı Komutu -> Anında Araç Çağrısı' formatında veri üretir.
    """
    dataset = []
    
    all_tools = get_tool_definitions()
    tool_map = {tool['function']['name']: tool['function'] for tool in all_tools}
    tool_names = list(tool_map.keys())

    print(f"Toplam {len(tool_names)} adet araç için veri üretilecek.")

    for i in range(num_samples):
        tool_name = random.choice(tool_names)
        tool_schema = tool_map[tool_name]
        
        user_prompt = random.choice(templates[tool_name])

        params = {}
        if 'parameters' in tool_schema and 'properties' in tool_schema['parameters']:
            for param_name, param_schema_def in tool_schema['parameters']['properties'].items():
                params[param_name] = generate_realistic_param(param_name, param_schema_def)

        dialogue = {
            "id": f"TF-V3-{uuid.uuid4().hex[:8]}",
            "senaryo": "Tool Forcing v3 - Direkt ve Kapsamlı Araç Çağrısı",
            "donguler": [
                {
                    "rol": "kullanici",
                    "icerik": user_prompt
                },
                {
                    "rol": "asistan",
                    "icerik": None,
                    "arac_cagrilari": [
                        {
                            "fonksiyon": tool_name,
                            "parametreler": params
                        }
                    ]
                }
            ]
        }
        dataset.append(dialogue)

    return dataset

def save_dataset(dataset: list, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"✅ 'Araç Zorlama' v3 veri seti başarıyla kaydedildi: {path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='v3 - Kapsamlı ve Profesyonel Araç Zorlama Veri Seti Üreticisi.')
    parser.add_argument('--num', type=int, default=3000, help='Üretilecek toplam örnek sayısı.')
    parser.add_argument('--output', type=str, default=str(PROJECT_ROOT / 'UniqeAi' / 'ai_model' / 'data' / 'tool_forcing_dataset_v3_professional.json'), help='Çıktı JSON dosyasının yolu.')
    
    args = parser.parse_args()
    
    print("🚀 Komut şablonları oluşturuluyor...")
    prompt_templates = create_prompt_templates()
    
    print(f"🚀 {args.num} adet 'Araç Zorlama v3' senaryosu üretiliyor...")
    final_dataset = generate_tool_forcing_dataset(args.num, prompt_templates)
    
    save_dataset(final_dataset, args.output)
    
    print(f"🎉 Cerrahi müdahale için v3 veri seti hazır! Toplam {len(final_dataset)} örnek üretildi.")
