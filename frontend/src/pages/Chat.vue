<template>
  <div class="flex flex-col h-screen" :class="{ 'dark-mode': darkMode }">
    <!-- Single unified background for entire chat -->
    <div class="fixed inset-0" :class="`bg-gradient-to-br ${currentBackground}`"></div>
    
    <!-- Chat Container with transparent background -->
    <div class="relative flex flex-col h-full max-w-3xl mx-auto w-full z-10">
      <!-- Chat Header -->
      <div class="p-4 bg-transparent flex items-center justify-between relative z-10">
        <div class="flex items-center">
          <router-link 
            to="/" 
            class="mr-4 p-2 transition-colors duration-300"
            :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-blue-400 hover:text-blue-300' : 'text-blue-800 hover:text-blue-600')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </router-link>
          
          <div class="flex items-center">
            <div class="mr-3">
              <LogoHeader :darkMode="darkMode" :currentTheme="currentTheme" />
            </div>
          </div>
        </div>
        
        <!-- Status -->
        <div class="flex items-center gap-4">
          <div class="text-sm font-sans flex items-center gap-2" :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-white/70' : 'text-blue-700/70')">
            <div class="w-2 h-2 rounded-full" :class="isConnected ? 'bg-green-500' : 'bg-red-500'"></div>
            {{ isConnected ? 'Bağlı' : 'Bağlantı Yok' }}
          </div>
          

        </div>
      </div>

      <!-- User Info - Fixed Position Top Left -->
      <div class="fixed top-4 left-4 z-30 flex items-center gap-3">
        <!-- User Profile Button -->
        <button 
          @click="toggleUserPanel"
          class="btn p-3 rounded-full backdrop-blur-sm border transition-all duration-300 shadow-lg"
          :class="currentTheme === 'monochrome' ? 'border-black/30 hover:bg-black/20 text-white' : 'border-blue-500/30 hover:bg-blue-600/20 text-blue-400'"
          title="Kullanıcı Profili"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </button>
      </div>

      <!-- Theme Controls - Fixed Position Top Right -->
      <div class="fixed top-4 right-4 z-30 flex items-center gap-3">
        <!-- Theme Color Toggle with Dropdown -->
        <div class="relative theme-menu-container">
          <button 
            @click="toggleThemeMenu" 
            class="btn p-3 rounded-full backdrop-blur-sm border transition-all duration-300 shadow-lg"
            :class="currentTheme === 'monochrome' ? 'border-black/30 hover:bg-black/20' : 'border-blue-500/30 hover:bg-blue-600/20'"
          >
            <span class="text-white text-lg w-5 h-5 flex items-center justify-center">{{ currentThemeIcon }}</span>
          </button>
          
          <!-- Theme Dropdown Menu -->
          <div 
            v-if="showThemeMenu" 
            class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 backdrop-blur-sm"
          >
            <div class="py-3">
              <div class="px-4 py-2 border-b border-gray-200">
                <h3 class="text-sm font-bold" :class="darkMode ? 'text-black' : 'text-gray-900'">
                  Tema Seçin
                </h3>
              </div>
              <div 
                v-for="theme in themes" 
                :key="theme.name"
                @click="selectTheme(theme.name)"
                class="flex items-center px-4 py-3 cursor-pointer transition-all duration-200 hover:bg-gray-100"
              >
                <div 
                  class="w-6 h-6 rounded-full mr-3 border-2 border-gray-300"
                  :class="currentTheme === theme.name ? 'ring-2 ring-blue-500' : ''"
                  :style="`background: linear-gradient(135deg, ${theme.colors.primary} 0%, ${theme.colors.secondary} 50%, ${theme.colors.accent} 100%);`"
                ></div>
                <span 
                  class="font-semibold flex-1 text-black"
                >
                  {{ getThemeDisplayName(theme.name) }}
                </span>
                <span 
                  v-if="currentTheme === theme.name"
                  class="font-bold"
                  :class="darkMode ? 'text-black' : 'text-gray-900'"
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
          class="btn p-3 rounded-full backdrop-blur-sm border transition-all duration-300 shadow-lg"
          :class="currentTheme === 'monochrome' ? 'border-black/30 hover:bg-black/20' : 'border-blue-500/30 hover:bg-blue-600/20'"
        >
        <svg v-if="darkMode" class="w-5 h-5 flex items-center justify-center" :class="currentTheme === 'monochrome' ? 'text-white' : 'text-yellow-400'" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
        </svg>
        <svg v-else class="w-5 h-5 flex items-center justify-center" :class="currentTheme === 'monochrome' ? 'text-white' : 'text-yellow-400'" fill="currentColor" viewBox="0 0 20 20">
          <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
        </svg>
      </button>
      </div>
      
      <!-- Messages Area - Flexible, Scrollable -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4 bg-transparent scroll-smooth scrollbar-hide flex flex-col">
        <div 
          v-for="message in messages" 
          :key="message.id"
          :class="[
            'flex',
            message.sender === 'user' ? 'justify-end' : 'justify-start'
          ]"
        >
          <div 
            :class="[
              'max-w-xs md:max-w-md lg:max-w-lg rounded-2xl p-4 relative font-sans transform transition-all duration-300',
              message.sender === 'user' 
                ? 'text-white rounded-br-md shadow-lg' 
                : 'rounded-bl-md shadow-lg'
            ]"
            :style="message.sender === 'user' 
              ? (currentTheme === 'monochrome' ? 'background: #000000; color: #ffffff;' : `background: ${getUserMessageGradient()}`)
              : currentTheme === 'monochrome'
                ? 'background: #ffffff; color: #000000;'
                : darkMode 
                  ? 'background: rgba(31, 41, 55, 0.9); color: #f9fafb;' 
                  : 'background: #f3f4f6; color: #111827;'"
          >
            <div class="whitespace-pre-wrap mb-3 text-sm leading-relaxed">
              {{ message.text }}
            </div>
            
            <!-- Araç sonuçları -->
            <div v-if="message.toolResults && message.toolResults.length > 0" class="mt-4">
              <div v-for="(tool, toolIndex) in message.toolResults" :key="toolIndex" class="mb-4">
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <div class="flex items-center mb-2">
                    <span class="bg-blue-500 text-white px-2 py-1 rounded text-xs font-medium">
                      {{ getToolDisplayName(tool.arac_adi) }}
                    </span>
                    <span class="ml-2 text-xs text-gray-600">
                      {{ getToolStatus(tool.durum) }}
                    </span>
                  </div>
                  
                  <!-- Fatura sonuçları -->
                  <div v-if="tool.arac_adi === 'get_past_bills' && tool.sonuc && tool.sonuc.success" class="space-y-2">
                    <div class="text-sm font-medium text-gray-800 mb-2">
                      📋 Geçmiş Faturalarınız ({{ tool.sonuc.data.bills.length }} adet)
                    </div>
                    <div class="max-h-60 overflow-y-auto space-y-2">
                      <div v-for="(bill, billIndex) in tool.sonuc.data.bills.slice(0, 5)" :key="billIndex" 
                           class="bg-white border border-gray-200 rounded p-3">
                        <div class="flex justify-between items-start mb-2">
                          <div class="text-sm font-medium text-gray-800">
                            Fatura #{{ bill.bill_id }}
                          </div>
                          <span :class="[
                            'px-2 py-1 rounded text-xs font-medium',
                            bill.status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          ]">
                            {{ bill.status === 'paid' ? 'Ödendi' : 'Ödenmedi' }}
                          </span>
                        </div>
                        <div class="text-sm text-gray-600">
                          <div>Tarih: {{ formatDate(bill.bill_date) }}</div>
                          <div>Vade: {{ formatDate(bill.due_date) }}</div>
                          <div class="font-medium text-gray-800 mt-1">
                            Tutar: {{ bill.amount }} {{ bill.currency }}
                          </div>
                        </div>
                        <div v-if="bill.services && bill.services.length > 0" class="mt-2 text-xs text-gray-500">
                          <div v-for="service in bill.services" :key="service.service_name">
                            • {{ service.service_name }}: {{ service.amount }} {{ bill.currency }}
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-if="tool.sonuc.data.bills.length > 5" class="text-xs text-gray-500 text-center mt-2">
                      ... ve {{ tool.sonuc.data.bills.length - 5 }} fatura daha
                    </div>
                  </div>
                  
                  <!-- Mevcut paket sonuçları -->
                  <div v-if="tool.arac_adi === 'get_current_package' && tool.sonuc && tool.sonuc.success" class="space-y-2">
                    <div class="text-sm font-medium text-gray-800 mb-2">
                      📄 Mevcut Paketiniz
                    </div>
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                      <div class="flex justify-between items-start mb-4">
                        <div class="text-xl font-bold text-gray-800">
                          {{ tool.sonuc.data.package_name }}
                        </div>
                        <div class="text-3xl font-bold text-blue-600">
                          {{ tool.sonuc.data.monthly_fee }}₺
                        </div>
                      </div>
                      <div class="text-sm text-gray-600 mb-4">
                        {{ tool.sonuc.data.description }}
                      </div>
                      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="space-y-2">
                          <div class="flex items-center text-sm">
                            <span class="text-blue-500 mr-2">🌐</span>
                            <span class="text-gray-700">{{ tool.sonuc.data.features.internet_gb }} GB İnternet</span>
                          </div>
                          <div class="flex items-center text-sm">
                            <span class="text-green-500 mr-2">📞</span>
                            <span class="text-gray-700">{{ tool.sonuc.data.features.voice_minutes }} Dakika</span>
                          </div>
                          <div class="flex items-center text-sm">
                            <span class="text-purple-500 mr-2">💬</span>
                            <span class="text-gray-700">{{ tool.sonuc.data.features.sms_count }} SMS</span>
                          </div>
                          <div v-if="tool.sonuc.data.features.roaming_enabled" class="flex items-center text-sm">
                            <span class="text-orange-500 mr-2">🌍</span>
                            <span class="text-gray-700">Yurtdışı Dahil</span>
                          </div>
                        </div>
                        <div class="space-y-2">
                          <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-600">Paket Durumu:</span>
                            <span :class="[
                              'px-2 py-1 rounded text-xs font-medium',
                              tool.sonuc.data.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            ]">
                              {{ tool.sonuc.data.status === 'active' ? 'Aktif' : 'Pasif' }}
                            </span>
                          </div>
                          <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-600">Başlangıç Tarihi:</span>
                            <span class="text-gray-800">{{ formatDate(tool.sonuc.data.start_date) }}</span>
                          </div>
                          <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-600">Bitiş Tarihi:</span>
                            <span class="text-gray-800">{{ formatDate(tool.sonuc.data.end_date) }}</span>
                          </div>
                          <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-600">Otomatik Yenileme:</span>
                            <span :class="[
                              'px-2 py-1 rounded text-xs font-medium',
                              tool.sonuc.data.auto_renewal ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                            ]">
                              {{ tool.sonuc.data.auto_renewal ? 'Açık' : 'Kapalı' }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Paket sonuçları -->
                  <div v-if="tool.arac_adi === 'get_available_packages' && tool.sonuc && tool.sonuc.success" class="space-y-2">
                    <div class="text-sm font-medium text-gray-800 mb-2">
                      📦 Mevcut Paketler ({{ tool.sonuc.data.packages.length }} adet)
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div v-for="(pkg, packageIndex) in tool.sonuc.data.packages" :key="packageIndex" 
                           class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div class="flex justify-between items-start mb-3">
                          <div class="text-lg font-bold text-gray-800">
                            {{ pkg.package_name }}
                          </div>
                          <div class="text-2xl font-bold text-blue-600">
                            {{ pkg.monthly_fee }}₺
                          </div>
                        </div>
                        <div class="text-sm text-gray-600 mb-3">
                          {{ pkg.description }}
                        </div>
                        <div class="space-y-2">
                          <div class="flex items-center text-sm">
                            <span class="text-blue-500 mr-2">🌐</span>
                            <span class="text-gray-700">{{ pkg.features.internet_gb }} GB İnternet</span>
                          </div>
                          <div class="flex items-center text-sm">
                            <span class="text-green-500 mr-2">📞</span>
                            <span class="text-gray-700">{{ pkg.features.voice_minutes }} Dakika</span>
                          </div>
                          <div class="flex items-center text-sm">
                            <span class="text-purple-500 mr-2">💬</span>
                            <span class="text-gray-700">{{ pkg.features.sms_count }} SMS</span>
                          </div>
                          <div v-if="pkg.features.roaming_enabled" class="flex items-center text-sm">
                            <span class="text-orange-500 mr-2">🌍</span>
                            <span class="text-gray-700">Yurtdışı Dahil</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Kota sonuçları -->
                  <div v-else-if="tool.arac_adi === 'get_remaining_quotas' && tool.sonuc && tool.sonuc.success" class="space-y-2">
                    <div class="text-sm font-medium text-gray-800 mb-2">
                      📊 Kalan Kota Bilgileriniz
                    </div>
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div v-for="(quota, quotaIndex) in tool.sonuc.data.quotas" :key="quotaIndex" 
                             class="text-center p-3 bg-gray-50 rounded-lg">
                          <div class="text-2xl font-bold text-blue-600 mb-1">
                            {{ quota.remaining }}{{ quota.unit }}
                          </div>
                          <div class="text-sm text-gray-600">
                            {{ quota.service_name }}
                          </div>
                          <div class="text-xs text-gray-500 mt-1">
                            Toplam: {{ quota.total }}{{ quota.unit }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Ağ durumu sonuçları -->
                  <div v-else-if="tool.arac_adi === 'check_network_status' && tool.sonuc && tool.sonuc.success" class="space-y-2">
                    <div class="text-sm font-medium text-gray-800 mb-2">
                      📡 Ağ Durumu
                    </div>
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                      <div class="space-y-3">
                        <div class="flex items-center justify-between">
                          <span class="text-gray-700">Durum:</span>
                          <span :class="[
                            'px-2 py-1 rounded text-xs font-medium',
                            tool.sonuc.data.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          ]">
                            {{ tool.sonuc.data.status === 'active' ? 'Aktif' : 'Pasif' }}
                          </span>
                        </div>
                        <div class="flex items-center justify-between">
                          <span class="text-gray-700">Sinyal Gücü:</span>
                          <span class="text-blue-600 font-medium">{{ tool.sonuc.data.signal_strength }}%</span>
                        </div>
                        <div class="flex items-center justify-between">
                          <span class="text-gray-700">Konum:</span>
                          <span class="text-gray-800">{{ tool.sonuc.data.location }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Hız testi sonuçları -->
                  <div v-else-if="tool.arac_adi === 'test_internet_speed' && tool.sonuc && tool.sonuc.success" class="space-y-2">
                    <div class="text-sm font-medium text-gray-800 mb-2">
                      ⚡ İnternet Hız Testi Sonuçları
                    </div>
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="text-center p-3 bg-blue-50 rounded-lg">
                          <div class="text-2xl font-bold text-blue-600 mb-1">
                            {{ tool.sonuc.data.download_speed }} Mbps
                          </div>
                          <div class="text-sm text-gray-600">İndirme Hızı</div>
                        </div>
                        <div class="text-center p-3 bg-green-50 rounded-lg">
                          <div class="text-2xl font-bold text-green-600 mb-1">
                            {{ tool.sonuc.data.upload_speed }} Mbps
                          </div>
                          <div class="text-sm text-gray-600">Yükleme Hızı</div>
                        </div>
                        <div class="text-center p-3 bg-purple-50 rounded-lg">
                          <div class="text-2xl font-bold text-purple-600 mb-1">
                            {{ tool.sonuc.data.ping }} ms
                          </div>
                          <div class="text-sm text-gray-600">Ping</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Mevcut fatura sonuçları -->
                  <div v-else-if="tool.arac_adi === 'get_current_bill' && tool.sonuc && tool.sonuc.success" class="space-y-2">
                    <div class="text-sm font-medium text-gray-800 mb-2">
                      📄 Mevcut Faturanız
                    </div>
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                      <div class="flex justify-between items-start mb-4">
                        <div class="text-lg font-bold text-gray-800">
                          Fatura #{{ tool.sonuc.data.bill_id }}
                        </div>
                        <div class="text-3xl font-bold text-blue-600">
                          {{ tool.sonuc.data.amount }} {{ tool.sonuc.data.currency }}
                        </div>
                      </div>
                      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="space-y-2">
                          <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-600">Fatura Tarihi:</span>
                            <span class="text-gray-800">{{ formatDate(tool.sonuc.data.bill_date) }}</span>
                          </div>
                          <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-600">Son Ödeme:</span>
                            <span class="text-gray-800">{{ formatDate(tool.sonuc.data.due_date) }}</span>
                          </div>
                          <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-600">Durum:</span>
                            <span :class="[
                              'px-2 py-1 rounded text-xs font-medium',
                              tool.sonuc.data.status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            ]">
                              {{ tool.sonuc.data.status === 'paid' ? 'Ödendi' : 'Ödenmedi' }}
                            </span>
                          </div>
                        </div>
                        <div class="space-y-2">
                          <div class="text-sm font-medium text-gray-700 mb-2">Hizmet Detayları:</div>
                          <div v-for="service in tool.sonuc.data.services" :key="service.service_name" 
                               class="flex items-center justify-between text-sm">
                            <span class="text-gray-600">{{ service.service_name }}:</span>
                            <span class="text-gray-800 font-medium">{{ service.amount }} {{ tool.sonuc.data.currency }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Genel JSON görünümü (sadece tanımlanmamış araçlar için) -->
                  <div v-else-if="tool.sonuc && !['get_past_bills', 'get_current_bill', 'get_current_package', 'get_available_packages', 'get_remaining_quotas', 'check_network_status', 'test_internet_speed'].includes(tool.arac_adi)" class="text-sm text-gray-700">
                    <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
                      <div class="text-xs text-gray-500 mb-2">Ham Veri:</div>
                      <pre class="bg-gray-100 p-2 rounded text-xs overflow-x-auto">{{ JSON.stringify(tool.sonuc, null, 2) }}</pre>
                    </div>
                  </div>
                  
                  <!-- Hata durumu -->
                  <div v-if="tool.hata_mesaji" class="text-sm text-red-600 mt-2">
                    ❌ Hata: {{ tool.hata_mesaji }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Message Footer -->
            <div class="flex items-center justify-between">
              <span 
                :class="[
                  'text-xs font-medium',
                  message.sender === 'user' ? 'text-white/80' : (currentTheme === 'monochrome' ? 'text-black' : 'text-gray-600')
                ]"
              >
                {{ message.sender === 'user' ? 'Siz' : 'Choyrens AI' }}
              </span>
              <span 
                :class="[
                  'text-xs opacity-75',
                  message.sender === 'user' ? 'text-white/80' : (currentTheme === 'monochrome' ? 'text-black' : 'text-gray-500')
                ]"
              >
                {{ formatTime(message.timestamp) }}
              </span>
            </div>

            <!-- Bot Message Actions -->
            <BotMessageActions
              v-if="message.sender !== 'user'"
              :message="message.text"
              :messageId="message.id"
              @like="handleFeedbackChanged"
              @dislike="handleFeedbackChanged"
              @speak="handleSpeakMessage"
            />
          </div>
        </div>
        
        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex justify-start">
          <div 
            class="rounded-bl-md p-4 shadow-lg font-sans"
            :style="currentTheme === 'monochrome'
              ? 'background: #ffffff; color: #000000;'
              : darkMode 
                ? 'background: rgba(31, 41, 55, 0.9); color: #f9fafb;' 
                : 'background: #f3f4f6; color: #111827;'"
          >
            <div class="flex items-center space-x-3">
              <div class="flex space-x-1">
                <div class="w-3 h-3 rounded-full animate-bounce" :style="`background-color: ${currentTheme === 'monochrome' ? '#000000' : getThemeColor()}`"></div>
                <div class="w-3 h-3 rounded-full animate-bounce" :style="`background-color: ${currentTheme === 'monochrome' ? '#000000' : '#6b7280'}; animation-delay: 0.1s`"></div>
                <div class="w-3 h-3 rounded-full animate-bounce" :style="`background-color: ${currentTheme === 'monochrome' ? '#000000' : '#64748b'}; animation-delay: 0.2s`"></div>
              </div>
                              <span class="text-sm font-medium" :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-gray-200' : 'text-gray-700')">
                  Choyrens AI yazıyor...
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Input Area - Transparent Seamless Footer -->
      <div class="composer p-4 relative z-20 flex-shrink-0 sticky bottom-0">
        <form @submit.prevent="sendMessage" class="flex items-center gap-4 max-w-2xl mx-auto">
          <!-- Model Selector -->
          <div class="relative">
            <button type="button"
                    @click="toggleModelMenu"
                    class="px-3 py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 flex items-center gap-2"
                    :class="currentTheme === 'monochrome' ? 'bg-black text-white' : 'bg-white text-gray-800 border border-gray-200'">
              <span class="text-xs font-semibold">{{ selectedModelLabel }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.08 1.04l-4.25 4.25a.75.75 0 01-1.08 0L5.21 8.27a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
              </svg>
            </button>
            <div v-if="showModelMenu" class="absolute left-0 bottom-full mb-2 w-56 rounded-xl shadow-2xl border z-50"
                 :class="currentTheme === 'monochrome' ? 'bg-black border-gray-700' : 'bg-white border-gray-200'">
              <div v-for="m in aiModels" :key="m.id"
                   @click="selectModel(m)"
                   class="px-4 py-3 cursor-pointer flex items-center justify-between hover:bg-gray-50"
                   :class="{ 'bg-blue-50': selectedModel === m.id }">
                <div class="flex items-center gap-2">
                  <div>
                    <div class="text-sm font-semibold">{{ m.label }}</div>
                    <div class="text-xs text-gray-500">{{ m.desc }}</div>
                  </div>
                </div>
                <span v-if="selectedModel === m.id">✓</span>
              </div>
            </div>
          </div>

          <input
            ref="messageInput"
            v-model="message"
            type="text"
            placeholder="Mesajınızı yazın veya sesli komut kullanın..."
            class="input flex-1 p-4 rounded-xl text-base font-sans shadow-lg hover:shadow-xl transition-all duration-300"
            :class="getInputClasses"
            @keydown="handleInputKeydown"
          />
          
          <!-- Voice Command Button -->
          <VoiceCommand
            :darkMode="darkMode"
            :currentTheme="currentTheme"
            @voice-result="handleVoiceResult"
          />
          
          <button
            type="submit"
            class="p-4 rounded-xl shadow-xl hover:shadow-2xl transform hover:scale-105 disabled:opacity-30 text-white font-semibold"
            :disabled="!message.trim()"
            :style="`background: ${currentTheme === 'monochrome' ? 'linear-gradient(135deg, #000000 0%, #000000 50%, #000000 100%)' : getUserMessageGradient()};`"
          >
            Gönder
          </button>
        </form>
      </div>
    </div>

    <!-- User Info Panel -->
    <UserInfoPanel
      :isVisible="showUserPanel"
      :darkMode="darkMode"
      :currentTheme="currentTheme"
      :userInfo="userInfo"
      @update:userInfo="userInfo = { ...userInfo, ...$event }"
      @close="closeUserPanel"
      @toggle-dark-mode="toggleDarkMode"
      @logout="handleLogout"
      @edit-profile="handleEditProfile"
    />
  </div>
</template>

<script>
import LogoHeader from '../components/LogoHeader.vue'
import VoiceCommand from '../components/VoiceCommand.vue'
import BotMessageActions from '../components/BotMessageActions.vue'
import UserInfoPanel from '../components/UserInfoPanel.vue'
import { chatAPI } from '../services/api.js'

export default {
  components: {
    LogoHeader,
    VoiceCommand,
    BotMessageActions,
    UserInfoPanel
  },
  data() {
    return {
      darkMode: false,
      currentTheme: 'blue',
      message: '',
      isTyping: false,
      sessionId: null,
      userId: null,
      isConnected: false,
      connectionTimer: null,
      showUserPanel: false,
      userInfo: {
        name: 'Enes Faruk Aydın',
        email: 'enes.faruk.aydin@email.com',
        avatar: null
      },
      // Model seçimi
      showModelMenu: false,
      selectedModel: 'default',
      aiModels: [
        { id: 'default', label: 'Varsayılan', desc: 'Otomatik seçim' },
        { id: 'telekom-v6', label: 'Choyrens v6', desc: 'GGUF 8B q5_k_m' },
        { id: 'telekom-v5', label: 'Choyrens v5', desc: 'q8_0 gguf' }
      ],
      messages: [
        {
          id: 1,
          sender: 'bot',
          text: 'Merhaba! Ben Choyrens AI, size nasıl yardımcı olabilirim?',
          timestamp: new Date()
        }
      ],
      themes: [
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
      ],
      showThemeMenu: false
    }
  },
  computed: {
    currentThemeIcon() {
      const theme = this.themes.find(t => t.name === this.currentTheme)
      return theme ? theme.icon : '🔵'
    },
    currentBackground() {
      const theme = this.themes.find(t => t.name === this.currentTheme)
      if (!theme) return this.darkMode ? 'from-black via-gray-900 to-blue-950' : 'from-blue-50 via-gray-50 to-slate-50'
      
      return this.darkMode ? theme.darkBackground : theme.lightBackground
    },

    getInputClasses() {
      const theme = this.themes.find(t => t.name === this.currentTheme)
      
      if (this.currentTheme === 'monochrome') {
        return this.darkMode 
          ? 'bg-white/6 backdrop-blur-sm text-white placeholder-white/50 border-white/20 focus:border-white/40 focus:bg-white/10' 
          : 'bg-black/6 backdrop-blur-sm text-black placeholder-gray-600/70 border-black/20 focus:border-black/40 focus:bg-black/10'
      }
      
      if (!theme) return this.darkMode 
        ? 'bg-white/6 backdrop-blur-sm text-white placeholder-white/50 border-white/20' 
        : 'bg-black/6 backdrop-blur-sm text-gray-900 placeholder-gray-600/70 border-black/20'
      
      // Tema rengine göre ultra hafif şeffaf input stilleri
      const themeInputs = {
        'blue': this.darkMode 
          ? 'bg-white/6 backdrop-blur-sm text-white placeholder-white/50 border-white/20 focus:border-white/40 focus:bg-white/10' 
          : 'bg-black/6 backdrop-blur-sm text-gray-900 placeholder-gray-700/70 border-black/20 focus:border-black/40 focus:bg-black/10',
        'burgundy': this.darkMode 
          ? 'bg-white/6 backdrop-blur-sm text-white placeholder-white/50 border-white/20 focus:border-white/40 focus:bg-white/10' 
          : 'bg-black/6 backdrop-blur-sm text-gray-900 placeholder-gray-700/70 border-black/20 focus:border-black/40 focus:bg-black/10',
        'purple': this.darkMode 
          ? 'bg-white/6 backdrop-blur-sm text-white placeholder-white/50 border-white/20 focus:border-white/40 focus:bg-white/10' 
          : 'bg-black/6 backdrop-blur-sm text-gray-900 placeholder-gray-700/70 border-black/20 focus:border-black/40 focus:bg-black/10',
        'emerald': this.darkMode 
          ? 'bg-white/6 backdrop-blur-sm text-white placeholder-white/50 border-white/20 focus:border-white/40 focus:bg-white/10' 
          : 'bg-black/6 backdrop-blur-sm text-gray-900 placeholder-gray-700/70 border-black/20 focus:border-black/40 focus:bg-black/10'
      }
      
      return themeInputs[this.currentTheme] || (this.darkMode 
        ? 'bg-white/6 backdrop-blur-sm text-white placeholder-white/50 border-white/20' 
        : 'bg-black/6 backdrop-blur-sm text-gray-900 placeholder-gray-600/70 border-black/20')
    },
    selectedModelLabel() {
      const found = this.aiModels.find(m => m.id === this.selectedModel)
      return found ? found.label : 'Model'
    }
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      if (this.darkMode) {
        document.documentElement.classList.add('dark')
        localStorage.setItem('darkMode', 'true')
      } else {
        document.documentElement.classList.remove('dark')
        localStorage.setItem('darkMode', 'false')
      }
    },
    toggleThemeMenu() {
      this.showThemeMenu = !this.showThemeMenu
    },
    selectTheme(themeName) {
      this.currentTheme = themeName
      this.showThemeMenu = false
      localStorage.setItem('themeColor', this.currentTheme)
      document.documentElement.setAttribute('data-theme', this.currentTheme)
      this.updateThemeColors()
      this.showThemeNotification()
    },
    toggleThemeColor() {
      // Cycle through themes
      const currentIndex = this.themes.findIndex(t => t.name === this.currentTheme)
      const nextIndex = (currentIndex + 1) % this.themes.length
      this.currentTheme = this.themes[nextIndex].name
      
      // Save theme preference
      localStorage.setItem('themeColor', this.currentTheme)
      
      // Apply theme to document
      document.documentElement.setAttribute('data-theme', this.currentTheme)
      
      // Force CSS variable updates
      this.updateThemeColors()
      
      // Show theme change notification
      this.showThemeNotification()
    },
    updateThemeColors() {
      const root = document.documentElement
      const theme = this.themes.find(t => t.name === this.currentTheme)
      
      if (theme) {
        if (theme.name === 'blue') {
          root.style.setProperty('--primary-color', '#3b82f6')
          root.style.setProperty('--secondary-color', '#1d4ed8')
          root.style.setProperty('--accent-color', '#1e40af')
          root.style.setProperty('--card-border', 'rgba(59, 130, 246, 0.15)')
          root.style.setProperty('--input-border', 'rgba(59, 130, 246, 0.3)')
          root.style.setProperty('--button-gradient', 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #1e40af 100%)')
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
    },
    showThemeNotification() {
      // Create a simple notification
      const notification = document.createElement('div')
      notification.className = 'fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all duration-300 font-semibold text-sm'
      notification.textContent = `Tema değiştirildi: ${this.getThemeDisplayName(this.currentTheme)}`
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
    },
    async sendMessage() {
      if (!this.message.trim()) return
      
      // Add user message
      this.messages.push({
        id: Date.now(),
        sender: 'user',
        text: this.message,
        timestamp: new Date()
      })
      
      const userMessage = this.message
      this.message = ''
      
      // Scroll to bottom after user message
      this.$nextTick(() => {
        this.scrollToBottom()
      })
      
      // Show typing indicator
      this.isTyping = true
      this.scrollToBottom()
      
      try {
        // Session ID oluştur (eğer yoksa)
        if (!this.sessionId) {
          this.sessionId = 'SESSION_' + Date.now().toString(36) + Math.random().toString(36).substr(2)
        }
        
        // API'ye mesaj gönder - daha uzun timeout ile
        console.log('AI yanıtı bekleniyor...')
        console.log('API URL:', import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000')
        console.log('Session ID:', this.sessionId)
        const response = await chatAPI.sendMessage(userMessage, this.userId, this.sessionId, this.selectedModel)
        
        // Hide typing indicator
        this.isTyping = false
        
        if (response.success) {
          // Bot yanıtını ekle
          this.messages.push({
            id: Date.now() + 1,
            sender: 'bot',
            text: response.response,
            timestamp: new Date(),
            toolResults: response.tool_calls || [],
            userQuestion: userMessage,
            feedback: {
              liked: false,
              disliked: false,
              emotion: response.emotion || '😊' // Backend'den gelen emoji veya varsayılan
            }
          })
          
          // Session ID'yi güncelle
          if (response.session_id) {
            this.sessionId = response.session_id
          }
          
          // User ID'yi güncelle
          if (response.user_id) {
            this.userId = response.user_id
          }
          
          this.isConnected = true
        } else {
          // Hata durumunda fallback yanıt
          this.messages.push({
            id: Date.now() + 1,
            sender: 'bot',
            text: 'Üzgünüm, şu anda yanıt veremiyorum. Lütfen daha sonra tekrar deneyin.',
            timestamp: new Date(),
            userQuestion: userMessage,
            feedback: {
              liked: false,
              disliked: false,
              emotion: '😕' // Hata durumunda üzgün emoji
            }
          })
        }
      } catch (error) {
        console.error('API Error:', error)
        
        // Hide typing indicator
        this.isTyping = false
        
        // Hata mesajını göster
        this.messages.push({
          id: Date.now() + 1,
          sender: 'bot',
          text: `Bağlantı hatası: ${error.message}`,
          timestamp: new Date(),
          userQuestion: userMessage,
          feedback: {
            liked: false,
            disliked: false,
            emotion: '😡' // Bağlantı hatası durumunda kızgın emoji
          }
        })
        
        this.isConnected = false
      }
      
      // Scroll to bottom after bot response
      this.$nextTick(() => {
        setTimeout(() => {
          this.scrollToBottom()
        }, 100)
      })
    },
    
    async sendBotMessage(text) {
      // Show typing indicator
      this.isTyping = true
      this.scrollToBottom()
      
      // Simulate typing delay
      await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 500))
      
      // Hide typing indicator
      this.isTyping = false
      
      this.messages.push({
        id: Date.now(),
        sender: 'bot',
        text: text,
        timestamp: new Date(),
        feedback: {
          liked: false,
          disliked: false,
          emotion: '😊' // Varsayılan emoji
        }
      })
      
      // Scroll to bottom after bot message
      this.$nextTick(() => {
        setTimeout(() => {
          this.scrollToBottom()
        }, 100)
      })
    },
    getBotResponse(text) {
      const lowerText = text.toLowerCase()
      
      if (lowerText.includes('fatura') || lowerText.includes('ödeme') || lowerText.includes('fatura bilgisi')) {
        return 'Fatura bilgileriniz için https://fatura.cayros.com adresini ziyaret edebilir veya müşteri numaranızı bana iletebilirsiniz. Size anında yardımcı olabilirim!'
      } else if (lowerText.includes('internet') || lowerText.includes('bağlantı')) {
        return 'İnternet bağlantı sorununuz için öncelikle modeminizi yeniden başlatmanızı öneririm. Sorun devam ederse teknik destek ekibimize yönlendirebilirim.'
      } else if (lowerText.includes('tarife') || lowerText.includes('paket')) {
        return 'Tarife ve paket bilgileriniz için müşteri numaranızı paylaşabilir misiniz? Size en uygun tarifeleri gösterebilirim!'
      } else if (lowerText.includes('kampanya') || lowerText.includes('indirim')) {
        return 'Güncel kampanyalarımızı görmek için https://kampanya.cayros.com adresini ziyaret edebilirsiniz. Size özel fırsatlar sunuyoruz!'
      } else if (lowerText.includes('teşekkür')) {
        return 'Ben teşekkür ederim! Başka bir konuda yardımcı olabilir miyim? Her zaman buradayım!'
      } else {
        return 'Anladığım kadarıyla ' + text + ' hakkında bilgi almak istiyorsunuz. Size en doğru bilgiyi verebilmek için lütfen daha detaylı bilgi paylaşabilir misiniz?'
      }
    },
    async mounted() {
      // Sayfa yüklendiğinde backend bağlantısını kontrol et
      await this.checkConnection()
      

      
      // Her 5 saniyede bir bağlantıyı kontrol et
      this.connectionTimer = setInterval(async () => {
        await this.checkConnection()
      }, 5000)
    },
    
    async checkConnection() {
      try {
        const healthResponse = await chatAPI.getHealth()
        // Backend yanıt veriyorsa bağlantı var demektir, status unhealthy olsa bile
        this.isConnected = true
        
        if (healthResponse.status === 'healthy') {
          console.log('Backend bağlantısı başarılı')
        } else {
          console.warn('Backend çalışıyor ama AI modeli yüklenmemiş')
        }
      } catch (error) {
        console.error('Backend bağlantı hatası:', error)
        this.isConnected = false
      }
    },
    formatTime(timestamp) {
      return timestamp.toLocaleTimeString('tr-TR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        // Force scroll to bottom with smooth behavior
        this.$nextTick(() => {
          container.scrollTop = container.scrollHeight
        })
      }
    },
         getUserMessageGradient() {
       const theme = this.themes.find(t => t.name === this.currentTheme)
       if (theme) {
         const { primary, secondary, accent } = theme.colors
         return `linear-gradient(135deg, ${primary} 0%, ${secondary} 50%, ${accent} 100%)`
       }
       return 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #1e40af 100%)' // Default gradient
     },
     getThemeColor() {
       const theme = this.themes.find(t => t.name === this.currentTheme)
       if (theme) {
         return theme.colors.primary
       }
       return '#3b82f6' // Default blue
     },
     getThemeDisplayName(name) {
       const themeNames = {
         'blue': 'Marmara',
         'burgundy': 'Anadolu',
         'purple': 'Ubuntu',
         'emerald': 'Gemlik',
         'monochrome': 'Monokrom'
       }
       return themeNames[name] || name
     },
         handleClickOutside(event) {
      // Close theme menu if clicking outside
      if (this.showThemeMenu && !event.target.closest('.theme-menu-container')) {
        this.showThemeMenu = false
      }
    },
    getToolDisplayName(toolName) {
      const toolNames = {
        'get_past_bills': '📋 Geçmiş Faturalar',
        'get_current_bill': '📄 Mevcut Fatura',
        'get_available_packages': '📦 Paketler',
        'get_remaining_quotas': '📊 Kalan Kota',
        'check_network_status': '📡 Ağ Durumu',
        'test_internet_speed': '⚡ Hız Testi'
      }
      return toolNames[toolName] || toolName
    },
    getToolStatus(status) {
      const statusMap = {
        'tamamlandi': '✅ Tamamlandı',
        'beklemede': '⏳ Beklemede',
        'hata': '❌ Hata',
        'bekliyor': '⏳ Bekliyor'
      }
      return statusMap[status] || status
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('tr-TR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    handleVoiceResult(voiceText) {
      // Set the voice text to message input
      this.message = voiceText.trim()
      
      // Focus on input field to show the text
      this.$nextTick(() => {
        if (this.$refs.messageInput) {
          this.$refs.messageInput.focus()
        }
      })
      
      // Auto-send the message after a short delay for better UX
      setTimeout(() => {
        if (this.message.trim()) {
          this.sendMessage()
        }
      }, 1500)
    },
    handleFeedbackChanged(feedbackData) {
      // Handle feedback changes from bot message actions
      console.log('Feedback received:', feedbackData)
      
      // Update the message feedback in the messages array
      const messageIndex = this.messages.findIndex(msg => msg.id === feedbackData.messageId)
      if (messageIndex !== -1) {
        this.$set(this.messages[messageIndex], 'feedback', feedbackData.feedback)
      }
      
      // You can add analytics or send feedback to backend here
      // For example: analytics.track('bot_message_feedback', feedbackData)
    },
    handleSpeakMessage(speakData) {
      // Handle speak action from bot message actions
      console.log('Message spoken:', speakData)
      
      // You can add analytics or other actions here
      // For example: analytics.track('bot_message_spoken', speakData)
    },
    handleInputKeydown(event) {
      // Handle Enter key specifically for input field
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault() // Prevent form submit
        event.stopPropagation() // Stop event from bubbling
        
        // Only send if there's a message
        if (this.message.trim()) {
          this.sendMessage()
        }
      }
      // Allow Shift+Enter for new lines (if input becomes textarea later)
    },
    handleFormEnter(event) {
      // Backup method - Only handle enter if it's coming from the input field
      if (event.target === this.$refs.messageInput) {
        event.preventDefault()
        this.sendMessage()
      }
    },

    // User Panel Methods
    toggleUserPanel() {
      this.showUserPanel = !this.showUserPanel
    },

    closeUserPanel() {
      this.showUserPanel = false
    },

    handleLogout() {
      // Clear user data
      localStorage.removeItem('userToken')
      localStorage.removeItem('userData')
      
      // Redirect to login or home
      this.$router.push('/')
      
      // Show notification
      const notification = document.createElement('div')
      notification.className = 'fixed top-4 right-4 bg-red-600 text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all duration-300 font-semibold text-sm'
      notification.textContent = '👋 Çıkış yapıldı'
      document.body.appendChild(notification)
      
      setTimeout(() => {
        notification.style.transform = 'translateY(-100%)'
        notification.style.opacity = '0'
        setTimeout(() => document.body.removeChild(notification), 300)
      }, 2000)
    },

    handleEditProfile() {
      // Bu alanı geliştirme için işaretleyelim
      console.log('Profil düzenleme özelliği yakında eklenecek')
      
      // Geçici bildirim
      const notification = document.createElement('div')
      notification.className = 'fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all duration-300 font-semibold text-sm'
      notification.textContent = '✏️ Profil düzenleme özelliği yakında eklenecek'
      document.body.appendChild(notification)
      
      setTimeout(() => {
        notification.style.transform = 'translateY(-100%)'
        notification.style.opacity = '0'
        setTimeout(() => document.body.removeChild(notification), 300)
      }, 2000)
    },
    toggleModelMenu() {
      this.showModelMenu = !this.showModelMenu
    },
    selectModel(model) {
      this.selectedModel = model.id
      this.showModelMenu = false
    }
  },
  mounted() {
    // Check for saved dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode')
    if (savedDarkMode === 'true') {
      this.darkMode = true
      document.documentElement.classList.add('dark')
    } else {
      this.darkMode = false
      document.documentElement.classList.remove('dark')
    }
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('themeColor')
    if (savedTheme && this.themes.find(t => t.name === savedTheme)) {
      this.currentTheme = savedTheme
      document.documentElement.setAttribute('data-theme', this.currentTheme)
      this.updateThemeColors()
    } else {
      // Set default theme
      document.documentElement.setAttribute('data-theme', 'blue')
      this.updateThemeColors()
    }
    
    // Add click outside listener for theme menu
    document.addEventListener('click', this.handleClickOutside)
    
    // Check backend connection initially and on interval
    this.checkConnection()
    this.connectionTimer = setInterval(() => {
      this.checkConnection()
    }, 5000)
    
    // Initial scroll to bottom
    this.$nextTick(() => {
      this.scrollToBottom()
    })
  },
  beforeUnmount() {
    // Timer'ı temizle
    if (this.connectionTimer) {
      clearInterval(this.connectionTimer)
    }
    
    // Event listener'ı temizle
    document.removeEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    // Remove click outside listener
    document.removeEventListener('click', this.handleClickOutside)
  },
  updated() {
    // Scroll to bottom whenever messages are updated
    this.$nextTick(() => {
      setTimeout(() => {
        this.scrollToBottom()
      }, 100)
    })
  }
}
</script>

<style scoped>
/* Dark mode styles are now handled globally in style.css */

/* Hide scrollbar for webkit browsers */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for Firefox */
.scrollbar-hide {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

/* WhatsApp-style chat layout */
.chat-container {
  height: 100vh;
  height: 100dvh; /* Dynamic viewport height for mobile */
}

/* Messages area smooth scrolling */
.messages-area {
  scroll-behavior: smooth;
}

/* Mobile viewport adjustments */
@supports (height: 100dvh) {
  .chat-container {
    height: 100dvh;
  }
}

/* iOS safe area support */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .input-area {
    padding-bottom: calc(1rem + env(safe-area-inset-bottom));
  }
}

/* Unified fullscreen background system */

/* Composer - completely transparent */
.composer {
  background: transparent !important;
  border: none !important;
  border-top: none !important;
}

/* Ultra-light input styling */
.composer input {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition: all 0.3s ease;
}

/* Enhanced focus state */
.composer input:focus {
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}
</style>