<template>
  <div class="space-y-4 mb-4">
    <div 
      v-for="(message, index) in messages" 
      :key="index"
      :class="[
        'bg-white rounded-lg p-4 shadow',
        message.isUser ? 'ml-8' : 'mr-8'
      ]"
    >
      <div class="text-gray-700">{{ message.text }}</div>
      
      <!-- Araç sonuçları için özel görünüm -->
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
            
            <!-- Diğer araç sonuçları için genel görünüm -->
            <div v-else-if="tool.sonuc" class="text-sm text-gray-700">
              <pre class="bg-gray-100 p-2 rounded text-xs overflow-x-auto">{{ JSON.stringify(tool.sonuc, null, 2) }}</pre>
            </div>
            
            <!-- Hata durumu -->
            <div v-if="tool.hata_mesaji" class="text-sm text-red-600 mt-2">
              ❌ Hata: {{ tool.hata_mesaji }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="text-right text-xs text-gray-500 mt-2">{{ message.time }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const messages = ref([])

const addMessage = (text, isUser = false, toolResults = null) => {
  messages.value.push({
    text,
    time: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
    isUser,
    toolResults
  })
}

const getToolDisplayName = (toolName) => {
  const toolNames = {
    'get_past_bills': '📋 Geçmiş Faturalar',
    'get_current_bill': '📄 Mevcut Fatura',
    'get_available_packages': '📦 Paketler',
    'get_remaining_quotas': '📊 Kalan Kota',
    'check_network_status': '📡 Ağ Durumu',
    'test_internet_speed': '⚡ Hız Testi'
  }
  return toolNames[toolName] || toolName
}

const getToolStatus = (status) => {
  const statusMap = {
    'tamamlandi': '✅ Tamamlandı',
    'beklemede': '⏳ Beklemede',
    'hata': '❌ Hata',
    'bekliyor': '⏳ Bekliyor'
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('tr-TR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Expose addMessage function for parent component
defineExpose({ addMessage })
</script>