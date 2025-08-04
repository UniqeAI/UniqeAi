import uuid
import random
import json
from enum import Enum
from typing import Dict, Any, List

# Enum tanımlamaları (örnek)
class ScenarioType(Enum):
    CHANGE_PACKAGE = "change_package"

class CognitiveState(Enum):
    STRATEGIC = "strategic"
    CURIOUS = "curious"
    OVERWHELMED = "overwhelmed"
    DECISIVE = "decisive"
    CONFUSED = "confused"

class EmotionalContext(Enum):
    EXCITED = "excited"
    NEUTRAL = "neutral"
    FRUSTRATED = "frustrated"
    SATISFIED = "satisfied"
    ANXIOUS = "anxious"
    CONFIDENT = "confident"

# Genişletilmiş veri setleri - %90+ benzersizlik için
PACKAGE_NAMES = [
    "Mega İnternet Paketi", "Süper Net 100", "FiberMax", "Ultra Hızlı İnternet", "Evim İçin Net",
    "Oyun Paketi", "Sınırsız Video", "Akıllı Ev Paketi", "Temel İnternet", "Yüksek Performans",
    "Güvenli Web", "Genç Paketi", "Aile İnternet Paketi", "Kurumsal Net", "Gece Süper Hız",
    "Hafta Sonu Keyfi", "Power Net", "StreamLine", "NetFest", "SpeedBoost",
    "HomeBase", "ProGamer", "MovieBuff", "SmartHome", "BasicNet",
    "HighSpeed", "SecureNet", "YouthPlan", "FamilyPlan", "BusinessLine",
    "NightSurfer", "WeekendWarrior", "TurboNet", "DataDeluxe", "ConnectPlus",
    "EliteSpeed", "GameOn", "ViewVault", "HomeHub", "WorkWired"
]

USER_EXPRESSIONS = [
    # Doğrudan istekler
    "Merhaba, mevcut paketimi '{new_package}' ile değiştirmek istiyorum.",
    "Yeni bir pakete geçmek istiyorum. '{new_package}' ilgimi çekti.",
    "Şu anki internet paketimden memnun değilim. '{new_package}' paketine geçmek istiyorum.",
    "Daha hızlı internet istiyorum. '{new_package}' paketine nasıl geçebilirim?",
    "İnternet paketimi değiştirmek istiyorum. '{new_package}' öneriyor musunuz?",
    "Faturamı düşürmek istiyorum. '{new_package}' daha uygun mu?",
    "Yeni çıkan '{new_package}' paketine geçmek istiyorum.",
    "Mevcut paketim artık yeterli gelmiyor. '{new_package}' paketine geçiş yapmak istiyorum.",
    "Paketimi '{new_package}' olarak güncellemek istiyorum.",
    "Yeni bir internet paketi almak istiyorum. '{new_package}' hakkında bilgi alabilir miyim?",
    "Hızımı artırmak istiyorum. '{new_package}' bunu sağlar mı?",
    "Şu anki paketimin yerine '{new_package}' paketini koymak istiyorum.",
    "İnternet paketimi '{new_package}' paketiyle değiştirmek mümkün mü?",
    "Mevcut aboneliğimi sonlandırıp '{new_package}' paketine geçmek istiyorum.",
    "Yeni bir teklif görmek istiyorum. '{new_package}' hakkında ne düşünüyorsunuz?",
    "Daha iyi bir paket arıyorum. '{new_package}' uygun olabilir mi?",
    "Paketimde değişiklik yapmak istiyorum. '{new_package}' önerin.",
    "İnternet paketimi yükseltmek istiyorum. '{new_package}' paketi uygun mu?",
    "Yeni bir plan düşünüyorum. '{new_package}' paketi hakkında yardımcı olur musunuz?",
    "Mevcut paketim yerine '{new_package}' paketini aktif etmek istiyorum.",
    
    # Dolaylı istekler / Sorular
    "'{new_package}' paketi nedir? Nasıl geçiş yapabilirim?",
    "'{new_package}' paketi bana ne kadar avantaj sağlar?",
    "Şu anda '{new_package}' paketiyle ilgileniyorum. Nasıl başvurabilirim?",
    "Yeni '{new_package}' kampanyasını duydum. Nasıl geçebilirim?",
    "'{new_package}' paketiyle ilgili detayları öğrenebilir miyim?",
    "Mevcut paketim yerine '{new_package}' paketi daha mı iyi?",
    "Yeni '{new_package}' paketiyle ilgili bilgi almak istiyorum.",
    "Paketimi '{new_package}' paketine yükseltmek istiyorum. Ne yapmam gerekiyor?",
    "Faturamı '{new_package}' paketiyle düşürebilir miyim?",
    "Yeni '{new_package}' paketi hakkında bilgi verir misiniz? Geçmek istiyorum.",
    
    # Problem odaklı
    "Şu anki internetim çok yavaş. '{new_package}' paketiyle sorunum çözülür mü?",
    "İnternetim sık sık kesiliyor. '{new_package}' paketi daha stabil mi?",
    "Faturam çok yüksek geldi. '{new_package}' paketi daha uygun fiyatlı mı?",
    "Mevcut paketim artık ihtiyaçlarımı karşılamıyor. '{new_package}' paketine geçmek istiyorum.",
    "İnternet hızından şikayetçiyim. '{new_package}' paketiyle hızlanır mıyım?",
    "Yeni oyunlar oynamakta zorlanıyorum. '{new_package}' paketi daha hızlı mı?",
    "Akıllı ev cihazlarım düzgün çalışmıyor. '{new_package}' paketi yardımcı olur mu?",
    "Video izlerken donmalar yaşıyorum. '{new_package}' paketiyle sorun kalkar mı?",
    "İşlerim için daha iyi bağlantıya ihtiyacım var. '{new_package}' paketi uygun mu?",
    "İnternetimde sorunlar yaşıyorum. '{new_package}' paketine geçmek istiyorum."
]

ASSISTANT_RESPONSES_START = [
    "Tabii ki. '{new_package}' için geçiş işlemlerinizi başlatıyorum.",
    "Elbette. '{new_package}' paketine geçiş yapıyorum.",
    "Pekala. '{new_package}' paketine geçiş talebinizi işleme alıyorum.",
    "Anladım. '{new_package}' paketi için sizi yönlendiriyorum.",
    "Memnuniyetle. '{new_package}' paketine geçiş işlemlerine başlıyorum.",
    "Hemen '{new_package}' paketine geçiş işlemlerini başlatıyorum.",
    "Tamam. '{new_package}' paketi için değişiklik talebinizi oluşturuyorum.",
    "Gerekli işlemleri başlatıyorum. '{new_package}' paketine geçiyorsunuz.",
    "İşlem başlatılıyor. '{new_package}' paketine geçiş talebiniz alındı.",
    "Hazır mısınız? '{new_package}' paketine geçiş yapıyorum.",
    "İşte size '{new_package}' paketi. Geçiş işlemlerini başlatıyorum.",
    "Seçiminiz '{new_package}'. Geçiş işlemlerine başlıyorum.",
    "Geçmek istediğiniz paket '{new_package}'. İşlemi başlatıyorum.",
    "Talebinizi alıyorum. '{new_package}' paketine geçiş yapıyorum.",
    "İşlem başlatılıyor: '{new_package}' paketine geçiş.",
    "Geçiş talebiniz alındı. '{new_package}' paketi için işlemler başlıyor.",
    "Yeni paketiniz '{new_package}'. Geçiş işlemlerine geçiyorum.",
    "Onaylıyorum. '{new_package}' paketine geçiyorsunuz.",
    "Geçiş talebinizi işliyorum. Yeni paketiniz '{new_package}'.",
    "Talebinizi yerine getiriyorum. '{new_package}' paketine geçiş başlatılıyor."
]

ASSISTANT_RESPONSES_END = [
    "Paket değişikliği talebiniz alınmıştır. Yeni paketiniz önümüzdeki fatura döneminde aktif olacaktır.",
    "Talebiniz başarıyla oluşturuldu. Yeni paketiniz {activation_time} tarihinde aktif olacaktır.",
    "Geçiş talebiniz işleme alındı. '{new_package}' paketi {activation_time} itibariyle aktif olacak.",
    "Yeni paket talebiniz kaydedildi. {activation_time} tarihinden itibaren '{new_package}' paketini kullanacaksınız.",
    "İşlem tamamlandı. '{new_package}' paketi {activation_time} tarihinde aktif olacaktır.",
    "Talebiniz alındı. Yeni paketiniz {activation_time} tarihinde etkinleşecek.",
    "Geçiş işlemi başlatıldı. '{new_package}' paketi {activation_time} tarihinde kullanıma açılacak.",
    "Yeni paket talebiniz onaylandı. {activation_time} tarihinde '{new_package}' paketi aktif olacaktır.",
    "Talebiniz başarıyla işlendi. '{new_package}' paketi {activation_time} tarihinden itibaren geçerli olacak.",
    "Geçiş talebiniz tamamlandı. Yeni paketiniz '{new_package}', {activation_time} tarihinde aktif olacak.",
    "İşlem başarılı. '{new_package}' paketi {activation_time} tarihinde etkinleşecek.",
    "Talebiniz gerçekleşti. '{new_package}' paketi {activation_time} tarihinden itibaren geçerli olacak.",
    "Yeni paket talebiniz alındı. '{new_package}' paketi {activation_time} tarihinde aktif edilecek.",
    "Geçiş talebiniz onaylandı. {activation_time} tarihinden itibaren '{new_package}' paketini kullanacaksınız.",
    "İşlem tamamlandı. Yeni paketiniz '{new_package}', {activation_time} tarihinde aktif olacaktır.",
    "Talebiniz işleme alındı. '{new_package}' paketi {activation_time} tarihinde etkinleşecek.",
    "Yeni paket talebiniz işleniyor. '{new_package}' paketi {activation_time} tarihinde aktif olacaktır.",
    "Geçiş talebiniz alındı. '{new_package}' paketi {activation_time} tarihinden itibaren geçerli olacak.",
    "İşlem başlatıldı. '{new_package}' paketi {activation_time} tarihinde aktif edilecek.",
    "Talebiniz kaydedildi. '{new_package}' paketi {activation_time} tarihinde kullanıma açılacak."
]

PERSONALITY_PROFILES = [
    "tech_savvy_millennial", "cautious_elderly", "busy_parent",
    "budget_conscious_student", "gaming_enthusiast", "remote_worker",
    "streaming_addict", "security_minded", "frequent_traveler", "small_business_owner"
]

COGNITIVE_STATES = [state.value for state in CognitiveState]
EMOTIONAL_CONTEXTS = [context.value for context in EmotionalContext]

ACTIVATION_TIMES = [
    "önümüzdeki fatura döneminde", "gelecek ay", "yakın bir tarihte",
    "yeni fatura döneminizde", "önümüzdeki ödeme döneminizde", "bir sonraki fatura tarihinizde",
    "yeni ödeme döngünüzde", "önümüzdeki ay", "gelecek fatura döneminizde", "yakında"
]

def _generate_user_id():
    return f"user_{uuid.uuid4().hex[:8]}"

def _create_validated_response(response_class, override_data=None):
    # Basitleştirilmiş bir örnek, aslında daha karmaşık olabilir
    base_data = {"status": "pending_activation"}
    if override_data:
        base_data.update(override_data)
    return base_data

class ChangePackageResponse:
    pass # Placeholder

def generate_change_package_scenarios(count: int = 1000) -> List[Dict[str, Any]]:
    """Belirtilen sayıda kullanıcı paket değiştirme senaryosu oluşturur."""
    scenarios = []
    used_hashes = set() # Benzersizliği kontrol etmek için
    
    attempts = 0
    max_attempts = count * 10 # Sonsuz döngüyü önlemek için
    
    while len(scenarios) < count and attempts < max_attempts:
        attempts += 1
        
        user_id = _generate_user_id()
        new_package = random.choice(PACKAGE_NAMES)
        user_expression_template = random.choice(USER_EXPRESSIONS)
        user_expression = user_expression_template.format(new_package=new_package)
        
        assistant_start_template = random.choice(ASSISTANT_RESPONSES_START)
        assistant_start = assistant_start_template.format(new_package=new_package)
        
        activation_time = random.choice(ACTIVATION_TIMES)
        assistant_end_template = random.choice(ASSISTANT_RESPONSES_END)
        assistant_end = assistant_end_template.format(new_package=new_package, activation_time=activation_time)
        
        # Senaryonun benzersizliğini kontrol etmek için bir hash oluştur
        # Bu hash, senaryonun anahtar bileşenlerine dayanır
        scenario_hash = hash((
            user_expression,
            assistant_start,
            assistant_end,
            random.choice(PERSONALITY_PROFILES),
            random.choice(COGNITIVE_STATES),
            random.choice(EMOTIONAL_CONTEXTS)
        ))
        
        # Eğer bu hash zaten kullanıldıysa, yeni bir tane oluştur
        if scenario_hash in used_hashes:
            continue
            
        used_hashes.add(scenario_hash)
        
        scenario = {
            "id": f"change_package_scenario_{uuid.uuid4().hex[:8]}",
            "scenario_type": ScenarioType.CHANGE_PACKAGE.value,
            "personality_profile": random.choice(PERSONALITY_PROFILES),
            "cognitive_state": random.choice(COGNITIVE_STATES),
            "emotional_context": random.choice(EMOTIONAL_CONTEXTS),
            "donguler": [
                {"rol": "kullanici", "icerik": user_expression},
                {"rol": "asistan", "icerik": assistant_start},
                {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "new_package_name": new_package}}]},
                {"rol": "arac", "icerik": _create_validated_response(ChangePackageResponse, override_data={"to_package": new_package, "status": "pending_activation"})},
                {"rol": "asistan", "icerik": assistant_end}
            ]
        }
        scenarios.append(scenario)
        
    if len(scenarios) < count:
        print(f"Uyarı: Sadece {len(scenarios)} adet benzersiz senaryo oluşturulabildi. Hedeflenen: {count}")
        
    return scenarios

# 1000 senaryo oluştur
scenarios = generate_change_package_scenarios(1000)

# Örnek bir senaryo yazdır
print("Örnek Senaryo:")
print(json.dumps(scenarios[0], indent=2, ensure_ascii=False))

print(f"\n\nToplam oluşturulan benzersiz senaryo sayısı: {len(scenarios)}")

# Senaryoları bir dosyaya kaydet
with open('change_package_scenarios.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios, f, indent=2, ensure_ascii=False)

print("Senaryolar 'change_package_scenarios.json' dosyasına kaydedildi.")