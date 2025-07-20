# -*- coding: utf-8 -*-
import json
import random
import os
import argparse
from datetime import datetime, timedelta
from faker import Faker
from pydantic import ValidationError

# === MODELLER ===
from telekom_api_schema import (
    GetRemainingQuotasResponse, UsagePercentage,
    GetAvailablePackagesResponse, AvailablePackageItem, AvailablePackageFeatures,
    GetPackageDetailsResponse, PackageDetailsFeatures,
    ChangePackageResponse,
    GetCurrentBillResponse, ServiceItem,
    TestInternetSpeedResponse,
    GetFaultTicketStatusResponse
)

# Faker'ı Türkçe ile başlat
fake = Faker("tr_TR")

# --- Yardımcı Fonksiyonlar ---
def generate_user_id():
    return fake.random_int(min=1000, max=999999)

def validate_response(model, data: dict) -> dict:
    try:
        validated = model(**data)
        return json.loads(validated.model_dump_json())
    except ValidationError as e:
        raise RuntimeError(f"Validation error ({model.__name__}): {e}")

# =====================================================================
# SENARYO: COMPLEX & MULTI-INTENT
# =====================================================================

def scenario_usage_and_upgrade_and_bill():
    """
    Kullanıcı tek cümlede hem kalan kotayı, hem paket yükseltmeyi,
    hem de son faturayı öğrenmek istiyor.
    """
    user_id = generate_user_id()
    # 1. Quotas
    rem_gb = round(random.uniform(0.2, 3.5), 1)
    usage_pct = random.randint(80, 98)
    quotas = {
        "internet_remaining_gb": rem_gb,
        "voice_remaining_minutes": random.randint(0, 50),
        "sms_remaining": random.randint(0, 100),
        "usage_percentage": {"internet": usage_pct, "voice": random.randint(60, 90), "sms": random.randint(50, 90)},
        "period_end": (datetime.now() + timedelta(days=random.randint(1,20))).isoformat()
    }
    # 2. Change Package
    change_id = f"C-{int(datetime.now().timestamp())}-{user_id}"
    to_pkg = random.choice(["Premium Paket", "Limitsiz Paket"])
    change_data = {
        "user_id": user_id,
        "change_id": change_id,
        "from_package": "Standart Paket",
        "to_package": to_pkg,
        "effective_date": datetime.now().isoformat(),
        "fee_difference": round(random.uniform(5, 25), 2),
        "status": "success"
    }
    # 3. Latest Bill
    amount = round(random.uniform(150, 600), 2)
    bill = {
        "user_id": user_id,
        "bill_id": f"F-{datetime.now().year}-{user_id}-{random.randint(1000,9999)}",
        "amount": amount,
        "currency": "TL",
        "bill_date": datetime.now().date().isoformat(),
        "due_date": (datetime.now() + timedelta(days=7)).date().isoformat(),
        "status": random.choice(["paid", "unpaid"]),
        "services": [
            {"service_name": "İnternet", "amount": round(amount * 0.7, 2)},
            {"service_name": "Ses", "amount": round(amount * 0.2, 2)},
            {"service_name": "Diğer", "amount": round(amount * 0.1, 2)}
        ]
    }

    return {
        "id": f"CMI-001-{user_id}-{int(datetime.now().timestamp())}",
        "senaryo": "usage_upgrade_bill",
        "intents": ["check_quota", "upgrade_package", "get_bill"],
        "dialogue": [
            {"rol": "kullanici", "icerik": f"Merhaba, kotam, paket yükseltme seçenekleri ve son faturamı öğrenebilir miyim? ID: {user_id}"},
            {"rol": "asistan", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": validate_response(GetRemainingQuotasResponse, quotas)},
            {"rol": "asistan", "icerik": f"Kalan kota: {rem_gb} GB (%{usage_pct}). Paket yükseltmek ister misiniz?"},
            {"rol": "kullanici", "icerik": "Evet, Limitsiz Paket'e geçmek istiyorum."},
            {"rol": "asistan", "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "to_package": to_pkg}}]},
            {"rol": "arac", "icerik": validate_response(ChangePackageResponse, change_data)},
            {"rol": "asistan", "icerik": f"Paketiniz {to_pkg} olarak güncellendi. Ücret farkı: {change_data['fee_difference']} TL."},
            {"rol": "asistan", "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": validate_response(GetCurrentBillResponse, bill)},
            {"rol": "asistan", "icerik": f"Son faturanız {amount} TL. Ödeme tarihi: {bill['due_date']}."}
        ]
    }

# =====================================================================
# Veri Kümesi Üretimi
# =====================================================================
def generate_dataset(num: int) -> list:
    # Tek bir karma senaryo; farklı varyasyonlar üretmek için
    data = []
    for _ in range(num):
        data.append(scenario_usage_and_upgrade_and_bill())
    return data

# =====================================================================
# Dosyaya Kaydetme
# =====================================================================
def save_dataset(dataset: list, path: str, jsonl: bool=False) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        if jsonl:
            for rec in dataset:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        else:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"Veri '{path}' kaydedildi.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Complex & Multi-Intent senaryo üretici')
    parser.add_argument('--num', type=int, default=500, help='Üretilecek örnek sayısı')
    parser.add_argument('--output', type=str, default='./data/complex_multi_intent.json', help='Çıktı dosyası')
    parser.add_argument('--jsonl', action='store_true', help='JSONL formatında kaydet')
    args = parser.parse_args()
    ds = generate_dataset(args.num)
    save_dataset(ds, args.output, jsonl=args.jsonl)
