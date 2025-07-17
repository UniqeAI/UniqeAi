# -*- coding: utf-8 -*-
"""
Merkezi Araç Tanımlama Dosyası (Central Tool Definitions)

Bu script, telekom_api_schema.py dosyasını okur ve LLM'lerin (özellikle Llama-3 serisi)
anlayacağı standart "araç" (tool) formatına dönüştürür.

Bu merkezi yaklaşımın faydaları:
- Tek ve Doğru Kaynak: API şeması değiştiğinde, sadece `telekom_api_schema.py`
  dosyasını güncellemek yeterlidir. Bu dosya, değişiklikleri otomatik olarak yansıtır.
- Tutarlılık: Hem eğitim, hem test hem de canlıya çıkma (production) aşamalarında
  aynı araç tanımının kullanılmasını garanti eder.
- Okunabilirlik: Araçların ne işe yaradığını ve hangi parametreleri aldığını
  açıkça belirtir.
"""

# Şu an için, fonksiyonları ve parametrelerini manuel olarak tanımlıyoruz.
# Gelecekte, telekom_api_schema.py'deki Pydantic modellerini ve docstring'leri
# okuyarak bu listeyi dinamik olarak üreten bir mekanizma eklenebilir.

# Bu yapı, OpenAI'nin ve Hugging Face'in tool-calling standartlarına uygundur.

import json
import sys
from pathlib import Path

# --- YENİ: Paketlenmiş Uygulama için Sağlamlaştırılmış Yol Yönetimi ---
def get_resource_path(relative_path: str) -> Path:
    """
    Kaynak dosyalarına (örn: JSON) erişmek için mutlak bir yol döndürür.
    Bu fonksiyon, hem normal script olarak çalışırken hem de PyInstaller ile
    paketlenmiş bir .exe olarak çalışırken doğru yolu bulur.
    """
    try:
        # PyInstaller, geçici bir klasör oluşturur ve yolu _MEIPASS içinde saklar.
        # Bu, .exe'nin içindeki dosyalara erişmemizi sağlar.
        base_path = Path(sys._MEIPASS)
    except Exception:
        # _MEIPASS yoksa, script normal şekilde çalışıyordur.
        # Dosyanın kendi konumundan yola çıkarak yolu buluruz.
        base_path = Path(__file__).resolve().parent.parent # .../ai_model/ klasörüne çıkar
    
    return base_path / relative_path

# --- GÜNCELLENDİ: fake_api_responses.json dosyasının yolu ---
FAKE_API_RESPONSES_PATH = get_resource_path("evaluation/fake_api_responses.json")


# Basit bir "sahte veritabanı" veya kural motoru
# Bu, hangi durumda hangi yanıtın verileceğini belirler.
MOCK_DB_RULES = {
    "invalid_user_ids": [9999, 1000],
    "users_with_no_bill": [8001, 8002],
    "paid_bill_ids": ["F-2025-PAID"],
    "ineligible_users_for_gamer_pro": [7001, 7002]
}


def get_tool_definitions():
    """
    Modelin kullanabileceği araçların Llama-3 formatında tanımlarını döndürür.
    Bu, modele "işte bunlar senin alet çantan" demenin standart yoludur.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_current_bill",
                "description": "Bir kullanıcının mevcut, ödenmemiş faturasını getirir. Fatura tutarı, son ödeme tarihi gibi detayları içerir.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "Faturası sorgulanacak kullanıcının numerik ID'si."
                        }
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
                        "bill_id": {
                            "type": "string",
                            "description": "Ödenecek faturanın benzersiz kimliği (örn: F-2025-3162)."
                        },
                        "method": {
                            "type": "string",
                            "description": "Ödeme yöntemi.",
                            "enum": ["credit_card", "bank_transfer"]
                        }
                    },
                    "required": ["bill_id", "method"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_remaining_quotas",
                "description": "Kullanıcının mevcut fatura döneminde kalan internet, dakika ve SMS gibi kotalarını sorgular.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "Kotaları sorgulanacak kullanıcının numerik ID'si."
                        }
                    },
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
                "name": "get_package_details",
                "description": "Belirli bir paketin fiyat, içerik, taahhüt süresi gibi tüm detaylarını getirir.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "package_name": {
                            "type": "string",
                            "description": "Detayları istenen paketin tam adı (örn: 'Gamer Pro')."
                        }
                    },
                    "required": ["package_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "change_package",
                "description": "Kullanıcının mevcut tarife/paketini, adı verilen yeni bir paketle değiştirir.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "Paketi değiştirilecek kullanıcının numerik ID'si."
                        },
                        "new_package_name": {
                            "type": "string",
                            "description": "Geçiş yapılacak yeni paketin tam adı."
                        }
                    },
                    "required": ["user_id", "new_package_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_fault_ticket",
                "description": "Kullanıcının bildirdiği bir sorun (örn: internet yavaşlığı) için teknik destek kaydı (arıza kaydı) oluşturur.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "Adına kayıt açılacak kullanıcının numerik ID'si."
                        },
                        "issue_description": {
                            "type": "string",
                            "description": "Sorunun kullanıcı tarafından yapılan kısa açıklaması."
                        }
                    },
                    "required": ["user_id", "issue_description"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_fault_ticket_status",
                "description": "Daha önceden açılmış bir arıza kaydının mevcut durumunu (örn: 'inceleniyor', 'çözüldü') sorgular.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "Durumu sorgulanacak arıza kaydının benzersiz kimliği (örn: T-EXIST-2025-937515)."
                        }
                    },
                    "required": ["ticket_id"]
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
                        "user_id": {
                            "type": "integer",
                            "description": "Geçmiş faturaları listelenecek kullanıcının numerik ID'si."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Kaç adet geçmiş faturanın getirileceği.",
                            "default": 3
                        }
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "test_internet_speed",
                "description": "Bir kullanıcının mevcut internet bağlantısının indirme (download) ve yükleme (upload) hızını test eder.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "Hız testi yapılacak kullanıcının numerik ID'si."
                        }
                    },
                    "required": ["user_id"]
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

        # --- YENİ: Akıllı Yanıt Seçim Mantığı ---
        
        # Varsayılan olarak başarı yanıtını hedefle
        response_template = responses[function_name].get("success")

        # Fonksiyona özel hata durumlarını kontrol et
        user_id = params.get("user_id")
        if function_name == "get_current_bill" and user_id in MOCK_DB_RULES["users_with_no_bill"]:
            response_template = responses[function_name]["error"]["NO_BILL"]

        elif function_name == "pay_bill":
            bill_id = params.get("bill_id")
            if bill_id in MOCK_DB_RULES["paid_bill_ids"]:
                response_template = responses[function_name]["error"]["BILL_NOT_FOUND"]

        elif function_name == "change_package":
            package_name = params.get("new_package_name")
            if package_name == "Gamer Pro" and user_id in MOCK_DB_RULES["ineligible_users_for_gamer_pro"]:
                 response_template = responses[function_name]["error"]["INELIGIBLE_FOR_PACKAGE"]

        if response_template is None:
             return json.dumps({"success": False, "error": f"{function_name} için uygun yanıt şablonu bulunamadı."}, ensure_ascii=False, indent=2)

        # Yanıtı kopyalayarak orijinal şablonu bozmuyoruz
        response_data = response_template.copy()

        # --- YENİ: Dinamik Veri Enjeksiyonu ---
        # Parametrelerdeki veriyi, yanıt JSON'ına enjekte et.
        # Bu, modelin "Ben sana 8901'i sordum, sen de bana 8901'i döndürdün"
        # mantığını kurmasına yardımcı olur.
        if "data" in response_data and response_data["data"] is not None:
            for key, value in params.items():
                if key in response_data["data"]:
                    response_data["data"][key] = value

        return json.dumps(response_data, ensure_ascii=False, indent=2)

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        return json.dumps({"success": False, "error": f"API yanıtı işlenirken hata oluştu: {e}"}, ensure_ascii=False, indent=2) 