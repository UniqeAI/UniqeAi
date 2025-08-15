<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden" :class="{ 'dark-mode': darkMode }">
    <!-- Dynamic Background based on Theme -->
    <div class="absolute inset-0" :class="`bg-gradient-to-br ${currentBackground}`"></div>

    <!-- Back to Home Button - Fixed Position Left Top -->
    <div class="fixed top-4 left-4 z-30">
      <router-link 
        to="/" 
        class="btn p-3 rounded-full backdrop-blur-sm border border-blue-500/30 hover:bg-blue-600/20 transition-all duration-300 shadow-lg"
        :class="darkMode ? 'text-white' : 'text-gray-900'"
      >
        <span class="text-lg">🏠</span>
        <span class="ml-2 text-sm font-medium">Ana Sayfa</span>
      </router-link>
    </div>

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
              class="input w-full p-3 text-base transition-all duration-300"
              :class="getInputClasses"
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

const router = useRouter()
const darkMode = ref(false)
const currentTheme = ref('blue')
const showThemeMenu = ref(false)
const email = ref('')
const password = ref('')
const rememberMe = ref(false)

// Available themes with dynamic dark mode background colors
const themes = [
  { 
    name: 'blue', 
    icon: '🔵', 
    colors: { 
      primary: '#1e3a8a', 
      secondary: '#1e40af', 
      accent: '#1d4ed8' 
    },
    darkBackground: 'from-black via-blue-950 via-blue-900 to-blue-800',
    lightBackground: 'from-blue-50 via-blue-100 to-blue-200'
  },
  { 
    name: 'burgundy', 
    icon: '🔴', 
    colors: { 
      primary: '#7f1d1d', 
      secondary: '#991b1b', 
      accent: '#b91c1c' 
    },
    darkBackground: 'from-black via-red-950 via-red-900 to-red-800',
    lightBackground: 'from-red-50 via-red-100 to-red-200'
  },
  { 
    name: 'purple', 
    icon: '🟣', 
    colors: { 
      primary: '#5b21b6', 
      secondary: '#6d28d9', 
      accent: '#7c3aed' 
    },
    darkBackground: 'from-black via-purple-950 via-purple-900 to-purple-800',
    lightBackground: 'from-purple-50 via-purple-100 to-purple-200'
  },
  { 
    name: 'emerald', 
    icon: '🟢', 
    colors: { 
      primary: '#065f46', 
      secondary: '#047857', 
      accent: '#059669' 
    },
    darkBackground: 'from-black via-emerald-950 via-emerald-900 to-emerald-800',
    lightBackground: 'from-emerald-50 via-emerald-100 to-emerald-200'
  },
  { 
    name: 'monochrome', 
    icon: '⚫', 
    colors: { 
      primary: '#000000', 
      secondary: '#000000', 
      accent: '#000000' 
    },
    darkBackground: 'from-black via-gray-900 via-gray-800 to-gray-700',
    lightBackground: 'from-gray-50 via-gray-100 to-gray-200'
  }
]

const currentThemeIcon = computed(() => {
  const theme = themes.find(t => t.name === currentTheme.value)
  return theme ? theme.icon : '🔵'
})

const currentBackground = computed(() => {
  const theme = themes.find(t => t.name === currentTheme.value)
  if (!theme) return darkMode.value ? 'from-black via-gray-900 to-blue-950' : 'from-blue-50 via-gray-50 to-slate-50'
  
  return darkMode.value ? theme.darkBackground : theme.lightBackground
})

const getInputClasses = computed(() => {
  const theme = themes.find(t => t.name === currentTheme.value)
  
  if (currentTheme.value === 'monochrome') {
    return darkMode.value 
      ? 'bg-gray-800 text-white placeholder-white/60 border-gray-600 focus:border-gray-500' 
      : 'bg-white text-black placeholder-gray-500 border-gray-300 focus:border-gray-400'
  }
  
  if (!theme) return darkMode.value 
    ? 'bg-gray-800 text-white placeholder-white/60 border-gray-600' 
    : 'bg-white text-gray-900 placeholder-gray-500 border-gray-300'
  
  // Tema rengine göre input stilleri
  const themeInputs = {
    'blue': darkMode.value 
      ? 'bg-blue-900/50 text-white placeholder-blue-200/60 border-blue-700 focus:border-blue-500' 
      : 'bg-white text-blue-900 placeholder-blue-600/60 border-blue-300 focus:border-blue-500',
    'burgundy': darkMode.value 
      ? 'bg-red-900/50 text-white placeholder-red-200/60 border-red-700 focus:border-red-500' 
      : 'bg-white text-red-900 placeholder-red-600/60 border-red-300 focus:border-red-500',
    'purple': darkMode.value 
      ? 'bg-purple-900/50 text-white placeholder-purple-200/60 border-purple-700 focus:border-purple-500' 
      : 'bg-white text-purple-900 placeholder-purple-600/60 border-purple-300 focus:border-purple-500',
    'emerald': darkMode.value 
      ? 'bg-emerald-900/50 text-white placeholder-emerald-200/60 border-emerald-700 focus:border-emerald-500' 
      : 'bg-white text-emerald-900 placeholder-emerald-600/60 border-emerald-300 focus:border-emerald-500'
  }
  
  return themeInputs[currentTheme.value] || (darkMode.value 
    ? 'bg-gray-800 text-white placeholder-white/60 border-gray-600' 
    : 'bg-white text-gray-900 placeholder-gray-500 border-gray-300')
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

import { userAPI, telekomAPI } from '../services/api.js'

const handleLogin = async () => {
  try {
    let loginResult = null
    
    // Try User API first
    try {
      const userCredentials = {
        email: email.value,
        password: password.value
      }
      loginResult = await userAPI.login(userCredentials)
      
      if (loginResult?.success && loginResult.data) {
        // Store session data from User API
        if (loginResult.data.session_token) {
          localStorage.setItem('session_token', loginResult.data.session_token)
          localStorage.setItem('user_id', String(loginResult.data.user_id || ''))
          localStorage.setItem('user_name', loginResult.data.name || '')
        }
        
        showNotification('Giriş başarılı!', 'success')
      } else {
        throw new Error('User API login failed')
      }
    } catch (userError) {
      // If User API fails, try Telekom API
      try {
        const telekomResult = await telekomAPI.login(email.value, password.value)
        if (telekomResult?.success && telekomResult.session_token) {
          // Store session data from Telekom API
          localStorage.setItem('session_token', telekomResult.session_token)
          localStorage.setItem('user_id', String(telekomResult.user_id || ''))
          localStorage.setItem('user_name', telekomResult.user_name || '')
          
          loginResult = telekomResult
          showNotification('Giriş başarılı!', 'success')
        } else {
          throw new Error(telekomResult?.message || 'Telekom API login failed')
        }
      } catch (telekomError) {
        throw new Error('Her iki giriş sistemi de başarısız oldu: ' + telekomError.message)
      }
    }
    
    // Optional remember me
    if (rememberMe.value) {
      localStorage.setItem('remember_email', email.value)
    } else {
      localStorage.removeItem('remember_email')
    }

    // Navigate to chat
    setTimeout(() => {
      router.push('/chat')
    }, 1000)
    
  } catch (err) {
    console.error('Login failed:', err)
    showNotification('Giriş başarısız: ' + (err.message || 'Bilinmeyen hata'), 'error')
  }
}

const showNotification = (message, type = 'info') => {
  const notification = document.createElement('div')
  const bgColor = type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-blue-600'
  notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all duration-300 font-semibold text-sm`
  notification.textContent = message
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

onMounted(() => {
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