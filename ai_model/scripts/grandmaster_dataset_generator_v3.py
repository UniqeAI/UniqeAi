#!/usr/bin/env python3
"""
GRANDMASTER VERİ SETİ OLUŞTURUCU V3 - OLAĞANÜSTÜ MODEL HEDEFİ
============================================================

Bu script, 'master' seviyesi script'in üzerine inşa edilmiş olup,
modele aşağıdaki 'Grandmaster' yeteneklerini kazandırmayı hedefler:
- Duygusal Zeka ve Ton Ayarlama
- Derin Koşullu Mantık ve Çoklu Bağımlılıklar
- Proaktif ve Tahmine Dayalı Asistanlık
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from faker import Faker
from pydantic import BaseModel, ValidationError
import sys
import os

# --- Proje Yolu Yapılandırması ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
sys.path.append(PROJECT_ROOT)

# --- Telekom API Şeması ---
try:
    from telekom_api_schema import (
        PayBillResponse,
        SetupAutopayResponse,
        TestInternetSpeedResponse,
        CreateFaultTicketResponse,
        GetCurrentBillResponse,
        ServiceItem,
        GetRemainingQuotasResponse,
        UsagePercentage,
        EnableRoamingResponse,
        GetAvailablePackagesResponse,
        AvailablePackageItem,
        AvailablePackageFeatures,
        ChangePackageResponse,
    )
except ImportError:
    print("HATA: telekom_api_schema.py bulunamadı. Lütfen dosyanın varlığını kontrol edin.")
    sys.exit(1)

# --- Faker Kurulumu ---
fake = Faker('tr_TR')

class GrandmasterDatasetGenerator:
    """
    Duygusal zeka, koşullu mantık ve proaktif yeteneklere sahip
    Grandmaster seviyesi veri seti oluşturucu.
    """
    
    def __init__(self):
        # API fonksiyonları ve ilgili senaryo üreticileri
        self.api_functions = {}
        prefix = '_generate_'
        suffix = '_scenario'
        for func_name in dir(self):
            if func_name.startswith(prefix) and func_name.endswith(suffix):
                key = func_name[len(prefix):-len(suffix)]
                self.api_functions[key] = getattr(self, func_name)
        
        # GRANDMASTER YETENEKLERİ
        self.user_emotions = {
            'annoyed': {
                "starters": ["Yeter artık, bir sorunum var!", "Sinirlerim bozuldu, yardım edin.", "Neden sürekli aynı sorunla karşılaşıyorum?"],
                "assistant_tone": {
                    "opening": "Yaşadığınız olumsuz deneyimden dolayı gerçekten üzgünüm. Konuyu hemen inceliyorum ve size yardımcı olmak için buradayım.",
                    "closing": "Umarım sunduğum çözümle durumu telafi edebilmişimdir. Başka bir konuda yardımcı olabilir miyim?"
                }
            },
            'neutral': {
                "starters": ["Merhaba, bilgi alabilir miyim?", "Bir işlem yapmak istiyorum.", "Nasılsınız?"],
                "assistant_tone": {
                    "opening": "Elbette, size nasıl yardımcı olabilirim?",
                    "closing": "İşleminiz tamamlandı. Başka bir konuda yardımcı olabilir miyim?"
                }
            },
            'happy': {
                "starters": ["Harika bir hizmet!", "Çok memnunum, bir sorum olacak.", "Merhaba, her şey yolunda mı?"],
                "assistant_tone": {
                    "opening": "Memnuniyetinizi duyduğuma sevindim! Size nasıl yardımcı olabilirim?",
                    "closing": "Yardımcı olabildiğime sevindim! İyi günler dilerim."
                }
            }
        }
        
        self.proactive_suggestions = {
            'pay_bill': 'setup_autopay',
            'suspend_line': 'enable_roaming'
        }
        
        self.error_scenarios = {
            'INVALID_USER': {'message': 'Kullanıcı bulunamadı', 'details': 'Girilen kullanıcı ID sistemde kayıtlı değil'},
            'PAYMENT_METHOD_NOT_FOUND': {'message': 'Ödeme yöntemi bulunamadı', 'details': 'Sistemde kayıtlı bir ödeme yönteminiz bulunmuyor'},
            'LINE_ALREADY_SUSPENDED': {'message': 'Hat zaten dondurulmuş', 'details': 'Bu hat daha önce dondurulduğu için tekrar dondurulamaz.'},
            'OUTSTANDING_BILL': {'message': 'Ödenmemiş fatura mevcut', 'details': 'İşlem yapabilmek için ödenmemiş faturanızı kapatmanız gerekmektedir.'},
            'COMMITMENT_EXISTS': {'message': 'Taahhüt bulunmaktadır', 'details': 'Hattınızda aktif bir taahhüt bulunduğu için bu işlem yapılamaz.'},
            'BILL_NOT_FOUND': {'message': 'Fatura bulunamadı', 'details': 'Belirtilen fatura ID sistemde mevcut değil veya daha önce ödenmiş.'},
            'INELIGIBLE_FOR_PACKAGE': {'message': 'Kullanıcı bu paket için uygun değil', 'details': 'Bu paket için gerekli kriterleri sağlamıyorsunuz.'}
        }

        self.chit_chat_dialogs = [
            [
                {"rol": "kullanici", "icerik": "Bu faturalar neden hep bu kadar karışık oluyor?"},
                {"rol": "asistan", "icerik": "Fatura detaylarının bazen kafa karıştırıcı olabildiğinin farkındayım. Genellikle ana hizmet bedeli, vergiler ve ek kullanımlar gibi birden fazla kalem içerdiği için karmaşık görünebilir. Faturanızda anlamadığınız belirli bir kısım varsa, açıklamak için yardımcı olabilirim."}
            ],
            [
                {"rol": "kullanici", "icerik": "Teşekkür ederim, sorunum çözüldü."},
                {"rol": "asistan", "icerik": "Rica ederim, yardımcı olabildiğime sevindim! Telekom'u tercih ettiğiniz için teşekkür ederiz. Başka bir konuda yardıma ihtiyacınız olursa çekinmeden tekrar ulaşabilirsiniz. İyi günler dilerim!"}
            ]
        ]

    # --- SENARYO ÜRETİCİ METODLARI (STRATEJİ 4 & 6 ODAKLI) ---

    def _generate_natural_chit_chat_scenario(self, scenario_type: str, emotion: str) -> Optional[Dict]:
        """STRATEJİ: Doğal Sohbet - API çağrısı gerektirmeyen durumlar."""
        selected_dialog = random.choice(self.chit_chat_dialogs)
        return {"veri_id": f"GM_CHITCHAT_{uuid.uuid4()}", "donguler": selected_dialog}

    def _generate_change_package_scenario(self, scenario_type: str, emotion: str) -> Optional[Dict]:
        """STRATEJİ 4: Koşullu Mantık & Hata Yönetimi - Tarife değişikliği."""
        user_id = self._generate_realistic_user_id()
        assistant_tone = self.user_emotions[emotion]['assistant_tone']
        user_starter = random.choice(self.user_emotions['neutral']['starters'])
        
        # Bu senaryo birden fazla hata durumunu kapsayabilir
        error_type = random.choice(['COMMITMENT_EXISTS', 'INELIGIBLE_FOR_PACKAGE'])

        if scenario_type == 'error_handling':
            package_name = "Gamer Pro" if error_type == 'COMMITMENT_EXISTS' else "Memur Özel"
            
            dialog = [
                {"rol": "kullanici", "icerik": f"{user_starter} Merhaba, '{package_name}' paketine geçmek istiyorum. ID: {user_id}"},
                {"rol": "asistan", "icerik": f"{assistant_tone['opening']} Elbette, talebinizi hemen kontrol ediyorum."}
            ]
            
            error_response = {"success": False, "error": self.error_scenarios[error_type]}
            dialog.extend(self._create_tool_call_step("change_package", {"user_id": user_id, "new_package_name": package_name}, error_response))

            if error_type == 'COMMITMENT_EXISTS':
                dialog.append({"rol": "asistan", "icerik": "Yaptığım kontrolde mevcut paketinizde aktif bir taahhüt olduğunu gördüm. Bu nedenle şu anda paket değişikliği yapamıyoruz. Taahhüt detaylarınızı ve ne zaman biteceğini öğrenmek ister misiniz?"})
            else: # INELIGIBLE_FOR_PACKAGE
                dialog.append({"rol": "asistan", "icerik": "Anladığım kadarıyla 'Memur Özel' tarifesi, belirli bir meslek grubuna özel olduğu için şu anki aboneliğinizle bu pakete geçiş yapamıyorsunuz. Size özel olarak geçebileceğiniz diğer kampanyalı paketleri listelememi ister misiniz?"})
            
            return {"veri_id": f"GM_ERROR_{error_type}_{uuid.uuid4()}", "donguler": dialog}
        return None

    def _generate_enable_roaming_scenario(self, scenario_type: str, emotion: str) -> Optional[Dict]:
        """STRATEJİ 6: Proaktif Yardım - Roaming açma ve paket önerme."""
        user_id = self._generate_realistic_user_id()
        assistant_tone = self.user_emotions['happy']['assistant_tone']

        if scenario_type == 'proactive_suggestion':
            dialog = [
                {"rol": "kullanici", "icerik": f"Selam, haftaya İtalya'ya gidiyorum. Hattımı yurt dışında kullanıma açabilir misiniz? ID: {user_id}"},
                {"rol": "asistan", "icerik": f"{assistant_tone['opening']} Harika bir seyahat sizi bekliyor! Hattınızı hemen yurt dışı kullanımına açıyorum."}
            ]
            
            dialog.extend(self._create_tool_call_step("enable_roaming", {"user_id": user_id}, EnableRoamingResponse(
                user_id=user_id, roaming_enabled=True, activation_time=datetime.now().isoformat(), daily_fee=25.0, data_package="Standart Roaming"
            )))
            
            dialog.append({
                "rol": "asistan",
                "icerik": "Hattınız yurt dışı kullanımına başarıyla açıldı. Standart dolaşım ücretlerinin yüksek olabileceğini hatırlatmak isterim. Seyahatiniz boyunca rahat etmeniz için uygun fiyatlı yurt dışı internet paketlerimiz bulunuyor. İncelemek ister misiniz?"
            })
            
            return {"veri_id": f"GM_PROACTIVE_ROAMING_{uuid.uuid4()}", "donguler": dialog}
        return None

    def _generate_pay_bill_scenario(self, scenario_type: str, emotion: str) -> Optional[Dict]:
        """pay_bill için Grandmaster senaryosu oluşturur."""
        user_id = self._generate_realistic_user_id()
        bill_id = self._generate_realistic_bill_id()
        amount = round(random.uniform(80.0, 350.0), 2)
        assistant_tone = self.user_emotions[emotion]['assistant_tone']
        user_starter = random.choice(self.user_emotions[emotion]['starters'])

        if scenario_type == 'proactive_suggestion':
            dialog = [
                {"rol": "kullanici", "icerik": f"{user_starter} Faturamı ödemek istiyorum. ID: {user_id}, Tutar: {amount} TL."},
                {"rol": "asistan", "icerik": f"{assistant_tone['opening']} Elbette, ödeme işleminizi hemen gerçekleştiriyorum."}
            ]
            dialog.extend(self._create_tool_call_step("pay_bill", {"user_id": user_id, "bill_id": bill_id, "amount": amount}, PayBillResponse(
                transaction_id=f"T-{uuid.uuid4()}", bill_id=bill_id, amount=amount, method="credit_card", status="Ödeme başarılı", timestamp=datetime.now().isoformat()
            )))
            dialog.append({"rol": "asistan", "icerik": f"Ödemeniz başarıyla alındı. Tekrarlayan fatura ödemelerinizi kolaylaştırmak için otomatik ödeme talimatı vermek ister misiniz? Bu sayede faturalarınız son ödeme tarihinde otomatik olarak ödenir."})
            
            # Tool Chaining adımı geri eklendi
            dialog.append({"rol": "kullanici", "icerik": "Evet, kulağa harika geliyor. Ayarlayalım lütfen."})
            dialog.extend(self._create_tool_call_step("setup_autopay", {"user_id": user_id, "payment_method": "credit_card"}, SetupAutopayResponse(
                user_id=user_id, autopay_enabled=True, payment_method="credit_card", next_payment_date=(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            )))
            dialog.append({"rol": "asistan", "icerik": "Otomatik ödeme talimatınız başarıyla oluşturuldu. Gelecek ay faturanız otomatik olarak ödenecektir."})

            return {"veri_id": f"GM_PROACTIVE_CHAIN_{uuid.uuid4()}", "donguler": dialog}

        elif scenario_type == 'error_handling': # Hata Yönetimi Senaryosu
            bill_id_to_pay = f"F-{random.randint(100000, 999999)}"
            dialog = [
                 {"rol": "kullanici", "icerik": f"{bill_id_to_pay} numaralı faturamı ödemek istiyorum."},
                 {"rol": "asistan", "icerik": f"Hemen {bill_id_to_pay} numaralı faturanız için ödeme işlemini başlatıyorum."}
            ]
            
            error_response = {"success": False, "error": self.error_scenarios['BILL_NOT_FOUND']}
            dialog.extend(self._create_tool_call_step("pay_bill", {"bill_id": bill_id_to_pay, "amount": amount, "user_id": user_id}, error_response))
            
            dialog.append({"rol": "asistan", "icerik": "Üzgünüm, belirttiğiniz fatura numarasını sistemde bulamadım ya da bu fatura daha önceden ödenmiş olabilir. Lütfen fatura numarasını kontrol eder misiniz? Dilerseniz müşteri numaranız üzerinden güncel borcunuzu sorgulayabilirim."})
            
            return {"veri_id": f"GM_ERROR_BILL_NOT_FOUND_{uuid.uuid4()}", "donguler": dialog}
        
        return None

    def _generate_create_fault_ticket_scenario(self, scenario_type: str, emotion: str) -> Optional[Dict]:
        """create_fault_ticket için Grandmaster senaryosu oluşturur (Problem Tespiti Zinciri)."""
        user_id = self._generate_realistic_user_id()
        assistant_tone = self.user_emotions['annoyed']['assistant_tone']
        user_starter = random.choice(self.user_emotions['annoyed']['starters'])

        if scenario_type == 'complex_chaining': # Tool Chaining geri eklendi
            dialog = [
                {"rol": "kullanici", "icerik": f"{user_starter} İnternetim çok yavaş, neredeyse hiçbir şey açılmıyor! ID: {user_id}"},
                {"rol": "asistan", "icerik": f"{assistant_tone['opening']} Yaşadığınız yavaşlık sorununu anlıyorum ve hemen kontrol sağlıyorum. Öncelikle mevcut internet hızınızı test edelim."}
            ]
            
            dialog.extend(self._create_tool_call_step("test_internet_speed", {"user_id": user_id}, TestInternetSpeedResponse(
                user_id=user_id, download_speed_mbps=2.5, upload_speed_mbps=0.8, ping_ms=150, test_timestamp=datetime.now().isoformat(), test_server="Istanbul", quality_rating="Poor"
            )))
            
            dialog.append({"rol": "asistan", "icerik": "Hız testini tamamladım. İndirme hızınız 2.5 Mbps olarak ölçüldü, bu beklenen değerin oldukça altında. Bu durum normal değil. Sizin için hemen bir arıza kaydı oluşturuyorum."})
            
            ticket_id = f"TKT-{uuid.uuid4()}"
            issue_desc = "Kullanıcı internet hızının çok yavaş olduğunu bildirdi. Yapılan testte hız 2.5 Mbps olarak ölçüldü, genel bir yavaşlık mevcut."
            dialog.extend(self._create_tool_call_step("create_fault_ticket", {"user_id": user_id, "issue_description": issue_desc, "category": "internet_speed"}, CreateFaultTicketResponse(
                ticket_id=ticket_id, user_id=user_id, issue_description=issue_desc, category="internet_speed", priority="high", status="Açık", created_at=datetime.now().isoformat(), estimated_resolution="24 saat içinde"
            )))

            dialog.append({"rol": "asistan", "icerik": f"Arıza kaydınız {ticket_id} numarasıyla oluşturulmuştur. Teknik ekiplerimiz en kısa sürede inceleyip sorunu çözecektir. Tahmini çözüm süresi 24 saattir. Sabrınız için teşekkür ederiz."})
            
            return {"veri_id": f"GM_DIAGNOSE_CHAIN_{uuid.uuid4()}", "donguler": dialog}
            
        return None

    def _generate_suspend_line_scenario(self, scenario_type: str, emotion: str) -> Optional[Dict]:
        """suspend_line için Grandmaster senaryosu oluşturur."""
        user_id = self._generate_realistic_user_id()
        line_number = fake.msisdn()
        assistant_tone = self.user_emotions[emotion]['assistant_tone']
        user_starter = random.choice(self.user_emotions[emotion]['starters'])

        if scenario_type == 'error_handling':
            dialog = [
                {"rol": "kullanici", "icerik": f"{user_starter} Hattımı geçici olarak dondurmak istiyorum. Numaram: {line_number}"},
                {"rol": "asistan", "icerik": f"{assistant_tone['opening']} Tabii, talebinizi aldım. Hattınızı dondurmadan önce kontrol etmem gereken bir nokta var."}
            ]
            
            error_response = {"success": False, "error": self.error_scenarios['OUTSTANDING_BILL']}
            dialog.extend(self._create_tool_call_step("suspend_line", {"user_id": user_id, "line_number": line_number}, error_response))

            dialog.append({"rol": "asistan", "icerik": "Kontrollerim sonucunda, sistemde adınıza kayıtlı ödenmemiş bir fatura görünüyor. Mevzuat gereği, hattınızı dondurabilmemiz için öncelikle bu faturayı ödemeniz gerekmektedir. Ödeme sonrası işlemi tekrar deneyebiliriz."})
            
            return {"veri_id": f"GM_ERROR_{uuid.uuid4()}", "donguler": dialog}

        return None

    # ... (Diğer helper metodlar: _generate_realistic_user_id, _create_api_response vb. master script'inden alınabilir)

    def _generate_get_current_bill_scenario(self, scenario_type: str, emotion: str) -> Optional[Dict]:
        """get_current_bill için Grandmaster senaryosu oluşturur."""
        user_id = self._generate_realistic_user_id()
        assistant_tone = self.user_emotions[emotion]['assistant_tone']

        if scenario_type == 'complex_chaining':
            user_starter = random.choice(self.user_emotions[emotion]['starters'])
            
            dialog = [
                {"rol": "kullanici", "icerik": f"{user_starter} Faturam çok yüksek geldi, nedenini öğrenebilir miyim? ID: {user_id}"},
                {"rol": "asistan", "icerik": f"{assistant_tone['opening']} Hemen faturanızı detaylı olarak inceliyorum."}
            ]
            
            dialog.extend(self._create_tool_call_step("get_current_bill", {"user_id": user_id}, GetCurrentBillResponse(
                bill_id=self._generate_realistic_bill_id(),
                user_id=user_id,
                amount=195.50,
                currency="TRY",
                due_date=(datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
                bill_date=datetime.now().strftime('%Y-%m-%d'),
                status="unpaid",
                services=[ServiceItem(service_name="Mega İnternet", amount=95.50), ServiceItem(service_name="Aşım Ücreti", amount=100.00)]
            )))
            
            dialog.append({"rol": "asistan", "icerik": "Faturanızı inceledim, 100 TL'lik bir aşım ücreti görünüyor. Bunun nedenini anlamak için kullanım kotalarınızı kontrol ediyorum."})
            
            # Tool Chaining adımı geri eklendi
            dialog.extend(self._create_tool_call_step("get_remaining_quotas", {"user_id": user_id}, GetRemainingQuotasResponse(
                internet_remaining_gb=0,
                voice_remaining_minutes=500,
                sms_remaining=1000,
                period_end=(datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
                usage_percentage=UsagePercentage(internet=100, voice=50, sms=0)
            )))

            dialog.append({"rol": "asistan", "icerik": "Teyit ettim, internet kotanız tamamen bittiği için aşım ücreti uygulanmış. Gelecekte bu durumu yaşamamanız için daha yüksek kotalı paketlerimizi listeleyebilirim. İncelemek ister misiniz?"})
            
            return {"veri_id": f"GM_CHAIN_ANALYSIS_{uuid.uuid4()}", "donguler": dialog}

        return None
        
    def generate_grandmaster_dataset(self, total_samples: int) -> List[Dict]:
        """Belirtilen sayıda Grandmaster senaryo üretir."""
        dataset = []
        function_list = list(self.api_functions.keys())
        
        print(f"🚀 Grandmaster V3 veri seti oluşturuluyor...")
        print(f"📊 Hedef: {total_samples} örnek")
        
        while len(dataset) < total_samples:
            try:
                # Rastgele bir fonksiyon ve senaryo tipi seç
                func_name = random.choice(function_list)
                generator_func = self.api_functions[func_name]
                
                scenario_type = random.choice(['simple_success', 'complex_chaining', 'error_handling', 'proactive_suggestion', 'emotional_response'])
                emotion = random.choice(list(self.user_emotions.keys()))

                scenario = generator_func(scenario_type=scenario_type, emotion=emotion)
                
                if scenario and scenario not in dataset:
                    dataset.append(scenario)
                    if len(dataset) % 100 == 0:
                        print(f"📈 İlerleme: {len(dataset)} / {total_samples} örnek oluşturuldu...")

            except Exception as e:
                print(f"❌ Üretim sırasında hata: {e}")
                continue
        
        print(f"✅ Toplam {len(dataset)} örnek oluşturuldu!")
        return dataset

    # Diğer fonksiyonlar için _generate_..._scenario metodları buraya eklenecek.
    # Bu sadece bir başlangıç ve yapı iskeletidir.

    # Helper metodlar (master script'ten taşınacak)
    def _generate_realistic_user_id(self) -> int: return random.randint(1000, 9999)
    def _generate_realistic_bill_id(self) -> str: return f"F-2024-{random.randint(1000, 9999)}"
    def _create_tool_call_step(self, func_name: str, params: Dict, response_data: Union[BaseModel, Dict]) -> List[Dict]:
        """Bir araç çağrımı ve cevabı için standart diyalog adımları oluşturur."""
        response_str = ""
        try:
            if isinstance(response_data, BaseModel):
                validated_response = response_data.model_dump(exclude_none=True)
                response_str = json.dumps(validated_response, ensure_ascii=False)
            elif isinstance(response_data, dict):
                response_str = json.dumps(response_data, ensure_ascii=False)
            else:
                raise TypeError("response_data must be a Pydantic model or a dictionary.")

        except (ValidationError, TypeError) as e:
            print(f"Schema Hatası veya Tip Hatası: {func_name} - {e}")
            response_str = json.dumps({"success": False, "error": {"code": "GENERATION_ERROR", "message": str(e)}}, ensure_ascii=False)
            
        return [
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": func_name, "parametreler": params}]},
            {"rol": "arac", "icerik": response_str}
        ]

    def save_dataset(self, dataset: List[Dict], filename: str):
        """Veri setini dosyaya kaydeder."""
        output_dir = os.path.join(PROJECT_ROOT, "ai_model", "data")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        print(f"✅ Veri seti kaydedildi: {filepath}")

if __name__ == "__main__":
    generator = GrandmasterDatasetGenerator()
    
    # Hedeflenen toplam örnek sayısı
    TARGET_COUNT = 2500
    
    # Grandmaster veri setini oluştur
    final_dataset = generator.generate_grandmaster_dataset(TARGET_COUNT)
    
    # Dosyaya kaydet
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"grandmaster_dataset_v3_{timestamp}.json"
    generator.save_dataset(final_dataset, filename)
    
    print(f"🎉 Grandmaster V3 veri seti başarıyla oluşturuldu!")
    print(f"📁 Dosya: {filename}")
    print(f"📊 Toplam örnek sayısı: {len(final_dataset)}") 