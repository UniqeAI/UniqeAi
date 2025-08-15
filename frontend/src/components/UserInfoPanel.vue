<template>
  <div v-if="isVisible" class="user-info-panel fixed top-16 left-4 z-40">
    <div class="panel-header">
      <h3 class="panel-title">Kullanıcı Bilgileri</h3>
      <button @click="togglePanel" class="toggle-btn">
        <svg v-if="isExpanded" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </div>
    
    <div v-if="isExpanded" class="panel-content">
      <div class="user-avatar">
        <div class="avatar-circle">
          {{ userInitials }}
        </div>
      </div>
      
      <div class="user-details">
        <div class="detail-item">
          <span class="label">İsim:</span>
          <span class="value">{{ userInfo.name || 'Bilinmiyor' }}</span>
        </div>
        
        <div class="detail-item">
          <span class="label">E-posta:</span>
          <span class="value">{{ userInfo.email || 'Bilinmiyor' }}</span>
        </div>
        
        <div class="detail-item">
          <span class="label">Telefon:</span>
          <span class="value">{{ userInfo.phone || 'Bilinmiyor' }}</span>
        </div>
        
        <div v-if="sessionInfo.session_token" class="detail-item">
          <span class="label">Oturum:</span>
          <span class="value text-green-600">Aktif</span>
        </div>
        
        <div v-if="packageInfo" class="detail-item">
          <span class="label">Paket:</span>
          <span class="value">{{ packageInfo.name || 'Bilinmiyor' }}</span>
        </div>
      </div>
      
      <div class="action-buttons">
        <button @click="refreshUserInfo" class="action-btn primary">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Yenile
        </button>
        
        <button @click="logout" class="action-btn secondary">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Çıkış
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userAPI, telekomAPI } from '../services/api.js'

// Props tanımlama
const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()

const isExpanded = ref(true)
const userInfo = ref({
  name: '',
  email: '',
  phone: ''
})
const sessionInfo = ref({})
const packageInfo = ref(null)

const userInitials = computed(() => {
  if (userInfo.value.name) {
    const names = userInfo.value.name.split(' ')
    return names.map(name => name.charAt(0).toUpperCase()).join('').slice(0, 2)
  }
  return '??'
})

onMounted(() => {
  loadUserInfo()
})

const loadUserInfo = () => {
  // Local storage'dan bilgileri yükle
  const storedUserName = localStorage.getItem('user_name')
  const storedUserId = localStorage.getItem('user_id')
  const storedSessionToken = localStorage.getItem('session_token')
  
  if (storedUserName) {
    userInfo.value.name = storedUserName
  }
  
  if (storedSessionToken) {
    sessionInfo.value.session_token = storedSessionToken
  }
  
  // API'den güncel bilgileri al
  if (storedSessionToken) {
    fetchUserProfile(storedSessionToken)
  }
}

const fetchUserProfile = async (sessionToken) => {
  try {
    // Telekom müşteri profilini al
    const profile = await telekomAPI.getCustomerProfile(sessionToken)
    if (profile && profile.success) {
      userInfo.value = {
        name: profile.data?.name || userInfo.value.name,
        email: profile.data?.email || userInfo.value.email,
        phone: profile.data?.phone || userInfo.value.phone
      }
    }
    
    // Paket bilgilerini al
    const packageData = await telekomAPI.getCurrentPackage(sessionToken)
    if (packageData && packageData.success) {
      packageInfo.value = packageData.data
    }
  } catch (error) {
    console.error('Kullanıcı profili yüklenirken hata:', error)
  }
}

const togglePanel = () => {
  isExpanded.value = !isExpanded.value
}

const refreshUserInfo = () => {
  const sessionToken = localStorage.getItem('session_token')
  if (sessionToken) {
    fetchUserProfile(sessionToken)
  } else {
    loadUserInfo()
  }
}

const logout = () => {
  if (confirm('Çıkış yapmak istediğinizden emin misiniz?')) {
    // Local storage'ı temizle
    localStorage.removeItem('session_token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('user_name')
    
    // Login sayfasına yönlendir
    router.push('/login')
  }
}
</script>

<style scoped>
.user-info-panel {
  @apply bg-white border border-gray-200 rounded-lg shadow-sm;
  max-width: 320px;
}

.panel-header {
  @apply flex items-center justify-between p-4 border-b border-gray-200;
}

.panel-title {
  @apply text-lg font-semibold text-gray-800;
}

.toggle-btn {
  @apply p-1 rounded-full hover:bg-gray-100 transition-colors;
  border: none;
  cursor: pointer;
}

.panel-content {
  @apply p-4 space-y-4;
}

.user-avatar {
  @apply flex justify-center;
}

.avatar-circle {
  @apply w-16 h-16 bg-blue-500 text-white rounded-full flex items-center justify-center text-xl font-bold;
}

.user-details {
  @apply space-y-3;
}

.detail-item {
  @apply flex justify-between items-center;
}

.label {
  @apply text-sm font-medium text-gray-600;
}

.value {
  @apply text-sm text-gray-900 font-medium;
}

.action-buttons {
  @apply flex gap-2 pt-4 border-t border-gray-200;
}

.action-btn {
  @apply flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium transition-colors;
  border: none;
  cursor: pointer;
  flex: 1;
}

.action-btn.primary {
  @apply bg-blue-500 text-white hover:bg-blue-600;
}

.action-btn.secondary {
  @apply bg-gray-100 text-gray-700 hover:bg-gray-200;
}
</style>
