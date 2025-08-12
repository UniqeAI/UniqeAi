from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="UniqueAi Backend",
    description="UniqueAi projesi için API'leri ve AI modelini sunan servis.",
    version="1.0.0",
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health", tags=["Monitoring"])
def health_check():
    """
    Servisin ayakta olup olmadığını kontrol eden endpoint.
    """
    return {
        "status": "ok",
        "ai_model_type": settings.AI_MODEL_TYPE,
        "backend_version": "1.0.0"
    }

@app.get("/", tags=["Monitoring"])
def root():
    return {"status":"ok"}

# favicon.ico isteğini sessizce yut (dosya olmadan)
@app.get("/favicon.ico")
def ignore_favicon():
    return Response(status_code=204)  # No Content

# Chat router'ını dahil et
from app.api.v1 import chat
app.include_router(chat.router, prefix="/api/v1")

# Mock test router'ı kaldırıldı - artık gerekli değil

# Telekom API router'ını dahil et
from app.api.v1 import telekom
app.include_router(telekom.router, prefix="/api/v1")

# User router'ını dahil et
from app.api.v1 import user
app.include_router(user.router, prefix="/api/v1")

# AI Model bilgisi endpoint'i
@app.get("/api/v1/ai/model-info", tags=["AI"])
def get_ai_model_info():
    """
    AI model bilgilerini döndür
    """
    return {
        "model_type": settings.AI_MODEL_TYPE,
        "model_name": settings.HUGGING_FACE_MODEL_NAME if settings.is_real_ai_mode() else "Mock AI Model",
        "is_mock_mode": settings.is_mock_mode(),
        "is_real_ai_mode": settings.is_real_ai_mode()
    }

# Gelecekte eklenecek diğer endpoint'ler için router'lar buraya dahil edilecek. 