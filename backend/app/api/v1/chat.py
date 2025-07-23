"""
Chat endpoint'i - AI ile sohbet için API
"""

from fastapi import APIRouter, HTTPException
from backend.app.schemas.chat import ChatMessage, ChatResponse
from backend.app.services.ai_orchestrator import ai_orchestrator
from typing import Dict, Any
import uuid

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Chat endpoint'i - AI ile sohbet
    Args:
        chat_message: Kullanıcı mesajı
    Returns:
        AI yanıtı
    """
    try:
        # Oturum ID oluştur (gerçek uygulamada kullanıcı oturumundan alınır)
        oturum_id = chat_message.session_id or f"SESSION_{uuid.uuid4().hex[:8]}"
        # AI orkestratör ile mesajı işle
        ai_sonuc = await ai_orchestrator.kullanici_mesaj_isle(
            mesaj=chat_message.message,
            kullanici_id=chat_message.user_id,
            oturum_id=oturum_id
        )
        return ChatResponse(
            success=True,
            message="AI yanıtı başarıyla oluşturuldu",
            data={
                "response": ai_sonuc["yanit"],
                "user_message": chat_message.message,
                "user_id": chat_message.user_id,
                "session_id": oturum_id,
                "yanit_id": ai_sonuc["yanit_id"],
                "guven_puani": ai_sonuc["guven_puani"],
                "arac_cagrilari": ai_sonuc["arac_cagrilari"],
                "metadata": ai_sonuc["metadata"]
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat işlemi sırasında hata oluştu: {str(e)}"
        )

@router.post("/session/clear")
async def clear_session(session_id: str):
    """
    Oturum konuşma geçmişini temizle
    Args:
        session_id: Temizlenecek oturum ID
    Returns:
        Temizleme durumu
    """
    try:
        await ai_orchestrator.oturum_temizle(session_id)
        return {
            "success": True,
            "message": "Oturum geçmişi başarıyla temizlendi",
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Oturum temizleme sırasında hata oluştu: {str(e)}"
        )

@router.get("/system/status")
async def system_status():
    """
    Sistem durumu bilgilerini getir
    Returns:
        Sistem durumu
    """
    try:
        durum = await ai_orchestrator.sistem_durumu_getir()
        return {
            "success": True,
            "message": "Sistem durumu başarıyla getirildi",
            "data": durum
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Sistem durumu getirme sırasında hata oluştu: {str(e)}"
        ) 