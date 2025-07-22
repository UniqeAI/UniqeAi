# -*- coding: utf-8 -*-
"""
Grandmaster Seviyesi Telekom Veri Seti Üretici - v3 "KAOS MOTORU"

Bu betik, 6 ana stratejiyi ve 5 zenginleştirme tekniğini (Proaktif, Zincirleme, Hata Yönetimi vb.)
birleştirerek, son derece karmaşık ve gerçekçi diyalog senaryoları üretir.

v3 Yükseltmeleri:
- Kaotik Kombinasyonlar: Birden fazla alakasız amacı tek bir kullanıcı talebinde birleştirir.
- Çoklu Kişilik Simülasyonu: Sabırsız, kafası karışık gibi farklı kullanıcı profilleri ekler.
- Bağlamsal Hafıza: Diyaloglara geçmişe referans veren ifadeler ekler.
- Veri Kirletme: Gerçek dünya yazım hataları, argo ve kısaltmalarla dili zenginleştirir.

Hedef: Modelin ezberciliğini kırmak, muhakeme yeteneğini en üst düzeye çıkarmak ve
gerçek dünyanın kaotik koşullarına karşı dayanıklılığını artırmak.
"""

import json
import random
import uuid
from pydantic import ValidationError
import os

# Proje içindeki ana API şemalarını ve modellerini içe aktar
from UniqeAi.ai_model.scripts.telekom_api_schema import (
    GetRemainingQuotasResponse,
    GetAvailablePackagesResponse,
    ChangePackageResponse,
    GetCurrentBillResponse,
    TestInternetSpeedResponse,
    GetFaultTicketStatusResponse,
    CreateFaultTicketResponse,
    GetCustomerProfileResponse,
    UpdateCustomerContactResponse,
    EnableRoamingResponse
)
from UniqeAi.ai_model.scripts.mock_backend_api import MockTelekomBackendAPI

def create_validated_json_response(pydantic_model, data: dict) -> str:
    try:
        validated_data = pydantic_model(**data)
        return validated_data.json()
    except ValidationError as e:
        print(f"Pydantic Hatası: {e}")
        raise

class GrandmasterDatasetGeneratorV3:
    """
    Karmaşık, çok adımlı ve çeşitli senaryolar üreten veri seti oluşturucu sınıfı.
    """
    def __init__(self):
        self.mock_api = MockTelekomBackendAPI()
        self.scenarios = []
        self.user_ids = list(self.mock_api.users.keys())
        
        # ADIM 1: Doğal Dil Çeşitliliği için Şablon Motoru
        self.phrase_templates = {
            "greet": ["Merhaba.", "Selam.", "Kolay gelsin.", "İyi günler."],
            "query_quota": [
                "Kalan kullanımlarım ne kadar?", "Bu ay internetimden ne kadar kalmış?", "Selam, kotamı bi' öğrenir miyim?", "GB'larım ne durumda?",
                "Kullanıcı ID'm {user_id}, internet kullanım hakkımı söyler misin?", "Paketimdeki kalanları öğrenmek istiyorum.", "Ne kadar internetim kaldı?"
            ],
            "request_payment": [
                "{user_id} numaralı hattımın faturasını ödemek istiyorum.", "Faturamı ödeyebilir miyim?", "Bu ayki borcum neyse kapatmak istiyorum.",
                "Ödeme yapacaktım, yardımcı olur musunuz?"
            ],
            "report_slow_internet": [
                "İnternetim yine çok yavaşladı, bir kontrol eder misiniz?", "İnternet bağlantım çok kötü.", "Neden internetim bu kadar yavaş?",
                "Bir bakın şuna, internette büyük bir sorun var gibi."
            ],
            "request_contact_update": [
                "Hesabımdaki e-posta adresini değiştirmek istiyorum.", "İletişim bilgilerimi güncelleyecektim.", "Yeni bir telefon numarası kaydetmem gerekiyor.",
                "Mail adresimi nasıl değiştiririm?"
            ],
            "request_roaming_activation": [
                "Merhaba, yarın yurt dışına çıkıyorum. Hattımı kullanıma açar mısınız?", "Yurt dışı kullanımını aktif hale getirebilir misiniz?",
                "Hattımı uluslararası dolaşıma açmak istiyorum."
            ],
            "request_ambiguous_package": [
                "Paketimi güncellemek istiyorum.", "Paketimle ilgili bir işlem yapacaktım.", "Mevcut paketimde bir değişiklik yapmak mümkün mü?"
            ],
            "clarify_internet_package": [
                "İnternet paketim.", "İnternet olanı.", "Sadece internet."
            ],
            "confirm_positive": [
                "Evet, lütfen.", "Evet, lütfen listele.", "Harika olur, devam et.", "Evet, yap.", "Tabii, bakalım.", "Evet, istiyorum.", "Onaylıyorum."
            ],
            "confirm_negative": [
                "Hayır, teşekkürler.", "Yok, istemiyorum.", "Gerek yok.", "Kalsın şimdilik.", "Hayır."
            ],
            "ask_for_details": [
                "Onun detaylarını alabilir miyim?", "Biraz daha bilgi verir misin?", "Özellikleri nelerdir?", "Detayları nedir?"
            ],
            "thank_and_bye": [
                "Teşekkür ederim, çok yardımcı oldunuz.", "Harika, teşekkürler.", "Tamamdır, iyi çalışmalar.", "Sağ olun, görüşmek üzere."
            ],
            "request_out_of_scope": [
                "Bana bir fıkra anlatır mısın?", "Hava durumu nasıl olacak?", "En yakın restoran nerede?", "Pizza sipariş etmek istiyorum.",
                "Bu akşamki maçın skoru ne oldu?"
            ],
            # v3 GÜNCELLEMESİ: Hafıza referansları ana şablonlara eklendi
            "report_recurrent_slow_internet": [
                "İnternetim yine yavaşladı, geçen hafta da aynı sorunu yaşamıştım, hatırlarsınız.",
                "Bu yavaş internet sorunu tekrar başladı. Lütfen yine kayıt açalım."
            ]
        }
        
        # v3 GÜNCELLEMESİ: Statik senaryo listesi yerine "Kaos Motoru"nu besleyecek görev havuzu
        self.task_pool = {
            "pay_bill": self.build_pay_bill_task,
            "check_quota": self.build_check_quota_task,
            "file_ticket": self.build_file_ticket_task,
            "list_packages": self.build_list_packages_task
        }
        
        # AŞAMA 2: Çoklu Kişilik Simülasyonu için şablonlar
        self.personality_injects = {
            "impatient": [
                "Hadi ama, daha hızlı lütfen.", "Cevap vermen ne kadar uzun sürdü!", "Acelem var, çabuk olur musun?"
            ],
            "confused": [
                "Pardon, ne demiştin, tam anlamadım?", "Bir saniye, kafam karıştı.", "Bu dediğin tam olarak ne anlama geliyor?"
            ],
            "topic_switch": [
                "Aklıma gelmişken, kotalarım ne durumdaydı?", "Dur bir saniye, önce şunu sorayım: yurt dışı paketleri ne oldu?",
                "Bu arada, fatura ödeme tarihim ne zamandı?"
            ]
        }
        
        # Ayrı history_references listesi kaldırıldı
        
        # Senaryo fonksiyonlarını dinamik jeneratörle değiştir
        self.scenario_functions = [
            self.generate_chaotic_combo_scenario,
            self.generate_graceful_failure_scenario,
            self.generate_disambiguation_scenario,
            self.generate_contextual_history_scenario # YENİ SENARYO EKLENDİ
        ]

        # AŞAMA 4: Veri Kirletme Motoru için kaynaklar
        self.typo_map = {'a': 's', 's': 'd', 'd': 'f', 'f': 'g', 'g': 'h', 'h': 'j', 'j': 'k', 'k': 'l', 'l': 'i'}
        self.slang_map = {'merhaba': 'slm', 'internet': 'net', 'sorun': 'sıkıntı', 'yavaşladı': 'gg oldu'}

    # ADIM 2: Rastgele Cümle Seçen Yardımcı Fonksiyon
    def get_random_phrase(self, intent, **kwargs):
        """Verilen bir niyet için rastgele bir cümle şablonu seçer ve formatlar."""
        phrase_template = random.choice(self.phrase_templates[intent])
        return phrase_template.format(**kwargs)

    # AŞAMA 4: YENİ FONKSİYON - VERİ KİRLETME MOTORU
    def perturb_user_phrase(self, phrase):
        """
        Bir cümleye rastgele yazım hataları, argo ve diğer "kirleri" enjekte eder.
        """
        words = phrase.split(' ')
        
        # %30 ihtimalle yazım hatası yap
        if random.random() < 0.3:
            word_to_mess_up_index = random.randint(0, len(words) - 1)
            word = list(words[word_to_mess_up_index])
            if len(word) > 3:
                char_to_mess_up_index = random.randint(0, len(word) - 1)
                char = word[char_to_mess_up_index].lower()
                if char in self.typo_map:
                    word[char_to_mess_up_index] = self.typo_map[char]
            words[word_to_mess_up_index] = "".join(word)

        # %20 ihtimalle argo kullan
        if random.random() < 0.2:
            for i, word in enumerate(words):
                clean_word = word.strip(".,?!").lower()
                if clean_word in self.slang_map:
                    words[i] = self.slang_map[clean_word]
                    break # Sadece ilk bulduğunu değiştir

        # %50 ihtimalle noktalama ve büyük/küçük harf ihmali
        if random.random() < 0.5:
            return " ".join(words).lower().replace("?", "").replace(".", "")
            
        return " ".join(words)

    def generate_scenario(self):
        """
        Rastgele bir senaryo tipi seçer ve oluşturur. Kaos motoru ana üreteçtir.
        """
        # Senaryoların çoğunluğu kaotik kombinasyonlardan oluşsun
        if random.random() < 0.7:
            scenario_func = self.generate_chaotic_combo_scenario
        else:
            scenario_func = random.choice([
                self.generate_graceful_failure_scenario, 
                self.generate_disambiguation_scenario,
                self.generate_contextual_history_scenario
            ])
        
        # Her senaryonun başına bir selamlaşma ekle
        conversation = [self.create_conversation_turn("user", self.get_random_phrase("greet"))]
        
        # Ana senaryo gövdesini oluştur
        scenario_body = scenario_func()
        
        # AŞAMA 2: Rastgele kişilik enjeksiyonu
        if scenario_func == self.generate_chaotic_combo_scenario and random.random() < 0.4: # %40 ihtimalle
            injection_type = random.choice(list(self.personality_injects.keys()))
            injection_phrase = random.choice(self.personality_injects[injection_type])
            
            # Enjeksiyonu diyaloğun ortasına rastgele bir yere yap
            injection_point = random.randint(1, len(scenario_body) - 1)
            scenario_body.insert(injection_point, self.create_conversation_turn("user", injection_phrase))
            
        conversation.extend(scenario_body)
        
        # Her senaryonun sonuna bir kapanış ifadesi ekle (eğer uygunsa)
        if scenario_func != self.generate_graceful_failure_scenario:
             conversation.append(self.create_conversation_turn("user", self.get_random_phrase("thank_and_bye")))
             conversation.append(self.create_conversation_turn("assistant", "Rica ederim, başka bir konuda yardımcı olabilir miyim?"))

        # AŞAMA 4: Tüm kullanıcı cümlelerini "kirlet"
        for turn in conversation:
            if turn["role"] == "user":
                turn["content"] = self.perturb_user_phrase(turn["content"])

        return conversation

    def create_conversation_turn(self, role, content, tool_calls=None):
        """Yardımcı fonksiyon: Bir konuşma turu oluşturur."""
        turn = {"role": role, "content": content}
        if tool_calls:
            turn["tool_calls"] = tool_calls
        return turn

    def generate(self, num_samples):
        """
        Belirtilen sayıda veri örneği (diyalog) üretir.
        """
        for _ in range(num_samples):
            # Her döngüde yeni bir senaryo üret
            scenario_conversation = self.generate_scenario()
            if scenario_conversation:
                self.scenarios.append({"id": f"gm_v3_{uuid.uuid4()}", "conversation": scenario_conversation})
        
        print(f"{len(self.scenarios)} adet Grandmaster v3 senaryo üretildi.")
        return self.scenarios

    def save_to_json(self, file_path):
        """
        Üretilen senaryoları JSON dosyasına kaydeder.
        Dosyayı, bu betiğin bulunduğu dizine göre kaydeder.
        """
        # Bu betiğin bulunduğu dizinin mutlak yolunu al
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Çıktı dosyasının tam yolunu oluştur
        output_path = os.path.join(script_dir, file_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.scenarios, f, ensure_ascii=False, indent=2)
        print(f"Veri seti başarıyla '{output_path}' dosyasına kaydedildi.")

    # ==============================================================================
    # AŞAMA 1: KAOS MOTORU VE DİNAMİK SENARYO ÜRETİMİ
    # ==============================================================================

    def generate_chaotic_combo_scenario(self):
        """
        Rastgele 2-3 görevi birleştirir, negatif koşullar ve öncelikler ekler.
        Bu fonksiyon, modelin ezberlemesini imkansız hale getirir.
        """
        user_id = random.choice(self.user_ids)
        num_tasks = random.randint(2, 3)
        selected_task_keys = random.sample(list(self.task_pool.keys()), num_tasks)
        
        tasks = [self.task_pool[key](user_id) for key in selected_task_keys]
        
        # Görevleri birleştirerek kaotik bir kullanıcı talebi oluştur
        user_request = "Merhaba, birkaç şey soracaktım. "
        user_request += " ve ".join([task['user_prompt'] for task in tasks]) + "."

        # Rastgele negatif koşul ekle
        if random.random() < 0.3:
            user_request += " Ama sakın hız testi yapma."

        conversation = [self.create_conversation_turn("user", user_request)]
        
        # Görevleri sırayla gerçekleştirerek diyalog akışını oluştur
        for task in tasks:
            conversation.extend(task['dialogue_flow'])

        return conversation

    # --- Kaos Motoru için Görev Yapılandırma Fonksiyonları ---

    def build_pay_bill_task(self, user_id):
        bill_id = f"F-2024-{user_id}"
        api_response_bill_data = self.mock_api.get_current_bill(user_id, force_unpaid=True)
        validated_response_bill = create_validated_json_response(GetCurrentBillResponse, api_response_bill_data['data'])
        amount = api_response_bill_data["data"]["amount"]

        api_response_pay_data = self.mock_api.pay_bill(bill_id, "credit_card")
        # Bu basit görevde başarılı olduğunu varsayıyoruz
        
        return {
            "user_prompt": "faturamı ödemek istiyorum",
            "dialogue_flow": [
                self.create_conversation_turn("assistant", f"Elbette, {user_id} numaralı hattınız için güncel faturanızı kontrol ediyorum.", 
                                              tool_calls=[{"name": "get_current_bill", "arguments": {"user_id": user_id}}]),
                self.create_conversation_turn("tool", validated_response_bill),
                self.create_conversation_turn("assistant", f"Toplam {amount} TL borcunuz görünüyor. Onaylarsanız ödemeyi gerçekleştiriyorum.",
                                              tool_calls=[{"name": "pay_bill", "arguments": {"bill_id": bill_id, "method": "credit_card"}}]),
                self.create_conversation_turn("tool", json.dumps(api_response_pay_data)),
                self.create_conversation_turn("assistant", "Ödemeniz başarıyla tamamlandı.")
            ]
        }

    def build_check_quota_task(self, user_id):
        api_response_quotas_data = self.mock_api.get_remaining_quotas(user_id)
        validated_response_quotas = create_validated_json_response(GetRemainingQuotasResponse, api_response_quotas_data['data'])
        remaining_gb = api_response_quotas_data["data"]["internet_remaining_gb"]
        
        return {
            "user_prompt": "kotalarımı öğrenmek istiyorum",
            "dialogue_flow": [
                self.create_conversation_turn("assistant", "Tabii, hemen kalan kullanımlarınızı sorguluyorum.", 
                                              tool_calls=[{"name": "get_remaining_quotas", "arguments": {"user_id": user_id}}]),
                self.create_conversation_turn("tool", validated_response_quotas),
                self.create_conversation_turn("assistant", f"Elbette, internet paketinizden {remaining_gb} GB kalmış görünüyor.")
            ]
        }

    def build_file_ticket_task(self, user_id):
        api_response_ticket_data = self.mock_api.create_fault_ticket(user_id, "İnternet çok yavaş.")
        validated_response_ticket = create_validated_json_response(CreateFaultTicketResponse, api_response_ticket_data['data'])
        ticket_id = api_response_ticket_data["data"]["ticket_id"]

        return {
            "user_prompt": "internetim yavaş diye arıza kaydı açacaktım",
            "dialogue_flow": [
                self.create_conversation_turn("assistant", "Anladım, yavaş internet sorununuz için bir arıza kaydı oluşturuyorum.", 
                                              tool_calls=[{"name": "create_fault_ticket", "arguments": {"user_id": user_id, "issue_description": "İnternet çok yavaş."}}]),
                self.create_conversation_turn("tool", validated_response_ticket),
                self.create_conversation_turn("assistant", f"Arıza kaydınız {ticket_id} numarasıyla başarıyla oluşturuldu. Gelişmelerle ilgili sizi bilgilendireceğiz.")
            ]
        }

    def build_list_packages_task(self, user_id):
        api_response_packages_data = self.mock_api.get_available_packages()
        validated_response_packages = create_validated_json_response(GetAvailablePackagesResponse, api_response_packages_data['data'])
        package_names = [pkg['name'] for pkg in api_response_packages_data['data']['packages']]

        return {
            "user_prompt": "mevcut paketleri listeler misin",
            "dialogue_flow": [
                self.create_conversation_turn("assistant", "Elbette, mevcut tüm paketleri sizin için listeliyorum.", 
                                              tool_calls=[{"name": "get_available_packages", "arguments": {}}]),
                self.create_conversation_turn("tool", validated_response_packages),
                self.create_conversation_turn("assistant", f"Şu anki popüler paketlerimiz: {', '.join(package_names)}. Detaylı bilgi istediğiniz bir paket var mı?")
            ]
        }
    
    # ESKİ STATİK SENARYOLAR SİLİNDİ
    
    def generate_disambiguation_scenario(self):
        """
        Kullanıcının belirsiz talebini, asistanın doğru sorularla netleştirdiği bir senaryo.
        Strateji: Belirsizlik Yönetimi (Disambiguation), Zincirleme Mantık.
        """
        user_id = random.choice(self.user_ids)
        conversation = []

        # 1. Kullanıcı belirsiz bir paket talebinde bulunur.
        conversation.append(self.create_conversation_turn("user", self.get_random_phrase("request_ambiguous_package")))

        # 2. Asistan, herhangi bir araç çağırmadan önce durumu netleştirmek için soru sorar.
        clarifying_question = "Elbette, yardımcı olmak isterim. Hangi paketinizle ilgili işlem yapmak istediğinizi öğrenebilir miyim? Örneğin: İnternet paketiniz mi, TV paketiniz mi?"
        conversation.append(self.create_conversation_turn("assistant", clarifying_question))

        # 3. Kullanıcı, "internet" paketini kastederek belirsizliği giderir.
        conversation.append(self.create_conversation_turn("user", self.get_random_phrase("clarify_internet_package")))

        # 4. Asistan, artık netleşen talep üzerine doğru aracı çağırır.
        assistant_response_after_clarification = "Anladım, internet paketinizle ilgili mevcut seçenekleri hemen listeliyorum."
        tool_call_packages = [{"name": "get_available_packages", "arguments": {}}]
        conversation.append(self.create_conversation_turn("assistant", assistant_response_after_clarification, tool_calls=tool_call_packages))

        # 5. Sahte API'den yanıt alınır ve doğrulanır.
        api_response_packages_data = self.mock_api.get_available_packages()
        validated_response_packages = create_validated_json_response(GetAvailablePackagesResponse, api_response_packages_data['data'])
        conversation.append(self.create_conversation_turn("tool", validated_response_packages))
        
        # 6. Asistan paketleri sunar.
        package_names = [pkg['name'] for pkg in api_response_packages_data['data']['packages']]
        final_response = f"Sizin için uygun olabilecek internet paketlerimiz şunlar: {', '.join(package_names)}. Hangisiyle ilgilenirsiniz?"
        conversation.append(self.create_conversation_turn("assistant", final_response))
        
        return conversation

    def generate_graceful_failure_scenario(self):
        """
        Modelin yetenekleri dışındaki bir talebi kibarca reddettiği bir senaryo.
        Strateji: Çözümsüz Senaryo Yönetimi.
        """
        conversation = []

        # 1. Kullanıcı, kapsam dışı bir talepte bulunur.
        conversation.append(self.create_conversation_turn("user", self.get_random_phrase("request_out_of_scope")))

        # 2. Asistan, kibarca yardımcı olamayacağını belirtir ve doğru yere yönlendirir.
        failure_response = "Üzgünüm, ben size yalnızca telekomünikasyon hizmetlerinizle ilgili konularda yardımcı olmak üzere tasarlanmış bir yapay zeka asistanıyım. Bu isteğinizi maalesef yerine getiremiyorum. Farklı bir konuda size nasıl destek olabilirim?"
        conversation.append(self.create_conversation_turn("assistant", failure_response))
        
        return conversation

    # AŞAMA 3: YENİ SENARYO FONKSİYONU
    def generate_contextual_history_scenario(self):
        """
        Kullanıcının geçmiş bir soruna referans verdiği ve asistanın bunu anladığını
        göstererek yanıt verdiği bir "hafıza" senaryosu.
        """
        user_id = random.choice(self.user_ids)
        conversation = []

        # 1. Kullanıcı, geçmiş bir soruna referans vererek diyaloğu başlatır.
        # Artık ana şablon havuzundan çağrılıyor
        conversation.append(self.create_conversation_turn("user", self.get_random_phrase("report_recurrent_slow_internet")))

        # 2. Asistan, durumu anladığını ve standart prosedürü atlayacağını belirtir.
        assistant_response = (
            f"Merhaba, {user_id} numaralı hattınızda bu sorunu tekrar yaşadığınızı anlıyorum ve özür dilerim. "
            "Bu sefer standart hız testi adımlarını atlayıp, durumun tekrarladığını belirterek sizin için "
            "doğrudan öncelikli bir arıza kaydı oluşturuyorum."
        )
        tool_call = [{"name": "create_fault_ticket", "arguments": {
            "user_id": user_id, 
            "issue_description": "Tekrarlayan yavaş internet sorunu. Öncelikli incelenmeli.",
            "priority": "high" # Varsayımsal parametre
        }}]
        conversation.append(self.create_conversation_turn("assistant", assistant_response, tool_calls=tool_call))

        # 3. API yanıtı ve kapanış
        api_response_ticket_data = self.mock_api.create_fault_ticket(user_id, "Tekrarlayan sorun", priority="high")
        validated_response_ticket = create_validated_json_response(CreateFaultTicketResponse, api_response_ticket_data['data'])
        ticket_id = api_response_ticket_data["data"]["ticket_id"]
        conversation.append(self.create_conversation_turn("tool", validated_response_ticket))
        conversation.append(self.create_conversation_turn("assistant", f"Kaydınız {ticket_id} numarasıyla en yüksek öncelikte oluşturuldu. Teknik ekibimiz doğrudan sizinle iletişime geçecektir."))

        return conversation


if __name__ == '__main__':
    generator = GrandmasterDatasetGeneratorV3()
    # Hedef: 10,000 adet son derece karmaşık ve çeşitli senaryo üretmek.
    grandmaster_data = generator.generate(10000)
    generator.save_to_json("grandmaster_dataset_10k_v3.json") 