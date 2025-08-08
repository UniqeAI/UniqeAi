<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden" :class="{ 'dark-mode': darkMode }">
    <!-- Static Background -->
    <div class="absolute inset-0" :class="darkMode ? 'bg-gradient-to-br from-black via-gray-900 to-blue-950' : 'bg-gradient-to-br from-blue-50 via-gray-50 to-slate-50'"></div>

    <!-- Theme Controls - Fixed Position -->
    <div class="fixed top-4 right-4 z-30 flex items-center gap-3">
      <!-- Theme Color Toggle with Dropdown -->
      <div class="relative theme-menu-container">
                  <button 
            @click="toggleThemeMenu" 
            class="btn p-3 rounded-full backdrop-blur-sm border border-blue-500/30 hover:bg-blue-600/20 transition-all duration-300 shadow-lg"
          >
          <span class="text-white text-lg">{{ currentThemeIcon }}</span>
        </button>
        
        <!-- Theme Dropdown Menu -->
        <div 
          v-if="showThemeMenu" 
          class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 backdrop-blur-sm"
          :class="darkMode ? 'bg-gray-800/95 border-gray-700' : 'bg-white/95 border-gray-200'"
        >
          <div class="py-3">
            <div class="px-4 py-2 border-b border-gray-200" :class="darkMode ? 'border-gray-700' : 'border-gray-200'">
              <h3 class="text-sm font-semibold" :class="darkMode ? 'text-gray-300' : 'text-gray-600'">
                Tema Seçin
              </h3>
            </div>
            <div 
              v-for="theme in themes" 
              :key="theme.name"
              @click="selectTheme(theme.name)"
              class="flex items-center px-4 py-3 cursor-pointer transition-all duration-200 hover:bg-gray-50"
              :class="darkMode ? 'hover:bg-gray-700/50' : 'hover:bg-gray-50'"
            >
              <div 
                class="w-6 h-6 rounded-full mr-3 border-2 border-gray-200"
                :class="currentTheme === theme.name ? 'ring-2 ring-blue-500' : ''"
                :style="`background: linear-gradient(135deg, ${theme.colors.primary} 0%, ${theme.colors.secondary} 50%, ${theme.colors.accent} 100%);`"
              ></div>
              <span 
                class="font-medium flex-1"
                :class="darkMode ? 'text-white' : 'text-gray-900'"
              >
                {{ getThemeDisplayName(theme.name) }}
              </span>
              <span 
                v-if="currentTheme === theme.name"
                class="text-blue-500 font-bold"
              >
                ✓
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Dark Mode Toggle -->
      <button 
        v-if="currentTheme !== 'monochrome'"
        @click="toggleDarkMode" 
        class="btn p-3 rounded-full backdrop-blur-sm border border-blue-500/30 hover:bg-blue-600/20 transition-all duration-300 shadow-lg"
      >
        <span class="text-white text-lg">{{ darkMode ? '☀️' : '🌙' }}</span>
      </button>
    </div>

    <!-- Login Container -->
    <div class="relative z-10 w-full max-w-md mx-auto p-8">
      <!-- Logo Section -->
      <div class="text-center mb-8">
        <div class="mb-6">
          <LogoHeader :darkMode="darkMode" />
        </div>
        <h2 class="text-2xl font-bold mb-2" :class="darkMode ? 'text-white' : 'text-gray-900'">
          Hoş Geldiniz
        </h2>
        <p class="text-sm" :class="darkMode ? 'text-white/70' : 'text-gray-700/70'">
          Hesabınıza giriş yapın
        </p>
        
        <!-- Demo Kullanıcı Bilgileri -->
        <div class="mt-4 p-4 bg-blue-50 rounded-lg" :class="darkMode ? 'bg-blue-900/20' : 'bg-blue-50'">
          <h3 class="text-sm font-semibold mb-2" :class="darkMode ? 'text-blue-300' : 'text-blue-700'">
            Demo Kullanıcılar:
          </h3>
          <div class="space-y-1 text-xs" :class="darkMode ? 'text-blue-200' : 'text-blue-600'">
            <div><strong>Enes:</strong> enes.faruk.aydin@email.com / enes123</div>
            <div><strong>Nisa:</strong> nisa.nur.ozkal@email.com / nisa123</div>
            <div><strong>Sedat:</strong> sedat.kilicoglu@email.com / sedat123</div>
            <div><strong>Erkan:</strong> erkan.tanriover@email.com / erkan123</div>
            <div><strong>Ahmet:</strong> ahmet.nazif.gemalmaz@email.com / ahmet123</div>
            <div><strong>Ziişan:</strong> ziisan.sahin@email.com / ziisan123</div>
          </div>
        </div>
      </div>

      <!-- Login Form -->
      <div class="card p-6 shadow-2xl">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Email Field -->
          <div>
            <label for="email" class="block text-sm font-medium mb-2" :class="darkMode ? 'text-white' : 'text-gray-900'">
              E-posta
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              placeholder="ornek@email.com"
              class="input w-full p-3 text-base"
              :class="darkMode ? 'text-white placeholder-white/50 bg-gray-900/50 border-gray-700' : 'text-gray-900 placeholder-gray-700/50'"
            />
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium mb-2" :class="darkMode ? 'text-white' : 'text-gray-900'">
              Şifre
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="input w-full p-3 text-base"
              :class="darkMode ? 'text-white placeholder-white/50 bg-gray-900/50 border-gray-700' : 'text-gray-900 placeholder-gray-700/50'"
            />
          </div>

          <!-- Remember Me & Forgot Password -->
          <div class="flex items-center justify-between">
            <label class="flex items-center">
              <input
                type="checkbox"
                v-model="rememberMe"
                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
                :class="darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'"
              />
              <span class="ml-2 text-sm" :class="darkMode ? 'text-white' : 'text-gray-900'">
                Beni hatırla
              </span>
            </label>
            <a href="#" class="text-sm font-medium transition-colors duration-300" :class="darkMode ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-500'">
              Şifremi unuttum
            </a>
          </div>

          <!-- Login Button -->
          <button
            type="submit"
            class="btn w-full p-4 text-lg font-semibold shadow-xl hover:shadow-2xl transform hover:scale-105"
          >
            Giriş Yap
          </button>
        </form>



        <!-- Register Link -->
        <div class="mt-6 text-center">
          <p class="text-sm" :class="darkMode ? 'text-white/70' : 'text-gray-700/70'">
            Hesabınız yok mu?
            <router-link 
              to="/register" 
              class="font-medium transition-colors duration-300"
              :class="darkMode ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-500'"
            >
              Kayıt olun
            </router-link>
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import LogoHeader from '../components/LogoHeader.vue'
import { userAPI } from '../services/api'

const router = useRouter()
const darkMode = ref(false)
const currentTheme = ref('blue')
const showThemeMenu = ref(false)
const email = ref('')
const password = ref('')
const rememberMe = ref(false)

// Available themes
const themes = [
  { 
    name: 'blue', 
    icon: '🔵', 
    colors: { 
      primary: '#1e3a8a', 
      secondary: '#1e40af', 
      accent: '#1d4ed8' 
    } 
  },
  { 
    name: 'burgundy', 
    icon: '🔴', 
    colors: { 
      primary: '#7f1d1d', 
      secondary: '#991b1b', 
      accent: '#b91c1c' 
    } 
  },
  { 
    name: 'purple', 
    icon: '🟣', 
    colors: { 
      primary: '#5b21b6', 
      secondary: '#6d28d9', 
      accent: '#7c3aed' 
    } 
  },
  { 
    name: 'emerald', 
    icon: '🟢', 
    colors: { 
      primary: '#065f46', 
      secondary: '#047857', 
      accent: '#059669' 
    } 
  },
  { 
    name: 'monochrome', 
    icon: '⚫', 
    colors: { 
      primary: '#000000', 
      secondary: '#000000', 
      accent: '#000000' 
    } 
  }
]

const currentThemeIcon = computed(() => {
  const theme = themes.find(t => t.name === currentTheme.value)
  return theme ? theme.icon : '🔵'
})

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('darkMode', 'true')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('darkMode', 'false')
  }
}

const toggleThemeMenu = () => {
  showThemeMenu.value = !showThemeMenu.value
}

const selectTheme = (themeName) => {
  currentTheme.value = themeName
  showThemeMenu.value = false
  localStorage.setItem('themeColor', currentTheme.value)
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  updateThemeColors()
  showThemeNotification()
}

const getThemeDisplayName = (name) => {
  const themeNames = {
    'blue': 'Marmara',
    'burgundy': 'Anadolu',
    'purple': 'Ubuntu',
    'emerald': 'Gemlik',
    'monochrome': 'Monokrom'
  }
  return themeNames[name] || name
}

const handleClickOutside = (event) => {
  if (showThemeMenu.value && !event.target.closest('.theme-menu-container')) {
    showThemeMenu.value = false
  }
}

const updateThemeColors = () => {
  const root = document.documentElement
  const theme = themes.find(t => t.name === currentTheme.value)
  
  if (theme) {
    if (theme.name === 'blue') {
      root.style.setProperty('--primary-color', '#3b82f6')
      root.style.setProperty('--secondary-color', '#1d4ed8')
      root.style.setProperty('--accent-color', '#1e40af')
    } else if (theme.name === 'burgundy') {
      root.style.setProperty('--primary-color', '#dc2626')
      root.style.setProperty('--secondary-color', '#b91c1c')
      root.style.setProperty('--accent-color', '#991b1b')
    } else if (theme.name === 'purple') {
      root.style.setProperty('--primary-color', '#8b5cf6')
      root.style.setProperty('--secondary-color', '#7c3aed')
      root.style.setProperty('--accent-color', '#6d28d9')
    } else if (theme.name === 'emerald') {
      root.style.setProperty('--primary-color', '#10b981')
      root.style.setProperty('--secondary-color', '#059669')
      root.style.setProperty('--accent-color', '#047857')
    } else if (theme.name === 'monochrome') {
      root.style.setProperty('--primary-color', '#000000')
      root.style.setProperty('--secondary-color', '#000000')
      root.style.setProperty('--accent-color', '#000000')
    }
  }
}

const showThemeNotification = () => {
  const notification = document.createElement('div')
  notification.className = 'fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all duration-300 font-semibold text-sm'
  notification.textContent = `Tema değiştirildi: ${getThemeDisplayName(currentTheme.value)}`
  notification.style.transform = 'translateY(-100%)'
  notification.style.opacity = '0'
  
  document.body.appendChild(notification)
  
  setTimeout(() => {
    notification.style.transform = 'translateY(0)'
    notification.style.opacity = '1'
  }, 10)
  
  setTimeout(() => {
    notification.style.transform = 'translateY(-100%)'
    notification.style.opacity = '0'
    setTimeout(() => {
      notification.remove()
    }, 300)
  }, 3000)
}

const handleLogin = async () => {
  try {
    console.log('Login attempt:', { email: email.value, password: password.value, rememberMe: rememberMe.value })
    
    // Eski session token'ı temizle
    localStorage.removeItem('session_token')
    
    // API ile giriş yap
    const response = await userAPI.login({
      email: email.value,
      password: password.value
    })
    
    console.log('Login successful:', response)
    
    // Session token'ı kaydet
    if (response.data && response.data.session_token) {
      localStorage.setItem('session_token', response.data.session_token)
    }
    
    // Başarılı giriş sonrası chat sayfasına yönlendir
    router.push('/chat')
    
  } catch (error) {
    console.error('Login error:', error)
    alert('Giriş başarısız: ' + (error.message || 'Bilinmeyen hata'))
  }
}

onMounted(() => {
  // Eski session token'ı temizle
  localStorage.removeItem('session_token')
  
  // Check for saved dark mode preference
  const savedDarkMode = localStorage.getItem('darkMode')
  if (savedDarkMode === 'true') {
    darkMode.value = true
    document.documentElement.classList.add('dark')
  } else {
    darkMode.value = false
    document.documentElement.classList.remove('dark')
  }
  
  // Check for saved theme preference
  const savedTheme = localStorage.getItem('themeColor')
  if (savedTheme && themes.find(t => t.name === savedTheme)) {
    currentTheme.value = savedTheme
    document.documentElement.setAttribute('data-theme', currentTheme.value)
    updateThemeColors()
  } else {
    document.documentElement.setAttribute('data-theme', 'blue')
    updateThemeColors()
  }
  
  // Add click outside listener for theme menu
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  // Remove click outside listener
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Dark mode styles are now handled globally in style.css */
</style> 