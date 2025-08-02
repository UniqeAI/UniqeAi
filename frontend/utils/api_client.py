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
        self.session_token = None  # Session token'ı saklamak için
    
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
        result = self._make_request("POST", "/api/v1/telekom/auth/register", user_data)
        
        # Başarılı kayıt durumunda session token'ı sakla
        if result.get("success"):
            self.session_token = result.get("session_token")
        
        return result
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Kullanıcı giriş"""
        result = self._make_request("POST", "/api/v1/telekom/auth/login", {
            "email": email,
            "password": password
        })
        
        # Başarılı giriş durumunda session token'ı sakla
        if result.get("success"):
            self.session_token = result.get("session_token")
        
        return result
    
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
            "user_id": user_id,
            "session_token": self.session_token
        })
    
    def check_chat_health(self) -> Dict[str, Any]:
        """Chat servisi sağlık kontrolü"""
        return self._make_request("GET", "/api/v1/chat/health")
    
    # === FATURA İŞLEMLERİ ===
    def get_current_bill(self) -> Dict[str, Any]:
        """Mevcut fatura getir"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/billing/current", {
            "session_token": self.session_token
        })
    
    def get_bill_history(self, limit: int = 12) -> Dict[str, Any]:
        """Fatura geçmişi getir"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/billing/history", {
            "session_token": self.session_token,
            "limit": limit
        })
    
    def pay_bill(self, bill_id: str, method: str = "kredi_karti") -> Dict[str, Any]:
        """Fatura öde"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/billing/pay", {
            "session_token": self.session_token,
            "bill_id": bill_id,
            "method": method
        })
    
    # === PAKET İŞLEMLERİ ===
    def get_current_package(self) -> Dict[str, Any]:
        """Mevcut paket getir"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/packages/current", {
            "session_token": self.session_token
        })
    
    def get_remaining_quotas(self) -> Dict[str, Any]:
        """Kalan kotalar"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/packages/quotas", {
            "session_token": self.session_token
        })
    
    def get_available_packages(self) -> Dict[str, Any]:
        """Kullanılabilir paketler"""
        return self._make_request("POST", "/api/v1/telekom/packages/available")
    
    # === MÜŞTERİ İŞLEMLERİ ===
    def get_customer_profile(self) -> Dict[str, Any]:
        """Müşteri profili"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/customers/profile", {
            "session_token": self.session_token
        })
    
    # === DESTEK İŞLEMLERİ ===
    def create_support_ticket(self, description: str, category: str = "technical") -> Dict[str, Any]:
        """Destek talebi oluştur"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/support/tickets", {
            "session_token": self.session_token,
            "issue_description": description,
            "category": category
        })
    
    def check_network_status(self, region: str) -> Dict[str, Any]:
        """Ağ durumu kontrolü"""
        return self._make_request("POST", "/api/v1/telekom/network/status", {
            "region": region
        })
    
    # === EKSİK ENDPOINT'LER ===
    
    # Fatura İşlemleri
    def get_payment_history(self) -> Dict[str, Any]:
        """Ödeme geçmişi getir"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/billing/payments", {
            "session_token": self.session_token
        })
    
    def setup_autopay(self, status: bool) -> Dict[str, Any]:
        """Otomatik ödeme ayarla"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/billing/autopay", {
            "session_token": self.session_token,
            "status": status
        })
    
    # Paket İşlemleri
    def change_package(self, new_package_name: str) -> Dict[str, Any]:
        """Paket değiştir"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/packages/change", {
            "session_token": self.session_token,
            "new_package_name": new_package_name
        })
    
    def get_package_details(self, package_name: str) -> Dict[str, Any]:
        """Paket detayları getir"""
        return self._make_request("POST", "/api/v1/telekom/packages/details", {
            "package_name": package_name
        })
    
    # Müşteri İşlemleri
    def update_customer_contact(self, contact_type: str, new_value: str) -> Dict[str, Any]:
        """Müşteri iletişim bilgilerini güncelle"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/customers/contact", {
            "session_token": self.session_token,
            "contact_type": contact_type,
            "new_value": new_value
        })
    
    # Destek İşlemleri
    def close_fault_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Destek talebini kapat"""
        return self._make_request("POST", "/api/v1/telekom/support/tickets/close", {
            "ticket_id": ticket_id
        })
    
    def get_fault_ticket_status(self, ticket_id: str) -> Dict[str, Any]:
        """Destek talebi durumu getir"""
        return self._make_request("POST", "/api/v1/telekom/support/tickets/status", {
            "ticket_id": ticket_id
        })
    
    def get_users_tickets(self) -> Dict[str, Any]:
        """Kullanıcının destek taleplerini getir"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/support/tickets/list", {
            "session_token": self.session_token
        })
    
    # Sistem İşlemleri
    def test_internet_speed(self) -> Dict[str, Any]:
        """İnternet hız testi yap"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/diagnostics/speed-test", {
            "session_token": self.session_token
        })
    
    def suspend_line(self, reason: str) -> Dict[str, Any]:
        """Hat askıya al"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/lines/suspend", {
            "session_token": self.session_token,
            "reason": reason
        })
    
    def reactivate_line(self) -> Dict[str, Any]:
        """Hat yeniden aktifleştir"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/lines/reactivate", {
            "session_token": self.session_token
        })
    
    # Roaming İşlemleri
    def enable_roaming(self, status: bool) -> Dict[str, Any]:
        """Roaming servisini aktifleştir/devre dışı bırak"""
        if not self.session_token:
            return {"success": False, "error": "Oturum açmanız gerekiyor"}
        
        return self._make_request("POST", "/api/v1/telekom/services/roaming", {
            "session_token": self.session_token,
            "status": status
        })
    
    # === TELEKOM AUTH ENDPOINT'LERİ ===
    
    def telekom_register(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Telekom auth register"""
        return self._make_request("POST", "/api/v1/telekom/auth/register", user_data)
    
    def telekom_login(self, email: str, password: str) -> Dict[str, Any]:
        """Telekom auth login"""
        return self._make_request("POST", "/api/v1/telekom/auth/login", {
            "email": email,
            "password": password
        })

# Global API client instance
@st.cache_resource
def get_api_client() -> TelekomAPIClient:
    """API client singleton"""
    return TelekomAPIClient() 