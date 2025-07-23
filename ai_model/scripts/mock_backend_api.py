"""
Mock Backend API - Model Eğitimi ve Test İçin

Bu modül, gerçek backend hazır olmadan AI modelini test etmemizi sağlar.
Tüm API çağrılarını simulate eder ve realistic response'lar döndürür.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import uuid

class MockTelekomBackendAPI:
    """
    Gerçek backend API'sini taklit eden mock sistem.
    
    Bu sınıf:
    - Tüm API endpoint'lerini simulate eder
    - Realistic test data'sı üretir  
    - API çağrı formatlarını validate eder
    - Model eğitimi için stabil environment sağlar
    """
    
    def __init__(self):
        """Mock database ve konfigürasyonları başlatır."""
        self._initialize_mock_data()
        self.call_log = []  # API çağrılarını loglar
        
    def _initialize_mock_data(self):
        """Test için gerekli mock verileri oluşturur."""
        # Mock users
        self.users = {
            i: {
                "user_id": i,
                "name": f"Müşteri {i}",
                "email": f"musteri{i}@example.com",
                "phone": f"+9055512{i:04d}",
                "address": f"İstanbul, Test Mahallesi {i}",
                "package": random.choice(["Mega İnternet", "Süper Konuşma", "Full Paket", "Öğrenci Dostu Tarife"]),
                "status": "active"
            }
            for i in range(1000, 10000)
        }
        
        # Mock packages
        self.packages = {
            "Mega İnternet": {
                "name": "Mega İnternet",
                "monthly_fee": 69.50,
                "features": {
                    "internet_gb": 50,
                    "voice_minutes": 1000,
                    "sms_count": 500
                }
            },
            "Süper Konuşma": {
                "name": "Süper Konuşma", 
                "monthly_fee": 59.90,
                "features": {
                    "internet_gb": 25,
                    "voice_minutes": 2000,
                    "sms_count": 1000
                }
            },
            "Full Paket": {
                "name": "Full Paket",
                "monthly_fee": 89.90,
                "features": {
                    "internet_gb": 100,
                    "voice_minutes": 3000,
                    "sms_count": 1000
                }
            },
            "Öğrenci Dostu Tarife": {
                "name": "Öğrenci Dostu Tarife",
                "monthly_fee": 49.90,
                "features": {
                    "internet_gb": 30,
                    "voice_minutes": 500,
                    "sms_count": 250
                }
            },
            "Esnaf Paketi": {
                "name": "Esnaf Paketi",
                "monthly_fee": 79.90,
                "features": {
                    "internet_gb": 75,
                    "voice_minutes": 1500,
                    "sms_count": 750
                }
            },
            "Yurt Dışı Avantaj": {
                "name": "Yurt Dışı Avantaj",
                "monthly_fee": 99.90,
                "features": {
                    "internet_gb": 60,
                    "voice_minutes": 1000,
                    "sms_count": 500,
                    "international_minutes": 200
                }
            }
        }
        
        # Mock regions
        self.regions = ["Marmara", "Ege", "Akdeniz", "İç Anadolu", "Karadeniz", "Doğu Anadolu", "Güneydoğu Anadolu"]
        
    def _log_call(self, function_name: str, params: Dict, response: Any):
        """API çağrılarını loglar."""
        self.call_log.append({
            "timestamp": datetime.now().isoformat(),
            "function": function_name,
            "params": params,
            "response_type": type(response).__name__,
            "success": True
        })
        
    def _validate_user_id(self, user_id: int) -> bool:
        """User ID'nin geçerli olup olmadığını kontrol eder."""
        return user_id in self.users

    # === FATURA & ÖDEME İŞLEMLERİ ===
    
    def get_current_bill(self, user_id: int) -> Dict[str, Any]:
        """Güncel fatura bilgilerini döndürür."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            response = {
                "success": True,
                "data": {
                    "bill_id": f"F-2024-{user_id}",
                    "user_id": user_id,
                    "amount": round(random.uniform(50.0, 150.0), 2),
                    "currency": "TRY",
                    "due_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
                    "bill_date": datetime.now().strftime("%Y-%m-%d"),
                    "status": random.choice(["paid", "unpaid", "overdue"])
                }
            }
        
        self._log_call("get_current_bill", {"user_id": user_id}, response)
        return response

    def get_past_bills(self, user_id: int, limit: int = 6) -> Dict[str, Any]:
        """Geçmiş fatura listesini döndürür."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            bills = []
            for i in range(min(limit, 12)):
                bill_date = datetime.now() - timedelta(days=30 * (i + 1))
                bills.append({
                    "bill_id": f"F-{bill_date.year}-{bill_date.month:02d}-{user_id}",
                    "amount": round(random.uniform(50.0, 150.0), 2),
                    "bill_date": bill_date.strftime("%Y-%m-%d"),
                    "status": "paid",
                    "paid_date": (bill_date + timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")
                })
            
            response = {
                "success": True,
                "data": {
                    "bills": bills,
                    "total_count": len(bills),
                    "total_amount_paid": sum(bill["amount"] for bill in bills)
                }
            }
        
        self._log_call("get_past_bills", {"user_id": user_id, "limit": limit}, response)
        return response

    def pay_bill(self, bill_id: str, method: str) -> Dict[str, Any]:
        """Fatura ödeme işlemi simulate eder."""
        if method not in ["credit_card", "bank_transfer"]:
            response = {"success": False, "error": {"code": "INVALID_METHOD", "message": "Geçersiz ödeme yöntemi"}}
        else:
            response = {
                "success": True,
                "data": {
                    "transaction_id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
                    "bill_id": bill_id,
                    "amount": round(random.uniform(50.0, 150.0), 2),
                    "method": method,
                    "status": "completed",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        self._log_call("pay_bill", {"bill_id": bill_id, "method": method}, response)
        return response

    def get_payment_history(self, user_id: int) -> Dict[str, Any]:
        """Ödeme geçmişini döndürür."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            payments = []
            for i in range(random.randint(3, 8)):
                payment_date = datetime.now() - timedelta(days=30 * i + random.randint(1, 10))
                payments.append({
                    "transaction_id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
                    "amount": round(random.uniform(50.0, 150.0), 2),
                    "method": random.choice(["credit_card", "bank_transfer"]),
                    "date": payment_date.isoformat(),
                    "bill_id": f"F-{payment_date.year}-{payment_date.month:02d}-{user_id}"
                })
            
            response = {
                "success": True,
                "data": {
                    "payments": payments,
                    "total_payments": len(payments),
                    "total_amount": sum(p["amount"] for p in payments)
                }
            }
        
        self._log_call("get_payment_history", {"user_id": user_id}, response)
        return response

    def setup_autopay(self, user_id: int, status: bool) -> Dict[str, Any]:
        """Otomatik ödeme ayarlarını düzenler."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            response = {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "autopay_enabled": status,
                    "payment_method": "credit_card_ending_1234" if status else None,
                    "next_payment_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d") if status else None
                }
            }
        
        self._log_call("setup_autopay", {"user_id": user_id, "status": status}, response)
        return response

    # === PAKET & TARİFE YÖNETİMİ ===
    
    def get_customer_package(self, user_id: int) -> Dict[str, Any]:
        """Müşterinin mevcut paket bilgilerini döndürür."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            user_package = self.users[user_id]["package"]
            package_info = self.packages[user_package].copy()
            package_info.update({
                "activation_date": "2024-01-01",
                "renewal_date": "2024-04-01"
            })
            
            response = {
                "success": True,
                "data": package_info
            }
        
        self._log_call("get_customer_package", {"user_id": user_id}, response)
        return response

    def get_remaining_quotas(self, user_id: int) -> Dict[str, Any]:
        """Kalan kullanım haklarını döndürür."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            user_package = self.users[user_id]["package"]
            features = self.packages[user_package]["features"]
            
            response = {
                "success": True,
                "data": {
                    "internet_remaining_gb": round(features["internet_gb"] * random.uniform(0.3, 0.9), 1),
                    "voice_remaining_minutes": int(features["voice_minutes"] * random.uniform(0.4, 0.8)),
                    "sms_remaining": int(features["sms_count"] * random.uniform(0.5, 0.9)),
                    "period_end": "2024-03-31"
                }
            }
        
        self._log_call("get_remaining_quotas", {"user_id": user_id}, response)
        return response

    def change_package(self, user_id: int, new_package_name: str) -> Dict[str, Any]:
        """Paket değiştirme işlemi."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        elif new_package_name not in self.packages:
            response = {"success": False, "error": {"code": "INVALID_PACKAGE", "message": f"Paket {new_package_name} bulunamadı"}}
        else:
            old_package = self.users[user_id]["package"]
            self.users[user_id]["package"] = new_package_name  # Mock database'i güncelle
            
            response = {
                "success": True,
                "data": {
                    "change_id": f"CHG-{uuid.uuid4().hex[:8].upper()}",
                    "from_package": old_package,
                    "to_package": new_package_name,
                    "effective_date": "2024-04-01",
                    "fee_difference": self.packages[new_package_name]["monthly_fee"] - self.packages[old_package]["monthly_fee"],
                    "status": "scheduled"
                }
            }
        
        self._log_call("change_package", {"user_id": user_id, "new_package_name": new_package_name}, response)
        return response

    def get_available_packages(self) -> Dict[str, Any]:
        """Mevcut tüm paketleri listeler."""
        response = {
            "success": True,
            "data": {
                "packages": list(self.packages.values())
            }
        }
        
        self._log_call("get_available_packages", {}, response)
        return response

    def get_package_details(self, package_name: str) -> Dict[str, Any]:
        """Belirli bir paketin detaylarını döndürür."""
        if package_name not in self.packages:
            response = {"success": False, "error": {"code": "INVALID_PACKAGE", "message": f"Paket {package_name} bulunamadı"}}
        else:
            package_info = self.packages[package_name].copy()
            package_info.update({
                "setup_fee": 0,
                "contract_duration": 24,
                "cancellation_fee": 50.00
            })
            
            response = {
                "success": True,
                "data": package_info
            }
        
        self._log_call("get_package_details", {"package_name": package_name}, response)
        return response

    def enable_roaming(self, user_id: int, status: bool) -> Dict[str, Any]:
        """Roaming hizmetini açar/kapatır."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            response = {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "roaming_enabled": status,
                    "activation_time": datetime.now().isoformat() if status else None,
                    "daily_fee": 25.00 if status else None,
                    "data_package": "1GB/day" if status else None
                }
            }
        
        self._log_call("enable_roaming", {"user_id": user_id, "status": status}, response)
        return response

    # === TEKNİK DESTEK & ARIZA ===
    
    def check_network_status(self, region: str) -> Dict[str, Any]:
        """Bölgesel network durumunu kontrol eder."""
        if region not in self.regions:
            response = {"success": False, "error": {"code": "INVALID_REGION", "message": f"Bölge {region} bulunamadı"}}
        else:
            has_outage = random.choice([True, False])
            response = {
                "success": True,
                "data": {
                    "region": region,
                    "status": "maintenance" if has_outage else "operational",
                    "coverage_percentage": random.randint(90, 99),
                    "active_outages": [
                        {
                            "area": f"{region} Test Bölgesi",
                            "issue": "Planlı bakım",
                            "start_time": datetime.now().isoformat(),
                            "estimated_end": (datetime.now() + timedelta(hours=4)).isoformat()
                        }
                    ] if has_outage else [],
                    "last_updated": datetime.now().isoformat()
                }
            }
        
        self._log_call("check_network_status", {"region": region}, response)
        return response

    def create_fault_ticket(self, user_id: int, issue_description: str) -> Dict[str, Any]:
        """Yeni arıza kaydı oluşturur."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            ticket_id = f"T-{random.randint(10000, 99999)}"
            response = {
                "success": True,
                "data": {
                    "ticket_id": ticket_id,
                    "user_id": user_id,
                    "issue_description": issue_description,
                    "category": random.choice(["internet_speed", "connectivity", "billing", "device"]),
                    "priority": random.choice(["low", "medium", "high"]),
                    "status": "open",
                    "created_at": datetime.now().isoformat(),
                    "estimated_resolution": (datetime.now() + timedelta(hours=24)).isoformat()
                }
            }
        
        self._log_call("create_fault_ticket", {"user_id": user_id, "issue_description": issue_description}, response)
        return response

    def get_fault_ticket_status(self, ticket_id: str) -> Dict[str, Any]:
        """Arıza kaydının durumunu sorgular."""
        response = {
            "success": True,
            "data": {
                "ticket_id": ticket_id,
                "status": random.choice(["open", "in_progress", "resolved", "closed"]),
                "resolution": "Bölgesel sinyal sorunu giderildi" if random.choice([True, False]) else None,
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 5))).isoformat(),
                "resolved_at": datetime.now().isoformat() if random.choice([True, False]) else None,
                "technician_notes": "Test arıza kaydı - Mock API"
            }
        }
        
        self._log_call("get_fault_ticket_status", {"ticket_id": ticket_id}, response)
        return response

    def test_internet_speed(self, user_id: int) -> Dict[str, Any]:
        """Internet hız testi yapar."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            response = {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "download_speed_mbps": round(random.uniform(10.0, 100.0), 1),
                    "upload_speed_mbps": round(random.uniform(5.0, 50.0), 1),
                    "ping_ms": random.randint(10, 50),
                    "test_timestamp": datetime.now().isoformat(),
                    "test_server": "Istanbul-Mock",
                    "quality_rating": random.choice(["poor", "fair", "good", "excellent"])
                }
            }
        
        self._log_call("test_internet_speed", {"user_id": user_id}, response)
        return response

    # === HESAP YÖNETİMİ ===
    
    def get_customer_profile(self, user_id: int) -> Dict[str, Any]:
        """Müşteri profil bilgilerini döndürür."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            user = self.users[user_id]
            response = {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "name": user["name"],
                    "phone_numbers": [
                        {
                            "number": user["phone"],
                            "type": "mobile",
                            "status": user["status"]
                        }
                    ],
                    "email": user["email"],
                    "address": user["address"],
                    "registration_date": "2023-01-15",
                    "customer_tier": random.choice(["bronze", "silver", "gold", "platinum"])
                }
            }
        
        self._log_call("get_customer_profile", {"user_id": user_id}, response)
        return response

    def update_customer_contact(self, user_id: int, contact_type: str, new_value: str) -> Dict[str, Any]:
        """Müşteri iletişim bilgilerini günceller."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        elif contact_type not in ["phone", "email", "address"]:
            response = {"success": False, "error": {"code": "INVALID_CONTACT_TYPE", "message": f"Geçersiz iletişim tipi: {contact_type}"}}
        else:
            old_value = self.users[user_id][contact_type]
            self.users[user_id][contact_type] = new_value  # Mock database'i güncelle
            
            response = {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "contact_type": contact_type,
                    "old_value": old_value,
                    "new_value": new_value,
                    "updated_at": datetime.now().isoformat(),
                    "verification_required": contact_type in ["phone", "email"]
                }
            }
        
        self._log_call("update_customer_contact", {"user_id": user_id, "contact_type": contact_type, "new_value": new_value}, response)
        return response

    def suspend_line(self, user_id: int, reason: str) -> Dict[str, Any]:
        """Hattı askıya alır."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            self.users[user_id]["status"] = "suspended"  # Mock database'i güncelle
            
            response = {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "line_number": self.users[user_id]["phone"],
                    "suspension_reason": reason,
                    "suspended_at": datetime.now().isoformat(),
                    "reactivation_fee": 0 if reason == "askerlik" else 25.0,
                    "max_suspension_days": 90
                }
            }
        
        self._log_call("suspend_line", {"user_id": user_id, "reason": reason}, response)
        return response

    def reactivate_line(self, user_id: int) -> Dict[str, Any]:
        """Askıdaki hattı tekrar aktive eder."""
        if not self._validate_user_id(user_id):
            response = {"success": False, "error": {"code": "INVALID_USER", "message": f"User {user_id} bulunamadı"}}
        else:
            self.users[user_id]["status"] = "active"  # Mock database'i güncelle
            
            response = {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "line_number": self.users[user_id]["phone"],
                    "reactivated_at": datetime.now().isoformat(),
                    "suspension_duration_days": random.randint(5, 30),
                    "reactivation_fee": random.choice([0, 25.0])
                }
            }
        
        self._log_call("reactivate_line", {"user_id": user_id}, response)
        return response

    # === UTILITY METHODS ===
    
    def get_call_statistics(self) -> Dict[str, Any]:
        """API çağrı istatistiklerini döndürür."""
        if not self.call_log:
            return {"total_calls": 0, "functions": {}}
            
        function_counts = {}
        for call in self.call_log:
            func_name = call["function"]
            function_counts[func_name] = function_counts.get(func_name, 0) + 1
            
        return {
            "total_calls": len(self.call_log),
            "functions": function_counts,
            "success_rate": 100.0,  # Mock sistemde her zaman başarılı
            "last_call": self.call_log[-1]["timestamp"] if self.call_log else None
        }
    
    def reset_call_log(self):
        """API çağrı logunu temizler."""
        self.call_log = []

# Global mock API instance
backend_api = MockTelekomBackendAPI()

if __name__ == "__main__":
    # Test script
    print("🧪 MOCK BACKEND API TEST")
    print("=" * 40)
    
    # Test API calls
    test_user_id = 5108
    
    print(f"\n1️⃣ Testing get_current_bill({test_user_id}):")
    result = backend_api.get_current_bill(test_user_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(f"\n2️⃣ Testing get_customer_package({test_user_id}):")
    result = backend_api.get_customer_package(test_user_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(f"\n3️⃣ Testing check_network_status('İstanbul'):")
    result = backend_api.check_network_status('Marmara')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(f"\n📊 API Call Statistics:")
    stats = backend_api.get_call_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False)) 