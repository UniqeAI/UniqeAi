import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_endpoint():
    """Chat endpoint'ini test et"""
    chat_data = {
        "message": "Merhaba",
        "user_id": 1
    }
    response = client.post("/api/v1/chat/", json=chat_data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "response" in data

def test_chat_endpoint_empty_message():
    """Boş mesaj ile chat endpoint'ini test et"""
    chat_data = {
        "message": "",
        "user_id": 1
    }
    response = client.post("/api/v1/chat/", json=chat_data)
    assert response.status_code == 200

def test_chat_endpoint_no_user_id():
    """User ID olmadan chat endpoint'ini test et"""
    chat_data = {
        "message": "Test mesajı"
    }
    response = client.post("/api/v1/chat/", json=chat_data)
    assert response.status_code == 200

def test_chat_health():
    """Chat sağlık kontrolü endpoint'ini test et"""
    response = client.get("/api/v1/chat/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data

def test_chat_invalid_data():
    """Geçersiz veri ile chat endpoint'ini test et"""
    invalid_data = {
        "invalid_field": "test"
    }
    response = client.post("/api/v1/chat/", json=invalid_data)
    assert response.status_code == 422  # Validation error 