"""
Telekom API endpoint'lerini test eden test dosyası
"""

import pytest
import httpx
import asyncio
from fastapi.testclient import TestClient
from backend.app.main import app

# Test client
client = TestClient(app)

class TestTelekomAPI:
    """Telekom API endpoint'lerini test eden sınıf"""
    
    def test_get_current_bill(self):
        """Mevcut fatura endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/billing/current",
            json={"user_id": 5108}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert data["data"]["user_id"] == 5108
        assert "bill_id" in data["data"]
        assert "amount" in data["data"]
    
    def test_get_past_bills(self):
        """Geçmiş faturalar endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/billing/history",
            json={"user_id": 3680, "limit": 12}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "bills" in data["data"]
        assert "total_count" in data["data"]
    
    def test_pay_bill(self):
        """Fatura ödeme endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/billing/pay",
            json={"bill_id": "F-2024-4306", "method": "credit_card"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert data["data"]["bill_id"] == "F-2024-4306"
        assert data["data"]["method"] == "credit_card"
    
    def test_get_customer_package(self):
        """Müşteri paketi endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/packages/current",
            json={"user_id": 9408}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "package_name" in data["data"]
        assert "monthly_fee" in data["data"]
    
    def test_get_remaining_quotas(self):
        """Kalan kotalar endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/packages/quotas",
            json={"user_id": 9408}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "internet_remaining_gb" in data["data"]
        assert "voice_remaining_minutes" in data["data"]
    
    def test_change_package(self):
        """Paket değişikliği endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/packages/change",
            json={"user_id": 9509, "new_package_name": "Öğrenci Dostu Tarife"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert data["data"]["to_package"] == "Öğrenci Dostu Tarife"
    
    def test_get_available_packages(self):
        """Kullanılabilir paketler endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/packages/available",
            json={}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "packages" in data["data"]
        assert len(data["data"]["packages"]) > 0
    
    def test_create_fault_ticket(self):
        """Arıza talebi oluşturma endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/support/tickets",
            json={
                "user_id": 7477,
                "issue_description": "Ev internetimin hızı çok yavaşladı"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "ticket_id" in data["data"]
        assert data["data"]["user_id"] == 7477
    
    def test_get_customer_profile(self):
        """Müşteri profili endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/customers/profile",
            json={"user_id": 2122}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "name" in data["data"]
        assert "phone_numbers" in data["data"]
    
    def test_check_network_status(self):
        """Ağ durumu endpoint'ini test et"""
        response = client.post(
            "/api/v1/telekom/network/status",
            json={"region": "Güneydoğu Anadolu"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert data["data"]["region"] == "Güneydoğu Anadolu"
        assert "status" in data["data"]

class TestTelekomAPIErrorHandling:
    """Hata durumlarını test eden sınıf"""
    
    def test_invalid_user_id(self):
        """Geçersiz user_id ile test"""
        response = client.post(
            "/api/v1/telekom/billing/current",
            json={"user_id": "invalid"}
        )
        
        # Pydantic validation hatası bekleniyor
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Eksik zorunlu alanlarla test"""
        response = client.post(
            "/api/v1/telekom/billing/current",
            json={}  # user_id eksik
        )
        
        assert response.status_code == 422
    
    def test_invalid_json(self):
        """Geçersiz JSON ile test"""
        response = client.post(
            "/api/v1/telekom/billing/current",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422

if __name__ == "__main__":
    # Test'leri çalıştır
    pytest.main([__file__, "-v"]) 