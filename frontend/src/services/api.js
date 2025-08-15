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

// Feedback API servisleri
export const feedbackAPI = {
  // Feedback gönder
  async submitFeedback(feedbackData) {
    try {
      console.log('Feedback gönderiliyor:', feedbackData)
      
      const response = await apiClient.post('/api/v1/feedback', feedbackData)
      
      console.log('Feedback yanıtı:', response.data)
      return response.data
    } catch (error) {
      console.error('Feedback gönderme hatası:', error)
      throw error
    }
  },

  // Kullanıcı feedback istatistiklerini getir
  async getUserFeedbackStats(userId) {
    try {
      const response = await apiClient.get(`/api/v1/feedback/stats/${userId}`)
      return response.data
    } catch (error) {
      console.error('Feedback istatistik hatası:', error)
      throw error
    }
  }
}

// Telekom API servisleri
export const telekomAPI = {
  // Auth endpoints
  async register(userData) {
    const response = await apiClient.post('/api/v1/telekom/auth/register', userData)
    return response.data
  },
  async login(email, password) {
    const response = await apiClient.post('/api/v1/telekom/auth/login', { email, password })
    return response.data
  },

  // Billing endpoints
  async getCurrentBill(sessionToken) {
    const response = await apiClient.post('/api/v1/telekom/billing/current', {
      session_token: sessionToken
    })
    return response.data
  },
  async getBillHistory(sessionToken, limit = 12) {
    const response = await apiClient.post('/api/v1/telekom/billing/history', {
      session_token: sessionToken,
      limit: limit
    })
    return response.data
  },
  async payBill(sessionToken, billId, method) {
    const response = await apiClient.post('/api/v1/telekom/billing/pay', {
      session_token: sessionToken,
      bill_id: billId,
      method: method
    })
    return response.data
  },
  async getPaymentHistory(sessionToken) {
    const response = await apiClient.post('/api/v1/telekom/billing/payments', {
      session_token: sessionToken
    })
    return response.data
  },
  async setupAutopay(sessionToken, status) {
    const response = await apiClient.post('/api/v1/telekom/billing/autopay', {
      session_token: sessionToken,
      status: status
    })
    return response.data
  },

  // Package endpoints
  async getCurrentPackage(sessionToken) {
    const response = await apiClient.post('/api/v1/telekom/packages/current', {
      session_token: sessionToken
    })
    return response.data
  },
  async getRemainingQuotas(sessionToken) {
    const response = await apiClient.post('/api/v1/telekom/packages/quotas', {
      session_token: sessionToken
    })
    return response.data
  },
  async changePackage(sessionToken, newPackageName) {
    const response = await apiClient.post('/api/v1/telekom/packages/change', {
      session_token: sessionToken,
      new_package_name: newPackageName
    })
    return response.data
  },
  async getAvailablePackages() {
    const response = await apiClient.post('/api/v1/telekom/packages/available')
    return response.data
  },
  async getPackageDetails(packageName) {
    const response = await apiClient.post('/api/v1/telekom/packages/details', {
      package_name: packageName
    })
    return response.data
  },

  // Customer endpoints
  async getCustomerProfile(sessionToken) {
    const response = await apiClient.post('/api/v1/telekom/customers/profile', {
      session_token: sessionToken
    })
    return response.data
  },
  async updateCustomerContact(sessionToken, contactType, newValue) {
    const response = await apiClient.post('/api/v1/telekom/customers/contact', {
      session_token: sessionToken,
      contact_type: contactType,
      new_value: newValue
    })
    return response.data
  },

  // Support endpoints
  async createSupportTicket(sessionToken, issueDescription, category, priority) {
    const response = await apiClient.post('/api/v1/telekom/support/tickets', {
      session_token: sessionToken,
      issue_description: issueDescription,
      category: category,
      priority: priority
    })
    return response.data
  },
  async closeSupportTicket(ticketId) {
    const response = await apiClient.post('/api/v1/telekom/support/tickets/close', {
      ticket_id: ticketId
    })
    return response.data
  },
  async getSupportTicketStatus(ticketId) {
    const response = await apiClient.post('/api/v1/telekom/support/tickets/status', {
      ticket_id: ticketId
    })
    return response.data
  },
  async getSupportTickets(sessionToken) {
    const response = await apiClient.post('/api/v1/telekom/support/tickets/list', {
      session_token: sessionToken
    })
    return response.data
  },

  // Services endpoints
  async enableRoaming(sessionToken, status) {
    const response = await apiClient.post('/api/v1/telekom/services/roaming', {
      session_token: sessionToken,
      status: status
    })
    return response.data
  },
  async suspendLine(sessionToken, reason) {
    const response = await apiClient.post('/api/v1/telekom/lines/suspend', {
      session_token: sessionToken,
      reason: reason
    })
    return response.data
  },
  async reactivateLine(sessionToken) {
    const response = await apiClient.post('/api/v1/telekom/lines/reactivate', {
      session_token: sessionToken
    })
    return response.data
  },

  // Network & Diagnostics endpoints
  async checkNetworkStatus(region) {
    const response = await apiClient.post('/api/v1/telekom/network/status', {
      region: region
    })
    return response.data
  },
  async testInternetSpeed(sessionToken) {
    const response = await apiClient.post('/api/v1/telekom/diagnostics/speed-test', {
      session_token: sessionToken
    })
    return response.data
  },

  // Test endpoint
  async test() {
    const response = await apiClient.get('/api/v1/telekom/test')
    return response.data
  }
}

// Chat API servisleri
export const chatAPI = {
  // Mesaj gönder
  async sendMessage(message, userId = null, sessionId = null, aiModel = null) {
    try {
      console.log('API çağrısı başlıyor:', { message, userId, sessionId, aiModel })
      console.log('API URL:', API_BASE_URL)
      console.log('Request payload:', {
        message,
        user_id: userId,
        session_id: sessionId,
        ai_model: aiModel,
        session_token: localStorage.getItem('session_token')
      })
      
      const response = await apiClient.post('/api/v1/chat/', {
        message,
        user_id: userId,
        session_id: sessionId,
        ai_model: aiModel,
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

  // Oturum temizle
  async clearSession(sessionId) {
    try {
      const response = await apiClient.post('/api/v1/chat/session/clear', {
        session_id: sessionId
      })
      return response.data
    } catch (error) {
      console.error('Oturum temizleme hatası:', error)
      throw error
    }
  },

  // Chat health
  async getHealth() {
    try {
      const response = await apiClient.get('/api/v1/chat/health')
      return response.data
    } catch (error) {
      console.error('Chat health hatası:', error)
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

  // Kullanıcı profili
  async getProfile() {
    try {
      const response = await apiClient.get('/api/v1/user/profile')
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Mevcut kullanıcı bilgilerini getir
  async getCurrentUser() {
    try {
      const response = await apiClient.get('/api/v1/user/current')
      return response.data
    } catch (error) {
      throw error
    }
  },

  // ID'ye göre kullanıcı bilgilerini getir
  async getUserById(userId) {
    try {
      const response = await apiClient.get(`/api/v1/user/by-id/${userId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Kullanıcı bilgilerini güncelle
  async updateProfile(updateData) {
    try {
      const response = await apiClient.put('/api/v1/user/current', updateData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Çıkış yap
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

export default apiClient 