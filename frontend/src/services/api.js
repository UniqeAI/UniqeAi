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

  // Kullanıcı profili
  async getProfile() {
    try {
      const response = await apiClient.get('/api/v1/user/profile')
      return response.data
    } catch (error) {
      throw error
    }
  }
}

export default apiClient 