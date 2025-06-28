from fastapi import FastAPI

app = FastAPI(
    title="Agent-Llama Backend",
    description="Agent-Llama projesi için mock API'leri ve AI modelini sunan servis.",
    version="0.1.0",
)

@app.get("/api/v1/health", tags=["Monitoring"])
def health_check():
    """
    Servisin ayakta olup olmadığını kontrol eden endpoint.
    """
    return {"status": "ok"}

# Gelecekte eklenecek diğer endpoint'ler için router'lar buraya dahil edilecek.
# from .api.v1 import chat
# app.include_router(chat.router, prefix="/api/v1") 