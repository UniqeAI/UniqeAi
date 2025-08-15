"""
Chat endpoint'i - AI ile sohbet için API
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uuid
import logging

from app.schemas.chat import ChatMessage, ChatResponse
from app.services.ai_orchestrator_v4 import ai_orchestrator_v4 as ai_orchestrator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    """Chat isteği modeli"""
    message: str
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    session_token: Optional[str] = None

class ChatResponseNew(BaseModel):
    """Chat yanıt modeli"""
    success: bool
    response: str
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    confidence: float = 0.0
    tool_calls: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}

@router.post("/", response_model=ChatResponseNew)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint'i - AI ile sohbet
    
    Args:
        request: Chat isteği
        
    Returns:
        AI yanıtı
    """
    try:
        # 1/4: Mesaj alındı
        oturum_id = request.session_id or f"SESSION_{uuid.uuid4().hex[:8]}"
        logger.info(f"[1/4] Mesaj alındı | session_id={oturum_id} user_id={request.user_id} text_len={len(request.message)}")
        
        # Özel "Backend nerede" kontrolü
        if "backend" in request.message.lower() or "nerede" in request.message.lower():
            return ChatResponseNew(
                success=True,
                response="Buradayım! Backend sistemi aktif ve çalışıyor. Size nasıl yardımcı olabilirim?",
                user_id=request.user_id,
                session_id=oturum_id,
                confidence=0.95,
                tool_calls=[],
                metadata={
                    "yanit_id": str(uuid.uuid4()),
                    "tool_results": [],
                    "processing_time": "< 1s",
                    "response_type": "backend_status"
                }
            )
        
        # 2/4: Orkestrasyon başlıyor
        logger.info("[2/4] Orkestrasyon başlıyor")
        try:
            import asyncio
            ai_sonuc = await asyncio.wait_for(
                ai_orchestrator.kullanici_mesaj_isle(
                    mesaj=request.message,
                    kullanici_id=str(request.user_id) if request.user_id else "1",
                    oturum_id=oturum_id,
                    session_token=request.session_token
                ),
                timeout=120.0  # 120 saniye timeout (2 dakika)
            )
        except asyncio.TimeoutError:
            logger.error("[HATA] Orkestrasyon zaman aşımı")
            return ChatResponseNew(
                success=False,
                response="AI modeli şu anda meşgul. Lütfen daha sonra tekrar deneyin.",
                user_id=request.user_id,
                session_id=oturum_id,
                confidence=0.0,
                tool_calls=[],
                metadata={
                    "yanit_id": str(uuid.uuid4()),
                    "tool_results": [],
                    "processing_time": "timeout",
                    "response_type": "timeout_error"
                }
            )
        
        # 3/4: Orkestrasyon tamamlandı
        tool_count = len(ai_sonuc.get("arac_cagrilari", [])) if isinstance(ai_sonuc, dict) else 0
        logger.info(f"[3/4] Orkestrasyon tamamlandı | tool_sayisi={tool_count} yanit_id={ai_sonuc.get('yanit_id') if isinstance(ai_sonuc, dict) else 'N/A'}")
        
        # 4/4: Yanıt gönderiliyor
        if ai_sonuc.get("yanit"):
            logger.info("[4/4] Yanıt gönderiliyor")
            return ChatResponseNew(
                success=True,
                response=ai_sonuc["yanit"],
                user_id=request.user_id,
                session_id=oturum_id,
                confidence=ai_sonuc.get("guven_puani", 0.95),
                tool_calls=[
                    {
                        "arac_adi": arac.get("arac_adi", "N/A"),
                        "parametreler": arac.get("parametreler", {}),
                        "durum": arac.get("durum", "beklemede"),
                        "sonuc": arac.get("sonuc", None),
                        "hata_mesaji": arac.get("hata_mesaji", None)
                    }
                    for arac in ai_sonuc.get("arac_cagrilari", [])
                ],
                metadata={
                    "yanit_id": ai_sonuc.get("yanit_id"),
                    "tool_results": ai_sonuc.get("arac_cagrilari", []),
                    "processing_time": "< 1s"
                }
            )
        else:
            return ChatResponseNew(
                success=False,
                response="Bir hata oluştu",
                user_id=request.user_id,
                session_id=oturum_id
            )
        
    except Exception as e:
        logger.error(f"Chat endpoint hatası: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat işlemi sırasında hata oluştu: {str(e)}"
        )

@router.post("/legacy", response_model=ChatResponse)
async def chat_endpoint_legacy(chat_message: ChatMessage):
    """
    Legacy chat endpoint'i - Geriye uyumluluk için
    
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

@router.get("/health")
async def chat_health():
    """
    Chat servisi sağlık kontrolü
    
    Returns:
        Sistem durumu
    """
    try:
        durum = await ai_orchestrator.sistem_durumu_getir()
        
        return {
            "status": "healthy" if durum.get("sistem_durumu") == "aktif" else "unhealthy",
            "model_loaded": durum.get("model_yuklu", False),
            "model_name": durum.get("model_adi", "unknown"),
            "active_sessions": durum.get("aktif_oturum_sayisi", 0),
            "registered_tools": durum.get("kayitli_arac_sayisi", 0)
        }
        
    except Exception as e:
        logger.error(f"Health check hatası: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

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