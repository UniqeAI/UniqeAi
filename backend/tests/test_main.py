import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Ana sayfa endpoint'ini test et"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_check():
    """Sağlık kontrolü endpoint'ini test et"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_favicon():
    """Favicon endpoint'ini test et"""
    response = client.get("/favicon.ico")
    assert response.status_code == 204

def test_docs():
    """API dokümantasyonu endpoint'ini test et"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi():
    """OpenAPI şeması endpoint'ini test et"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json() 