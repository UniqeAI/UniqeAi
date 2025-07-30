import os
from typing import Literal

class Settings:
    """Uygulama ayarları"""
    
    # AI Model Seçimi
    AI_MODEL_TYPE: Literal["mock", "real"] = os.getenv("AI_MODEL_TYPE", "real")
    
    # Hugging Face Model Ayarları
    HUGGING_FACE_MODEL_NAME: str = os.getenv(
        "HUGGING_FACE_MODEL_NAME", 
        "Choyrens/ChoyrensAI-Telekom-Agent-v1-merged"
    )
    
    # Backend Ayarları
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # CORS Ayarları
    CORS_ORIGINS: list = [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Logging Ayarları
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Test Ayarları
    TESTING: bool = os.getenv("TESTING", "false").lower() == "true"
    
    @classmethod
    def get_ai_orchestrator_class(cls) -> str:
        """AI orchestrator sınıfını döndür"""
        if cls.AI_MODEL_TYPE == "real":
            return "ai_orchestrator_real"
        else:
            return "ai_orchestrator"
    
    @classmethod
    def is_mock_mode(cls) -> bool:
        """Mock modda mı kontrol et"""
        return cls.AI_MODEL_TYPE == "mock"
    
    @classmethod
    def is_real_ai_mode(cls) -> bool:
        """Gerçek AI modda mı kontrol et"""
        return cls.AI_MODEL_TYPE == "real"

# Global settings instance
settings = Settings() 