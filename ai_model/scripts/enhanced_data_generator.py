# -*- coding: utf-8 -*-
"""
Enhanced Data Generator (v2) for EH and NC Strategies

This script generates high-quality, diverse training data for:
- Strategy 4: Error Handling (EH)
- Strategy 6: Natural Chit-Chat (NC)

It addresses the limitations of the previous generator by:
1.  Using "response pools" to increase variety.
2.  Generating multi-turn dialogues for more natural conversations.
3.  Diversifying user requests and assistant interim phrases.
"""
import json
import random
import os

# ==============================================================================
# 🎯 [CORE IMPROVEMENT] DATA POOLS FOR DIVERSITY
# ==============================================================================

ASSISTANT_INTERIM_PHRASES = [
    "Hemen işleminizi gerçekleştiriyorum.",
    "Elbette, kontrol ediyorum.",
    "Tabii, isteğinizi işleme alıyorum.",
    "Bir saniye, bilgileri getiriyorum.",
    "Hay hay, sistemden sorguluyorum.",
    "Hemen bakıyorum.",
    "İsteğiniz üzerine kontrol sağlıyorum."
]

# --- ERROR HANDLING (EH) POOLS ---

ERROR_HANDLING_SCENARIOS = {
    "BILL_NOT_FOUND": {
        "function": "pay_bill",
        "user_requests": [
            "F-2024-{bill_id} numaralı faturamı ödemek istiyorum.",
            "Merhaba, {bill_id} ID'li faturayı kapatabilir miyiz?",
            "Acil şu {bill_id} nolu faturayı ödemem lazım."
        ],
        "assistant_responses": [
            "Üzgünüm, belirttiğiniz fatura numarasını sistemde bulamadım ya da bu fatura daha önceden ödenmiş olabilir. Lütfen fatura numarasını kontrol eder misiniz?",
            "Bu fatura numarasıyla eşleşen bir kayıt bulamadım. Numaranın doğru olduğundan emin misiniz? Dilerseniz güncel borcunuzu sorgulayabilirim.",
            "Sistemlerimizde bu faturayı göremedim. Belki de ödemesi çoktan yapılmıştır. Farklı bir fatura numarası denemek ister misiniz?"
        ]
    },
    "INELIGIBLE_FOR_PACKAGE": {
        "function": "change_package",
        "user_requests": [
            "Beni '{package_name}' tarifesine geçirir misin? User ID {user_id}",
            "Selam, {package_name} kampanyasından yararlanmak istiyorum. Müşteri no: {user_id}",
            "Acilen '{package_name}' paketine geçmem gerekiyor. ID'm {user_id}."
        ],
        "assistant_responses": [
            "Anladığım kadarıyla '{package_name}' tarifesi, belirli bir meslek grubuna özel olduğu için şu anki aboneliğinizle bu pakete geçiş yapamıyorsunuz. Size özel olarak geçebileceğiniz diğer kampanyalı paketleri listelememi ister misiniz?",
            "Maalesef '{package_name}' paketine geçiş için uygun görünmüyorsunuz. Bu kampanya belirli kriterlere sahip müşterilerimiz için geçerlidir. Size uygun diğer popüler paketlerimizi göstermemi ister misiniz?",
            "Sistem, '{package_name}' paketine geçişinize izin vermiyor. Genellikle bu durum, kampanya koşullarını karşılamadığınızda olur. Sizin için uygun güncel kampanyaları kontrol edebilirim."
        ]
    },
    "INSUFFICIENT_FUNDS": {
        "function": "pay_bill",
        "user_requests": [
            "Kartımla faturamı ödemek istiyorum. User ID {user_id}",
            "Güncel borcumu online ödeyebilir miyim? User ID: {user_id}",
            "Lütfen faturamı çekin. {user_id}"
        ],
        "assistant_responses": [
            "Kartınızda yetersiz bakiye bulunuyor. Farklı bir ödeme yöntemi kullanmak ister misiniz?",
            "Görünüşe göre kartınızın limiti bu işlem için yeterli değil. Başka bir kartla denemeye ne dersiniz?",
            "Ödeme, yetersiz bakiye nedeniyle tamamlanamadı. Dilerseniz banka havalesi seçeneğini değerlendirebiliriz."
        ]
    },
    "INVALID_USER": {
        "function": "get_customer_package",
        "user_requests": [
            "Mevcut paketimi kontrol eder misin? User ID {user_id}",
            "Paket detaylarımı öğrenmek istiyorum. ID {user_id}",
            "{user_id} nolu müşterinin paket bilgisi nedir?"
        ],
        "assistant_responses": [
            "Sistemde bu kullanıcı ID'sine ait bir kayıt bulamadım. Lütfen müşteri numaranızı kontrol eder misiniz?",
            "Girdiğiniz müşteri numarası sistemlerimizde bulunamadı. Numaranın doğru olduğundan emin misiniz?",
            "Bu ID ile bir müşteri bulamadım. Lütfen tekrar dener misiniz?"
        ]
    }
}

# --- NATURAL CHIT-CHAT (NC) POOLS ---

NATURAL_CHAT_SCENARIOS = {
    "genel_bilgi": {
        "user": [
            "Bu faturalar neden hep bu kadar karışık oluyor?",
            "Roaming tam olarak nasıl çalışıyor?",
            "Otomatik ödeme talimatı vermek güvenli mi?"
        ],
        "assistant": [
            "Fatura detaylarının bazen kafa karıştırıcı olabildiğinin farkındayım. Genellikle ana hizmet bedeli, vergiler ve ek kullanımlar içerdiği için karmaşık görünebilir.",
            "Roaming hizmetimiz, yurt dışında kendi hattınızı kullanmanızı sağlar. Genellikle günlük veya haftalık paketlerle ücretlendirilir. Hangi ülkeye gideceğinize göre seçenekler değişebilir.",
            "Evet, otomatik ödeme son derece güvenlidir. Bankanızla aramızdaki şifreli bağlantılar üzerinden çalışır ve fatura takibi derdinden kurtarır."
        ]
    },
    "tesekkur": {
        "user": [
            "Teşekkür ederim, sorunum çözüldü.",
            "Sağ ol, yardımın için teşekkürler.",
            "Harika, tam istediğim gibi oldu."
        ],
        "assistant": [
            "Rica ederim, yardımcı olabildiğime sevindim! Başka bir konuda yardıma ihtiyacınız olursa çekinmeden tekrar ulaşabilirsiniz.",
            "Ne demek, görevimiz! Memnun kalmanıza çok sevindim. İyi günler dilerim!",
            "Harika! Sorununuzun çözüldüğünü duymak güzel. Telekom'u tercih ettiğiniz için teşekkür ederiz."
        ]
    },
    "multi_turn_complaint": {
        "turns": [
            {"rol": "kullanici", "icerik": "İnternet hızım yine yerlerde sürünüyor, bıktım artık!"},
            {"rol": "asistan", "icerik": "Yaşadığınız sorundan dolayı gerçekten üzgünüm. Hız sorunlarının ne kadar can sıkıcı olabildiğini biliyorum. Sorunu daha iyi anlayabilmek için, bu yavaşlığı günün belirli saatlerinde mi yoksa sürekli mi yaşıyorsunuz?"},
            {"rol": "kullanici", "icerik": "Genellikle akşam saatlerinde oluyor."},
            {"rol": "asistan", "icerik": "Anladım, bu bilgi çok değerli. Akşam saatlerindeki yoğunluk bazen bölgesel yavaşlamalara neden olabiliyor. Sizin için hemen bir hat kontrolü başlatıp durumu detaylıca inceleyebilirim. Uygun mudur?"}
        ]
    }
}


# ==============================================================================
# 🚀 ENHANCED GENERATOR FUNCTIONS
# ==============================================================================

def generate_eh_data_v2(count=1000):
    """Generates diverse Error Handling (EH) data."""
    dataset = []
    print(f"🚀 {count} adet Gelişmiş EH verisi üretiliyor...")

    for i in range(count):
        error_code, scenario = random.choice(list(ERROR_HANDLING_SCENARIOS.items()))
        
        user_id = random.randint(1000, 9999)
        bill_id = random.randint(1000, 9999)
        package_name = random.choice(["Memur Özel", "Öğrenci Dostu"])
        
        user_request = random.choice(scenario["user_requests"]).format(
            user_id=user_id, bill_id=bill_id, package_name=package_name
        )
        assistant_response = random.choice(scenario["assistant_responses"])
        interim_response = random.choice(ASSISTANT_INTERIM_PHRASES)

        params = {}
        if scenario["function"] == "pay_bill":
            params = {"bill_id": f"F-2024-{bill_id}", "method": "credit_card"}
        elif scenario["function"] == "change_package":
            params = {"user_id": user_id, "new_package_name": package_name}
        else:
            params = {"user_id": user_id}

        error_json = json.dumps({
            "success": False,
            "error": {"code": error_code, "message": "API Error"}
        })

        data = {
            "id": f"EH-V2-{(i + 1):04d}",
            "senaryo": f"Error Handling - {error_code}",
            "donguler": [
                {"rol": "kullanici", "icerik": user_request},
                {"rol": "asistan", "icerik": interim_response},
                {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": scenario["function"], "parametreler": params}]},
                {"rol": "arac", "icerik": error_json},
                {"rol": "asistan", "icerik": assistant_response}
            ]
        }
        dataset.append(data)
    
    return dataset


def generate_nc_data_v2(count=1000):
    """Generates diverse and multi-turn Natural Chit-Chat (NC) data."""
    dataset = []
    print(f"🚀 {count} adet Gelişmiş NC verisi üretiliyor...")

    # Ağırlıklandırma: %70 tek turlu, %30 çok turlu olsun
    scenario_types = ["single_turn"] * 7 + ["multi_turn"] * 3
    
    for i in range(count):
        scenario_type = random.choice(scenario_types)
        
        if scenario_type == "multi_turn":
            # Şimdilik sadece bir çok turlu senaryo var, ileride çoğaltılabilir
            data = {
                "id": f"NC-V2-{(i + 1):04d}",
                "senaryo": "Natural Chit-Chat - Multi-Turn Complaint",
                "donguler": NATURAL_CHAT_SCENARIOS["multi_turn_complaint"]["turns"]
            }
        else: # single_turn
            category_name, category_data = random.choice([
                item for item in NATURAL_CHAT_SCENARIOS.items() if "turns" not in item[1]
            ])
            
            user_question = random.choice(category_data["user"])
            assistant_response = random.choice(category_data["assistant"])
            
            data = {
                "id": f"NC-V2-{(i + 1):04d}",
                "senaryo": f"Natural Chit-Chat - {category_name}",
                "donguler": [
                    {"rol": "kullanici", "icerik": user_question},
                    {"rol": "asistan", "icerik": assistant_response}
                ]
            }
        dataset.append(data)

    return dataset

# ==============================================================================
# 💾 MAIN EXECUTION AND SAVING
# ==============================================================================

def main(eh_count=1000, nc_count=1000):
    """Generates and saves all datasets."""
    print("🎯 Enhanced Data Generator (v2) Başlatılıyor...")
    print("=" * 50)
    
    eh_data = generate_eh_data_v2(eh_count)
    nc_data = generate_nc_data_v2(nc_count)
    
    combined_data = eh_data + nc_data
    
    # --- Dosya Kaydetme ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    eh_file = os.path.join(data_dir, f"error_handling_data_v2_{eh_count}.json")
    nc_file = os.path.join(data_dir, f"natural_chit_chat_data_v2_{nc_count}.json")
    combined_file = os.path.join(data_dir, f"combined_enhanced_data_v2_{eh_count + nc_count}.json")
    
    with open(eh_file, 'w', encoding='utf-8') as f:
        json.dump(eh_data, f, ensure_ascii=False, indent=2)
    with open(nc_file, 'w', encoding='utf-8') as f:
        json.dump(nc_data, f, ensure_ascii=False, indent=2)
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
        
    print("\n🎉 Tamamlandı! v2 Veri Setleri Oluşturuldu.")
    print(f"📁 EH v2 Dosyası: {os.path.basename(eh_file)}")
    print(f"📁 NC v2 Dosyası: {os.path.basename(nc_file)}")
    print(f"📁 Birleşik v2 Dosyası: {os.path.basename(combined_file)}")
    print(f"📊 Toplam: {len(combined_data)} veri")

if __name__ == "__main__":
    # Hızlı test için küçük sayılarla çalıştır
    main(eh_count=50, nc_count=50) 