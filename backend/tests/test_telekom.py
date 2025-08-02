import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_current_bill():
    """Mevcut fatura endpoint'ini test et"""
    data = {"user_id": 1}
    response = client.post("/api/v1/telekom/billing/current", json=data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "data" in data

def test_get_bill_history():
    """Fatura geçmişi endpoint'ini test et"""
    data = {"user_id": 1, "limit": 5}
    response = client.post("/api/v1/telekom/billing/history", json=data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_pay_bill():
    """Fatura ödeme endpoint'ini test et"""
    data = {"bill_id": "BILL001", "method": "kredi_karti"}
    response = client.post("/api/v1/telekom/billing/pay", json=data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_get_current_package():
    """Mevcut paket endpoint'ini test et"""
    data = {"user_id": 1}
    response = client.post("/api/v1/telekom/packages/current", json=data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_get_remaining_quotas():
    """Kalan kotalar endpoint'ini test et"""
    data = {"user_id": 1}
    response = client.post("/api/v1/telekom/packages/quotas", json=data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_get_available_packages():
    """Kullanılabilir paketler endpoint'ini test et"""
    response = client.post("/api/v1/telekom/packages/available")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_get_customer_profile():
    """Müşteri profili endpoint'ini test et"""
    data = {"user_id": 1}
    response = client.post("/api/v1/telekom/customers/profile", json=data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_create_support_ticket():
    """Destek talebi oluşturma endpoint'ini test et"""
    data = {
        "user_id": 1,
        "issue_description": "İnternet bağlantım yavaş",
        "category": "technical"
    }
    response = client.post("/api/v1/telekom/support/tickets", json=data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_check_network_status():
    """Ağ durumu kontrolü endpoint'ini test et"""
    data = {"region": "istanbul"}
    response = client.post("/api/v1/telekom/network/status", json=data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data 