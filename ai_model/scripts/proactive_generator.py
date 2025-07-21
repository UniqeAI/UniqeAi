# -*- coding: utf-8 -*-
import json
import random
import uuid
import os
from faker import Faker

# Faker'ı Türkçe yerelleştirme ile başlat
fake = Faker("tr_TR")

# --- Yardımcı Fonksiyonlar ---

def generate_user_id():
    """Rastgele bir kullanıcı ID'si oluşturur."""
    return fake.random_int(min=7000, max=9999)

# ==============================================================================
# SENARYO 1: PROAKTİF YARDIM - DÜŞÜK KOTA TESPİTİ VE EK PAKET ÖNERİSİ
# Amaç: Model, kullanıcının kotasını kontrol eder, düşük olduğunu anlar ve
# proaktif olarak bir çözüm (ek paket veya tarife yükseltme) sunar.
# ==============================================================================
def scenario_proactive_low_quota():
    """
    Kullanıcının internet kotasının azaldığı ve asistanın proaktif olarak
    ek paket önerdiği bir diyalog senaryosu oluşturur.
    """
    user_id = generate_user_id()
    remaining_gb = round(random.uniform(0.5, 4.9), 1)
    usage_percentage = random.randint(91, 99)

    # API Yanıt Verisini Hazırla (get_remaining_quotas)
    # Bu JSON, "arac" rolünün döndüreceği çıktıdır.
    get_remaining_quotas_response = {
        "success": True,
        "data": {
            "internet_remaining_gb": remaining_gb,
            "usage_percentage": {
                "internet": usage_percentage
            },
            "period_end": fake.future_date(end_date="+20d").isoformat()
        }
    }

    # Kullanıcının sorabileceği farklı başlangıç cümleleri
    user_prompts = [
        f"İnternet paketimden ne kadar kalmış öğrenebilir miyim? Müşteri no: {user_id}",
        f"Merhaba, {user_id} için kalan internetimi söyler misin?",
        f"Ay sonuna daha çok var, internetim ne kadar kalmış? (ID: {user_id})",
        f"Güncel internet kullanımımı kontrol eder misin? Numaram {user_id}."
    ]

    # Asistanın proaktif olarak sunabileceği farklı öneriler
    assistant_suggestions = [
        f"İnternet paketinizin %{usage_percentage}'sini kullanmışsınız ve sadece {remaining_gb} GB kalmış. Ay sonuna doğru internetinizin bitmemesi için günlük veya haftalık ek paketlerimizi incelemek ister misiniz?",
        f"Sadece {remaining_gb} GB internetiniz kalmış görünüyor. Bu ay internetsiz kalmamanız için size özel indirimli ek paketlerimizi listeyebilirim. Ne dersiniz?",
        f"Paketinizin neredeyse tamamını ({usage_percentage}%) kullanmışsınız. Dilerseniz mevcut tarifenizi daha yüksek kotalı bir seçenekle değiştirebiliriz. İlgilenir misiniz?"
    ]

    return {
        "senaryo": "Proactive - Kalan kota az, model ek paket önerir",
        "donguler": [
            {
                "rol": "kullanici",
                "icerik": random.choice(user_prompts)
            },
            {
                "rol": "asistan",
                "icerik": None,
                "arac_cagrilari": [{
                    "fonksiyon": "get_remaining_quotas",
                    "parametreler": {"user_id": user_id}
                }]
            },
            {
                "rol": "arac",
                "icerik": json.dumps(get_remaining_quotas_response, ensure_ascii=False)
            },
            {
                "rol": "asistan",
                "icerik": random.choice(assistant_suggestions)
            }
        ]
    }

# ==============================================================================
# SENARYO 2: PROAKTİF YARDIM - YURT DIŞI SEYAHATİ VE ROAMING TEKLİFİ
# Amaç: Model, kullanıcının yurt dışına çıkacağını ifade eden bir cümlesini
# yakalar ve ilgili hizmeti (roaming) proaktif olarak teklif eder.
# ==============================================================================
def scenario_proactive_roaming():
    """
    Kullanıcının yurt dışına seyahat edeceğini belirtmesi üzerine asistanın
    proaktif olarak roaming hizmetini etkinleştirmeyi teklif ettiği bir senaryo oluşturur.
    """
    user_id = generate_user_id()
    country = fake.country()
    daily_fee = round(random.uniform(20.0, 50.0), 2)

    # API Yanıt Verisini Hazırla (enable_roaming)
    enable_roaming_response = {
        "success": True,
        "data": {
            "user_id": user_id,
            "roaming_enabled": True,
            "daily_fee": daily_fee
        }
    }

    # Kullanıcının seyahat planını belirtebileceği farklı yollar
    user_prompts = [
        f"Merhaba, haftaya {country}'ya bir iş seyahatim olacak. Hattımla ilgili bir hazırlık yapmalı mıyım? ID: {user_id}",
        f"Ben {user_id}, {country}'ya tatile gidiyorum da hattımı orada kullanabilir miyim?",
        f"Yarın {country} yolcusuyum, telefonumu yurt dışında kullanmak için ne yapmam lazım?",
        f"Hattımı yurt dışı kullanımına açtırmak istiyorum, {country}'ya gideceğim. user_id={user_id}"
    ]
    
    # Asistanın yanıtları
    assistant_initial_response = "Harika bir seyahat dilerim! Yurt dışında hattınızı sorunsuzca kullanabilmeniz için 'roaming' yani yurt dışı kullanım hizmetini aktif etmeniz gerekiyor. Sizin için bu hizmeti şimdi etkinleştirmemi ister misiniz?"
    assistant_confirmation_response = f"Yurt dışı kullanım hizmetiniz (roaming) başarıyla aktif edilmiştir. Güncel günlük kullanım ücreti {daily_fee:.2f} TL'dir. İyi yolculuklar!"

    return {
        "senaryo": "Proactive - Kullanıcı yurt dışına çıkacağını söyler, model roaming açmayı teklif eder",
        "donguler": [
            {
                "rol": "kullanici",
                "icerik": random.choice(user_prompts)
            },
            {
                "rol": "asistan",
                "icerik": assistant_initial_response
            },
            {
                "rol": "kullanici",
                "icerik": random.choice(["Evet, lütfen etkinleştirin.", "Tabii, yapalım.", "Evet, açalım lütfen."])
            },
            {
                "rol": "asistan",
                "icerik": None,
                "arac_cagrilari": [{
                    "fonksiyon": "enable_roaming",
                    "parametreler": {"user_id": user_id, "status": True}
                }]
            },
            {
                "rol": "arac",
                "icerik": json.dumps(enable_roaming_response, ensure_ascii=False)
            },
            {
                "rol": "asistan",
                "icerik": assistant_confirmation_response
            }
        ]
    }


def main(num_samples=1000):
    """
    Belirtilen sayıda senaryo üreterek bir JSON dosyasına kaydeder.
    """
    # Üretilecek senaryo fonksiyonlarını bir listede topla
    scenarios = [
        scenario_proactive_low_quota,
        scenario_proactive_roaming
    ]
    dataset = []
    
    print(f"{num_samples} adet 'Proaktif Yardım' senaryosu üretiliyor...")
    
    # Her senaryonun kaç kez üretildiğini saymak için bir sayaç
    scenario_counts = {sc.__name__: 0 for sc in scenarios}

    for i in range(num_samples):
        # Listeden rastgele bir senaryo üretme fonksiyonu seç
        selected_scenario_func = random.choice(scenarios)
        scenario_counts[selected_scenario_func.__name__] += 1
        
        # Seçilen fonksiyonu çağırarak senaryo verisini al
        data = selected_scenario_func()
        
        # Her senaryoya benzersiz bir ID ata
        data["id"] = f"PA-V1-{(i + 1):04d}"
        dataset.append(data)

    # Betiğin bulunduğu dizine veriyi kaydet
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, "proactive_assistance_data_end.json")

    # Veri setini JSON dosyasına yaz
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print("\n--- Üretim Tamamlandı! ---")
    print(f"Başarılı! {len(dataset)} adet veri örneği oluşturuldu.")
    print(f"Dosya konumu: '{os.path.abspath(output_filename)}'")
    print("\nSenaryo Dağılımı:")
    for name, count in scenario_counts.items():
        print(f"- {name.replace('scenario_', '')}: {count} adet")

if __name__ == "__main__":
    main(num_samples=1000)