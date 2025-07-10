"""
Gelişmiş Sentetik Diyalog Veri Seti Üreticisi

Bu script, "DATASET_ENRICHMENT_GUIDE.md" rehberinde ve API spesifikasyonlarında
tanımlanan ilkelere dayanarak, yüksek kaliteli ve çeşitli bir diyalog veri seti üretir.

Temel Özellikler:
- **Senaryo Tabanlı Üretim:** Rastgele fonksiyon çağırmak yerine, önceden tanımlanmış
  karmaşık senaryo arketiplerini (örn: kararsız kullanıcı, proaktif asistan) kullanır.
- **Gerçekçi Veri:** `Faker` kütüphanesi ile gerçekçi kullanıcı verileri (isim, telefon vb.) üretir.
- **Dinamik Akış:** Tek ve zincirleme araç kullanımı, hata yönetimi ve doğal sohbet
  gibi farklı diyalog akışlarını simüle eder.
- **Çeşitlilik:** Hem kullanıcıların isteklerini ifade etme biçimlerinde hem de asistanın
  yanıtlarında çeşitlilik sağlayarak modelin ezber yapmasını engeller.
"""

import json
import random
import uuid
from faker import Faker

# --- Konfigürasyon ---
NUM_SAMPLES = 10000
OUTPUT_FILE = "../data/telekom_dataset_10k_advanced.json"
FAKE = Faker('tr_TR')

# --- Veri Havuzları ve Yardımcı Fonksiyonlar ---

# API Şemasından alınan fonksiyon listesi
AVAILABLE_TOOLS = [
    "get_customer_package", "get_available_packages", "change_package",
    "get_remaining_quotas", "get_package_details", "enable_roaming",
    "get_current_bill", "get_past_bills", "pay_bill",
    "get_payment_history", "setup_autopay", "check_network_status",
    "create_fault_ticket", "get_fault_ticket_status", "test_internet_speed",
    "get_customer_profile", "update_customer_contact", "suspend_line",
    "reactivate_line", "check_number_portability"
]

USER_PHRASES = {
    "get_current_bill": ["Bu ayki faturam ne kadar?", "Güncel borcumu öğrenebilir miyim?", "Faturamı gönderir misin?"],
    "change_package": ["Tarifemi değiştirmek istiyorum.", "Daha iyi bir pakete geçebilir miyim?", "Paketimi yükselt."],
    "enable_roaming": ["Yurtdışına çıkıyorum, hattımı açar mısın?", "Roaming'i aktive et.", "Hattımı yurtdışı kullanımına aç."],
    "create_fault_ticket": ["İnternetim çalışmıyor.", "Mobil verimde bir sorun var, kayıt oluştur.", "Hızım çok yavaş, arıza kaydı açar mısın?"],
    "chit_chat_greet": ["Merhaba", "Selam", "İyi günler"],
    "chit_chat_thanks": ["Teşekkürler", "Sağ ol", "Teşekkür ederim"],
    "chit_chat_who_are_you": ["Sen kimsin?", "Nesin sen?", "Yapay zeka mısın?"]
}

ASSISTANT_PHRASES = {
    "greeting": "Merhaba, size nasıl yardımcı olabilirim?",
    "checking": "Elbette, hemen kontrol ediyorum.",
    "anything_else": "Başka bir konuda yardımcı olabilir miyim?",
    "goodbye": "İyi günler dilerim.",
    "confirmation": "İşleminiz başarıyla tamamlandı.",
    "error_generic": "Üzgünüm, şu anda bu işlemi gerçekleştiremiyorum. Lütfen daha sonra tekrar deneyin.",
    "error_api": "Sistemlerimize ulaşırken anlık bir sorun yaşadık. Bu durum için özür dilerim.",
    "who_are_you": "Ben size telekomünikasyon hizmetlerinizle ilgili yardımcı olmak için tasarlanmış bir yapay zeka asistanıyım."
}

def generate_user_id():
    return random.randint(1000, 9999)

def generate_ticket_id():
    return f"T-{random.randint(10000, 99999)}"

def generate_bill_id():
    return f"F-2024-{random.randint(1000, 9999)}"

# --- Senaryo Üretim Fonksiyonları ---

def create_turn(role, content=None, tool_calls=None):
    turn = {"rol": role}
    if content:
        turn["icerik"] = content
    if tool_calls:
        turn["arac_cagrilari"] = tool_calls
    return turn

def generate_happy_path():
    """Basit, tek adımlı ve başarılı senaryo."""
    tool_name = random.choice(AVAILABLE_TOOLS)
    user_id = generate_user_id()
    
    user_phrase = random.choice(USER_PHRASES.get(tool_name, ["Lütfen " + tool_name.replace('_', ' ')]))
    
    donguler = [
        create_turn("asistan", ASSISTANT_PHRASES["greeting"]),
        create_turn("kullanici", user_phrase),
        create_turn("asistan", ASSISTANT_PHRASES["checking"]),
        create_turn("asistan", tool_calls=[{"fonksiyon": tool_name, "parametreler": {"user_id": user_id}}]),
        create_turn("asistan", ASSISTANT_PHRASES["confirmation"]),
        create_turn("kullanici", random.choice(USER_PHRASES["chit_chat_thanks"]))
    ]
    return "happy_path", donguler

def generate_proactive_assistant():
    """Asistanın bir işlem sonrası proaktif öneri yaptığı senaryo."""
    user_id = generate_user_id()
    bill_id = generate_bill_id()

    donguler = [
        create_turn("asistan", ASSISTANT_PHRASES["greeting"]),
        create_turn("kullanici", "Faturamı ödemek istiyorum."),
        create_turn("asistan", tool_calls=[{"fonksiyon": "pay_bill", "parametreler": {"user_id": user_id, "bill_id": bill_id}}]),
        create_turn("asistan", "Faturanız başarıyla ödendi. Bu arada, dilerseniz otomatik ödeme talimatı vererek bir daha fatura takibi yapmak zorunda kalmazsınız. Kurulum yapmak ister misiniz?"),
        create_turn("kullanici", "Evet, lütfen."),
        create_turn("asistan", tool_calls=[{"fonksiyon": "setup_autopay", "parametreler": {"user_id": user_id, "status": True}}]),
        create_turn("asistan", "Otomatik ödeme talimatınız başarıyla oluşturuldu.")
    ]
    return "proactive_assistant", donguler

def generate_indecisive_user():
    """Kullanıcının fikrini değiştirdiği veya ek bilgi istediği senaryo."""
    user_id = generate_user_id()
    
    donguler = [
        create_turn("asistan", ASSISTANT_PHRASES["greeting"]),
        create_turn("kullanici", "Tarifemi daha yüksek bir paketle değiştirmek istiyorum."),
        create_turn("asistan", "Elbette. 'Süper Hız 50GB' ve 'Mega İnternet 100GB' paketlerimiz mevcut. Hangisiyle ilgilenirsiniz?"),
        create_turn("kullanici", "P emin olamadım. Önce bu ay ne kadar internetim kalmış öğrenebilir miyim?"),
        create_turn("asistan", ASSISTANT_PHRASES["checking"]),
        create_turn("asistan", tool_calls=[{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]),
        create_turn("asistan", "Bu ay kotanızdan 8GB internet kalmış."),
        create_turn("kullanici", "Anladım, o zaman 'Mega İnternet 100GB' paketine geçelim."),
        create_turn("asistan", tool_calls=[{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "new_package_name": "Mega İnternet 100GB"}}]),
        create_turn("asistan", ASSISTANT_PHRASES["confirmation"])
    ]
    return "indecisive_user", donguler

def generate_chained_tool_use():
    """Bir isteği çözmek için birden fazla aracın zincirleme kullanıldığı senaryo."""
    user_id = generate_user_id()

    donguler = [
        create_turn("asistan", ASSISTANT_PHRASES["greeting"]),
        create_turn("kullanici", "Haftaya Almanya'ya gideceğim. Hattımı yurtdışı kullanımına açıp bana en uygun paketi önerir misin?"),
        create_turn("asistan", "Tabii ki. Öncelikle hattınızı yurtdışı kullanımına açıyorum."),
        create_turn("asistan", tool_calls=[{"fonksiyon": "enable_roaming", "parametreler": {"user_id": user_id, "status": True}}]),
        create_turn("asistan", "Hattınız artık yurtdışında kullanıma açık. Şimdi Almanya için en uygun paketleri listeliyorum."),
        create_turn("asistan", tool_calls=[{"fonksiyon": "get_available_packages", "parametreler": {"context": "roaming", "country": "Almanya"}}]),
        create_turn("asistan", "Almanya için 'Avrupa Haftalık 5GB' paketi en avantajlısı görünüyor. Aktive etmemi ister misiniz?"),
        create_turn("kullanici", "Evet, lütfen aktive et."),
        create_turn("asistan", tool_calls=[{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "new_package_name": "Avrupa Haftalık 5GB"}}])
    ]
    return "chained_tool_use", donguler

def generate_error_handling():
    """API'den hata döndüğü ve asistanın bunu yönettiği senaryo."""
    user_id = generate_user_id()
    ticket_id = generate_ticket_id()

    donguler = [
        create_turn("asistan", ASSISTANT_PHRASES["greeting"]),
        create_turn("kullanici", f"{ticket_id} numaralı arıza kaydım ne durumda?"),
        create_turn("asistan", ASSISTANT_PHRASES["checking"]),
        # Bu çağrının başarısız olduğunu varsayıyoruz
        create_turn("asistan", tool_calls=[{"fonksiyon": "get_fault_ticket_status", "parametreler": {"ticket_id": ticket_id}}]),
        create_turn("asistan", ASSISTANT_PHRASES["error_api"]),
        create_turn("kullanici", "Peki, teşekkürler.")
    ]
    return "error_handling", donguler

def generate_chit_chat():
    """Araç kullanımı gerektirmeyen doğal sohbet senaryosu."""
    phrase_type = random.choice(["greet", "thanks", "who_are_you"])
    
    if phrase_type == "greet":
        donguler = [
            create_turn("kullanici", random.choice(USER_PHRASES["chit_chat_greet"])),
            create_turn("asistan", ASSISTANT_PHRASES["greeting"])
        ]
    elif phrase_type == "thanks":
        donguler = [
            create_turn("kullanici", random.choice(USER_PHRASES["chit_chat_thanks"])),
            create_turn("asistan", "Rica ederim, yardımcı olabildiğime sevindim.")
        ]
    else: # who_are_you
        donguler = [
            create_turn("kullanici", random.choice(USER_PHRASES["chit_chat_who_are_you"])),
            create_turn("asistan", ASSISTANT_PHRASES["who_are_you"])
        ]
    return "chit_chat", donguler

# --- Ana Üretim Motoru ---

def generate_conversations():
    """Belirlenen sayıda ve çeşitlilikte diyalog üretir."""
    
    scenario_generators = {
        generate_happy_path: 0.40,
        generate_proactive_assistant: 0.10,
        generate_indecisive_user: 0.15,
        generate_chained_tool_use: 0.10,
        generate_error_handling: 0.10,
        generate_chit_chat: 0.15,
    }
    
    generators = list(scenario_generators.keys())
    weights = list(scenario_generators.values())
    
    all_conversations = []
    
    print(f"Toplam {NUM_SAMPLES} adet gelişmiş diyalog üretiliyor...")
    
    for i in range(NUM_SAMPLES):
        # Ağırlıklara göre bir senaryo tipi seç
        chosen_generator = random.choices(generators, weights, k=1)[0]
        senaryo_tipi, donguler = chosen_generator()
        
        conversation = {
            "id": f"SYNTH_{str(uuid.uuid4())[:8]}",
            "senaryo": senaryo_tipi,
            "donguler": donguler
        }
        all_conversations.append(conversation)
        
        if (i + 1) % 500 == 0:
            print(f"  -> {i + 1}/{NUM_SAMPLES} diyalog üretildi...")
            
    print("Diyalog üretimi tamamlandı.")
    return {"konusmalar": all_conversations}

def save_to_json(data, filepath):
    """Veriyi JSON dosyasına kaydeder."""
    print(f"Veri seti '{filepath}' dosyasına kaydediliyor...")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Kaydetme işlemi tamamlandı.")

if __name__ == "__main__":
    final_dataset = generate_conversations()
    save_to_json(final_dataset, OUTPUT_FILE)
    print("\nİşlem başarıyla tamamlandı!")
    print(f"Oluşturulan dosya: {OUTPUT_FILE}") 