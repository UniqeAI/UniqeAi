<template>
  <div 
    v-if="isVisible" 
    class="fixed top-16 left-4 z-40 w-80 max-w-[calc(100vw-2rem)] max-h-[calc(100vh-8rem)] transform transition-all duration-300 md:w-80"
  >
    <!-- Panel -->
    <div 
      class="relative w-full rounded-2xl border shadow-2xl transform transition-all duration-300 max-h-full flex flex-col"
      :class="getPanelClasses"
    >
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b" :class="getBorderClasses">
        <h2 class="text-xl font-semibold" :class="getTextClasses">
          👤 Kullanıcı Bilgileri
        </h2>
        <button 
          @click="closePanel"
          class="p-2 rounded-full hover:bg-gray-100/10 transition-colors"
          :class="getTextClasses"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6 space-y-4 overflow-y-auto flex-1 scrollbar-hide">
        <!-- Avatar Section -->
        <div class="flex flex-col items-center space-y-3">
          <div 
            class="w-20 h-20 rounded-full flex items-center justify-center text-2xl"
            :class="getAvatarClasses"
          >
            {{ getInitials }}
          </div>
          <div class="text-center">
            <h3 class="font-medium" :class="getTextClasses">{{ userInfo.name || 'Kullanıcı' }}</h3>
            <p class="text-sm opacity-70" :class="getTextClasses">{{ userInfo.email || 'email@example.com' }}</p>
          </div>
        </div>

        <!-- User Stats -->
        <div class="grid grid-cols-2 gap-4 mt-6">
          <div class="text-center p-3 rounded-lg" :class="getStatClasses">
            <div class="text-lg font-semibold" :class="getTextClasses">{{ userStats.totalMessages }}</div>
            <div class="text-xs opacity-70" :class="getTextClasses">Toplam Mesaj</div>
          </div>
          <div class="text-center p-3 rounded-lg" :class="getStatClasses">
            <div class="text-lg font-semibold" :class="getTextClasses">{{ userStats.sessionsToday }}</div>
            <div class="text-xs opacity-70" :class="getTextClasses">Bugünkü Sohbet</div>
          </div>
        </div>

        <!-- Remaining Usage (Kalan Kullanımlar) -->
        <div class="mt-6">
          <h4 class="text-sm font-medium mb-3" :class="getTextClasses">📊 Kalan Kullanımlar</h4>
          <div class="space-y-3">
            <!-- Internet Quota -->
            <div class="p-3 rounded-lg" :class="getStatClasses">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm flex items-center" :class="getTextClasses">
                  <span class="text-blue-500 mr-2">🌐</span>
                  İnternet
                </span>
                <span class="text-sm font-semibold" :class="getTextClasses">
                  {{ userProfile.remainingQuotas.internet.remaining }} / {{ userProfile.remainingQuotas.internet.total }} {{ userProfile.remainingQuotas.internet.unit }}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2" :class="darkMode ? 'bg-gray-600' : 'bg-gray-200'">
                <div 
                  class="h-2 rounded-full transition-all duration-300"
                  :class="getThemeColor"
                  :style="`width: ${(userProfile.remainingQuotas.internet.remaining / userProfile.remainingQuotas.internet.total) * 100}%`"
                ></div>
              </div>
            </div>
            
            <!-- Voice Quota -->
            <div class="p-3 rounded-lg" :class="getStatClasses">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm flex items-center" :class="getTextClasses">
                  <span class="text-green-500 mr-2">📞</span>
                  Konuşma
                </span>
                <span class="text-sm font-semibold" :class="getTextClasses">
                  {{ userProfile.remainingQuotas.voice.remaining }} / {{ userProfile.remainingQuotas.voice.total }} {{ userProfile.remainingQuotas.voice.unit }}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2" :class="darkMode ? 'bg-gray-600' : 'bg-gray-200'">
                <div 
                  class="bg-green-500 h-2 rounded-full transition-all duration-300"
                  :style="`width: ${(userProfile.remainingQuotas.voice.remaining / userProfile.remainingQuotas.voice.total) * 100}%`"
                ></div>
              </div>
            </div>
            
            <!-- SMS Quota -->
            <div class="p-3 rounded-lg" :class="getStatClasses">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm flex items-center" :class="getTextClasses">
                  <span class="text-purple-500 mr-2">💬</span>
                  SMS
                </span>
                <span class="text-sm font-semibold" :class="getTextClasses">
                  {{ userProfile.remainingQuotas.sms.remaining }} / {{ userProfile.remainingQuotas.sms.total }} {{ userProfile.remainingQuotas.sms.unit }}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2" :class="darkMode ? 'bg-gray-600' : 'bg-gray-200'">
                <div 
                  class="bg-purple-500 h-2 rounded-full transition-all duration-300"
                  :style="`width: ${(userProfile.remainingQuotas.sms.remaining / userProfile.remainingQuotas.sms.total) * 100}%`"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Subscription Period (Taahhüt Süresi) -->
        <div class="mt-6">
          <h4 class="text-sm font-medium mb-3" :class="getTextClasses">📅 Taahhüt Bilgileri</h4>
          <div class="p-4 rounded-lg" :class="getStatClasses">
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Paket:</span>
                <span class="text-sm font-medium" :class="getTextClasses">{{ userProfile.subscription.packageName }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Süre:</span>
                <span class="text-sm font-medium" :class="getTextClasses">{{ userProfile.subscription.contractDuration }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Başlangıç:</span>
                <span class="text-sm font-medium" :class="getTextClasses">{{ formatDate(userProfile.subscription.startDate) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Bitiş:</span>
                <span class="text-sm font-medium" :class="getTextClasses">{{ formatDate(userProfile.subscription.endDate) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Otomatik Yenileme:</span>
                <span 
                  class="text-xs px-2 py-1 rounded-full font-medium"
                  :class="userProfile.subscription.autoRenewal 
                    ? (darkMode ? 'bg-green-800 text-green-200' : 'bg-green-100 text-green-800')
                    : (darkMode ? 'bg-red-800 text-red-200' : 'bg-red-100 text-red-800')"
                >
                  {{ userProfile.subscription.autoRenewal ? 'Açık' : 'Kapalı' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Current Bill Info (Fatura Bilgisi) -->
        <div class="mt-6">
          <h4 class="text-sm font-medium mb-3" :class="getTextClasses">💳 Mevcut Fatura</h4>
          <div class="p-4 rounded-lg" :class="getStatClasses">
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Tutar:</span>
                <span class="text-lg font-bold" :class="getTextClasses">
                  {{ userProfile.billing.currentBill.amount }} {{ userProfile.billing.currentBill.currency }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Fatura Tarihi:</span>
                <span class="text-sm font-medium" :class="getTextClasses">{{ formatDate(userProfile.billing.currentBill.billDate) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Son Ödeme:</span>
                <span class="text-sm font-medium" :class="getTextClasses">{{ formatDate(userProfile.billing.currentBill.dueDate) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Durum:</span>
                <span 
                  class="text-xs px-2 py-1 rounded-full font-medium"
                  :class="userProfile.billing.currentBill.status === 'paid' 
                    ? (darkMode ? 'bg-green-800 text-green-200' : 'bg-green-100 text-green-800')
                    : (darkMode ? 'bg-yellow-800 text-yellow-200' : 'bg-yellow-100 text-yellow-800')"
                >
                  {{ userProfile.billing.currentBill.status === 'paid' ? 'Ödendi' : 'Beklemede' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Last Payment (Son Ödeme Tarihi) -->
        <div class="mt-6">
          <h4 class="text-sm font-medium mb-3" :class="getTextClasses">🕒 Son Ödeme</h4>
          <div class="p-4 rounded-lg" :class="getStatClasses">
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Tutar:</span>
                <span class="text-sm font-bold" :class="getTextClasses">
                  {{ userProfile.billing.lastPayment.amount }} {{ userProfile.billing.lastPayment.currency }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Tarih:</span>
                <span class="text-sm font-medium" :class="getTextClasses">{{ formatDate(userProfile.billing.lastPayment.date) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm" :class="getTextClasses">Yöntem:</span>
                <span class="text-sm font-medium" :class="getTextClasses">{{ userProfile.billing.lastPayment.method }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Theme Selection -->
        <div class="mt-6">
          <h4 class="text-sm font-medium mb-3" :class="getTextClasses">🎨 Aktif Tema</h4>
          <div class="flex items-center justify-between p-3 rounded-lg" :class="getStatClasses">
            <span class="text-sm" :class="getTextClasses">{{ getThemeName }}</span>
            <div 
              class="w-6 h-6 rounded-full border-2 border-white/30"
              :class="getThemeColor"
            ></div>
          </div>
        </div>

        <!-- Settings -->
        <div class="mt-6">
          <h4 class="text-sm font-medium mb-3" :class="getTextClasses">⚙️ Ayarlar</h4>
          <div class="space-y-2">
            <!-- Dark Mode Toggle -->
            <div class="flex items-center justify-between p-3 rounded-lg" :class="getStatClasses">
              <span class="text-sm" :class="getTextClasses">Karanlık Mod</span>
              <button 
                @click="toggleDarkMode"
                class="relative inline-flex items-center h-6 rounded-full w-11 transition-colors"
                :class="darkMode ? getThemeColor : 'bg-gray-300'"
              >
                <span 
                  class="inline-block w-4 h-4 transform bg-white rounded-full transition-transform"
                  :class="darkMode ? 'translate-x-6' : 'translate-x-1'"
                ></span>
              </button>
            </div>

            <!-- Notifications -->
            <div class="flex items-center justify-between p-3 rounded-lg" :class="getStatClasses">
              <span class="text-sm" :class="getTextClasses">Bildirimler</span>
              <button 
                @click="toggleNotifications"
                class="relative inline-flex items-center h-6 rounded-full w-11 transition-colors"
                :class="userSettings.notifications ? getThemeColor : 'bg-gray-300'"
              >
                <span 
                  class="inline-block w-4 h-4 transform bg-white rounded-full transition-transform"
                  :class="userSettings.notifications ? 'translate-x-6' : 'translate-x-1'"
                ></span>
              </button>
            </div>
          </div>
        </div>

      </div>
      
      <!-- Action Buttons - Fixed at bottom -->
      <div class="flex gap-3 p-6 pt-0 border-t flex-shrink-0" :class="getBorderClasses">
        <button 
          @click="editProfile"
          class="flex-1 py-2 px-4 rounded-lg border transition-colors text-sm font-medium"
          :class="getButtonClasses"
        >
          ✏️ Profili Düzenle
        </button>
        <button 
          @click="logout"
          class="flex-1 py-2 px-4 rounded-lg transition-colors text-sm font-medium"
          :class="getLogoutButtonClasses"
        >
          🚪 Çıkış Yap
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserInfoPanel',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    darkMode: {
      type: Boolean,
      default: false
    },
    currentTheme: {
      type: String,
      default: 'blue'
    },
    userInfo: {
      type: Object,
      default: () => ({
        name: 'Kullanıcı',
        email: 'kullanici@example.com',
        avatar: null
      })
    }
  },
  emits: ['close', 'toggle-dark-mode', 'logout', 'edit-profile'],
  data() {
    return {
      userStats: {
        totalMessages: 156,
        sessionsToday: 3
      },
      userSettings: {
        notifications: true
      },
      // Sample user profile data - in real app this would come from API
      userProfile: {
        remainingQuotas: {
          internet: { remaining: 8.5, total: 15, unit: 'GB' },
          voice: { remaining: 450, total: 1000, unit: 'dk' },
          sms: { remaining: 80, total: 100, unit: 'SMS' }
        },
        subscription: {
          startDate: '2024-01-15',
          endDate: '2024-12-15',
          contractDuration: '12 ay',
          packageName: 'Premium Plus',
          autoRenewal: true
        },
        billing: {
          currentBill: {
            amount: 149.90,
            currency: 'TL',
            dueDate: '2024-02-15',
            status: 'pending',
            billDate: '2024-01-15'
          },
          lastPayment: {
            amount: 149.90,
            currency: 'TL',
            date: '2024-01-10',
            method: 'Kredi Kartı'
          }
        }
      }
    }
  },
  computed: {
    getInitials() {
      if (this.userInfo.name) {
        return this.userInfo.name
          .split(' ')
          .map(word => word.charAt(0))
          .join('')
          .toUpperCase()
          .slice(0, 2)
      }
      return 'K'
    },
    
    getPanelClasses() {
      return this.darkMode 
        ? 'bg-gray-800/95 backdrop-blur-xl border-gray-700/50' 
        : 'bg-white/95 backdrop-blur-xl border-gray-200/50'
    },
    
    getBorderClasses() {
      return this.darkMode ? 'border-gray-700/50' : 'border-gray-200/50'
    },
    
    getTextClasses() {
      return this.darkMode ? 'text-white' : 'text-gray-900'
    },
    
    getAvatarClasses() {
      const themeColors = {
        'blue': this.darkMode ? 'bg-blue-600 text-white' : 'bg-blue-500 text-white',
        'burgundy': this.darkMode ? 'bg-red-600 text-white' : 'bg-red-500 text-white',
        'purple': this.darkMode ? 'bg-purple-600 text-white' : 'bg-purple-500 text-white',
        'emerald': this.darkMode ? 'bg-emerald-600 text-white' : 'bg-emerald-500 text-white',
        'monochrome': this.darkMode ? 'bg-gray-600 text-white' : 'bg-gray-700 text-white'
      }
      return themeColors[this.currentTheme] || themeColors.blue
    },
    
    getStatClasses() {
      return this.darkMode 
        ? 'bg-gray-700/50 border border-gray-600/30' 
        : 'bg-gray-50 border border-gray-200/50'
    },
    
    getButtonClasses() {
      return this.darkMode 
        ? 'border-gray-600 text-gray-300 hover:bg-gray-700/50' 
        : 'border-gray-300 text-gray-700 hover:bg-gray-50'
    },
    
    getLogoutButtonClasses() {
      return this.darkMode 
        ? 'bg-red-600/20 text-red-400 hover:bg-red-600/30' 
        : 'bg-red-50 text-red-600 hover:bg-red-100'
    },
    
    getThemeColor() {
      const themeColors = {
        'blue': 'bg-blue-500',
        'burgundy': 'bg-red-500', 
        'purple': 'bg-purple-500',
        'emerald': 'bg-emerald-500',
        'monochrome': 'bg-gray-500'
      }
      return themeColors[this.currentTheme] || 'bg-blue-500'
    },
    
    getThemeName() {
      const themeNames = {
        'blue': 'Mavi',
        'burgundy': 'Bordo',
        'purple': 'Mor', 
        'emerald': 'Yeşil',
        'monochrome': 'Monokrom'
      }
      return themeNames[this.currentTheme] || 'Mavi'
    }
  },
  methods: {
    closePanel() {
      this.$emit('close')
    },
    
    toggleDarkMode() {
      this.$emit('toggle-dark-mode')
    },
    
    toggleNotifications() {
      this.userSettings.notifications = !this.userSettings.notifications
    },
    
    editProfile() {
      this.$emit('edit-profile')
      this.closePanel()
    },
    
    logout() {
      this.$emit('logout')
      this.closePanel()
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('tr-TR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
/* Hide scrollbar for webkit browsers */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for Firefox */
.scrollbar-hide {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

/* Smooth animations */
.transform {
  transition: transform 0.3s ease;
}

/* Panel enter/leave animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Scale animation for panel */
.scale-enter-active, .scale-leave-active {
  transition: transform 0.3s ease;
}
.scale-enter-from, .scale-leave-to {
  transform: scale(0.95);
}
</style>
