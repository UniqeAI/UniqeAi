import axios from 'axios'

// API konfigürasyonu
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

console.log('API Base URL:', API_BASE_URL)
console.log('API Timeout: Sınırsız')

// Axios instance oluştur - timeout yok
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor - her istekte otomatik olarak eklenen header'lar
apiClient.interceptors.request.use(
  (config) => {
    // Session token varsa ekle
    const sessionToken = localStorage.getItem('session_token')
    if (sessionToken) {
      config.headers['Authorization'] = `Bearer ${sessionToken}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - hata yönetimi
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error)
    
    // Network hatası
    if (!error.response) {
      throw new Error('Sunucuya bağlanılamıyor. Lütfen internet bağlantınızı kontrol edin.')
    }
    
    // HTTP hata kodları
    switch (error.response.status) {
      case 401:
        throw new Error('Oturum süreniz dolmuş. Lütfen tekrar giriş yapın.')
      case 403:
        throw new Error('Bu işlem için yetkiniz bulunmuyor.')
      case 404:
        throw new Error('İstenen kaynak bulunamadı.')
      case 500:
        throw new Error('Sunucu hatası. Lütfen daha sonra tekrar deneyin.')
      default:
        throw new Error(error.response.data?.detail || 'Bir hata oluştu.')
    }
  }
)

// Chat API servisleri
export const chatAPI = {
  // Mesaj gönder
  async sendMessage(message, userId = null, sessionId = null) {
    try {
      console.log('API çağrısı başlıyor:', { message, userId, sessionId })
      console.log('API URL:', API_BASE_URL)
      console.log('Request payload:', {
        message,
        user_id: userId,
        session_id: sessionId,
        session_token: localStorage.getItem('session_token')
      })
      
      const response = await apiClient.post('/api/v1/chat/', {
        message,
        user_id: userId,
        session_id: sessionId,
        session_token: localStorage.getItem('session_token')
      })
      
      console.log('API yanıtı alındı:', response.data)
      return response.data
    } catch (error) {
      console.error('API hatası detayları:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: error.config
      })
      throw error
    }
  },

  // Legacy mesaj gönder
  async sendMessageLegacy(message, userId = null, sessionId = null) {
    try {
      const response = await apiClient.post('/api/v1/chat/legacy', {
        message,
        user_id: userId,
        session_id: sessionId,
        session_token: localStorage.getItem('session_token')
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Oturum temizle
  async clearSession(sessionId) {
    try {
      const response = await apiClient.post('/api/v1/chat/session/clear', {
        session_id: sessionId
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Sistem durumu kontrol et
  async getHealth() {
    try {
      console.log('Health check başlıyor...')
      console.log('API URL:', API_BASE_URL)
      const response = await apiClient.get('/api/v1/health')
      console.log('Health check başarılı:', response.data)
      return response.data
    } catch (error) {
      console.error('Health check hatası:', error)
      throw error
    }
  },

  // Sistem durumu
  async getSystemStatus() {
    try {
      const response = await apiClient.get('/api/v1/chat/system/status')
      return response.data
    } catch (error) {
      throw error
    }
  }
}

// User API servisleri
export const userAPI = {
  // Kullanıcı girişi
  async login(credentials) {
    try {
      const response = await apiClient.post('/api/v1/user/login', credentials)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Kullanıcı kaydı
  async register(userData) {
    try {
      const response = await apiClient.post('/api/v1/user/register', userData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Kullanıcı profili (mevcut kullanıcı)
  async getProfile() {
    try {
      const response = await apiClient.get('/api/v1/user/profile')
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Kullanıcı profili (ID ile)
  async getUserById(userId) {
    try {
      const response = await apiClient.get(`/api/v1/user/by-id/${userId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Kullanıcı profili güncelle
  async updateProfile(userData) {
    try {
      const response = await apiClient.put('/api/v1/user/current', userData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Kullanıcı çıkışı
  async logout() {
    try {
      const response = await apiClient.post('/api/v1/user/logout')
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Tüm aktif kullanıcıları getir
  async getAllActiveUsers() {
    try {
      const response = await apiClient.get('/api/v1/user/all-active')
      return response.data
    } catch (error) {
      throw error
    }
  }
}

// Telekom API servisleri
export const telekomAPI = {
  // Test endpoint
  async test() {
    try {
      const response = await apiClient.get('/api/v1/telekom/test')
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Fatura işlemleri
  async getCurrentBill(userId) {
    try {
      const response = await apiClient.get(`/api/v1/telekom/billing/current/${userId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getCurrentBillPost(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/billing/current', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getBillingHistory(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/billing/history', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async payBill(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/billing/pay', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getPayments(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/billing/payments', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async setAutoPay(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/billing/autopay', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Paket işlemleri
  async getCurrentPackage(userId) {
    try {
      const response = await apiClient.get(`/api/v1/telekom/packages/current/${userId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getCurrentPackagePost(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/packages/current', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getQuotas(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/packages/quotas', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async changePackage(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/packages/change', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getAvailablePackages(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/packages/available', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getPackageDetails(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/packages/details', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Müşteri işlemleri
  async getCustomerProfile(userId) {
    try {
      const response = await apiClient.get(`/api/v1/telekom/customers/profile/${userId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getCustomerProfilePost(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/customers/profile', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async updateCustomerContact(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/customers/contact', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Hizmet işlemleri
  async getRoamingServices(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/services/roaming', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Ağ işlemleri
  async getNetworkStatus(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/network/status', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Destek işlemleri
  async createSupportTicket(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/support/tickets', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async closeSupportTicket(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/support/tickets/close', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getSupportTicketStatus(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/support/tickets/status', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getSupportTicketsList(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/support/tickets/list', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Diagnostik işlemleri
  async testInternetSpeed(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/diagnostics/speed-test', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Hat işlemleri
  async suspendLine(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/lines/suspend', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async reactivateLine(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/lines/reactivate', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Kimlik doğrulama işlemleri
  async registerAuth(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/auth/register', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async loginAuth(data) {
    try {
      const response = await apiClient.post('/api/v1/telekom/auth/login', data)
      return response.data
    } catch (error) {
      throw error
    }
  }
}

// AI API servisleri
export const aiAPI = {
  // AI model bilgilerini getir
  async getModelInfo() {
    try {
      const response = await apiClient.get('/api/v1/ai/model-info')
      return response.data
    } catch (error) {
      throw error
    }
  }
}

export default apiClient 