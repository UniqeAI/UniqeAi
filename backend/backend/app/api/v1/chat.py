"""
Chat endpoint'i - AI ile sohbet için API
"""

from fastapi import APIRouter, HTTPException
from ...schemas.chat import ChatMessage, ChatResponse
from typing import Dict, Any

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Chat endpoint'i - AI ile sohbet
    
    Args:
        chat_message: Kullanıcı mesajı
        
    Returns:
        AI yanıtı (şimdilik sabit)
    """
    try:
        # Şimdilik sabit yanıt
        response = "Merhaba! Bu bir test yanıtıdır. Gerçek AI entegrasyonu gelecek haftalarda eklenecek."
        
        return ChatResponse(
            success=True,
            message="AI yanıtı başarıyla oluşturuldu",
            data={
                "response": response,
                "user_message": chat_message.message,
                "user_id": chat_message.user_id
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat işlemi sırasında hata oluştu: {str(e)}"
        ) 