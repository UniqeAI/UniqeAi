# -*- coding: utf-8 -*-
"""
Merkezi Araç Tanımlama Dosyası v2.0 (Schema-Synchronized)

Bu script, telekom_api_schema.py dosyasını referans alarak LLM'lerin (özellikle Llama-3 serisi)
anlayacağı standart "araç" (tool) formatını oluşturur. Bu sürüm, `telekom_api_schema.py`
içindeki `API_MAP` ile tam senkronize edilmiştir.

- Tek ve Doğru Kaynak: API şeması değiştiğinde, önce `telekom_api_schema.py` güncellenmeli,
  sonra bu dosya onunla senkronize edilmelidir.
- Tutarlılık: Projenin tüm aşamalarında aynı araç setinin kullanılmasını garanti eder.
"""

import json
import sys
from pathlib import Path

def get_resource_path(relative_path: str) -> Path:
    """
    Kaynak dosyalarına (örn: JSON) erişmek için mutlak bir yol döndürür.
    Bu fonksiyon, hem normal script olarak çalışırken hem de PyInstaller ile
    paketlenmiş bir .exe olarak çalışırken doğru yolu bulur.
    """
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).resolve().parent.parent
    return base_path / relative_path

FAKE_API_RESPONSES_PATH = get_resource_path("evaluation/fake_api_responses.json")

MOCK_DB_RULES = {
    "invalid_user_ids": [9999, 1000],
    "users_with_no_bill": [8001, 8002],
    "paid_bill_ids": ["F-2025-PAID"],
    "ineligible_users_for_gamer_pro": [7001, 7002]
}

def get_tool_definitions():
    """
    Modelin kullanabileceği araçların Llama-3 formatında tanımlarını döndürür.
    Bu liste, `telekom_api_schema.py`'deki `API_MAP` ile tam senkronizedir.
    """
    return [
        # === 1. Fatura & Ödeme İşlemleri ===
        {
            "type": "function",
            "function": {
                "name": "get_current_bill",
                "description": "Bir kullanıcının mevcut, ödenmemiş faturasını getirir.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Faturası sorgulanacak kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_past_bills",
                "description": "Bir kullanıcının geçmişe dönük ödenmiş faturalarını listeler.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Geçmiş faturaları listelenecek kullanıcının numerik ID'si."},
                        "limit": {"type": "integer", "description": "Kaç adet geçmiş faturanın getirileceği.", "default": 3}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "pay_bill",
                "description": "Bir fatura ID'si kullanarak fatura ödeme işlemini başlatır.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "bill_id": {"type": "string", "description": "Ödenecek faturanın benzersiz kimliği."},
                        "method": {"type": "string", "description": "Ödeme yöntemi.", "enum": ["credit_card", "bank_transfer"]}
                    },
                    "required": ["bill_id", "method"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_payment_history",
                "description": "Kullanıcının geçmiş ödeme işlemlerini listeler.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Ödeme geçmişi sorgulanacak kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "setup_autopay",
                "description": "Otomatik fatura ödeme talimatı oluşturur veya günceller.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Otomatik ödeme ayarlanacak kullanıcının numerik ID'si."},
                        "payment_method": {"type": "string", "description": "Otomatik ödeme için kullanılacak kart veya hesap bilgisi."}
                    },
                    "required": ["user_id", "payment_method"]
                }
            }
        },
        # === 2. Paket & Tarife Yönetimi ===
        {
            "type": "function",
            "function": {
                "name": "get_customer_package",
                "description": "Kullanıcının mevcut tarife ve paket bilgilerini getirir.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Paketi sorgulanacak kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_available_packages",
                "description": "Kullanıcının geçiş yapabileceği mevcut tüm tarife ve paketleri listeler.",
                "parameters": {"type": "object", "properties": {}}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "change_package",
                "description": "Kullanıcının mevcut paketini yeni bir paketle değiştirir.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Paketi değiştirilecek kullanıcının numerik ID'si."},
                        "new_package_name": {"type": "string", "description": "Geçiş yapılacak yeni paketin tam adı."}
                    },
                    "required": ["user_id", "new_package_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_remaining_quotas",
                "description": "Kullanıcının kalan internet, dakika ve SMS kotalarını sorgular.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Kotaları sorgulanacak kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_package_details",
                "description": "Belirli bir paketin tüm detaylarını getirir.",
                "parameters": {
                    "type": "object",
                    "properties": {"package_name": {"type": "string", "description": "Detayları istenen paketin tam adı."}},
                    "required": ["package_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "enable_roaming",
                "description": "Kullanıcının hattı için yurt dışı kullanımını (roaming) aktif eder.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Roaming açılacak kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        # === 3. Teknik Destek & Arıza Kaydı ===
        {
            "type": "function",
            "function": {
                "name": "check_network_status",
                "description": "Belirli bir bölgedeki ağ durumunu ve aktif arızaları kontrol eder.",
                "parameters": {
                    "type": "object",
                    "properties": {"region": {"type": "string", "description": "Kontrol edilecek bölge adı."}},
                    "required": ["region"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_fault_ticket",
                "description": "Bir sorun için teknik destek (arıza) kaydı oluşturur.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Adına kayıt açılacak kullanıcının numerik ID'si."},
                        "issue_description": {"type": "string", "description": "Sorunun kısa açıklaması."}
                    },
                    "required": ["user_id", "issue_description"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "close_fault_ticket",
                "description": "Açık bir arıza kaydını kapatır.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string", "description": "Kapatılacak arıza kaydının benzersiz kimliği."},
                        "resolution_notes": {"type": "string", "description": "Sorunun nasıl çözüldüğüne dair kapanış notları."}
                    },
                    "required": ["ticket_id", "resolution_notes"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_users_tickets",
                "description": "Bir kullanıcıya ait tüm arıza kayıtlarını listeler.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Arıza kayıtları listelenecek kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_fault_ticket_status",
                "description": "Bir arıza kaydının mevcut durumunu sorgular.",
                "parameters": {
                    "type": "object",
                    "properties": {"ticket_id": {"type": "string", "description": "Durumu sorgulanacak arıza kaydının benzersiz kimliği."}},
                    "required": ["ticket_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "test_internet_speed",
                "description": "Kullanıcının internet bağlantı hızını test eder.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Hız testi yapılacak kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        # === 4. Hesap & Hat Yönetimi ===
        {
            "type": "function",
            "function": {
                "name": "get_customer_profile",
                "description": "Kullanıcının detaylı profil bilgilerini getirir.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Profil bilgileri getirilen kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_customer_contact",
                "description": "Kullanıcının iletişim bilgilerini günceller.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Bilgisi güncellenecek kullanıcının numerik ID'si."},
                        "contact_type": {"type": "string", "description": "Güncellenecek iletişim türü.", "enum": ["email", "address"]},
                        "new_value": {"type": "string", "description": "Yeni e-posta adresi veya tam adres."}
                    },
                    "required": ["user_id", "contact_type", "new_value"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "suspend_line",
                "description": "Kullanıcının hattını geçici olarak askıya alır.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Hattı askıya alınacak kullanıcının numerik ID'si."},
                        "line_number": {"type": "string", "description": "Askıya alınacak telefon hattı numarası."},
                        "reason": {"type": "string", "description": "Hattın askıya alınma sebebi."}
                    },
                    "required": ["user_id", "line_number", "reason"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "reactivate_line",
                "description": "Askıya alınmış bir hattı tekrar aktif hale getirir.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Hattı yeniden aktif edilecek kullanıcının numerik ID'si."},
                        "line_number": {"type": "string", "description": "Yeniden aktif edilecek telefon hattı numarası."}
                    },
                    "required": ["user_id", "line_number"]
                }
            }
        },
        # === 5. Gelişmiş & Acil Durum Servisleri ===
        {
            "type": "function",
            "function": {
                "name": "activate_emergency_service",
                "description": "Acil durumlarda kullanıcıya özel limitsiz kullanım hakkı tanır.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Acil durum servisi aktive edilecek kullanıcının numerik ID'si."},
                        "emergency_type": {"type": "string", "description": "Acil durumun türü (örn: 'deprem', 'sel')."}
                    },
                    "required": ["user_id", "emergency_type"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "check_5g_coverage",
                "description": "Kullanıcının konumundaki 5G kapsama durumunu kontrol eder.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "5G kapsamı kontrol edilecek kullanıcının numerik ID'si."},
                        "location": {"type": "string", "description": "Kontrol edilecek konum."}
                    },
                    "required": ["user_id", "location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_cultural_context",
                "description": "Kullanıcının kültürel geçmişine göre servis adaptasyonları önerir.",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "description": "Kültürel analizi yapılacak kullanıcının numerik ID'si."}},
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_learning_adaptation",
                "description": "Modelin kullanıcı etkileşimlerinden öğrendiği tercihleri günceller.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "Öğrenme profili güncellenecek kullanıcının numerik ID'si."},
                        "learned_preferences": {"type": "object", "description": "Kullanıcının yeni öğrenilen tercihleri (JSON formatında)."}
                    },
                    "required": ["user_id", "learned_preferences"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "generate_creative_analysis",
                "description": "Karmaşık problemler için yaratıcı çözüm önerileri üretir.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "problem_description": {"type": "string", "description": "Analiz edilecek problemin açıklaması."},
                        "innovation_level": {"type": "string", "description": "İnovasyon seviyesi.", "enum": ["basic", "advanced", "strategic"]}
                    },
                    "required": ["problem_description", "innovation_level"]
                }
            }
        }
    ]

def get_tool_response(function_name: str, params: dict) -> str:
    """
    Verilen bir fonksiyon adı ve parametreler için sahte ama akıllı bir yanıt döndürür.
    Bu, gerçek bir API'ye ihtiyaç duymadan farklı senaryoları test etmemizi sağlar.
    fake_api_responses.json dosyasını okur ve parametrelere göre mantıklı bir
    yanıt (başarı veya hata) seçer.
    """
    try:
        with open(FAKE_API_RESPONSES_PATH, 'r', encoding='utf-8') as f:
            responses = json.load(f)

        if function_name not in responses:
            return json.dumps({"success": False, "error": f"Bilinmeyen fonksiyon: {function_name}"}, ensure_ascii=False, indent=2)

        response_template = responses[function_name].get("success")
        
        user_id = params.get("user_id")
        if function_name == "get_current_bill" and user_id in MOCK_DB_RULES["users_with_no_bill"]:
            response_template = responses[function_name]["error"]["NO_BILL"]

        elif function_name == "pay_bill":
            bill_id = params.get("bill_id")
            # Sadece daha önce ödenmiş faturalar için hata ver
            if bill_id in MOCK_DB_RULES["paid_bill_ids"]:
                response_template = responses[function_name]["error"]["BILL_NOT_FOUND"]

        elif function_name == "change_package":
            package_name = params.get("new_package_name")
            if package_name == "Gamer Pro" and user_id in MOCK_DB_RULES["ineligible_users_for_gamer_pro"]:
                 response_template = responses[function_name]["error"]["INELIGIBLE_FOR_PACKAGE"]

        if response_template is None:
             return json.dumps({"success": False, "error": f"{function_name} için uygun yanıt şablonu bulunamadı."}, ensure_ascii=False, indent=2)

        response_data = response_template.copy()

        if "data" in response_data and response_data["data"] is not None:
            for key, value in params.items():
                if key in response_data["data"]:
                    response_data["data"][key] = value

        return json.dumps(response_data, ensure_ascii=False, indent=2)

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        return json.dumps({"success": False, "error": f"API yanıtı işlenirken hata oluştu: {e}"}, ensure_ascii=False, indent=2)
