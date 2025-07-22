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
from datetime import datetime, timedelta

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
        # Pydantic v2 uyumluluğu için .model_dump_json() kullanılır
        return validated_data.model_dump_json()
    except ValidationError as e:
        print(f"Pydantic Hatası: {e}")
        raise

class GrandmasterDatasetGeneratorV3:
    """
    Kaotik, çok kişilikli, hafızalı ve kirli veri üreten v3 jeneratörü.
    """
    def __init__(self):
        self.mock_api = MockTelekomBackendAPI()
        self.scenarios = []
        self.user_ids = list(self.mock_api.users.keys())

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
            "report_recurrent_slow_internet": [
                "İnternetim yine yavaşladı, geçen hafta da aynı sorunu yaşamıştım, hatırlarsınız.",
                "Bu yavaş internet sorunu tekrar başladı. Lütfen yine kayıt açalım."
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
            "confirm_positive": ["Evet, lütfen.", "Evet, lütfen listele.", "Harika olur, devam et.", "Evet, yap.", "Tabii, bakalım.", "Evet, istiyorum.", "Onaylıyorum."],
            "confirm_negative": ["Hayır, teşekkürler.", "Yok, istemiyorum.", "Gerek yok.", "Kalsın şimdilik.", "Hayır."],
            "ask_for_details": ["Onun detaylarını alabilir miyim?", "Biraz daha bilgi verir misin?", "Özellikleri nelerdir?", "Detayları nedir?"],
            "thank_and_bye": ["Teşekkür ederim, çok yardımcı oldunuz.", "Harika, teşekkürler.", "Tamamdır, iyi çalışmalar.", "Sağ olun, görüşmek üzere."],
            "request_out_of_scope": ["Bana bir fıkra anlatır mısın?", "Hava durumu nasıl olacak?", "En yakın restoran nerede?", "Pizza sipariş etmek istiyorum.","Bu akşamki maçın skoru ne oldu?"]
        }
        
        self.personality_injects = {
            "impatient": ["Hadi ama, daha hızlı lütfen.", "Cevap vermen ne kadar uzun sürdü!", "Acelem var, çabuk olur musun?"],
            "confused": ["Pardon, ne demiştin, tam anlamadım?", "Bir saniye, kafam karıştı.", "Bu dediğin tam olarak ne anlama geliyor?"],
            "topic_switch": ["Aklıma gelmişken, kotalarım ne durumdaydı?", "Dur bir saniye, önce şunu sorayım: yurt dışı paketleri ne oldu?", "Bu arada, fatura ödeme tarihim ne zamandı?"]
        }
        
        self.typo_map = {'a': 's', 's': 'd', 'd': 'f', 'f': 'g', 'g': 'h', 'h': 'j', 'j': 'k', 'k': 'l', 'l': 'i'}
        self.slang_map = {'merhaba': 'slm', 'internet': 'net', 'sorun': 'sıkıntı', 'yavaşladı': 'gg oldu', 'faturamı': 'borcumu'}
        
        self.task_pool = {
            "pay_bill": self.build_pay_bill_task,
            "check_quota": self.build_check_quota_task,
            "file_ticket": self.build_file_ticket_task,
            "list_packages": self.build_list_packages_task
        }
        
        self.scenario_functions = [
            self.generate_chaotic_combo_scenario,
            self.generate_graceful_failure_scenario,
            self.generate_disambiguation_scenario,
            self.generate_contextual_history_scenario
        ]

    def get_random_phrase(self, intent, **kwargs):
        phrase_template = random.choice(self.phrase_templates[intent])
        return phrase_template.format(**kwargs)

    def perturb_user_phrase(self, phrase):
        words = phrase.split(' ')
        if random.random() < 0.3:
            word_idx = random.randint(0, len(words) - 1)
            word = list(words[word_idx])
            if len(word) > 3:
                char_idx = random.randint(0, len(word) - 1)
                char = word[char_idx].lower()
                if char in self.typo_map:
                    word[char_idx] = self.typo_map[char]
            words[word_idx] = "".join(word)
        if random.random() < 0.2:
            for i, word in enumerate(words):
                clean_word = word.strip(".,?!").lower()
                if clean_word in self.slang_map:
                    words[i] = self.slang_map[clean_word]
                    break
        if random.random() < 0.5:
            return " ".join(words).lower().replace("?", "").replace(".", "")
        return " ".join(words)

    def generate_scenario(self):
        if random.random() < 0.7:
            scenario_func = self.generate_chaotic_combo_scenario
        else:
            scenario_func = random.choice([
                self.generate_graceful_failure_scenario, 
                self.generate_disambiguation_scenario,
                self.generate_contextual_history_scenario
            ])
        
        conversation = [self.create_conversation_turn("user", self.get_random_phrase("greet"))]
        scenario_body = scenario_func()
        if not scenario_body: return None

        if scenario_func == self.generate_chaotic_combo_scenario and random.random() < 0.4:
            injection_type = random.choice(list(self.personality_injects.keys()))
            injection_phrase = random.choice(self.personality_injects[injection_type])
            if len(scenario_body) > 1:
                injection_point = random.randint(1, len(scenario_body) - 1)
                scenario_body.insert(injection_point, self.create_conversation_turn("user", injection_phrase))
            
        conversation.extend(scenario_body)
        
        if scenario_func != self.generate_graceful_failure_scenario:
             conversation.append(self.create_conversation_turn("user", self.get_random_phrase("thank_and_bye")))
             conversation.append(self.create_conversation_turn("assistant", "Rica ederim, başka bir konuda yardımcı olabilir miyim?"))

        for turn in conversation:
            if turn["role"] == "user":
                turn["content"] = self.perturb_user_phrase(turn["content"])

        return conversation

    def create_conversation_turn(self, role, content, tool_calls=None):
        turn = {"role": role, "content": content}
        if tool_calls:
            turn["tool_calls"] = tool_calls
        return turn

    def generate(self, num_samples):
        for _ in range(num_samples):
            scenario_conversation = self.generate_scenario()
            if scenario_conversation:
                self.scenarios.append({"id": f"gm_v3_{uuid.uuid4()}", "conversation": scenario_conversation})
        print(f"{len(self.scenarios)} adet Grandmaster v3 senaryo üretildi.")
        return self.scenarios

    def save_to_json(self, file_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, file_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.scenarios, f, ensure_ascii=False, indent=2)
        print(f"Veri seti başarıyla '{output_path}' dosyasına kaydedildi.")

    def generate_chaotic_combo_scenario(self):
        user_id = random.choice(self.user_ids)
        num_tasks = random.randint(2, 3)
        selected_task_keys = random.sample(list(self.task_pool.keys()), num_tasks)
        tasks = [self.task_pool[key](user_id) for key in selected_task_keys]
        
        user_request = "Merhaba, birkaç şey soracaktım. "
        user_request += " ve ".join([task['user_prompt'] for task in tasks]) + "."
        if random.random() < 0.3: user_request += " Ama sakın hız testi yapma."

        conversation = [self.create_conversation_turn("user", user_request)]
        for task in tasks:
            conversation.extend(task['dialogue_flow'])
        return conversation

    def build_pay_bill_task(self, user_id):
        bill_id = f"F-2024-{user_id}"
        api_response_bill_data = self.mock_api.get_current_bill(user_id, force_unpaid=True)
        validated_response_bill = create_validated_json_response(GetCurrentBillResponse, api_response_bill_data['data'])
        amount = api_response_bill_data["data"]["amount"]
        api_response_pay_data = self.mock_api.pay_bill(bill_id, "credit_card")
        
        return {
            "user_prompt": "faturamı ödemek istiyorum",
            "dialogue_flow": [
                self.create_conversation_turn("assistant", f"Elbette, {user_id} numaralı hattınız için güncel faturanızı kontrol ediyorum.", tool_calls=[{"name": "get_current_bill", "arguments": {"user_id": user_id}}]),
                self.create_conversation_turn("tool", validated_response_bill),
                self.create_conversation_turn("assistant", f"Toplam {amount} TL borcunuz görünüyor. Onaylarsanız ödemeyi gerçekleştiriyorum.", tool_calls=[{"name": "pay_bill", "arguments": {"bill_id": bill_id, "method": "credit_card"}}]),
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
                self.create_conversation_turn("assistant", "Tabii, hemen kalan kullanımlarınızı sorguluyorum.", tool_calls=[{"name": "get_remaining_quotas", "arguments": {"user_id": user_id}}]),
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
                self.create_conversation_turn("assistant", "Anladım, yavaş internet sorununuz için bir arıza kaydı oluşturuyorum.", tool_calls=[{"name": "create_fault_ticket", "arguments": {"user_id": user_id, "issue_description": "İnternet çok yavaş."}}]),
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
                self.create_conversation_turn("assistant", "Elbette, mevcut tüm paketleri sizin için listeliyorum.", tool_calls=[{"name": "get_available_packages", "arguments": {}}]),
                self.create_conversation_turn("tool", validated_response_packages),
                self.create_conversation_turn("assistant", f"Şu anki popüler paketlerimiz: {', '.join(package_names)}. Detaylı bilgi istediğiniz bir paket var mı?")
            ]
        }
    
    def generate_contextual_history_scenario(self):
        user_id = random.choice(self.user_ids)
        conversation = []
        conversation.append(self.create_conversation_turn("user", self.get_random_phrase("report_recurrent_slow_internet")))
        assistant_response = (f"Merhaba, {user_id} numaralı hattınızda bu sorunu tekrar yaşadığınızı anlıyorum ve özür dilerim. Bu sefer standart hız testi adımlarını atlayıp, durumun tekrarladığını belirterek sizin için doğrudan öncelikli bir arıza kaydı oluşturuyorum.")
        tool_call = [{"name": "create_fault_ticket", "arguments": {"user_id": user_id, "issue_description": "Tekrarlayan yavaş internet sorunu. Öncelikli incelenmeli.", "priority": "high"}}]
        conversation.append(self.create_conversation_turn("assistant", assistant_response, tool_calls=tool_call))
        api_response_ticket_data = self.mock_api.create_fault_ticket(user_id, "Tekrarlayan sorun", priority="high")
        validated_response_ticket = create_validated_json_response(CreateFaultTicketResponse, api_response_ticket_data['data'])
        ticket_id = api_response_ticket_data["data"]["ticket_id"]
        conversation.append(self.create_conversation_turn("tool", validated_response_ticket))
        conversation.append(self.create_conversation_turn("assistant", f"Kaydınız {ticket_id} numarasıyla en yüksek öncelikte oluşturuldu. Teknik ekibimiz doğrudan sizinle iletişime geçecektir."))
        return conversation

    def generate_disambiguation_scenario(self):
        user_id = random.choice(self.user_ids)
        conversation = []
        conversation.append(self.create_conversation_turn("user", self.get_random_phrase("request_ambiguous_package")))
        clarifying_question = "Elbette, yardımcı olmak isterim. Hangi paketinizle ilgili işlem yapmak istediğinizi öğrenebilir miyim? Örneğin: İnternet paketiniz mi, TV paketiniz mi?"
        conversation.append(self.create_conversation_turn("assistant", clarifying_question))
        conversation.append(self.create_conversation_turn("user", self.get_random_phrase("clarify_internet_package")))
        assistant_response_after_clarification = "Anladım, internet paketinizle ilgili mevcut seçenekleri hemen listeliyorum."
        tool_call_packages = [{"name": "get_available_packages", "arguments": {}}]
        conversation.append(self.create_conversation_turn("assistant", assistant_response_after_clarification, tool_calls=tool_call_packages))
        api_response_packages_data = self.mock_api.get_available_packages()
        validated_response_packages = create_validated_json_response(GetAvailablePackagesResponse, api_response_packages_data['data'])
        conversation.append(self.create_conversation_turn("tool", validated_response_packages))
        package_names = [pkg['name'] for pkg in api_response_packages_data['data']['packages']]
        final_response = f"Sizin için uygun olabilecek internet paketlerimiz şunlar: {', '.join(package_names)}. Hangisiyle ilgilenirsiniz?"
        conversation.append(self.create_conversation_turn("assistant", final_response))
        return conversation

    def generate_graceful_failure_scenario(self):
        conversation = []
        conversation.append(self.create_conversation_turn("user", self.get_random_phrase("request_out_of_scope")))
        failure_response = "Üzgünüm, ben size yalnızca telekomünikasyon hizmetlerinizle ilgili konularda yardımcı olmak üzere tasarlanmış bir yapay zeka asistanıyım. Bu isteğinizi maalesef yerine getiremiyorum. Farklı bir konuda size nasıl destek olabilirim?"
        conversation.append(self.create_conversation_turn("assistant", failure_response))
        return conversation


if __name__ == '__main__':
    generator = GrandmasterDatasetGeneratorV3()
    grandmaster_data = generator.generate(10000)
    generator.save_to_json("grandmaster_dataset_10k_v3.json") 