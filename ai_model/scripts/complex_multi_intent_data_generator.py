# -*- coding: utf-8 -*-
"""
🚀 Olağanüstü Multi-Intent (Çok Niyetli) Veri Seti Üretici - v3
==================================================================

Bu script, Strateji 5 (Complex & Multi-Intent) için advanced_training_scenarios.md'deki örneklerle %100 uyumlu,
her adımda API yanıtlarını Pydantic modelleriyle doğrulayan, olağanüstü kaliteli ve çeşitli bir veri seti üretir.

- API yanıtları telekom_api_schema'dan alınan Pydantic modelleriyle doğrulanır.
- Her diyalog adımı, advanced_training_scenarios.md'deki format ve kaliteye uygun şekilde üretilir.
- Her örnek, birden fazla niyeti (intent) mantıklı bir zincirle işler.
- Doğal dil ve duygu tonu çeşitliliği, hata senaryoları ve gerçekçi müşteri hizmetleri akışları içerir.
"""

import json
import random
import uuid
import os
from faker import Faker
from pydantic import ValidationError
from datetime import timedelta

# === GÜVENLİK ADIMI: ANA SÖZLEŞMEYİ (Pydantic Modelleri) İÇE AKTAR ===
from telekom_api_schema import (
    GetCurrentBillResponse, ServiceItem,
    CreateFaultTicketResponse,
    GetRemainingQuotasResponse, UsagePercentage,
    GetAvailablePackagesResponse, AvailablePackageItem, AvailablePackageFeatures,
    ChangePackageResponse,
    GetPastBillsResponse, PastBillItem,
    GetPackageDetailsResponse, PackageDetailsFeatures,
    PayBillResponse,
    TestInternetSpeedResponse,
    EnableRoamingResponse,
    ErrorResponse, ErrorDetail,
    SuspendLineResponse, ReactivateLineResponse, UpdateCustomerContactResponse
)

fake = Faker("tr_TR")

# --- Gelişmiş Duygu ve Dil Varyasyonları ---
USER_TONES = {
    "neutral": [
        "Mevcut paketimle ilgili ve faturam hakkında bilgi alabilir miyim?",
        "Hem kota hem de son fatura detaylarımı öğrenmek istiyorum.",
        "Paket değişikliği ve fatura sorgusu yapabilir miyiz?",
        "Hesap bilgilerimi ve son ödememi kontrol edebilir misiniz?",
        "Hattımı geçici olarak askıya almak istiyorum."
    ],
    "angry": [
        "Faturam yine çok yüksek geldi, ayrıca internetim de sürekli bitiyor! Bir bakın şuna!",
        "Bu ne biçim hizmet! Hem kota hem fatura sorunlu, ilgilenin artık!",
        "Hattımda sürekli sorun var, artık çözün şunu!",
        "Neden hala eski bilgilerim sistemde, güncelleyin artık!"
    ],
    "confused": [
        "Sanırım paketim bana uygun değil, bir de faturamı anlamadım. Yardımcı olur musunuz?",
        "Hem kota hem de fatura konusunda kafam karışık, açıklayabilir misiniz?",
        "Hattım neden askıya alındı, anlamadım. Açıklayabilir misiniz?",
        "Numaramı değiştirdim ama sistemde görünmüyor, neden?"
    ],
    "impatient": [
        "Hızlıca hem kota hem fatura detaylarımı öğrenmek istiyorum, acelem var.",
        "Lütfen hemen paket değişikliği ve fatura sorgusu yapalım.",
        "Hattımı hemen açtırmak istiyorum, bekleyemem.",
        "İletişim bilgilerimi hızlıca güncelleyin, vaktim yok."
    ]
}

ASSISTANT_TEMPLATES = {
    "neutral": [
        "Elbette, taleplerinizi sırayla kontrol ediyorum.",
        "Tabii, önce paket ve kota bilgilerinize bakıyorum, ardından fatura detayınızı sunacağım.",
        "İstediğiniz işlemleri sırayla başlatıyorum.",
        "Hesap ve fatura bilgilerinizi hemen kontrol ediyorum."
    ],
    "angry": [
        "Yaşadığınız olumsuzluk için üzgünüm, hemen detaylıca inceleyip bilgi vereceğim.",
        "Sizi anlıyorum, tüm sorunlarınızı sırayla çözeceğim.",
        "Hemen ilgileniyorum, mağduriyetinizi gidereceğim.",
        "Bilgilerinizi güncellemek ve sorunları çözmek için buradayım."
    ],
    "confused": [
        "Kafanızın karışık olduğunu anlıyorum, adım adım açıklayacağım.",
        "Her iki konuda da detaylı bilgi vereceğim, birlikte çözelim.",
        "Hattınız ve bilgilerinizle ilgili tüm detayları açıklayacağım.",
        "Numara ve iletişim değişikliklerinizi birlikte kontrol edelim."
    ],
    "impatient": [
        "Hemen işlemlerinizi başlatıyorum, zamanınızı almadan sonuçlandıracağım.",
        "En hızlı şekilde hem kota hem fatura detayınızı sunuyorum.",
        "Hattınızı açmak ve bilgilerinizi güncellemek için hızlıca işlem yapıyorum.",
        "Tüm işlemleri hızla tamamlayacağım."
    ]
}

# --- Gerçekçi Zaman ve Kimlik Üretimi ---
def generate_user_id():
    # 4-6 haneli, 1000-999999 arası, gerçekçi
    return random.randint(1000, 999999)

def generate_ticket_id():
    year = fake.date_this_year().year
    return f"T-{year}-{random.randint(1000, 9999)}"

def generate_bill_id(user_id):
    year = fake.date_this_year().year
    return f"F-{year}-{user_id}-{random.randint(1000,9999)}"

def generate_date_pair():
    # Fatura tarihi ile ödeme tarihi ilişkili olsun
    bill_date = fake.date_this_year()
    due_date = bill_date + timedelta(days=random.randint(5, 20))
    return bill_date.isoformat(), due_date.isoformat()

# --- API UYUMLU YARDIMCI FONKSİYONLAR ---
def create_validated_json_response(pydantic_model, data: dict) -> str:
    try:
        validated_data = pydantic_model(**data)
        return validated_data.model_dump_json(indent=None)
    except ValidationError as e:
        print(f"!!! VERİ DOĞRULAMA HATASI: Model '{pydantic_model.__name__}' !!!\nHatalı veri: {data}\nPydantic Hatası: {e}")
        raise

# --- Hata Senaryosu Üretici ---
def random_api_error():
    return random.choice([
        {"success": False, "error": {"code": "BILL_NOT_FOUND", "message": "Fatura bulunamadı veya daha önce ödenmiş."}},
        {"success": False, "error": {"code": "INELIGIBLE_FOR_PACKAGE", "message": "Kullanıcı bu paket için uygun değil.", "details": "Bu paket sadece belirli kullanıcılar içindir."}},
        {"success": False, "error": {"code": "DUPLICATE_TICKET_FOUND", "message": "Aynı konuda zaten açık bir arıza kaydınız bulunuyor."}},
        {"success": False, "error": {"code": "MISSING_PARAMETER", "message": "Gerekli parametre eksik."}}
    ])

# =====================================================================
# SENARYOLAR: COMPLEX & MULTI-INTENT (Strateji 5)
# =====================================================================

def scenario_fault_and_bill(tone="neutral", with_error=False):
    if tone == "random":
        tone = random.choice(list(USER_TONES.keys()))
    user_id = generate_user_id()
    ticket_id = generate_ticket_id()
    bill_amount = round(random.uniform(80, 350), 2)
    user_utter = random.choice(USER_TONES[tone])
    assistant_utter = random.choice(ASSISTANT_TEMPLATES[tone])
    fault_data = {
        "ticket_id": ticket_id,
        "user_id": user_id,
        "status": "open",
        "created_at": fake.iso8601(),
        "issue_description": "İnternet hızı çok yavaş.",
        "category": "internet_speed",
        "priority": "medium",
        "estimated_resolution": fake.future_date(end_date='+2d').isoformat()
    }
    bill = {
        "user_id": user_id,
        "bill_id": generate_bill_id(user_id),
        "amount": bill_amount,
        "currency": "TL",
        "bill_date": fake.date_this_year().isoformat(),
        "due_date": fake.future_date(end_date='+10d').isoformat(),
        "status": random.choice(["paid", "unpaid"]),
        "services": [
            {"service_name": "İnternet", "amount": round(bill_amount * 0.7, 2)},
            {"service_name": "Ses", "amount": round(bill_amount * 0.2, 2)},
            {"service_name": "Diğer", "amount": round(bill_amount * 0.1, 2)}
        ]
    }
    donguler = [
        {"rol": "kullanici", "icerik": user_utter},
        {"rol": "asistan", "icerik": assistant_utter + " Öncelikle arıza kaydınızı açıyorum."},
        {"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "create_fault_ticket",
            "parametreler": {
                "user_id": user_id,
                "issue_description": "İnternet hızı çok yavaş.",
                "category": "internet_speed",
                "priority": "medium"
            }
        }]},
    ]
    if with_error and random.random() < 0.5:
        donguler.append({"rol": "arac", "icerik": ErrorResponse(error={"code": "TICKET_CREATION_FAILED", "message": "Arıza kaydı oluşturulamadı."}).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": "Arıza kaydı oluşturulamadı. Farklı bir işlem yapmak ister misiniz?"})
    else:
        donguler.append({"rol": "arac", "icerik": create_validated_json_response(CreateFaultTicketResponse, fault_data)})
        donguler.append({"rol": "asistan", "icerik": f"Arıza kaydınız {ticket_id} numarasıyla oluşturuldu. Şimdi fatura detayınıza bakıyorum."})
        donguler.append({"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "get_current_bill",
            "parametreler": {"user_id": user_id}
        }]})
        if with_error and random.random() < 0.5:
            donguler.append({"rol": "arac", "icerik": ErrorResponse(error={"code": "BILL_NOT_FOUND", "message": "Fatura bilgisi alınamadı."}).model_dump_json()})
            donguler.append({"rol": "asistan", "icerik": "Fatura bilgisi alınamadı. Başka bir isteğiniz var mı?"})
        else:
            donguler.append({"rol": "arac", "icerik": create_validated_json_response(GetCurrentBillResponse, bill)})
            donguler.append({"rol": "asistan", "icerik": f"Son fatura tutarınız {bill_amount} TL. ({bill['status']})"})
    return {
        "id": f"MI-001-{user_id}-{uuid.uuid4().hex[:8]}",
        "senaryo": "Multi-Intent - Arıza kaydı ve fatura bilgisi (çeşitli ton ve hata)",
        "donguler": donguler
    }

def scenario_quota_and_upgrade_and_bill(tone="neutral", with_error=False):
    if tone == "random":
        tone = random.choice(list(USER_TONES.keys()))
    user_id = generate_user_id()
    rem_gb = round(random.uniform(0.2, 3.5), 1)
    usage_pct = random.randint(80, 98)
    quotas = {
        "internet_remaining_gb": rem_gb,
        "voice_remaining_minutes": random.randint(0, 50),
        "sms_remaining": random.randint(0, 100),
        "usage_percentage": {"internet": usage_pct, "voice": random.randint(60, 90), "sms": random.randint(50, 90)},
        "period_end": fake.future_date(end_date='+20d').isoformat()
    }
    to_pkg = random.choice(["Premium Paket", "Limitsiz Paket"])
    available_packages = {
        "packages": [
            {"name": "Standart Paket", "monthly_fee": 59.9, "features": {"internet_gb": 20, "voice_minutes": 500, "sms_count": 100}},
            {"name": to_pkg, "monthly_fee": 129.9, "features": {"internet_gb": 100, "voice_minutes": 2000, "sms_count": 1000}}
        ]
    }
    change_data = {
        "change_id": f"C-{uuid.uuid4().hex[:8]}",
        "from_package": "Standart Paket",
        "to_package": to_pkg,
        "effective_date": fake.future_date(end_date='+1d').isoformat(),
        "fee_difference": round(random.uniform(5, 25), 2),
        "status": "success"
    }
    amount = round(random.uniform(150, 600), 2)
    bill = {
        "user_id": user_id,
        "bill_id": generate_bill_id(user_id),
        "amount": amount,
        "currency": "TL",
        "bill_date": fake.date_this_year().isoformat(),
        "due_date": fake.future_date(end_date='+7d').isoformat(),
        "status": random.choice(["paid", "unpaid"]),
        "services": [
            {"service_name": "İnternet", "amount": round(amount * 0.7, 2)},
            {"service_name": "Ses", "amount": round(amount * 0.2, 2)},
            {"service_name": "Diğer", "amount": round(amount * 0.1, 2)}
        ]
    }
    user_utter = random.choice(USER_TONES[tone])
    assistant_utter = random.choice(ASSISTANT_TEMPLATES[tone])
    donguler = [
        {"rol": "kullanici", "icerik": user_utter},
        {"rol": "asistan", "icerik": assistant_utter + " Önce kalan kotanızı sorguluyorum."},
        {"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "get_remaining_quotas",
            "parametreler": {"user_id": user_id}
        }]},
    ]
    if with_error and random.random() < 0.3:
        donguler.append({"rol": "arac", "icerik": ErrorResponse(error={"code": "QUOTA_NOT_FOUND", "message": "Kota bilgisi alınamadı."}).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": "Kota bilgisi alınamadı. Devam etmek ister misiniz?"})
    else:
        donguler.append({"rol": "arac", "icerik": create_validated_json_response(GetRemainingQuotasResponse, quotas)})
        donguler.append({"rol": "asistan", "icerik": f"Kalan kota: {rem_gb} GB (%{usage_pct}). Paket yükseltmek ister misiniz?"})
        donguler.append({"rol": "kullanici", "icerik": f"Evet, {to_pkg} paketine geçmek istiyorum."})
        donguler.append({"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "change_package",
            "parametreler": {"user_id": user_id, "to_package": to_pkg}
        }]})
        if with_error and random.random() < 0.3:
            donguler.append({"rol": "arac", "icerik": ErrorResponse(error={"code": "PACKAGE_CHANGE_FAILED", "message": "Paket değişikliği yapılamadı."}).model_dump_json()})
            donguler.append({"rol": "asistan", "icerik": "Paket değişikliği yapılamadı. Fatura sorgusuna geçiyorum."})
        else:
            donguler.append({"rol": "arac", "icerik": create_validated_json_response(ChangePackageResponse, change_data)})
            donguler.append({"rol": "asistan", "icerik": f"Paketiniz {to_pkg} olarak güncellendi. Ücret farkı: {change_data['fee_difference']} TL. Şimdi son faturanıza bakıyorum."})
        donguler.append({"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "get_current_bill",
            "parametreler": {"user_id": user_id}
        }]})
        if with_error and random.random() < 0.3:
            donguler.append({"rol": "arac", "icerik": ErrorResponse(error={"code": "BILL_NOT_FOUND", "message": "Fatura bilgisi alınamadı."}).model_dump_json()})
            donguler.append({"rol": "asistan", "icerik": "Fatura bilgisi alınamadı. Başka bir isteğiniz var mı?"})
        else:
            donguler.append({"rol": "arac", "icerik": create_validated_json_response(GetCurrentBillResponse, bill)})
            donguler.append({"rol": "asistan", "icerik": f"Son faturanız {amount} TL. Ödeme tarihi: {bill['due_date']}."})
    return {
        "id": f"MI-002-{user_id}-{uuid.uuid4().hex[:8]}",
        "senaryo": "Multi-Intent - Kota, paket yükseltme ve fatura bilgisi (çeşitli ton ve hata)",
        "donguler": donguler
    }

# Ekstra: Geçmiş fatura ve paket detayını da zincire ekleyen bir senaryo
def scenario_past_bill_and_package_details(tone="neutral", with_error=False):
    if tone == "random":
        tone = random.choice(list(USER_TONES.keys()))
    user_id = generate_user_id()
    bill_amount = round(random.uniform(80, 350), 2)
    # Geçmiş fatura için Pydantic model
    past_bill = GetPastBillsResponse(
        bills=[PastBillItem(
            bill_id=f"F-{fake.date_this_year().year-1}-{user_id}-{random.randint(1000,9999)}",
            amount=bill_amount,
            bill_date=fake.date_this_year().replace(year=fake.date_this_year().year-1).isoformat(),
            status=random.choice(["paid", "unpaid"]),
            paid_date=fake.date_this_year().isoformat()
        )],
        total_count=1,
        total_amount_paid=bill_amount
    )
    pkg_name = random.choice(["Mega İnternet", "Gamer Pro", "Sosyal Medya Uzmanı"])
    pkg_details = GetPackageDetailsResponse(
        name=pkg_name,
        monthly_fee=round(random.uniform(50, 150), 2),
        setup_fee=0.0,
        features=PackageDetailsFeatures(
            internet_gb=random.choice([20, 50, 100]),
            voice_minutes=random.choice([500, 1000, 2000]),
            sms_count=random.choice([100, 500, 1000]),
            international_minutes=random.choice([0, 100, 250])
        ),
        contract_duration=random.choice([12, 24]),
        cancellation_fee=round(random.uniform(20, 100), 2)
    )
    user_utter = f"Geçen yılki faturamı ve {pkg_name} paketinin detaylarını öğrenmek istiyorum. Kullanıcı no: {user_id}"
    donguler = [
        {"rol": "kullanici", "icerik": user_utter},
        {"rol": "asistan", "icerik": "Tabii, önce geçmiş faturanıza bakıyorum."},
        {"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "get_past_bills",
            "parametreler": {"user_id": user_id, "limit": 1}
        }]},
    ]
    if with_error and random.random() < 0.5:
        donguler.append({"rol": "arac", "icerik": ErrorResponse(error={"code": "BILL_NOT_FOUND", "message": "Geçmiş fatura bulunamadı."}).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": "Geçmiş fatura bilgisi alınamadı. Paket detayına geçiyorum."})
    else:
        donguler.append({"rol": "arac", "icerik": past_bill.model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": f"Geçen yılki fatura tutarınız {bill_amount} TL."})
    donguler.append({"rol": "asistan", "icerik": None, "arac_cagrilari": [{
        "fonksiyon": "get_package_details",
        "parametreler": {"package_name": pkg_name}
    }]})
    if with_error and random.random() < 0.5:
        donguler.append({"rol": "arac", "icerik": ErrorResponse(error={"code": "PACKAGE_NOT_FOUND", "message": "Paket detay bilgisi alınamadı."}).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": "Paket detay bilgisi alınamadı. Başka bir isteğiniz var mı?"})
    else:
        donguler.append({"rol": "arac", "icerik": pkg_details.model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": f"{pkg_name} paketi: {pkg_details.features.internet_gb} GB internet, {pkg_details.features.voice_minutes} dakika konuşma, {pkg_details.features.sms_count} SMS içerir."})
    return {
        "id": f"MI-003-{user_id}-{uuid.uuid4().hex[:8]}",
        "senaryo": "Multi-Intent - Geçmiş fatura ve paket detay (çeşitli hata)",
        "donguler": donguler
    }

# --- Yeni API Endpoint Senaryoları ---
def scenario_suspend_line(tone="neutral", with_error=False):
    if tone == "random":
        tone = random.choice(list(USER_TONES.keys()))
    user_id = generate_user_id()
    line_number = f"+9055{random.randint(10000000,99999999)}"
    suspension_reason = random.choice(["geçici durdurma", "fatura ödenmedi", "kullanıcı talebi"])
    suspended_at = fake.date_this_year().isoformat()
    reactivation_fee = round(random.uniform(0, 50), 2)
    max_suspension_days = random.choice([30, 60, 90])
    user_utter = random.choice(USER_TONES[tone])
    assistant_utter = random.choice(ASSISTANT_TEMPLATES[tone])
    donguler = [
        {"rol": "kullanici", "icerik": user_utter},
        {"rol": "asistan", "icerik": assistant_utter + " Hattınızı askıya alıyorum."},
        {"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "suspend_line",
            "parametreler": {"user_id": user_id, "reason": suspension_reason}
        }]},
    ]
    if with_error and random.random() < 0.5:
        donguler.append({"rol": "arac", "icerik": ErrorResponse(error=ErrorDetail(code="SUSPEND_FAILED", message="Hat askıya alınamadı.")).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": "Hat askıya alınamadı. Başka bir işlem yapmak ister misiniz?"})
    else:
        donguler.append({"rol": "arac", "icerik": SuspendLineResponse(
            user_id=user_id,
            line_number=line_number,
            suspension_reason=suspension_reason,
            suspended_at=suspended_at,
            reactivation_fee=reactivation_fee,
            max_suspension_days=max_suspension_days
        ).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": f"Hattınız başarıyla askıya alındı. Maksimum {max_suspension_days} gün sonra otomatik açılır."})
    return {
        "id": f"MI-004-{user_id}-{uuid.uuid4().hex[:8]}",
        "senaryo": "Suspend Line - Hat askıya alma (çeşitli hata)",
        "donguler": donguler
    }

def scenario_reactivate_line(tone="neutral", with_error=False):
    if tone == "random":
        tone = random.choice(list(USER_TONES.keys()))
    user_id = generate_user_id()
    line_number = f"+9055{random.randint(10000000,99999999)}"
    reactivated_at = fake.date_this_year().isoformat()
    suspension_duration_days = random.choice([5, 15, 30])
    reactivation_fee = round(random.uniform(0, 50), 2)
    user_utter = random.choice(USER_TONES[tone])
    assistant_utter = random.choice(ASSISTANT_TEMPLATES[tone])
    donguler = [
        {"rol": "kullanici", "icerik": user_utter},
        {"rol": "asistan", "icerik": assistant_utter + " Hattınızı yeniden aktif ediyorum."},
        {"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "reactivate_line",
            "parametreler": {"user_id": user_id}
        }]},
    ]
    if with_error and random.random() < 0.5:
        donguler.append({"rol": "arac", "icerik": ErrorResponse(error=ErrorDetail(code="REACTIVATE_FAILED", message="Hat yeniden aktif edilemedi.")).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": "Hat yeniden aktif edilemedi. Başka bir işlem yapmak ister misiniz?"})
    else:
        donguler.append({"rol": "arac", "icerik": ReactivateLineResponse(
            user_id=user_id,
            line_number=line_number,
            reactivated_at=reactivated_at,
            suspension_duration_days=suspension_duration_days,
            reactivation_fee=reactivation_fee
        ).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": f"Hattınız başarıyla yeniden aktif edildi. Toplam askıda kalma süresi: {suspension_duration_days} gün."})
    return {
        "id": f"MI-005-{user_id}-{uuid.uuid4().hex[:8]}",
        "senaryo": "Reactivate Line - Hat yeniden açma (çeşitli hata)",
        "donguler": donguler
    }

def scenario_update_customer_contact(tone="neutral", with_error=False):
    if tone == "random":
        tone = random.choice(list(USER_TONES.keys()))
    user_id = generate_user_id()
    contact_type = random.choice(["phone", "email", "address"])
    old_value = fake.phone_number() if contact_type == "phone" else fake.email() if contact_type == "email" else fake.address()
    new_value = fake.phone_number() if contact_type == "phone" else fake.email() if contact_type == "email" else fake.address()
    updated_at = fake.date_this_year().isoformat()
    verification_required = random.choice([True, False])
    user_utter = random.choice(USER_TONES[tone])
    assistant_utter = random.choice(ASSISTANT_TEMPLATES[tone])
    donguler = [
        {"rol": "kullanici", "icerik": user_utter},
        {"rol": "asistan", "icerik": assistant_utter + f" {contact_type} bilgilerinizi güncelliyorum."},
        {"rol": "asistan", "icerik": None, "arac_cagrilari": [{
            "fonksiyon": "update_customer_contact",
            "parametreler": {"user_id": user_id, "contact_type": contact_type, "new_value": new_value}
        }]},
    ]
    if with_error and random.random() < 0.5:
        donguler.append({"rol": "arac", "icerik": ErrorResponse(error=ErrorDetail(code="UPDATE_FAILED", message="Bilgi güncellenemedi.")).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": f"{contact_type} bilgisi güncellenemedi. Başka bir işlem yapmak ister misiniz?"})
    else:
        donguler.append({"rol": "arac", "icerik": UpdateCustomerContactResponse(
            user_id=user_id,
            contact_type=contact_type,
            old_value=old_value,
            new_value=new_value,
            updated_at=updated_at,
            verification_required=verification_required
        ).model_dump_json()})
        donguler.append({"rol": "asistan", "icerik": f"{contact_type.capitalize()} bilginiz başarıyla güncellendi."})
    return {
        "id": f"MI-006-{user_id}-{uuid.uuid4().hex[:8]}",
        "senaryo": "Update Customer Contact - Bilgi güncelleme (çeşitli hata)",
        "donguler": donguler
    }

# =====================================================================
# Veri Kümesi Üretimi
# =====================================================================
def generate_dataset(num: int) -> list:
    data = []
    scenario_funcs = [
        scenario_fault_and_bill,
        scenario_quota_and_upgrade_and_bill,
        scenario_past_bill_and_package_details,
        scenario_suspend_line,
        scenario_reactivate_line,
        scenario_update_customer_contact
    ]
    for _ in range(num):
        scenario_func = random.choices(scenario_funcs, weights=[3, 3, 2, 1, 1, 1], k=1)[0]
        tone = random.choice(["neutral", "angry", "confused", "impatient"])
        with_error = random.random() < 0.4
        try:
            data.append(scenario_func(tone=tone, with_error=with_error))
        except Exception as e:
            print(f"Veri üretiminde hata: {e}")
    return data

# =====================================================================
# Dosyaya Kaydetme
# =====================================================================
def save_dataset(dataset: list, path: str, jsonl: bool=False) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        if jsonl:
            for rec in dataset:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        else:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"Veri '{path}' kaydedildi.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Complex & Multi-Intent senaryo üretici (olağanüstü uzman seviye)')
    parser.add_argument('--num', type=int, default=2000, help='Üretilecek örnek sayısı')
    parser.add_argument('--output', type=str, default='./data/complex_multi_intent.json', help='Çıktı dosyası')
    parser.add_argument('--jsonl', action='store_true', help='JSONL formatında kaydet')
    args = parser.parse_args()
    ds = generate_dataset(args.num)
    save_dataset(ds, args.output, jsonl=args.jsonl)
