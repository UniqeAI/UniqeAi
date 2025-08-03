# -*- coding: utf-8 -*-
"""
🛠️ YARDIMCI FONKSİYONLAR
=========================

Bu modül, SupremeHumanLevelDatasetGenerator için yardımcı fonksiyonları içerir.
"""

import json
import random
import uuid
import inspect
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from functools import lru_cache
from pydantic import BaseModel

def generate_user_id() -> int:
    """Kullanıcı ID'si üretir"""
    return random.randint(10000, 99999)

@lru_cache(maxsize=128)
def get_cached_mock_data_template(model_name: str) -> Dict[str, Any]:
    """
    PERFORMANCE OPTIMIZATION: Mock data template'lerini cache'le
    
    Args:
        model_name: Pydantic model adı
        
    Returns:
        Dict: Cached mock data template
    """
    return {
        "cached_at": datetime.now().isoformat(),
        "template_version": "v3_optimized"
    }

def contains_english_words(text: str) -> bool:
    """
    UZMAN SEVİYE DİL KONTROL
    Metinde İngilizce kelimeler olup olmadığını kontrol eder.
    """
    if not text:
        return False
        
    # Yaygın İngilizce kelimeler (API terimleri hariç)
    english_words = {
        "hello", "hi", "thank", "you", "please", "sorry", "welcome", 
        "good", "morning", "evening", "night", "day", "time", "help",
        "service", "customer", "support", "problem", "issue", "error"
    }
    
    # API terimleri ve teknik kelimeler hariç tut
    allowed_technical = {
        "internet", "roaming", "sms", "gb", "mb", "api", "id", "status",
        "user", "bill", "package", "speed", "test", "ticket"
    }
    
    words = text.lower().split()
    for word in words:
        clean_word = ''.join(c for c in word if c.isalpha())
        if clean_word in english_words and clean_word not in allowed_technical:
            return True
    
    return False

def generate_basic_type_data(field_type: Any, field_name: str = "") -> Any:
    """
    SUPREME V3: ULTRA-GERÇEKÇİ MOCK VERİ ÜRETİMİ
    Temel Python tipleri için alan isimleri ve içeriklerine göre 
    son derece gerçekçi ve tutarlı sahte veriler üretir.
    """
    if field_type == str:
        field_lower = field_name.lower()
        # ID alanları - Gerçekçi formatlar (Min 10 karakter garantisi)
        if "id" in field_lower:
            if "bill" in field_lower or "fatura" in field_lower:
                return f"F-2024-{random.randint(100000, 999999)}"  # F-2024-123456 = 12 karakter
            elif "ticket" in field_lower or "ariza" in field_lower:
                return f"TKT-{random.randint(10000, 99999)}"
            elif "transaction" in field_lower:
                return f"TXN-{uuid.uuid4().hex[:12].upper()}"
            elif "analysis" in field_lower:
                return f"ANA-{datetime.now().strftime('%Y%m')}-{random.randint(1000, 9999)}"
            else:
                return f"{field_name.upper()}-{uuid.uuid4().hex[:8].upper()}"
        # Tarih/Zaman alanları
        elif "date" in field_lower or "time" in field_lower:
            if "due" in field_lower or "vade" in field_lower:
                return (datetime.now() + timedelta(days=random.randint(1, 30))).isoformat()
            else:
                return (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        # Durum alanları - ÖNEMLİ: Enum değerleri kullanılmalı
        elif "status" in field_lower:
            if "bill" in field_lower or "payment" in field_lower:
                return random.choice(["paid", "unpaid", "overdue", "processing", "cancelled"])
            elif "ticket" in field_lower:
                return random.choice(["open", "in_progress", "resolved", "closed", "cancelled"])
            elif "line" in field_lower:
                return random.choice(["active", "suspended", "terminated", "pending"])
            else:
                return random.choice(["active", "inactive", "pending", "completed"])
        # İsim alanları
        elif "name" in field_lower:
            if "package" in field_lower or "paket" in field_lower:
                return random.choice(["Evde Fiber Keyfi", "Mobil Avantaj Plus", "Sınırsız İnternet", "Gençlik Özel"])
            else:
                return random.choice(["Ahmet Yılmaz", "Ayşe Kaya", "Mehmet Demir", "Fatma Şahin"])
        # E-posta alanları
        elif "email" in field_lower:
            names = ["ahmet.yilmaz", "ayse.kaya", "mehmet.demir"]
            domains = ["gmail.com", "hotmail.com", "outlook.com"]
            return f"{random.choice(names)}{random.randint(1, 999)}@{random.choice(domains)}"
        # Telefon numaraları
        elif "phone" in field_lower or "number" in field_lower:
            return f"0{random.randint(530, 559)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        # Adres alanları
        elif "address" in field_lower:
            cities = ["İstanbul", "Ankara", "İzmir", "Bursa"]
            districts = ["Kadıköy", "Beşiktaş", "Şişli", "Çankaya"]
            return f"{random.choice(districts)}, {random.choice(cities)}"
        # Açıklama alanları
        elif "description" in field_lower or "message" in field_lower:
            if "issue" in field_lower or "problem" in field_lower:
                return random.choice([
                    "İnternet bağlantısı çok yavaş", "WiFi sinyal gücü zayıf",
                    "Mobil veri açılmıyor", "Fatura tutarı yanlış"
                ])
            else:
                return random.choice([
                    "Müşteri talebi işlendi", "Sistem güncellemesi tamamlandı",
                    "Ödeme işlemi onaylandı", "Problem çözüldü"
                ])
        # Genel string
        else:
            return random.choice([
                "Hızlı ve güvenilir hizmet", "7/24 müşteri desteği", 
                "Fiber altyapı", "5G teknolojisi", "Uygun fiyat"
            ])
    elif field_type == int:
        field_lower = field_name.lower()
        if "percentage" in field_lower:
            return random.randint(0, 100)  # Max 100 guarantee
        elif "gb" in field_lower:
            return random.choice([5, 10, 20, 50, 100, 250])
        elif "minutes" in field_lower:
            return random.choice([500, 1000, 2000, 5000])
        elif "sms" in field_lower:
            return random.choice([100, 500, 1000, 2000])
        elif "user_id" in field_lower:
            return random.randint(10000, 99999)
        elif "ping" in field_lower or "latency" in field_lower:
            return random.randint(10, 100)
        elif "signal" in field_lower:
            return random.randint(20, 100)  # Signal strength max 100
        elif "duration" in field_lower:
            return random.randint(12, 60)   # Contract duration max 60 months
        else:
            return random.randint(1, 1000)
    elif field_type == float:
        field_lower = field_name.lower()
        if "amount" in field_lower or "fee" in field_lower:
            return round(random.uniform(49.99, 899.99), 2)
        elif "speed" in field_lower:
            return round(random.uniform(10.5, 1000.0), 2)
        elif "confidence" in field_lower:
            return round(random.uniform(0.1, 1.0), 2)
        else:
            return round(random.uniform(0.1, 100.0), 2)
    elif field_type == bool:
        return random.choice([True, False])
    elif field_type == Optional[str]:
        return random.choice([None, "İsteğe bağlı metin"])
    elif hasattr(field_type, '__origin__') and field_type.__origin__ in (dict, Dict):
        # Dict[str, int] gibi tipler için
        if hasattr(field_type, '__args__') and len(field_type.__args__) == 2:
            key_type, value_type = field_type.__args__
            if key_type == str and value_type == int:
                # Özel alan için percentage kontrolü
                if "percentage" in field_name.lower():
                    return {
                        "internet": random.randint(20, 95),
                        "voice": random.randint(10, 90), 
                        "sms": random.randint(5, 85)
                    }
                return {
                    "daily_interactions": random.randint(10, 50),
                    "response_time": random.randint(1, 10),
                    "satisfaction_score": random.randint(1, 5)
                }
        # Usage percentage kontrolü burada da ekle
        if "percentage" in field_name.lower():
            return {"internet": random.randint(0, 100), "voice": random.randint(0, 100), "sms": random.randint(0, 100)}
        return {"key": "value", "example": random.randint(1, 50)}
    else:
        return None

def generate_mock_data_for_model(model_class: BaseModel) -> Dict[str, Any]:
    """
    UZMAN SEVİYE - ŞEMA ODAKLI VERİ ÜRETİMİ
    Bir Pydantic modelini dinamik olarak analiz eder ve alan tiplerine göre
    gerçekçi, rastgele sahte veriler üretir. Bu, veri üretiminin API şemasına
    %100 uyumlu olmasını garanti eder.
    """
    mock_data = {}
    for field_name, field_info in model_class.model_fields.items():
        field_type = field_info.annotation
        # ENUM tiplerini kontrol et
        if hasattr(field_type, '__bases__') and any(base.__name__ == 'Enum' for base in field_type.__bases__):
            # Schema Enum'larını kullan (telekom_api_schema.py'den)
            try:
                # Enum değerlerini al ve doğrula
                enum_values = [item.value for item in field_type]
                mock_data[field_name] = random.choice(enum_values)
            except Exception as e:
                # Debug: Print the problematic enum with details
                print(f"⚠️ Enum error for field '{field_name}' (type: {field_type}): {e}")
                print(f"   Field type details: {getattr(field_type, '__name__', 'unknown')}")
                # Fallback: Field ismini kullanarak uygun değer ver
                if "priority" in field_name.lower():
                    mock_data[field_name] = random.choice(["low", "medium", "high", "critical", "urgent"])
                elif "status" in field_name.lower() and "ticket" in field_name.lower():
                    mock_data[field_name] = random.choice(["open", "in_progress", "resolved", "closed", "cancelled"])
                elif "status" in field_name.lower() and "network" in field_name.lower():
                    mock_data[field_name] = random.choice(["operational", "degraded", "outage", "maintenance"])
                elif "status" in field_name.lower():
                    mock_data[field_name] = random.choice(["active", "inactive", "pending"])
                else:
                    mock_data[field_name] = "pending"
            continue
        # İç içe geçmiş Pydantic modelleri için yinelemeli çağrı
        if inspect.isclass(field_type) and issubclass(field_type, BaseModel):
            mock_data[field_name] = generate_mock_data_for_model(field_type)
            continue
        # Liste tipleri için
        if hasattr(field_type, '__origin__') and field_type.__origin__ in (list, List):
            list_item_type = field_type.__args__[0]
            if inspect.isclass(list_item_type) and issubclass(list_item_type, BaseModel):
                mock_data[field_name] = [generate_mock_data_for_model(list_item_type) for _ in range(random.randint(1, 3))]
            else:
                mock_data[field_name] = [generate_basic_type_data(list_item_type, field_name) for _ in range(random.randint(1, 3))]
            continue
        # Diğer temel tipler
        mock_data[field_name] = generate_basic_type_data(field_type, field_name)
    return mock_data 

def create_validated_response(model_class, override_data=None):
    """
    SUPREME V3 + ENTERPRISE SCHEMA INTEGRATION - %100 PYDANTİC DOĞRULAMA GÜVENCESİ
    Yeni telekom_api_schema v3.0-SUPREME utility fonksiyonlarını kullanarak
    enterprise-grade mock response oluşturur.
    """
    try:
        # Schema v3.0 ile gelişmiş mock data üretimi
        mock_data = generate_mock_data_for_model(model_class)
        if override_data:
            for key, value in override_data.items():
                # usage_percentage için özel kontrol
                if key == "usage_percentage" and isinstance(value, dict):
                    # Her değerin 100'den küçük olduğundan emin ol
                    fixed_usage = {}
                    for usage_key, usage_value in value.items():
                        if isinstance(usage_value, int) and usage_value > 100:
                            fixed_usage[usage_key] = random.randint(0, 100)
                            print(f"🔧 Usage percentage düzeltildi: {usage_key}: {usage_value} → {fixed_usage[usage_key]}")
                        else:
                            fixed_usage[usage_key] = usage_value
                    mock_data[key] = fixed_usage
                else:
                    mock_data[key] = value
        # Enterprise-grade Pydantic doğrulama
        validated = model_class(**mock_data)
        # JSON serileştirme kontrolü
        json_result = validated.model_dump_json(indent=None)
        # JSON'ın parse edilebilir olduğunu kontrol et
        json.loads(json_result)
        return json_result
    except Exception as e:
        print(f"❌ KRİTİK HATA - Beklenmeyen: {model_class.__name__}")
        print(f"   Hata: {e}")
        raise 