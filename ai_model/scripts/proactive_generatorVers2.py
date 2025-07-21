# -*- coding: utf-8 -*-
import json
import random
import os
import argparse
from datetime import datetime
from faker import Faker
from pydantic import ValidationError

# === GÜVENLİK ADIMI: Pydantic Modelleri ===
from telekom_api_schema import (
    GetRemainingQuotasResponse,
    ChangePackageResponse,
    GetCurrentBillResponse,
    GetFaultTicketStatusResponse,
    TestInternetSpeedResponse
)

# Faker'ı Türkçe ile başlat
fake = Faker("tr_TR")

# --- Yardımcı Fonksiyonlar ---
def generate_user_id():
    """4-6 haneli rastgele kullanıcı ID"""
    return fake.random_int(min=1000, max=999999)

# --- JSON Doğrulama ---
def create_validated_json_response(model, data: dict) -> dict:
    try:
        validated = model(**data)
        return json.loads(validated.model_dump_json())
    except ValidationError as e:
        raise RuntimeError(f"Doğrulama hatası ({model.__name__}): {e}")

# =====================================================================
# PROAKTİF SENARYOLAR
# =====================================================================

def scenario_proactive_low_quota():
    user_id = generate_user_id()
    remaining_gb = round(random.uniform(0.5, 4.9), 1)
    voice_min = random.randint(0, 100)
    sms_count = random.randint(0, 200)
    usage_internet = random.randint(70, 99)
    usage_voice = random.randint(70, 99)
    usage_sms = random.randint(70, 99)
    quotas = {
        "internet_remaining_gb": remaining_gb,
        "voice_remaining_minutes": voice_min,
        "sms_remaining": sms_count,
        "usage_percentage": {"internet": usage_internet, "voice": usage_voice, "sms": usage_sms},
        "period_end": fake.future_date(end_date='+20d').isoformat()
    }
    return {
        "id": f"PRO-LOW-{user_id}-{int(datetime.now().timestamp())}",
        "senaryo": "low_quota",
        "etiketler": ["kota", "proaktif", "internet"],
        "zaman": datetime.now().isoformat(),
        "donguler": [
            {"rol": "kullanici", "icerik": f"Kota ne kadar kaldı? ID: {user_id}"},
            {"rol": "asistan", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetRemainingQuotasResponse, quotas)},
            {"rol": "asistan", "icerik": f"Kota {usage_internet}% doldu, kalan {remaining_gb} GB. Ek paket ister misiniz?"}
        ]
    }


def scenario_proactive_roaming():
    user_id = generate_user_id()
    change_id = f"C-{int(datetime.now().timestamp())}-{user_id}"
    from_pkg = "Standart Paket"
    to_pkg = "Roaming Paketi"
    effective_date = datetime.now().isoformat()
    fee_diff = round(random.uniform(-10, 50), 2)
    status = "success"
    change_data = {"user_id": user_id, "change_id": change_id, "from_package": from_pkg, "to_package": to_pkg, "effective_date": effective_date, "fee_difference": fee_diff, "status": status}
    return {
        "id": f"PRO-ROAM-{user_id}-{int(datetime.now().timestamp())}",
        "senaryo": "roaming_offer",
        "etiketler": ["roaming", "seyahat", "proaktif"],
        "zaman": datetime.now().isoformat(),
        "donguler": [
            {"rol": "kullanici", "icerik": f"{fake.country()} seyahati planlıyorum. ID: {user_id}"},
            {"rol": "asistan", "icerik": "Roaming hizmetini etkinleştireyim mi?"},
            {"rol": "kullanici", "icerik": "Evet, lütfen."},
            {"rol": "asistan", "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "to_package": to_pkg}}]},
            {"rol": "arac", "icerik": create_validated_json_response(ChangePackageResponse, change_data)},
            {"rol": "asistan", "icerik": f"{from_pkg} paketinden {to_pkg} paketine geçiş tamamlandı. Ücret farkı: {fee_diff} TL."}
        ]
    }


def scenario_proactive_high_bill():
    user_id = generate_user_id()
    amount = round(random.uniform(200, 800), 2)
    bill_id = f"F-{datetime.now().year}-{user_id}-{random.randint(1000,9999)}"
    currency = "TL"
    bill_date = datetime.now().date().isoformat()
    due_date = fake.future_date(end_date='+10d').isoformat()
    status = random.choice(["paid", "unpaid"])
    services = [{"service_name": "İnternet Paketi", "amount": round(amount*0.7,2)}, {"service_name": "Ses Paketi", "amount": round(amount*0.2,2)}, {"service_name": "Diğer Ücretler", "amount": round(amount*0.1,2)}]
    bill_data = {"user_id": user_id, "bill_id": bill_id, "amount": amount, "currency": currency, "bill_date": bill_date, "due_date": due_date, "status": status, "services": services}
    return {
        "id": f"PRO-BILL-{user_id}-{int(datetime.now().timestamp())}",
        "senaryo": "high_bill_warning",
        "etiketler": ["fatura", "uyarı", "proaktif"],
        "zaman": datetime.now().isoformat(),
        "donguler": [
            {"rol": "kullanici", "icerik": f"Fatura tutarımı öğrenebilir miyim? ID: {user_id}"},
            {"rol": "asistan", "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetCurrentBillResponse, bill_data)},
            {"rol": "asistan", "icerik": f"Faturanız {amount} {currency}. Son ödeme tarihi: {due_date}."}
        ]
    }


def scenario_proactive_fault_followup():
    user_id = generate_user_id()
    ticket_id = fake.bothify(text='TKT-####-??')
    status = random.choice(['open','in_progress','resolved'])
    resolution = fake.sentence(nb_words=6)
    created_at_dt = fake.date_time_between(start_date='-7d', end_date='now')
    created_at = created_at_dt.isoformat()
    resolved_at = fake.date_time_between(start_date=created_at_dt, end_date=datetime.now()).isoformat() if status=='resolved' else None
    technician_notes = fake.text(max_nb_chars=60)
    fault_data = {"user_id": user_id, "ticket_id": ticket_id, "status": status, "resolution": resolution, "created_at": created_at, "resolved_at": resolved_at, "technician_notes": technician_notes}
    return {
        "id": f"PRO-FAULT-{user_id}-{int(datetime.now().timestamp())}",
        "senaryo": "fault_ticket_followup",
        "etiketler": ["arıza","takip","proaktif"],
        "zaman": datetime.now().isoformat(),
        "donguler": [
            {"rol": "kullanici", "icerik": f"Arıza durumum ne? ID: {user_id}"},
            {"rol": "asistan", "arac_cagrilari": [{"fonksiyon": "get_fault_ticket_status", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetFaultTicketStatusResponse, fault_data)},
            {"rol": "asistan", "icerik": f"Bilet {ticket_id} durumu: {status}. Notlar: {technician_notes}"}
        ]
    }


def scenario_proactive_speed_test():
    user_id = generate_user_id()
    download = round(random.uniform(1,5),1)
    upload = round(random.uniform(0.2,1),1)
    ping = random.randint(20,100)
    timestamp = datetime.now().isoformat()
    server = fake.domain_name()
    quality = random.choice(["excellent","good","fair","poor"])
    speed_data = {"user_id": user_id, "download_speed_mbps": download, "upload_speed_mbps": upload, "ping_ms": ping, "test_timestamp": timestamp, "test_server": server, "quality_rating": quality}
    return {
        "id": f"PRO-SPEED-{user_id}-{int(datetime.now().timestamp())}",
        "senaryo": "speed_test_alert",
        "etiketler": ["hız","performans","proaktif"],
        "zaman": datetime.now().isoformat(),
        "donguler": [
            {"rol": "asistan","icerik": "Mevcut internet hızınızı test ediyorum..."},
            {"rol": "asistan","arac_cagrilari": [{"fonksiyon":"test_internet_speed","parametreler": {"user_id": user_id}}]},
            {"rol": "arac","icerik": create_validated_json_response(TestInternetSpeedResponse, speed_data)},
            {"rol": "asistan","icerik": f"Download: {download} Mbps, Upload: {upload} Mbps, Ping: {ping} ms, Sunucu: {server}, Durum: {quality}."}
        ]
    }


def generate_dataset(num_samples: int) -> list:
    scenario_funcs = [scenario_proactive_low_quota, scenario_proactive_roaming, scenario_proactive_high_bill, scenario_proactive_fault_followup, scenario_proactive_speed_test]
    return [random.choice(scenario_funcs)() for _ in range(num_samples)]


def save_dataset(dataset: list, output_path: str, jsonl: bool=False) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        if jsonl:
            for record in dataset:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        else:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"Veri '{output_path}' kaydedildi ({'JSONL' if jsonl else 'JSON'}).")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Proaktif senaryo veri üretici')
    parser.add_argument('--num', type=int, default=1000, help='Üretilecek örnek sayısı')
    parser.add_argument('--output', type=str, default='./data/proactive_data.json', help='Çıktı dosyası')
    parser.add_argument('--jsonl', action='store_true', help='JSONL formatında kaydet')
    args = parser.parse_args()
    ds = generate_dataset(args.num)
    save_dataset(ds, args.output, jsonl=args.jsonl)
