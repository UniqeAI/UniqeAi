import json
import random
from faker import Faker
import nlpaug.augmenter.word as naw
import nltk

# 1. Eğer synonym augmentation kullanacaksanız, bu üç satırı açın bir kez indirme için:
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')

fake = Faker('tr_TR')
synonym_aug = naw.SynonymAug(aug_src='wordnet')
use_augmentation = False   # ← Bunu True yaparsanız paraphrase uygulanır

# Senaryo tanımları
scenarios = {
    "paket_arttirma": {
        "templates": [
            "İnternetim çok hızlı tükeniyor, daha yüksek GB içeren bir pakete nasıl geçebilirim?",
            "Mevcut paketim yetmiyor, artırmak istiyorum."
        ],
        "function": "get_available_packages"
    },
    "fatura_odeme": {
        "templates": [
            "Bu ayki faturamı göremiyorum, yardım eder misiniz?",
            "Faturam nerede gözüküyor acaba?"
        ],
        "function": "get_current_bill"
    },
    "internet_sorunu": {
        "templates": [
            "Evde internet bağlantım yok, neden?",
            "İnternetim çok yavaş, yardım edebilir misiniz?"
        ],
        "function": ["check_network_status", "test_internet_speed"]
    },
    # Buraya isterseniz "numara_taşıma", "roaming", "sms_sorunu" vb. senaryolar ekleyebilirsiniz...
}

dataset = {"konusmalar": []}

for i in range(1, 2501):
    key = random.choice(list(scenarios.keys()))
    scen = scenarios[key]
    
    # 2. Kullanıcı metnini seç
    user_text = random.choice(scen["templates"])
    # 3. Opsiyonel paraphrase
    if use_augmentation:
        user_text = synonym_aug.augment(user_text)
    
    # 4. Bağlam üretimi
    context = {}
    if key == "paket_arttirma":
        context = {"mevcut_paket": random.choice(["25GB_Temel","Mega İnternet","Öğrenci Dostu Tarife"])}
    elif key == "fatura_odeme":
        context = {"kullanici_tipi": random.choice(["bireysel","kurumsal"])}
    elif key == "internet_sorunu":
        context = {"konum": fake.city()}
    
    # 5. Fonksiyon çağrıları
    funcs = scen["function"]
    if isinstance(funcs, list):
        calls = [{"fonksiyon": f, "parametreler": context} for f in funcs]
    else:
        calls = [{"fonksiyon": funcs, "parametreler": context}]
    
    # 6. 5+ adımlı döngü
    donguler = [
        {"rol": "asistan", "icerik": "Merhaba, nasıl yardımcı olabilirim?", "baglam": {}},
        {"rol": "kullanici", "icerik": user_text, "baglam": context},
        {"rol": "asistan", "icerik": "Bir saniye, kontrol ediyorum.", "baglam": {}},
        {"rol": "asistan", "icerik": "İşleminiz tamamlandı, lütfen kontrol edin.", "arac_cagrilari": calls},
        {"rol": "kullanici", "icerik": "Teşekkür ederim.", "baglam": {}},
        {"rol": "asistan", "icerik": "Başka bir konuda yardımcı olabilir miyim?", "baglam": {}},
        {"rol": "kullanici", "icerik": "Hayır, teşekkürler.", "baglam": {}},
        {"rol": "asistan", "icerik": "İyi günler dilerim.", "baglam": {}}
    ]
    
    dataset["konusmalar"].append({
        "id": f"TK_{i:04d}",
        "senaryo": key,
        "donguler": donguler
    })

# 7. JSON'a kaydet
with open("telekom_dataset_2500.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("2500 örnek başarıyla oluşturuldu: telekom_dataset_2500.json")
