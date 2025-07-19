from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Agent-Llama Backend",
    description="Agent-Llama projesi için mock API'leri ve AI modelini sunan servis.",
    version="0.1.0",
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Güvenlik için production'da spesifik domain'ler belirtin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health", tags=["Monitoring"])
def health_check():
    """
    Servisin ayakta olup olmadığını kontrol eden endpoint.
    """
    return {"status": "ok"}

@app.get("/", tags=["Monitoring"])
def root():
    return {"status":"ok"}

# favicon.ico isteğini sessizce yut (dosya olmadan)
@app.get("/favicon.ico")
def ignore_favicon():
    return Response(status_code=204)  # No Content

# Chat router'ını dahil et
from backend.app.api.v1 import chat
app.include_router(chat.router, prefix="/api/v1")

# Mock test router'ını dahil et
from backend.app.api.v1 import mock_test
app.include_router(mock_test.router, prefix="/api/v1")

# Telekom API router'ını dahil et
from backend.app.api.v1 import telekom
app.include_router(telekom.router, prefix="/api/v1")

# User router'ını dahil et
from backend.app.api.v1 import user
app.include_router(user.router, prefix="/api/v1")

# Gelecekte eklenecek diğer endpoint'ler için router'lar buraya dahil edilecek. 