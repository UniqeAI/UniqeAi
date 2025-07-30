import urllib.request
import urllib.parse
import json
import streamlit as st
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TelekomAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """HTTP isteği gönder"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                if data:
                    # GET istekleri için parametreleri URL'e ekle
                    params = urllib.parse.urlencode(data)
                    url = f"{url}?{params}"
                response = urllib.request.urlopen(url)
            elif method.upper() == "POST":
                if data:
                    data_bytes = json.dumps(data).encode('utf-8')
                    req = urllib.request.Request(
                        url, 
                        data=data_bytes,
                        headers={"Content-Type": "application/json"}
                    )
                else:
                    req = urllib.request.Request(url)
                response = urllib.request.urlopen(req)
            else:
                raise ValueError(f"Desteklenmeyen HTTP method: {method}")
            
            result = json.loads(response.read().decode())
            return result
            
        except urllib.error.HTTPError as e:
            # HTTP hata kodlarını yakala
            error_detail = "Bilinmeyen hata"
            try:
                error_response = json.loads(e.read().decode())
                if "detail" in error_response:
                    error_detail = error_response["detail"]
            except:
                pass
            
            if e.code == 401:
                return {
                    "success": False,
                    "error": "Kullanıcı kaydı yok veya şifre hatalı"
                }
            elif e.code == 400:
                return {
                    "success": False,
                    "error": f"Geçersiz istek: {error_detail}"
                }
            elif e.code == 500:
                return {
                    "success": False,
                    "error": f"Sunucu hatası: {error_detail}"
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {e.code}: {error_detail}"
                }
        except urllib.error.URLError as e:
            logger.error(f"API isteği hatası: {e}")
            return {
                "success": False,
                "error": f"Bağlantı hatası: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {e}")
            return {
                "success": False,
                "error": f"Hata: {str(e)}"
            }
    
    # === KULLANICI İŞLEMLERİ ===
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Kullanıcı kayıt"""
        return self._make_request("POST", "/api/v1/user/register", user_data)
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Kullanıcı giriş"""
        return self._make_request("POST", "/api/v1/user/login", {
            "email": email,
            "password": password
        })
    
    def get_current_user(self) -> Dict[str, Any]:
        """Geçerli kullanıcı bilgileri"""
        return self._make_request("GET", "/api/v1/user/current")
    
    def logout_user(self) -> Dict[str, Any]:
        """Kullanıcı çıkış"""
        return self._make_request("POST", "/api/v1/user/logout")
    
    # === CHAT İŞLEMLERİ ===
    def send_chat_message(self, message: str, user_id: int = None) -> Dict[str, Any]:
        """AI'ya mesaj gönder"""
        return self._make_request("POST", "/api/v1/chat/", {
            "message": message,
            "user_id": user_id
        })
    
    def check_chat_health(self) -> Dict[str, Any]:
        """Chat servisi sağlık kontrolü"""
        return self._make_request("GET", "/api/v1/chat/health")
    
    # === FATURA İŞLEMLERİ ===
    def get_current_bill(self, user_id: int) -> Dict[str, Any]:
        """Mevcut fatura getir"""
        return self._make_request("POST", "/api/v1/telekom/billing/current", {
            "user_id": user_id
        })
    
    def get_bill_history(self, user_id: int, limit: int = 12) -> Dict[str, Any]:
        """Fatura geçmişi getir"""
        return self._make_request("POST", "/api/v1/telekom/billing/history", {
            "user_id": user_id,
            "limit": limit
        })
    
    def pay_bill(self, bill_id: str, method: str = "kredi_karti") -> Dict[str, Any]:
        """Fatura öde"""
        return self._make_request("POST", "/api/v1/telekom/billing/pay", {
            "bill_id": bill_id,
            "method": method
        })
    
    # === PAKET İŞLEMLERİ ===
    def get_current_package(self, user_id: int) -> Dict[str, Any]:
        """Mevcut paket getir"""
        return self._make_request("POST", "/api/v1/telekom/packages/current", {
            "user_id": user_id
        })
    
    def get_remaining_quotas(self, user_id: int) -> Dict[str, Any]:
        """Kalan kotalar"""
        return self._make_request("POST", "/api/v1/telekom/packages/quotas", {
            "user_id": user_id
        })
    
    def get_available_packages(self) -> Dict[str, Any]:
        """Kullanılabilir paketler"""
        return self._make_request("POST", "/api/v1/telekom/packages/available")
    
    # === MÜŞTERİ İŞLEMLERİ ===
    def get_customer_profile(self, user_id: int) -> Dict[str, Any]:
        """Müşteri profili"""
        return self._make_request("POST", "/api/v1/telekom/customers/profile", {
            "user_id": user_id
        })
    
    # === DESTEK İŞLEMLERİ ===
    def create_support_ticket(self, user_id: int, description: str, category: str = "technical") -> Dict[str, Any]:
        """Destek talebi oluştur"""
        return self._make_request("POST", "/api/v1/telekom/support/tickets", {
            "user_id": user_id,
            "issue_description": description,
            "category": category
        })
    
    def check_network_status(self, region: str) -> Dict[str, Any]:
        """Ağ durumu kontrolü"""
        return self._make_request("POST", "/api/v1/telekom/network/status", {
            "region": region
        })

# Global API client instance
@st.cache_resource
def get_api_client() -> TelekomAPIClient:
    """API client singleton"""
    return TelekomAPIClient() 