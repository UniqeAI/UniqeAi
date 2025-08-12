<template>
  <div class="min-h-screen relative overflow-hidden" :class="{ 'dark-mode': darkMode }">
    <!-- Dynamic Background based on Theme -->
    <div class="absolute inset-0" :class="`bg-gradient-to-br ${currentBackground}`"></div>

    <!-- Header with Logo -->
    <header class="relative z-20 py-6 px-8">
      <div class="max-w-7xl mx-auto flex justify-center items-center">
        <!-- Logo -->
        <div class="flex justify-center">
          <div class="transform scale-150">
            <LogoHeader :darkMode="darkMode" />
          </div>
        </div>
      </div>
    </header>

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

    <!-- Hero Section -->
    <section class="text-center py-12 relative z-10">
      <div class="max-w-4xl mx-auto px-4">
        <h2 class="text-xl font-semibold mb-2 font-sans" :class="darkMode ? 'text-blue-200' : 'text-gray-900'">
          Akıllı Telekom Asistanınız
        </h2>
        
        <p class="text-base max-w-2xl mx-auto mb-6 leading-relaxed font-sans" :class="darkMode ? 'text-white/80' : 'text-gray-700/80'">
          Her an, her yerde, sorularınıza anında çözüm. Yapay zeka destekli akıllı asistanınız.
        </p>
      </div>
    </section>
    
    <!-- Features Section -->
    <section class="py-6 px-4 relative z-10">
      <div class="max-w-4xl mx-auto">
                 <div class="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
           <div class="card p-4 transform hover:scale-105 transition-all duration-300 bg-white shadow-lg hover:shadow-xl"
                :style="currentTheme === 'monochrome' 
                  ? 'border: 1px solid #000000;' 
                  : currentTheme === 'burgundy'
                    ? 'border: 1px solid #7f1d1d;'
                    : currentTheme === 'purple'
                      ? 'border: 1px solid #5b21b6;'
                      : currentTheme === 'emerald'
                        ? 'border: 1px solid #065f46;'
                        : 'border: 1px solid #1e3a8a;'">
             <div class="text-center">
               
               <h3 class="text-lg font-bold mb-2" :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-gray-100' : 'text-gray-900')">7/24 Hizmet</h3>
               <p class="text-sm" :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-gray-200' : 'text-gray-700')">Her zaman yanınızdayız. Gece gündüz, sorularınızı yanıtlıyoruz.</p>
             </div>
           </div>
           
           <div class="card p-4 transform hover:scale-105 transition-all duration-300 bg-white shadow-lg hover:shadow-xl"
                :style="currentTheme === 'monochrome' 
                  ? 'border: 1px solid #000000;' 
                  : currentTheme === 'burgundy'
                    ? 'border: 1px solid #7f1d1d;'
                    : currentTheme === 'purple'
                      ? 'border: 1px solid #5b21b6;'
                      : currentTheme === 'emerald'
                        ? 'border: 1px solid #065f46;'
                        : 'border: 1px solid #1e3a8a;'">
             <div class="text-center">
               
               <h3 class="text-lg font-bold mb-2" :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-gray-100' : 'text-gray-900')">Akıllı Asistan</h3>
               <p class="text-sm" :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-gray-200' : 'text-gray-700')">Yapay zeka destekli hızlı çözümler. Anında ve doğru yanıtlar.</p>
             </div>
           </div>
           
           <div class="card p-4 transform hover:scale-105 transition-all duration-300 bg-white shadow-lg hover:shadow-xl"
                :style="currentTheme === 'monochrome' 
                  ? 'border: 1px solid #000000;' 
                  : currentTheme === 'burgundy'
                    ? 'border: 1px solid #7f1d1d;'
                    : currentTheme === 'purple'
                      ? 'border: 1px solid #5b21b6;'
                      : currentTheme === 'emerald'
                        ? 'border: 1px solid #065f46;'
                        : 'border: 1px solid #1e3a8a;'">
             <div class="text-center">
               
               <h3 class="text-lg font-bold mb-2" :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-slate-100' : 'text-slate-900')">Kolay Kullanım</h3>
               <p class="text-sm" :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-slate-200' : 'text-slate-700')">Basit ve kullanıcı dostu arayüz. Tek tıkla başlayın.</p>
             </div>
           </div>
         </div>
      </div>
    </section>

    <!-- Action Buttons Section -->
    <section class="py-8 px-4 relative z-10">
      <div class="max-w-md mx-auto text-center">
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
                     <router-link 
             to="/chat"
             class="inline-flex items-center justify-center px-8 py-4 text-lg font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 border-0 text-white"
             :style="currentTheme === 'monochrome' 
               ? 'background: linear-gradient(135deg, #000000 0%, #000000 50%, #000000 100%); color: #ffffff;' 
               : currentTheme === 'burgundy'
                 ? 'background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 50%, #b91c1c 100%); color: #ffffff;'
                 : currentTheme === 'purple'
                   ? 'background: linear-gradient(135deg, #5b21b6 0%, #6d28d9 50%, #7c3aed 100%); color: #ffffff;'
                   : currentTheme === 'emerald'
                     ? 'background: linear-gradient(135deg, #065f46 0%, #047857 50%, #059669 100%); color: #ffffff;'
                   : 'background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1d4ed8 100%); color: #ffffff;'"
           >
             Hemen Başla
           </router-link>
          
                                                                                       <router-link 
               to="/login"
               class="card px-8 py-4 text-lg font-bold border-2 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
               :class="currentTheme === 'monochrome' ? 'border-black hover:bg-black/20 text-black bg-white' : (darkMode ? 'border-blue-700 hover:bg-blue-800/20 text-white bg-gradient-to-r from-blue-950/20 to-blue-900/20' : 'border-blue-700 hover:bg-blue-600/20 text-blue-900 bg-gradient-to-r from-blue-100 to-blue-200')"
               :style="currentTheme === 'monochrome' 
                 ? 'border-color: #000000;' 
                 : currentTheme === 'burgundy'
                   ? 'border-color: #7f1d1d;'
                   : currentTheme === 'purple'
                     ? 'border-color: #5b21b6;'
                     : currentTheme === 'emerald'
                       ? 'border-color: #065f46;'
                       : 'border-color: #1e3a8a;'"
             >
               Giriş Yap
             </router-link>
        </div>
      </div>
    </section>

    
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import LogoHeader from '../components/LogoHeader.vue'

const darkMode = ref(false) // Default to light mode
const currentTheme = ref('blue') // Default theme
const showThemeMenu = ref(false) // Theme menu visibility

// Available themes with dynamic background colors
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

const updateThemeColors = () => {
  const root = document.documentElement
  const theme = themes.find(t => t.name === currentTheme.value)
  
  if (theme) {
    // Update CSS custom properties based on theme
    if (theme.name === 'blue') {
      root.style.setProperty('--primary-color', '#3b82f6')
      root.style.setProperty('--secondary-color', '#2563eb')
      root.style.setProperty('--accent-color', '#1d4ed8')
      root.style.setProperty('--card-border', 'rgba(59, 130, 246, 0.15)')
      root.style.setProperty('--input-border', 'rgba(59, 130, 246, 0.3)')
      root.style.setProperty('--button-gradient', 'linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%)')
    } else if (theme.name === 'burgundy') {
      root.style.setProperty('--primary-color', '#dc2626')
      root.style.setProperty('--secondary-color', '#b91c1c')
      root.style.setProperty('--accent-color', '#991b1b')
      root.style.setProperty('--card-border', 'rgba(220, 38, 38, 0.15)')
      root.style.setProperty('--input-border', 'rgba(220, 38, 38, 0.3)')
      root.style.setProperty('--button-gradient', 'linear-gradient(135deg, #dc2626 0%, #b91c1c 50%, #991b1b 100%)')
    } else if (theme.name === 'purple') {
      root.style.setProperty('--primary-color', '#8b5cf6')
      root.style.setProperty('--secondary-color', '#7c3aed')
      root.style.setProperty('--accent-color', '#6d28d9')
      root.style.setProperty('--card-border', 'rgba(139, 92, 246, 0.15)')
      root.style.setProperty('--input-border', 'rgba(139, 92, 246, 0.3)')
      root.style.setProperty('--button-gradient', 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 50%, #6d28d9 100%)')
    } else if (theme.name === 'emerald') {
      root.style.setProperty('--primary-color', '#10b981')
      root.style.setProperty('--secondary-color', '#059669')
      root.style.setProperty('--accent-color', '#047857')
      root.style.setProperty('--card-border', 'rgba(16, 185, 129, 0.15)')
      root.style.setProperty('--input-border', 'rgba(16, 185, 129, 0.3)')
      root.style.setProperty('--button-gradient', 'linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%)')
    } else if (theme.name === 'monochrome') {
      root.style.setProperty('--primary-color', '#000000')
      root.style.setProperty('--secondary-color', '#000000')
      root.style.setProperty('--accent-color', '#000000')
      root.style.setProperty('--card-border', 'rgba(0, 0, 0, 0.15)')
      root.style.setProperty('--input-border', 'rgba(0, 0, 0, 0.3)')
      root.style.setProperty('--button-gradient', 'linear-gradient(135deg, #000000 0%, #000000 50%, #000000 100%)')
    }
  }
}



const showThemeNotification = () => {
  // Create a simple notification
  const notification = document.createElement('div')
  notification.className = 'fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all duration-300 font-semibold text-sm'
  
  const themeNames = {
    'blue': 'Marmara',
    'burgundy': 'Anadolu',
    'purple': 'Ubuntu',
    'emerald': 'Gemlik',
    'monochrome': 'Monokrom'
  }
  const displayName = themeNames[currentTheme.value] || currentTheme.value
  notification.textContent = `Tema değiştirildi: ${displayName}`
  notification.style.transform = 'translateY(-100%)'
  notification.style.opacity = '0'
  
  document.body.appendChild(notification)
  
  // Add entrance animation
  setTimeout(() => {
    notification.style.transform = 'translateY(0)'
    notification.style.opacity = '1'
  }, 10)
  
  // Remove notification after 3 seconds
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
    // Set default theme
    document.documentElement.setAttribute('data-theme', 'blue')
    updateThemeColors()
  }
  
})


</script>

<style scoped>
/* Dark mode styles are now handled globally in style.css */
</style>