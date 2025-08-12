#!/usr/bin/env python3
"""
Basit FastAPI Backend Servisi
Bağlantı sorunlarını test etmek için minimal server
"""

from fastapi import FastAPI
import uvicorn

# FastAPI uygulaması oluştur
app = FastAPI(
    title="UniqueAi Test Backend",
    description="Bağlantı testi için basit backend",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "🚀 Backend başarıyla çalışıyor!",
        "status": "ok",
        "port": 8000
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "UniqueAi Backend"
    }

@app.get("/test")
def test_endpoint():
    return {
        "test": "success",
        "message": "Test endpoint çalışıyor"
    }

if __name__ == "__main__":
    print("🚀 Backend başlatılıyor...")
    print("📡 URL: http://localhost:8000")
    print("🩺 Health: http://localhost:8000/health")
    print("🧪 Test: http://localhost:8000/test")
    print("📖 Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000, 
        log_level="info"
    )
