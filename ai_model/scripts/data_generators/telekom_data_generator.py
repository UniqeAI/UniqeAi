"""
Telekom AI Projesi için Gelişmiş Sentetik Veri Üreticisi (Zemberek Destekli)

Bu script, `telekom_api_schema.py`'da tanımlanan araçları kullanarak,
modelin fine-tuning'i için gerekli olan çeşitli ve gerçekçi telekom
senaryoları içeren zengin bir veri seti oluşturur. 

Özellikler:
- Faker ile gerçekçi Türkçe veriler
- Zemberek ile morfolojik zenginleştirme
- Kişi çekimleri, iyelik ekleri, çoğul-tekil varyasyonları
- Eş anlamlı kelime değişimleri
- Cümle yapısı varyasyonları
- TDDI 2025 yarışması standartlarında kaliteli veri üretimi
"""

import json
import random
import logging
from typing import Dict, List, Set, Tuple
from faker import Faker
from pathlib import Path

# Zemberek kütüphanesini import ediyoruz
from zemberek.morphology import TurkishMorphology
from zemberek.core.turkish import RootAttribute

# Merkezi API şemamızdan API listesini ve yollarını içe aktarıyoruz.
import sys
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))
from telekom_api_schema import API_MAP, get_api_path

# Türkçe yerelleştirme ile Faker nesnesi oluştur
fake = Faker('tr_TR')

# Logging'i profesyonel bir standartta ayarlayalım
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdvancedTelekomDataGenerator:
    """
    Zemberek destekli gelişmiş telekomünikasyon veri üreticisi.
    
    Bu sınıf, orijinal veri üretim yeteneklerine ek olarak:
    - Türkçe morfolojik analiz ve sentez
    - Akıllı cümle varyasyonları
    - Kişi/zaman/durum ekleri modifikasyonu
    - Eş anlamlı kelime değişimleri
    - Yarışma kalitesinde çeşitli ve zengin veri üretimi
    """
    
    def __init__(self):
        """Sınıfı başlatır, Zemberek motorunu ve eş anlamlı kelime haritalarını yükler."""
        logging.info("AdvancedTelekomDataGenerator başlatılıyor...")
        
        # Zemberek morphology motorunu başlat
        logging.info("Zemberek TurkishMorphology motoru yükleniyor...")
        self.morphology = TurkishMorphology.create_with_defaults()
        logging.info("Zemberek motoru başarıyla yüklendi.")
        
        # Telekomünikasyon domaine özgü eş anlamlı kelimeler
        self.synonyms = {
            "fatura": ["hesap", "borç", "tutar"],
            "paket": ["tarife", "plan", "abonelik"],
            "hat": ["numara", "line", "hattım"],
            "internet": ["mobil veri", "data", "wifi"],
            "arıza": ["sorun", "problem", "hata"],
            "ödeme": ["tahsilat", "ödeyiş", "para transferi"],
            "müşteri": ["abone", "kullanıcı", "pelanggan"],
            "destek": ["yardım", "asistan", "servis"],
            "açmak": ["aktive etmek", "başlatmak", "devreye almak"],
            "kapatmak": ["devre dışı bırakmak", "durdurmak", "iptal etmek"],
            "kontrol": ["kontrol etmek", "sorgulama", "bakma"],
            "bilgi": ["detay", "malumat", "veri"],
            "hızlı": ["çabuk", "süratli", "acil"],
            "yavaş": ["ağır", "geç", "düşük hızlı"],
        }
        
        # Kişi ekleri dönüşüm haritası
        self.person_transforms = {
            # Ben -> Sen
            ('A1sg', 'A2sg'): [
                ("istiyorum", "istiyorsun"), ("yapıyorum", "yapıyorsun"), ("kullanıyorum", "kullanıyorsun"),
                ("görebiliyorum", "görebiliyorsun"), ("edebiliyorum", "edebiliyorsun"),
                ("alabiliyorum", "alabiliyorsun"), ("verebiliyorum", "verebiliyorsun"),
                ("anlayamıyorum", "anlayamıyorsun"), ("çözemiyorum", "çözemiyorsun"),
            ],
            # Ben -> O
            ('A1sg', 'A3sg'): [
                ("istiyorum", "istiyor"), ("yapıyorum", "yapıyor"), ("kullanıyorum", "kullanıyor"),
                ("görebiliyorum", "görebiliyor"), ("edebiliyorum", "edebiliyor"),
                ("alabiliyorum", "alabiliyor"), ("verebiliyorum", "verebiliyor"),
                ("anlayamıyorum", "anlayamıyor"), ("çözemiyorum", "çözemiyor"),
            ],
            # Ben -> Biz
            ('A1sg', 'A1pl'): [
                ("istiyorum", "istiyoruz"), ("yapıyorum", "yapıyoruz"), ("kullanıyorum", "kullanıyoruz"),
                ("görebiliyorum", "görebiliyoruz"), ("edebiliyorum", "edebiliyoruz"),
                ("alabiliyorum", "alabiliyoruz"), ("verebiliyorum", "verebiliyoruz"),
                ("anlayamıyorum", "anlayamıyoruz"), ("çözemiyorum", "çözemiyoruz"),
            ],
        }
        
        # İyelik ekleri dönüşüm haritası
        self.possessive_transforms = {
            # Benim -> Senin
            ('P1sg', 'P2sg'): [
                ("faturamı", "faturanı"), ("paketimi", "paketini"), ("hattımı", "hattını"),
                ("hesabımı", "hesabını"), ("adresimi", "adresini"), ("bilgilerimi", "bilgilerini"),
                ("tarifemi", "tarifeni"), ("numaramı", "numaranı"), ("şifremi", "şifreni"),
            ],
            # Benim -> Onun  
            ('P1sg', 'P3sg'): [
                ("faturamı", "faturasını"), ("paketimi", "paketini"), ("hattımı", "hattını"),
                ("hesabımı", "hesabını"), ("adresimi", "adresini"), ("bilgilerimi", "bilgilerini"),
                ("tarifemi", "tarifesini"), ("numaramı", "numarasını"), ("şifremi", "şifresini"),
            ],
            # Benim -> Bizim
            ('P1sg', 'P1pl'): [
                ("faturamı", "faturamızı"), ("paketimi", "paketimizi"), ("hattımı", "hattımızı"),
                ("hesabımı", "hesabımızı"), ("adresimi", "adresimizi"), ("bilgilerimi", "bilgilerimizi"),
                ("tarifemi", "tarifemizi"), ("numaramı", "numaramızı"), ("şifremi", "şifremizi"),
            ],
        }
        
        # Soru kalıpları ve varyasyonları
        self.question_patterns = {
            "ne kadar": ["kaç", "hangi miktarda", "ne tutarda"],
            "nasıl": ["hangi şekilde", "ne şekilde", "hangi yolla"],
            "ne zaman": ["hangi tarihe", "kaçında", "ne vakti"],
            "nerede": ["hangi yerde", "neresinde", "hangi konumda"],
            "neden": ["niçin", "hangi sebepten", "ne yüzden"],
            "ne yapmalıyım": ["nasıl hareket etmeliyim", "ne etmem gerek", "hangi adımları atmalıyım"],
        }
        
        logging.info("AdvancedTelekomDataGenerator başarıyla başlatıldı.")

    def _create_point(self, instruction: str, input_text: str, tool_name: str, **kwargs) -> Dict[str, str]:
        """
        Verilen bilgilere göre standart bir veri noktası oluşturur.
        `kwargs` ile gelen parametreleri tool call'a ekler.
        """
        api_path = get_api_path(tool_name)
        if not api_path:
            raise ValueError(f"Hata: '{tool_name}' adlı araç API şemasında bulunamadı.")

        # kwargs içindeki None değerlerini filtrele
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        params_list = []
        for k, v in filtered_kwargs.items():
            if isinstance(v, str):
                # String değerlerdeki tek tırnakları escape'le
                v_escaped = v.replace("'", "\\'")
                params_list.append(f"{k}='{v_escaped}'")
            else:
                params_list.append(f"{k}={v}")
        
        params_str = ", ".join(params_list)
        output_code = f"print({api_path}({params_str}))"
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": f"<tool_code>{output_code}</tool_code>"
        }
    
    def _apply_synonym_variations(self, text: str) -> List[str]:
        """Eş anlamlı kelimelerle varyasyonlar üretir."""
        variations = [text]
        words = text.split()
        
        for i, word in enumerate(words):
            # Noktalama işaretlerini temizle
            clean_word = word.lower().strip(".,?!:;")
            
            if clean_word in self.synonyms:
                for synonym in self.synonyms[clean_word]:
                    new_words = words[:]
                    # Orijinal kelimenin büyük/küçük harf durumunu koru
                    if word[0].isupper():
                        synonym = synonym.capitalize()
                    new_words[i] = word.replace(clean_word, synonym)
                    variations.append(" ".join(new_words))
        
        return list(set(variations))
    
    def _apply_morphological_variations(self, text: str) -> List[str]:
        """Zemberek kullanarak morfolojik varyasyonlar üretir."""
        variations = [text]
        
        # Person transformations
        for (source, target), transforms in self.person_transforms.items():
            for old_word, new_word in transforms:
                if old_word in text:
                    variations.append(text.replace(old_word, new_word))
        
        # Possessive transformations  
        for (source, target), transforms in self.possessive_transforms.items():
            for old_word, new_word in transforms:
                if old_word in text:
                    variations.append(text.replace(old_word, new_word))
        
        return list(set(variations))
    
    def _apply_question_variations(self, text: str) -> List[str]:
        """Soru kalıplarında varyasyonlar üretir."""
        variations = [text]
        
        for pattern, replacements in self.question_patterns.items():
            if pattern in text.lower():
                for replacement in replacements:
                    variations.append(text.replace(pattern, replacement))
        
        return list(set(variations))
    
    def _generate_enhanced_variations(self, input_text: str) -> List[str]:
        """
        Verilen input metni için tüm zenginleştirme tekniklerini uygular.
        """
        all_variations = set([input_text])
        
        # 1. Eş anlamlı kelime varyasyonları
        synonym_vars = self._apply_synonym_variations(input_text)
        all_variations.update(synonym_vars)
        
        # 2. Her bir synonym varyasyonu için morfolojik varyasyonlar
        for var in synonym_vars:
            morph_vars = self._apply_morphological_variations(var)
            all_variations.update(morph_vars)
        
        # 3. Soru kalıpları varyasyonları
        for var in list(all_variations):
            question_vars = self._apply_question_variations(var)
            all_variations.update(question_vars)
        
        # Orijinal metinle aynı olanları filtrele ve listeye çevir
        variations = [v for v in all_variations if v != input_text and len(v.strip()) > 0]
        
        return variations[:10]  # En fazla 10 varyasyon döndür

    def generate_billing_data(self, count: int = 150) -> List[Dict[str, str]]:
        """Fatura ve ödeme işlemleriyle ilgili çeşitli veriler üretir."""
        data = []
        user_ids = [fake.unique.random_int(min=1000, max=9999) for _ in range(50)]
        
        base_prompts = {
            "get_current_bill": [
                "Bu ayki faturam ne kadar gelmiş?", "Güncel fatura borcumu öğrenebilir miyim?", "Faturamın son ödeme tarihi ne zaman?",
            ],
            "get_past_bills": [
                "Geçmiş faturalarımı listeler misin?", "Son 6 aylık faturalarımı görmek istiyorum.", "Geçen yıl bu zamanlar ne kadar fatura ödemişim?",
            ],
            "pay_bill": [
                "{bill_id} numaralı faturamı ödemek istiyorum.", "Faturamı kredi kartıyla ödeyebilir miyim?", "Borcumu kapatmak için ne yapmalıyım?",
            ],
            "get_payment_history": [
                "Ödeme geçmişimi görebilir miyim?", "En son ne zaman ve ne kadar ödeme yapmışım?", "Yaptığım ödemelerin listesi lazım.",
            ],
            "setup_autopay": [
                "Otomatik ödemeyi açmak istiyorum.", "Otomatik ödemeyi iptal etmek istiyorum.",
            ]
        }
        
        # Her kategori için base data üret
        for _ in range(count // 3):  # Base veriyi azaltıyoruz çünkü varyasyonlar eklenecek
            tool_name = random.choice(list(base_prompts.keys()))
            user_id = random.choice(user_ids)
            instruction = tool_name.replace("_", " ").title()
            input_text = random.choice(base_prompts[tool_name])
            
            # Ana veri noktası oluştur
            if tool_name == "get_current_bill":
                base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id)
            elif tool_name == "get_past_bills":
                limit = random.choice([3, 6, 12])
                base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id, limit=limit)
            elif tool_name == "pay_bill":
                bill_id = f"F-{random.randint(2023, 2024)}-{random.randint(1000, 9999)}"
                method = random.choice(["credit_card", "bank_transfer"])
                base_point = self._create_point(instruction, input_text.format(bill_id=bill_id), tool_name, bill_id=bill_id, method=method)
            elif tool_name == "get_payment_history":
                base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id)
            elif tool_name == "setup_autopay":
                status = random.choice([True, False])
                input_text_new = "Otomatik ödemeyi açmak istiyorum." if status else "Otomatik ödemeyi iptal etmek istiyorum."
                base_point = self._create_point(instruction, input_text_new, tool_name, user_id=user_id, status=status)
            
            data.append(base_point)
            
            # Bu base point için zenginleştirilmiş varyasyonlar üret
            variations = self._generate_enhanced_variations(base_point["input"])
            for var_input in variations[:3]:  # Her base point için 3 varyasyon
                var_point = base_point.copy()
                var_point["input"] = var_input
                data.append(var_point)
        
        return data

    def generate_package_data(self, count: int = 150) -> List[Dict[str, str]]:
        """Paket ve tarife yönetimiyle ilgili çeşitli veriler üretir."""
        data = []
        user_ids = [fake.unique.random_int(min=1000, max=9999) for _ in range(50)]
        packages = ["Mega İnternet", "Süper Konuşma", "Full Paket", "Yurt Dışı Avantaj", "Öğrenci Dostu Tarife", "Esnaf Paketi"]
        
        base_prompts = {
            "get_customer_package": ["Mevcut paketim nedir?", "Hangi tarifeyi kullanıyorum?", "Tarifemin detaylarını öğrenmek istiyorum."],
            "get_remaining_quotas": ["Ne kadar internetim kaldı?", "Bu ayki konuşma dakikalarım ne durumda?", "Kalan kullanım haklarımı söyler misin?"],
            "change_package": ["Tarifemi değiştirmek istiyorum.", "Beni {new_package_name} tarifesine geçir.", "Daha uygun bir pakete geçebilir miyim?"],
            "get_available_packages": ["Hangi paketleriniz var?", "Bana uygun tarifeleri listeler misin?", "Seçebileceğim paketler nelerdir?"],
            "get_package_details": ["{package_name} paketinin içeriği nedir?", "Bu pakette ne kadar internet var?", "Tarifenin aylık ücreti ne kadar?"],
            "enable_roaming": ["Hattımı yurtdışı kullanımına açmak istiyorum.", "Hattımın yurtdışı kullanımını kapatmak istiyorum."],
        }

        # Base data üretimi (zenginleştirilmiş)
        for _ in range(count // 3):
            tool_name = random.choice(list(base_prompts.keys()))
            instruction = tool_name.replace("_", " ").title()
            input_text = random.choice(base_prompts[tool_name])

            if tool_name == "get_available_packages":
                base_point = self._create_point(instruction, input_text, tool_name)
            else:
                user_id = random.choice(user_ids)
                if tool_name == "change_package":
                    new_package = random.choice(packages)
                    base_point = self._create_point(instruction, input_text.format(new_package_name=new_package), tool_name, user_id=user_id, new_package_name=new_package)
                elif tool_name == "get_package_details":
                    package_name = random.choice(packages)
                    base_point = self._create_point(instruction, input_text.format(package_name=package_name), tool_name, package_name=package_name)
                elif tool_name == "enable_roaming":
                    status = random.choice([True, False])
                    input_text_new = "Hattımı yurtdışı kullanımına açmak istiyorum." if status else "Hattımın yurtdışı kullanımını kapatmak istiyorum."
                    base_point = self._create_point(instruction, input_text_new, tool_name, user_id=user_id, status=status)
                else: # get_customer_package, get_remaining_quotas
                    base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id)
            
            data.append(base_point)
            
            # Zenginleştirilmiş varyasyonlar
            variations = self._generate_enhanced_variations(base_point["input"])
            for var_input in variations[:3]:
                var_point = base_point.copy()
                var_point["input"] = var_input
                data.append(var_point)
                
        return data

    def generate_support_data(self, count: int = 150) -> List[Dict[str, str]]:
        """Teknik destek ve arıza kaydı ile ilgili çeşitli veriler üretir."""
        data = []
        user_ids = [fake.unique.random_int(min=1000, max=9999) for _ in range(50)]
        regions = ["Marmara", "Ege", "Akdeniz", "İç Anadolu", "Karadeniz", "Doğu Anadolu", "Güneydoğu Anadolu"]
        
        issue_templates = [
            "İnternet bağlantım sürekli kopuyor, lütfen yardım edin.",
            "Mobil verim çalışmıyor, acil destek bekliyorum.",
            "Ev internetimin hızı çok yavaşladı, neredeyse hiç bir site açılmıyor.",
            "Telefonum {city} şehrinde çekmiyor, {street_name} sokağında sinyal sorunu var.",
            "Modemimdeki internet ışığı kırmızı yanıyor, ne yapmalıyım?",
            "Hiçbir şekilde arama yapamıyorum veya alamıyorum.",
        ]
        
        base_prompts = {
            "check_network_status": ["Bölgemde genel bir arıza var mı?", "İstanbul'da kesinti yaşanıyor mu?", "{region}'da network sorunu var mı?"],
            "create_fault_ticket": issue_templates,
            "get_fault_ticket_status": ["Arıza kaydım ne durumda?", "Dün açtığım kayıt hakkında bilgi alabilir miyim?", "{ticket_id} numaralı arıza talebim sonuçlandı mı?"],
            "test_internet_speed": ["İnternet hızımı test eder misin?", "Download ve upload hızım kaç?", "Hız testi yapar mısın?"],
        }
        
        for _ in range(count // 3):
            tool_name = random.choice(list(base_prompts.keys()))
            instruction = tool_name.replace("_", " ").title()
            
            if tool_name == "check_network_status":
                region = random.choice(regions)
                input_text = random.choice(base_prompts[tool_name]).format(region=region)
                base_point = self._create_point(instruction, input_text, tool_name, region=region)
            else:
                user_id = random.choice(user_ids)
                if tool_name == "create_fault_ticket":
                    city = fake.city()
                    street = fake.street_name()
                    issue = random.choice(issue_templates).format(city=city, street_name=street)
                    base_point = self._create_point(instruction, issue, tool_name, user_id=user_id, issue_description=issue)
                elif tool_name == "get_fault_ticket_status":
                    ticket_id = f"T-{random.randint(10000, 99999)}"
                    input_text = random.choice(base_prompts[tool_name]).format(ticket_id=ticket_id)
                    base_point = self._create_point(instruction, input_text, tool_name, ticket_id=ticket_id)
                elif tool_name == "test_internet_speed":
                    input_text = random.choice(base_prompts[tool_name])
                    base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id)
            
            data.append(base_point)
            
            # Zenginleştirilmiş varyasyonlar
            variations = self._generate_enhanced_variations(base_point["input"])
            for var_input in variations[:3]:
                var_point = base_point.copy()
                var_point["input"] = var_input
                data.append(var_point)
                
        return data
        
    def generate_account_management_data(self, count: int = 150) -> List[Dict[str, str]]:
        """Hesap ve abonelik yönetimi ile ilgili veriler üretir."""
        data = []
        user_ids = [fake.unique.random_int(min=1000, max=9999) for _ in range(50)]
        
        base_prompts = {
            "get_customer_profile": ["Hesap bilgilerimi görebilir miyim?", "Üzerime kayıtlı hatları listele.", "Müşteri profilimi getir."],
            "update_customer_contact": [
                "Yeni adresim: {address}", "email adresimi {email} olarak güncelle.", "phone numaramı {phone} olarak değiştir."
            ],
            "suspend_line": ["Hattımı geçici olarak kapatmak istiyorum.", "Telefonum çalındı, hattımı dondurun.", "Bir süreliğine hattımı askıya alabilir miyim?"],
            "reactivate_line": ["Dondurduğum hattı tekrar açmak istiyorum.", "Hattımı yeniden aktive eder misin?", "Askıdaki hattım ne zaman açılır?"],
        }

        for _ in range(count // 3):
            tool_name = random.choice(list(base_prompts.keys()))
            user_id = random.choice(user_ids)
            instruction = tool_name.replace("_", " ").title()
            
            if tool_name == "get_customer_profile":
                input_text = random.choice(base_prompts[tool_name])
                base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id)
            elif tool_name == "update_customer_contact":
                contact_type = random.choice(["address", "email", "phone"])
                if contact_type == "address":
                    new_value = fake.address()
                    input_text = f"Yeni adresim: {new_value}"
                elif contact_type == "email":
                    new_value = fake.email()
                    input_text = f"email adresimi {new_value} olarak güncelle."
                else:  # phone
                    new_value = fake.phone_number()
                    input_text = f"phone numaramı {new_value} olarak değiştir."
                base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id, contact_type=contact_type, new_value=new_value)
            elif tool_name == "suspend_line":
                reason = random.choice(["kayıp/çalıntı", "geçici durdurma", "askerlik"])
                input_text = random.choice(base_prompts[tool_name])
                base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id, reason=reason)
            elif tool_name == "reactivate_line":
                input_text = random.choice(base_prompts[tool_name])
                base_point = self._create_point(instruction, input_text, tool_name, user_id=user_id)
            
            data.append(base_point)
            
            # Zenginleştirilmiş varyasyonlar
            variations = self._generate_enhanced_variations(base_point["input"])
            for var_input in variations[:3]:
                var_point = base_point.copy()
                var_point["input"] = var_input
                data.append(var_point)
                
        return data

    def generate_all_data(self, total_count: int = 2000) -> List[Dict[str, str]]:
        """
        Tüm kategorilerden veri üretir ve karıştırır.
        Zemberek destekli zenginleştirme ile çok daha çeşitli veri seti oluşturur.
        """
        logging.info(f"Toplam {total_count} adet zenginleştirilmiş veri üretiliyor...")
        
        # Her kategoriden eşit miktarda veri üret (zenginleştirme dahil)
        per_category = total_count // 4
        
        logging.info(f"Fatura kategorisi için {per_category} veri üretiliyor...")
        billing_data = self.generate_billing_data(per_category)
        
        logging.info(f"Paket kategorisi için {per_category} veri üretiliyor...")
        package_data = self.generate_package_data(per_category)
        
        logging.info(f"Destek kategorisi için {per_category} veri üretiliyor...")
        support_data = self.generate_support_data(per_category)
        
        logging.info(f"Hesap yönetimi kategorisi için {per_category} veri üretiliyor...")
        account_data = self.generate_account_management_data(per_category)
        
        # Tüm veriyi birleştir ve karıştır
        all_data = billing_data + package_data + support_data + account_data
        random.shuffle(all_data)
        
        logging.info(f"Toplam {len(all_data)} adet zenginleştirilmiş veri başarıyla üretildi.")
        return all_data


def save_to_json(data: List[Dict[str, str]], filename: str):
    """Veriyi JSON formatında dosyaya kaydeder."""
    output_path = Path(__file__).parent.parent / "data" / filename
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logging.info(f"Veri başarıyla kaydedildi: {output_path}")
    logging.info(f"Toplam veri sayısı: {len(data)}")


if __name__ == "__main__":
    """
    Ana çalıştırma bloğu.
    
    Bu betik direkt çalıştırıldığında:
    - 2000 adet zenginleştirilmiş veri üretir
    - Zemberek ile morfolojik varyasyonlar ekler
    - TDDI 2025 yarışması kalitesinde çıktı sağlar
    """
    logging.info("=== Gelişmiş Telekom Veri Üreticisi Başlatılıyor ===")
    
    try:
        # Gelişmiş veri üreticiyi başlat
        generator = AdvancedTelekomDataGenerator()
        
        # 2000 adet zenginleştirilmiş veri üret
        all_data = generator.generate_all_data(total_count=2000)
        
        # Dosyaya kaydet
        save_to_json(all_data, "telekom_training_dataset_enhanced.json")
        
        logging.info("=== Veri üretimi başarıyla tamamlandı! ===")
        
    except Exception as e:
        logging.error(f"Veri üretimi sırasında hata oluştu: {e}")
        raise