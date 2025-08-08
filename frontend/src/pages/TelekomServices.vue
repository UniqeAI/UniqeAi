<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">Telekom Hizmetleri</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/" class="text-blue-600 hover:text-blue-800">
              Ana Sayfa
            </router-link>
            <router-link to="/chat" class="text-blue-600 hover:text-blue-800">
              Chat
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <span class="text-green-600 text-sm">📊</span>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Bağlantı Durumu</h3>
              <p class="text-sm text-gray-500">{{ connectionStatus }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <span class="text-blue-600 text-sm">🤖</span>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">AI Model</h3>
              <p class="text-sm text-gray-500">{{ aiModelInfo.model_type || 'Yükleniyor...' }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <span class="text-purple-600 text-sm">👤</span>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Kullanıcı</h3>
              <p class="text-sm text-gray-500">{{ userProfile?.username || 'Giriş yapılmamış' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Service Categories -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Fatura İşlemleri -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">💰 Fatura İşlemleri</h2>
          </div>
          <div class="p-6 space-y-4">
            <button @click="testCurrentBill" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Mevcut Fatura</h3>
                  <p class="text-sm text-gray-500">Güncel fatura bilgilerini getir</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testBillingHistory" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Fatura Geçmişi</h3>
                  <p class="text-sm text-gray-500">Geçmiş faturaları listele</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testPayBill" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Fatura Öde</h3>
                  <p class="text-sm text-gray-500">Fatura ödeme işlemi</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Paket İşlemleri -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">📦 Paket İşlemleri</h2>
          </div>
          <div class="p-6 space-y-4">
            <button @click="testCurrentPackage" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Mevcut Paket</h3>
                  <p class="text-sm text-gray-500">Aktif paket bilgilerini getir</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testAvailablePackages" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Kullanılabilir Paketler</h3>
                  <p class="text-sm text-gray-500">Mevcut paket seçenekleri</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testQuotas" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Kalan Kotalar</h3>
                  <p class="text-sm text-gray-500">Paket kullanım durumu</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Ağ ve Destek -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">📡 Ağ ve Destek</h2>
          </div>
          <div class="p-6 space-y-4">
            <button @click="testNetworkStatus" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Ağ Durumu</h3>
                  <p class="text-sm text-gray-500">Sinyal ve bağlantı durumu</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testSpeedTest" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Hız Testi</h3>
                  <p class="text-sm text-gray-500">İnternet hızını ölç</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testSupportTicket" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Destek Talebi</h3>
                  <p class="text-sm text-gray-500">Yeni destek talebi oluştur</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Müşteri İşlemleri -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">👤 Müşteri İşlemleri</h2>
          </div>
          <div class="p-6 space-y-4">
            <button @click="testCustomerProfile" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Müşteri Profili</h3>
                  <p class="text-sm text-gray-500">Müşteri bilgilerini getir</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testRoamingServices" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Yurtdışı Hizmetleri</h3>
                  <p class="text-sm text-gray-500">Roaming paketleri</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testLineOperations" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Hat İşlemleri</h3>
                  <p class="text-sm text-gray-500">Hat askıya alma/aktifleştirme</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>

            <button @click="testAllActiveUsers" class="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Tüm Aktif Kullanıcılar</h3>
                  <p class="text-sm text-gray-500">Sistemdeki tüm kullanıcıları listele</p>
                </div>
                <span class="text-blue-600">→</span>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="lastResult" class="mt-8 bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">Son Sonuç</h2>
        </div>
        <div class="p-6">
          <div class="bg-gray-50 rounded-lg p-4">
            <pre class="text-sm text-gray-800 overflow-x-auto">{{ JSON.stringify(lastResult, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { chatAPI, userAPI, telekomAPI, aiAPI } from '../services/api'

export default {
  name: 'TelekomServices',
  setup() {
    const connectionStatus = ref('Kontrol ediliyor...')
    const aiModelInfo = ref({})
    const userProfile = ref(null)
    const lastResult = ref(null)

    // Bağlantı durumunu kontrol et
    const checkConnection = async () => {
      try {
        await chatAPI.getHealth()
        connectionStatus.value = 'Bağlı'
      } catch (error) {
        connectionStatus.value = 'Bağlantı Yok'
      }
    }

    // AI model bilgilerini getir
    const loadAIModelInfo = async () => {
      try {
        aiModelInfo.value = await aiAPI.getModelInfo()
      } catch (error) {
        console.error('AI model bilgisi alınamadı:', error)
      }
    }

    // Kullanıcı profilini getir
    const loadUserProfile = async () => {
      try {
        userProfile.value = await userAPI.getProfile()
      } catch (error) {
        console.error('Kullanıcı profili alınamadı:', error)
      }
    }

    // Test fonksiyonları
    const testCurrentBill = async () => {
      try {
        const result = await telekomAPI.getCurrentBillPost({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testBillingHistory = async () => {
      try {
        const result = await telekomAPI.getBillingHistory({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testPayBill = async () => {
      try {
        const result = await telekomAPI.payBill({ 
          user_id: 'test_user',
          bill_id: 'test_bill',
          amount: 100
        })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testCurrentPackage = async () => {
      try {
        const result = await telekomAPI.getCurrentPackagePost({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testAvailablePackages = async () => {
      try {
        const result = await telekomAPI.getAvailablePackages({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testQuotas = async () => {
      try {
        const result = await telekomAPI.getQuotas({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testNetworkStatus = async () => {
      try {
        const result = await telekomAPI.getNetworkStatus({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testSpeedTest = async () => {
      try {
        const result = await telekomAPI.testInternetSpeed({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testSupportTicket = async () => {
      try {
        const result = await telekomAPI.createSupportTicket({
          user_id: 'test_user',
          subject: 'Test Destek Talebi',
          description: 'Bu bir test destek talebidir.'
        })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testCustomerProfile = async () => {
      try {
        const result = await telekomAPI.getCustomerProfilePost({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testRoamingServices = async () => {
      try {
        const result = await telekomAPI.getRoamingServices({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testLineOperations = async () => {
      try {
        const result = await telekomAPI.suspendLine({ user_id: 'test_user' })
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    const testAllActiveUsers = async () => {
      try {
        const result = await userAPI.getAllActiveUsers()
        lastResult.value = result
      } catch (error) {
        lastResult.value = { error: error.message }
      }
    }

    onMounted(async () => {
      await checkConnection()
      await loadAIModelInfo()
      await loadUserProfile()
    })

    return {
      connectionStatus,
      aiModelInfo,
      userProfile,
      lastResult,
      testCurrentBill,
      testBillingHistory,
      testPayBill,
      testCurrentPackage,
      testAvailablePackages,
      testQuotas,
      testNetworkStatus,
      testSpeedTest,
      testSupportTicket,
      testCustomerProfile,
      testRoamingServices,
      testLineOperations,
      testAllActiveUsers
    }
  }
}
</script> 