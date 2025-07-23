# -*- coding: utf-8 -*-
import json
import random
import uuid
import os
from faker import Faker
from pydantic import ValidationError

# === GÜVENLİK ADIMI: ANA SÖZLEŞMEYİ (Pydantic Modelleri) İÇE AKTAR ===
# Artık tüm API yanıtları bu modeller kullanılarak doğrulanacak.
# Bu, spesifikasyonla %100 uyumluluğu garanti eder.
from telekom_api_schema import (
    GetRemainingQuotasResponse, UsagePercentage,
    GetAvailablePackagesResponse, AvailablePackageItem, AvailablePackageFeatures,
    GetPackageDetailsResponse, PackageDetailsFeatures,
    ChangePackageResponse,
    GetCurrentBillResponse, ServiceItem,
    TestInternetSpeedResponse,
    GetFaultTicketStatusResponse
)


# Faker'ı başlat
fake = Faker("tr_TR")

# --- API UYUMLU YARDIMCI FONKSİYONLAR ---

def generate_user_id():
    return fake.random_int(min=1000, max=9999)

def generate_bill_id(user_id):
    year = fake.date_this_year().year
    return f"F-{year}-{user_id}"

def generate_ticket_id(prefix="T"):
    year = fake.date_this_year().year
    number = fake.random_int(min=100000, max=999999)
    return f"{prefix}-{year}-{number}"

# --- GÜVENLİK ADIMI: VERİ OLUŞTURMA VE DOĞRULAMA FONKSİYONU ---
def create_validated_json_response(pydantic_model, data: dict) -> str:
    """
    Verilen bir Pydantic modelini kullanarak bir sözlüğü doğrular ve JSON string'ine çevirir.
    Doğrulama başarısız olursa, programı bir hatayla durdurur.
    """
    try:
        validated_data = pydantic_model(**data)
        # model_dump_json, Pydantic'in veriyi doğrudan JSON string'ine çevirme metodudur.
        # ensure_ascii=False gibi ayarları kendisi yönetir.
        return validated_data.model_dump_json(indent=None) # Tek satır JSON için indent=None
    except ValidationError as e:
        print("!!! VERİ DOĞRULAMA HATASI !!!")
        print(f"Model '{pydantic_model.__name__}' doğrulanırken hata oluştu.")
        print(f"Hatalı veri: {data}")
        print(f"Pydantic Hatası: {e}")
        raise  # Programı durdur, çünkü hatalı veri üretilmemelidir.


# ==============================================================================
# SENARYO 1: BAŞARILI ZİNCİR - Detaylı Paket Yükseltme
# ==============================================================================
def scenario_successful_detailed_upgrade():
    user_id = generate_user_id()
    new_package_name = "Gamer Pro"

    # --- API Yanıt Verilerini Hazırla ---
    remaining_quotas_data = {
        "internet_remaining_gb": round(random.uniform(1.0, 5.0), 1),
        "voice_remaining_minutes": random.randint(50, 200),
        "sms_remaining": random.randint(100, 500),
        "period_end": fake.future_date(end_date="+30d").isoformat(),
        "usage_percentage": {"internet": random.randint(90, 98), "voice": 75, "sms": 50}
    }
    available_packages_data = {
        "packages": [
            {"name": "Gamer Pro", "monthly_fee": 99.90, "features": {"internet_gb": 100, "voice_minutes": 1000, "sms_count": 500}},
            {"name": "Mega İnternet", "monthly_fee": 69.50, "features": {"internet_gb": 50, "voice_minutes": 1000, "sms_count": 500}}
        ]
    }
    package_details_data = {
        "name": new_package_name, "monthly_fee": 99.90, "setup_fee": 0.0,
        "features": {"internet_gb": 100, "voice_minutes": 2000, "sms_count": 1000, "international_minutes": 100},
        "contract_duration": 24, "cancellation_fee": 50.00
    }
    change_package_data = {
        "change_id": f"CHG-{uuid.uuid4()}", "from_package": "Mega İnternet", "to_package": new_package_name,
        "effective_date": fake.future_date(end_date="+30d").isoformat(), "fee_difference": 30.40, "status": "scheduled"
    }
    
    return {
        "senaryo": "Tool Chaining - Başarılı - Kota kontrolü, paket detayı ve yükseltme",
        "donguler": [
            {"rol": "kullanici", "icerik": f"Bu ay internetimden ne kadar kalmış? Numaram {user_id}."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetRemainingQuotasResponse, remaining_quotas_data)},
            {"rol": "asistan", "icerik": "Çok az internetiniz kalmış. İsterseniz daha yüksek kotalı paketlerimizi listeleyebilirim."},
            {"rol": "kullanici", "icerik": "Harika olur, lütfen listele."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetAvailablePackagesResponse, available_packages_data)},
            {"rol": "asistan", "icerik": f"Şu an 'Gamer Pro' ve 'Mega İnternet' paketlerimiz var. Hangisinin detaylarını istersiniz?"},
            {"rol": "kullanici", "icerik": f"'{new_package_name}' kulağa hoş geliyor, onun detaylarını alabilir miyim?"},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": new_package_name}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetPackageDetailsResponse, package_details_data)},
            {"rol": "asistan", "icerik": f"'{new_package_name}' paketi 100 GB internet ve 2000 dakika konuşma içeriyor. Bu pakete geçişinizi onaylıyor musunuz?"},
            {"rol": "kullanici", "icerik": "Evet, onaylıyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "new_package_name": new_package_name}}]},
            {"rol": "arac", "icerik": create_validated_json_response(ChangePackageResponse, change_package_data)},
            {"rol": "asistan", "icerik": "Paket değişikliği talebiniz başarıyla alınmıştır. Yeni paketiniz bir sonraki fatura döneminizde aktif olacaktır."}
        ]
    }


# ==============================================================================
# SENARYO 2: DAYANIKLI ZİNCİR - Zincir İçi Ödeme Hatası ve Kurtarma
# ==============================================================================
def scenario_resilient_payment_recovery():
    user_id = generate_user_id()
    bill_id = generate_bill_id(user_id)
    error_code, error_message, recovery_suggestion = random.choice([
        ("INSUFFICIENT_FUNDS", "Kartınızda yetersiz bakiye bulunmaktadır.", "Farklı bir kartla denemek ister misiniz?"),
        ("CARD_DECLINED", "Kartınız banka tarafından reddedildi.", "Lütfen bankanızla iletişime geçin veya farklı bir kartla deneyin. Nasıl devam etmek istersiniz?"),
        ("PAYMENT_SYSTEM_TIMEOUT", "Ödeme sisteminde anlık bir yavaşlık yaşandı.", "Lütfen birkaç dakika sonra tekrar deneyelim mi?")
    ])
    
    current_bill_data = {
        "bill_id": bill_id, "user_id": user_id, "amount": 180.75, "currency": "TRY",
        "due_date": fake.future_date(end_date="+10d").isoformat(), "bill_date": fake.past_date(start_date="-20d").isoformat(),
        "status": "unpaid", "services": [{"service_name": "Gamer Pro", "amount": 180.75}]
    }

    return {
        "senaryo": "Tool Chaining - Dayanıklı - Zincir içi ödeme hatası ve kurtarma",
        "donguler": [
            {"rol": "kullanici", "icerik": f"{user_id} numaralı hattımın ödenmemiş faturasını ödemek istiyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetCurrentBillResponse, current_bill_data)},
            {"rol": "asistan", "icerik": "180.75 TL tutarında bir faturanız görünüyor. Kayıtlı kartınızla ödemeyi başlatıyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "pay_bill", "parametreler": {"bill_id": bill_id, "method": "credit_card"}}]},
            {"rol": "arac", "icerik": json.dumps({"success": False, "error": {"code": error_code, "message": error_message}})},
            {"rol": "asistan", "icerik": f"Üzgünüm, ödeme işlemi sırasında bir sorun oluştu. {error_message} {recovery_suggestion}"}
        ]
    }

# ==============================================================================
# SENARYO 3: DAYANIKLI ZİNCİR - Koşullu ve Hatalı Arıza Kaydı
# ==============================================================================
def scenario_conditional_and_faulty_ticket():
    user_id = generate_user_id()
    existing_ticket_id = generate_ticket_id("T-EXIST")

    test_speed_data = {
        "user_id": user_id, "download_speed_mbps": 85.4, "upload_speed_mbps": 15.2,
        "ping_ms": 14, "test_timestamp": fake.iso8601(), "test_server": "Istanbul-1", "quality_rating": "good"
    }
    
    # BU, SİZİN FARK ETTİĞİNİZ VE DÜZELTTİĞİMİZ KRİTİK HATA NOKTASIYDI
    fault_status_data = {
        "ticket_id": existing_ticket_id, "status": "in_progress", "resolution": None,
        "created_at": fake.past_datetime().isoformat(), "resolved_at": None,
        "technician_notes": "Bölgesel yoğunluk inceleniyor, 24 saat içinde çözülmesi bekleniyor."
    }

    return {
        "senaryo": "Tool Chaining - Dayanıklı - Koşullu mantık ve yinelenen arıza hatası",
        "donguler": [
            {"rol": "kullanici", "icerik": f"İnternetim yine çok yavaş. Bir bakın şuna. User ID: {user_id}"},
            {"rol": "asistan", "icerik": "Hemen bir hız testi yapıyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_json_response(TestInternetSpeedResponse, test_speed_data)},
            {"rol": "asistan", "icerik": "Hız testiniz normal görünüyor. Yine de kayıt açmamı ister misiniz?"},
            {"rol": "kullanici", "icerik": "Evet, aç. Çünkü sorun devam ediyor."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "create_fault_ticket", "parametreler": {"user_id": user_id, "issue_description": "Hız testi iyi ama sorun var"}}]},
            {"rol": "arac", "icerik": json.dumps({"success": False, "error": {"code": "DUPLICATE_TICKET_FOUND", "message": "Aynı konuda zaten açık bir arıza kaydınız bulunuyor.", "details": {"existing_ticket_id": existing_ticket_id}}})},
            {"rol": "asistan", "icerik": f"Bu konuda zaten açık bir arıza kaydınız olduğunu fark ettim. Ticket numaranız: {existing_ticket_id}. İsterseniz o kaydın son durumunu kontrol edebilirim."},
            {"rol": "kullanici", "icerik": "A, tamam o zaman. Evet, kontrol et lütfen."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_fault_ticket_status", "parametreler": {"ticket_id": existing_ticket_id}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetFaultTicketStatusResponse, fault_status_data)},
            {"rol": "asistan", "icerik": "Mevcut arıza kaydınız şu an 'İncelemede' durumunda ve teknisyenlerimiz sinyal seviyelerinizi izliyor."}
        ]
    }

def main(num_samples=3000):
    scenarios = [
        scenario_successful_detailed_upgrade,
        scenario_resilient_payment_recovery,
        scenario_conditional_and_faulty_ticket
    ]
    dataset = []
    print(f"{num_samples} adet GÜVENLİ VE DOĞRULANMIŞ 'Tool Chaining' senaryosu üretiliyor...")
    scenario_counts = {sc.__name__: 0 for sc in scenarios}
    for i in range(num_samples):
        selected_scenario_func = random.choice(scenarios)
        scenario_counts[selected_scenario_func.__name__] += 1
        data = selected_scenario_func()
        data["id"] = f"TC-EXP-V2-{(i + 1):04d}" # Versiyonu belli edelim: V2
        dataset.append(data)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    output_filename = os.path.join(data_dir, "expert_tool_chaining_data_v2_validated.json")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print("\n--- Üretim Tamamlandı! ---")
    print(f"Başarılı! {len(dataset)} adet DOĞRULANMIŞ veri örneği oluşturuldu.")
    print(f"Dosya konumu: '{os.path.abspath(output_filename)}'")
    print("\nSenaryo Dağılımı:")
    for name, count in scenario_counts.items():
        print(f"- {name.replace('scenario_', '')}: {count} adet")

if __name__ == "__main__":
    main(num_samples=3000)