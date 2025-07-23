# -*- coding: utf-8 -*-
import json
import random
import uuid
import os
from faker import Faker
from pydantic import ValidationError

# === ANA SÖZLEŞMEYİ (Pydantic Modelleri) İÇE AKTAR ===
from telekom_api_schema import (
    GetAvailablePackagesResponse, AvailablePackageItem, AvailablePackageFeatures,
    GetPackageDetailsResponse, PackageDetailsFeatures,
    GetCurrentBillResponse, ServiceItem,
    GetPastBillsResponse, PastBillItem,
    ChangePackageResponse
)

# Faker'ı başlat
fake = Faker("tr_TR")

# ==============================================================================
# ADIM 1: DUYGUSAL VE DİLSEL ÇEŞİTLİLİK BANKASI
# ==============================================================================

# Farklı kullanıcı ruh hallerini ve konuşma tarzlarını temsil eden ifade havuzları
TONES = {
    "angry": [
        "Faturam yine kazık gibi gelmiş, dalga mı geçiyorsunuz?!",
        "Bu internet sürekli kesiliyor, çıldırmak üzereyim! Acil bir çözüm bulun!",
        "Beni 'Süpersonik' pakete geçirecektiniz, neden hala olmadı? Bu ne sorumsuzluk!",
        "Hala bir çözüm bulamadınız mı? Kaç saattir bekliyorum, işim gücüm var benim!"
    ],
    "confused": [
        "Merhaba, faturamda anlamadığım bir kalem var, 'cihaz bedeli' diyor ama ben yeni cihaz almadım ki...",
        "Paketimi değiştirmek istiyorum ama hangisinin bana uygun olduğundan emin değilim, çok karışık görünüyorlar.",
        "Bir SMS geldi ama tam olarak ne anlama geldiğini çözemedim, 'tarife taahhüdünüz yenileniyor' diyor?",
        "Ben şimdi yurt dışına çıkacağım, roaming mi açtırmam gerekiyor yoksa başka bir şey mi?"
    ],
    "impatient": [
        "Acil internet paketine ihtiyacım var, en hızlısından hangisiyse ona geçirin beni hemen.",
        "Tamam tamam, anladım özellikleri. Hemen o 'Gamer Pro'ya geçiş yapalım, vaktim yok.",
        "Sonuç ne oldu? Faturamı kontrol ettiniz mi? Daha ne kadar bekleyeceğim?",
        "Listeyi gördüm, en çok internet hangisindeyse onu istiyorum, detaylarla uğraşamam."
    ],
    "neutral": [
        "Mevcut tarifemi değiştirmek istiyorum.",
        "Faturam hakkında bilgi alabilir miyim?",
        "Paket seçeneklerini listeleyebilir misiniz?"
    ]
}

# Asistanın bu tonlara uygun yanıt vermesi için yatıştırıcı/yönlendirici ifade havuzları
ASSISTANT_RESPONSES = {
    "deescalate_angry": "Yaşadığınız olumsuz deneyim için gerçekten üzgünüm. Durumu hemen inceleyip size net bir açıklama sunacağım.",
    "clarify_confused": "Elbette, bu tür konular kafa karıştırıcı olabilir. Adım adım ilerleyerek durumu açıklığa kavuşturalım.",
    "accelerate_impatient": "Tabii ki, hemen işleminizi hızlandırıyorum. Vaktinizi almadan en hızlı çözümü sunacağım.",
    "neutral": "Elbette, yardımcı olabilirim."
}


# --- API UYUMLU YARDIMCI FONKSİYONLAR ---
def generate_user_id():
    return fake.random_int(min=1000, max=9999)

def generate_bill_id(user_id):
    return f"F-{fake.date_this_year().year}-{user_id}"

# --- GÜVENLİK ADIMI: VERİ OLUŞTURMA VE DOĞRULAMA FONKSİYONU ---
def create_validated_json_response(pydantic_model, data: dict) -> str:
    try:
        validated_data = pydantic_model(**data)
        return validated_data.model_dump_json(indent=None)
    except ValidationError as e:
        print(f"!!! VERİ DOĞRULAMA HATASI: Model '{pydantic_model.__name__}' !!!\nHatalı veri: {data}\nPydantic Hatası: {e}")
        raise

# ==============================================================================
# "OLAĞANÜSTÜ SEVİYE" SENARYOLAR
# ==============================================================================

def scenario_clarify_by_presenting_options():
    # Bu senaryo artık farklı tonlarda başlayabilir
    tone = random.choice(["neutral", "confused"])
    user_id = generate_user_id()
    
    initial_user_query = "Daha fazla internet içeren bir pakete geçmek istiyorum."
    if tone == "confused":
        initial_user_query = random.choice(TONES["confused"])

    available_packages_data = { "packages": [ {"name": "Sosyal Medya Uzmanı", "monthly_fee": 75.0, "features": {"internet_gb": 75, "voice_minutes": 750, "sms_count": 500}}, {"name": "Gamer Pro", "monthly_fee": 99.9, "features": {"internet_gb": 100, "voice_minutes": 1000, "sms_count": 500}} ]}
    package_details_data = { "name": "Gamer Pro", "monthly_fee": 99.9, "setup_fee": 0.0, "features": {"internet_gb": 100, "voice_minutes": 2000, "sms_count": 1000, "international_minutes": 100}, "contract_duration": 12, "cancellation_fee": 40.0}

    return {
        "senaryo": f"Disambiguation - Seçenek Sunma ({tone})",
        "donguler": [
            {"rol": "kullanici", "icerik": initial_user_query},
            {"rol": "asistan", "icerik": f"{ASSISTANT_RESPONSES['clarify_confused' if tone == 'confused' else 'neutral']} Size en uygun paketi bulmak için mevcut seçenekleri hemen listeliyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetAvailablePackagesResponse, available_packages_data)},
            {"rol": "asistan", "icerik": "Şu an 'Sosyal Medya Uzmanı' (75 GB) ve 'Gamer Pro' (100 GB) seçeneklerimiz var. Hangisini incelemek istersiniz?"},
        ]
    }


def scenario_long_and_winding_road():
    """
    Bu senaryo, belirttiğimiz tüm eksiklikleri hedefler:
    1. Duygusal Ton (Sinirli başlar)
    2. Öngörülemeyen Akış (Kullanıcı konuyu değiştirir)
    3. Çok Adımlı Çözüm (Diyalog uzar ve esneklik gerektirir)
    """
    user_id = generate_user_id()
    past_bill_id = generate_bill_id(user_id)
    package_to_change = "Gamer Pro"

    # API Yanıt Verileri
    available_packages_data = { "packages": [ {"name": "Sosyal Medya Uzmanı", "monthly_fee": 75.0, "features": {"internet_gb": 75, "voice_minutes": 750, "sms_count": 500}}, {"name": package_to_change, "monthly_fee": 99.9, "features": {"internet_gb": 100, "voice_minutes": 1000, "sms_count": 500}} ]}
    past_bills_data = { "bills": [ {"bill_id": past_bill_id, "amount": 142.50, "bill_date": fake.past_date().isoformat(), "status": "paid", "paid_date": fake.past_date().isoformat()} ], "total_count": 1, "total_amount_paid": 142.50}
    change_package_data = { "change_id": f"CHG-{uuid.uuid4()}", "from_package": "Eski Paket", "to_package": package_to_change, "effective_date": fake.future_date().isoformat(), "fee_difference": 24.90, "status": "scheduled"}

    return {
        "senaryo": "Disambiguation - Uzun, duygusal ve dallanan diyalog",
        "donguler": [
            # 1. Adım: Sinirli ve belirsiz başlangıç
            {"rol": "kullanici", "icerik": random.choice(TONES["angry"])},
            # 2. Adım: Asistan yatıştırır ve konuyu netleştirmeye çalışır
            {"rol": "asistan", "icerik": f"{ASSISTANT_RESPONSES['deescalate_angry']} Paket seçeneklerinizi kontrol ediyorum ki size daha iyi bir çözüm sunabileyim."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetAvailablePackagesResponse, available_packages_data)},
            {"rol": "asistan", "icerik": "Şu an geçebileceğiniz 'Sosyal Medya Uzmanı' ve 'Gamer Pro' paketleri mevcut."},
            # 3. Adım: Kullanıcı konuyu aniden değiştirir (Öngörülemeyen Akış)
            {"rol": "kullanici", "icerik": "Bir dakika ya, aklıma takıldı. Benim geçen ayki faturam ne kadar gelmişti?"},
            # 4. Adım: Asistan esneklik gösterir ve yan görevi yapar
            {"rol": "asistan", "icerik": "Elbette, hemen kontrol ediyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 1}}]},
            {"rol": "arac", "icerik": create_validated_json_response(GetPastBillsResponse, past_bills_data)},
            # 5. Adım: Asistan yan görevi tamamlar ve ana konuya geri döner
            {"rol": "asistan", "icerik": f"Geçen ayki faturanız {past_bills_data['bills'][0]['amount']} TL olarak ödenmiş görünüyor. Şimdi paket değişikliği konusuna geri dönebilir miyiz?"},
            # 6. Adım: Kullanıcı ana konuya döner ve net bir istekte bulunur
            {"rol": "kullanici", "icerik": f"Evet, tamam. Bana o '{package_to_change}' paketini ayarla lütfen."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "new_package_name": package_to_change}}]},
            {"rol": "arac", "icerik": create_validated_json_response(ChangePackageResponse, change_package_data)},
            {"rol": "asistan", "icerik": "Harika. Talebiniz alınmıştır. Yeni paketiniz bir sonraki fatura döneminde aktif olacaktır."}
        ]
    }


def main(num_samples=2000):
    # Senaryo havuzunu ve ağırlıklarını belirliyoruz.
    # "Olağanüstü" senaryonun daha sık çıkmasını sağlayarak modele daha değerli örnekler sunuyoruz.
    scenario_pool = [
        (scenario_clarify_by_presenting_options, 3), # Normal senaryo ağırlığı
        (scenario_long_and_winding_road, 7),        # "Olağanüstü" senaryo ağırlığı
    ]
    
    # Ağırlıklara göre senaryo listesi oluştur
    scenarios = []
    for func, weight in scenario_pool:
        scenarios.extend([func] * weight)

    dataset = []
    print(f"{num_samples} adet OLAĞANÜSTÜ SEVİYE 'Disambiguation' senaryosu üretiliyor...")
    
    scenario_counts = {sc[0].__name__: 0 for sc in scenario_pool}

    for i in range(num_samples):
        selected_scenario_func = random.choice(scenarios)
        scenario_counts[selected_scenario_func.__name__] += 1
        data = selected_scenario_func()
        data["id"] = f"DA-ULTRA-V1-{(i + 1):04d}" # ID'yi "ULTRA" olarak güncelledik
        dataset.append(data)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    output_filename = os.path.join(data_dir, "ultra_disambiguation_data_v1_validated.json")

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print("\n--- Üretim Tamamlandı! ---")
    print(f"Başarılı! {len(dataset)} adet DOĞRULANMIŞ veri örneği oluşturuldu.")
    print(f"Dosya konumu: '{os.path.abspath(output_filename)}'")
    print("\nSenaryo Dağılımı:")
    total = sum(scenario_counts.values())
    for name, count in scenario_counts.items():
        percentage = (count / total) * 100
        print(f"- {name.replace('scenario_', '')}: {count} adet (~{percentage:.1f}%)")

if __name__ == "__main__":
    main(num_samples=2000) 