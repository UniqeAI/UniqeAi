# Gelişmiş AI Modeli için Eğitim Veri Seti Kılavuzu

> **Takım İçin Not:** Bu doküman, "olağanüstü" bir AI asistanı eğitmek için gereken gelişmiş diyalog senaryolarını ve veri formatını açıklamaktadır. Lütfen her strateji başlığı için burada belirtilen kalitede ve yapıda **en az 2000 adet** yeni ve özgün diyalog verisi oluşturun.

## 🎯 Nihai Veri Formatı

Modelimizin sadece araç çağırmayı değil, aynı zamanda bu araçların sonuçlarını anlamayı ve buna göre hareket etmeyi öğrenmesi kritik öneme sahiptir. Bu nedenle, standart diyalog formatımıza `rol: "arac"` (tool) adımını ekliyoruz.

**Gelişmiş Diyalog Yapısı:**

```json
{
  "id": "SCENARIO-001",
  "senaryo": "Strateji Adı - Kısa Açıklama",
  "donguler": [
    { 
      "rol": "kullanici", 
      "icerik": "Kullanıcının ilk talebi." 
    },
    { 
      "rol": "asistan", 
      "icerik": "Asistanın ilk sözlü yanıtı (isteğe bağlı, doğallık katar)." 
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "API_fonksiyon_adi",
          "parametreler": { "param1": "deger1" }
      }]
    },
    {
      "rol": "arac",
      "icerik": "{ \"success\": true, \"data\": { ... } }",
      "arac_cagrisi_kimligi": "fonksiyon_adi_ile_ilgili_bir_id" // Gelecekteki kullanımlar için
    },
    {
      "rol": "asistan",
      "icerik": "Asistanın, araç sonucunu yorumladıktan sonraki sözlü yanıtı."
    }
  ]
}
```

---

## 🧠 Stratejiler ve Örnek Veri Setleri

### Strateji 1: Zincirleme Araç Kullanımı (Tool Chaining)

**Amaç:** Modelin, bir API çağrısının sonucunu kullanarak bir sonraki mantıklı adımı atmasını sağlamak. Bu, tek bir kullanıcı talebini çözmek için birden fazla aracın sırayla kullanılmasını içerir.

**Örnek 1.1:**
```json
{
  "id": "TC-001",
  "senaryo": "Tool Chaining - Ödenmemiş faturayı bul ve ödeme teklif et",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "Merhaba, bu ayki faturamı ve durumunu öğrenebilir miyim? Müşteri numaram 8901."
    },
    {
      "rol": "asistan",
      "icerik": "Elbette, 8901 numaralı üyeliğiniz için güncel fatura bilgilerinizi hemen kontrol ediyorum."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [
        {
          "fonksiyon": "get_current_bill",
          "parametreler": { "user_id": 8901 }
        }
      ]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"bill_id\": \"F-2024-8901\", \"user_id\": 8901, \"amount\": 125.50, \"currency\": \"TRY\", \"due_date\": \"2024-08-20\", \"status\": \"unpaid\"}}"
    },
    {
      "rol": "asistan",
      "icerik": "Güncel faturanız 125.50 TL tutarındadır ve son ödeme tarihi 20 Ağustos 2024 olarak görünmektedir. Henüz ödenmemiş. Kredi kartınızla şimdi ödemek ister misiniz?"
    },
    {
      "rol": "kullanici",
      "icerik": "Evet, lütfen yapalım."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [
        {
          "fonksiyon": "pay_bill",
          "parametreler": {
            "bill_id": "F-2024-8901",
            "method": "credit_card"
          }
        }
      ]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"transaction_id\": \"TXN-2024-99812\", \"status\": \"completed\"}}"
    },
    {
      "rol": "asistan",
      "icerik": "Ödemeniz başarıyla tamamlandı. İşlem referans numaranız: TXN-2024-99812. Başka bir konuda yardımcı olabilir miyim?"
    }
  ]
}
```

**Örnek 1.2:**
```json
{
  "id": "TC-002",
  "senaryo": "Tool Chaining - Kullanıcı paketini yetersiz bulur, asistan yeni paketleri listeler ve detay verir",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "İnternetim sürekli bitiyor, paketimde ne kadar kalmış bir bakar mısın? User ID: 9408"
    },
    {
      "rol": "asistan",
      "icerik": "Tabii, 9408 ID'li hesabınız için kalan kullanım haklarınızı kontrol ediyorum."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "get_remaining_quotas",
          "parametreler": { "user_id": 9408 }
      }]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"internet_remaining_gb\": 3.2, \"voice_remaining_minutes\": 850, \"period_end\": \"2024-09-30\"}}"
    },
    {
      "rol": "asistan",
      "icerik": "Dönem sonuna daha 15 gün varken sadece 3.2 GB internetiniz kalmış. Dilerseniz size daha uygun, daha yüksek kotalı paketlerimizi listeleyebilirim."
    },
    {
      "rol": "kullanici",
      "icerik": "Evet, harika olur. Özellikle interneti bol olanları görmek istiyorum."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "get_available_packages",
          "parametreler": {}
      }]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"packages\": [{\"name\": \"Mega İnternet\", \"monthly_fee\": 69.50, \"features\": {\"internet_gb\": 50}}, {\"name\": \"Gamer Pro\", \"monthly_fee\": 99.90, \"features\": {\"internet_gb\": 100}}]}}"
    },
    {
      "rol": "asistan",
      "icerik": "Şu anda iki popüler seçeneğimiz var: 50 GB internet içeren 'Mega İnternet' ve 100 GB içeren 'Gamer Pro'. Hangisinin detaylarını istersiniz?"
    },
    {
      "rol": "kullanici",
      "icerik": "Gamer Pro kulağa hoş geliyor, onun detaylarını alabilir miyim?"
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "get_package_details",
          "parametreler": { "package_name": "Gamer Pro" }
      }]
    }
  ]
}
```

---

### Strateji 2: Belirsizliği Giderme (Disambiguation)

**Amaç:** Modelin, kullanıcı talebi eksik veya belirsiz olduğunda varsayımlarda bulunmak yerine, doğru aracı kullanabilmek için netleştirici sorular sormasını sağlamak.

**Örnek 2.1:**
```json
{
  "id": "DA-001",
  "senaryo": "Disambiguation - Kullanıcı 'paketimi değiştir' der, model hangi pakete geçileceğini sorar",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "Merhaba, mevcut tarifemi değiştirmek istiyorum."
    },
    {
      "rol": "asistan",
      "icerik": "Elbette, tarife değişikliği konusunda size yardımcı olabilirim. Hangi tarifeye geçmek istediğinizi belirtmemişsiniz. Size uygun olanları bulmam için mevcut tarifeleri listelememi ister misiniz?"
    },
    {
      "rol": "kullanici",
      "icerik": "Evet, lütfen listele."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [
        {
          "fonksiyon": "get_available_packages",
          "parametreler": {}
        }
      ]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"packages\": [{\"name\": \"Öğrenci Dostu Tarife\", \"monthly_fee\": 49.90}, {\"name\": \"Süper Konuşma\", \"monthly_fee\": 59.90}]}}"
    },
    {
      "rol": "asistan",
      "icerik": "Şu an geçebileceğiniz paketler: 'Öğrenci Dostu Tarife' ve 'Süper Konuşma'. Hangisiyle devam etmek istersiniz?"
    }
  ]
}
```

**Örnek 2.2:**
```json
{
  "id": "DA-002",
  "senaryo": "Disambiguation - Kullanıcı 'arıza' kelimesini kullanır, model arızanın ne olduğunu ve nerede olduğunu sorar",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "Bölgemde bir arıza mı var?"
    },
    {
      "rol": "asistan",
      "icerik": "Size en doğru bilgiyi verebilmem için hangi il veya bölgedeki network durumunu kontrol etmemi istersiniz?"
    },
    {
      "rol": "kullanici",
      "icerik": "Güneydoğu Anadolu, özellikle Diyarbakır için bakabilir misin?"
    },
    {
      "rol": "asistan",
      "icerik": "Hemen Güneydoğu Anadolu bölgesi için genel durumu kontrol ediyorum."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [
        {
          "fonksiyon": "check_network_status",
          "parametreler": {
            "region": "Güneydoğu Anadolu"
          }
        }
      ]
    }
  ]
}
```

---

### Strateji 3: Proaktif Yardım ve Öneri (Proactive Assistance)

**Amaç:** Modelin, sadece isteneni yapmakla kalmayıp, kullanıcının durumunu analiz ederek bir sonraki olası ihtiyacını tahmin etmesini ve proaktif olarak çözüm önermesini sağlamak.

**Örnek 3.1:**
```json
{
  "id": "PA-001",
  "senaryo": "Proactive - Kalan kota az, model ek paket önerir",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "Ay sonuna daha çok var, internetim ne kadar kalmış? (ID: 9408)"
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "get_remaining_quotas",
          "parametreler": { "user_id": 9408 }
      }]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"internet_remaining_gb\": 4.1, \"usage_percentage\": {\"internet\": 92}, \"period_end\": \"2024-10-31\"}}"
    },
    {
      "rol": "asistan",
      "icerik": "İnternet paketinizin %92'sini kullanmışsınız ve sadece 4.1 GB kalmış. Ay sonuna doğru internetinizin bitmemesi için ek paketlerimizi incelemek veya daha yüksek kotalı bir tarifeye geçmek gibi seçenekleri değerlendirmek ister misiniz?"
    }
  ]
}
```

**Örnek 3.2:**
```json
{
  "id": "PA-002",
  "senaryo": "Proactive - Kullanıcı yurt dışına çıkacağını söyler, model roaming açmayı teklif eder",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "Haftaya Almanya'ya gideceğim, hattımla ilgili bir şey yapmam gerekiyor mu? user_id=8763"
    },
    {
      "rol": "asistan",
      "icerik": "Harika bir seyahat dilerim! Yurt dışında hattınızı sorunsuzca kullanabilmeniz için 'roaming' yani yurt dışı kullanım hizmetini aktif etmeniz gerekiyor. Sizin için bu hizmeti şimdi etkinleştirmemi ister misiniz?"
    },
    {
      "rol": "kullanici",
      "icerik": "Evet, lütfen etkinleştir."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "enable_roaming",
          "parametreler": { "user_id": 8763, "status": true }
      }]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"user_id\": 8763, \"roaming_enabled\": true, \"daily_fee\": 25.00}}"
    },
    {
      "rol": "asistan",
      "icerik": "Yurt dışı kullanım hizmetiniz (roaming) başarıyla aktif edilmiştir. Güncel günlük kullanım ücreti 25.00 TL'dir. İyi yolculuklar!"
    }
  ]
}
```

---

### Strateji 4: Hata Yönetimi ve Düzeltme (Error Handling)

**Amaç:** Modelin, bir API çağrısı başarısız olduğunda (`success: false`) paniğe kapılmak yerine, hatanın nedenini kullanıcıya nazikçe açıklamasını ve çözüme yönelik bir sonraki adımı önermesini sağlamak.

**Örnek 4.1:**
```json
{
  "id": "EH-001",
  "senaryo": "Error Handling - Var olmayan bir fatura ID'si ile ödeme yapılmaya çalışılır",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "F-12345678 numaralı faturamı ödemek istiyorum."
    },
    {
      "rol": "asistan",
      "icerik": "Hemen F-12345678 numaralı faturanız için ödeme işlemini başlatıyorum."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "pay_bill",
          "parametreler": { "bill_id": "F-12345678", "method": "credit_card" }
      }]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": false, \"error\": {\"code\": \"BILL_NOT_FOUND\", \"message\": \"Fatura bulunamadı veya daha önce ödenmiş.\"}}"
    },
    {
      "rol": "asistan",
      "icerik": "Üzgünüm, belirttiğiniz fatura numarasını sistemde bulamadım ya da bu fatura daha önceden ödenmiş olabilir. Lütfen fatura numarasını kontrol eder misiniz? Dilerseniz müşteri numaranız üzerinden güncel borcunuzu sorgulayabilirim."
    }
  ]
}
```

**Örnek 4.2:**
```json
{
  "id": "EH-002",
  "senaryo": "Error Handling - Kullanıcı, yetkisi olmayan bir pakete geçmeye çalışır",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "Beni 'Memur Özel' tarifesine geçirir misin? User ID 9509"
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "change_package",
          "parametreler": { "user_id": 9509, "new_package_name": "Memur Özel" }
      }]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": false, \"error\": {\"code\": \"INELIGIBLE_FOR_PACKAGE\", \"message\": \"Kullanıcı bu paket için uygun değil.\", \"details\": \"Bu paket sadece devlet memurları içindir.\"}}"
    },
    {
      "rol": "asistan",
      "icerik": "Anladığım kadarıyla 'Memur Özel' tarifesi, belirli bir meslek grubuna özel olduğu için şu anki aboneliğinizle bu pakete geçiş yapamıyorsunuz. Size özel olarak geçebileceğiniz diğer kampanyalı paketleri listelememi ister misiniz?"
    }
  ]
}
```

---

### Strateji 5: Karmaşık ve Çok Niyetli Görevler (Complex & Multi-Intent)

**Amaç:** Modelin, kullanıcının tek bir cümlesindeki birden fazla isteği (niyeti) ayrıştırıp, bunları mantıklı bir sırayla planlayıp gerçekleştirmesini sağlamak.

**Örnek 5.1:**
```json
{
  "id": "MI-001",
  "senaryo": "Multi-Intent - Hem arıza kaydı oluştur hem de fatura bilgisi sor",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "İnternetim çok yavaş, bir arıza kaydı açalım. Ayrıca son faturam ne kadar geldi? Müşteri no: 7477."
    },
    {
      "rol": "asistan",
      "icerik": "Elbette, 7477 numaralı hesabınız için her iki talebinizi de hemen işleme alıyorum. Öncelikle yavaş internet sorununuz için bir arıza kaydı oluşturalım."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "create_fault_ticket",
          "parametreler": {
            "user_id": 7477,
            "issue_description": "İnternet hızı çok yavaş.",
            "category": "internet_speed",
            "priority": "medium"
          }
      }]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"ticket_id\": \"T-2024-001235\", \"status\": \"open\"}}"
    },
    {
      "rol": "asistan",
      "icerik": "İnternet yavaşlığıyla ilgili arıza kaydınız T-2024-001235 numarasıyla oluşturulmuştur. Teknik ekibimiz en kısa sürede inceleyecektir. Şimdi de son fatura tutarınızı kontrol ediyorum."
    },
    {
      "rol": "asistan",
      "icerik": null,
      "arac_cagrilari": [{
          "fonksiyon": "get_current_bill",
          "parametreler": { "user_id": 7477 }
      }]
    },
    {
      "rol": "arac",
      "icerik": "{\"success\": true, \"data\": {\"amount\": 95.80, \"status\": \"paid\"}}"
    },
    {
      "rol": "asistan",
      "icerik": "Son fatura tutarınız 95.80 TL olup, ödenmiş olarak görünmektedir. Başka bir isteğiniz var mı?"
    }
  ]
}
```

---

### Strateji 6: Doğal Sohbet ve Araçsız Yanıt (Natural & Tool-Free)

**Amaç:** Modelin, her soruya bir API ile cevap vermesi gerekmediğini öğrenmesini sağlamak. Genel bilgi, sohbeti yönlendirme veya basit teyitler için araç kullanmadan, doğal bir dil ile cevap üretmelidir.

**Örnek 6.1:**
```json
{
  "id": "NC-001",
  "senaryo": "Natural Chit-Chat - Genel soruya sohbet ile cevap",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "Bu faturalar neden hep bu kadar karışık oluyor?"
    },
    {
      "rol": "asistan",
      "icerik": "Fatura detaylarının bazen kafa karıştırıcı olabildiğinin farkındayım. Genellikle ana hizmet bedeli, vergiler ve ek kullanımlar gibi birden fazla kalem içerdiği için karmaşık görünebilir. Faturanızda anlamadığınız belirli bir kısım varsa, açıklamak için yardımcı olabilirim."
    }
  ]
}
```

**Örnek 6.2:**
```json
{
  "id": "NC-002",
  "senaryo": "Natural Chit-Chat - İşlem sonrası kapanış diyaloğu",
  "donguler": [
    {
      "rol": "kullanici",
      "icerik": "Teşekkür ederim, sorunum çözüldü."
    },
    {
      "rol": "asistan",
      "icerik": "Rica ederim, yardımcı olabildiğime sevindim! Telekom'u tercih ettiğiniz için teşekkür ederiz. Başka bir konuda yardıma ihtiyacınız olursa çekinmeden tekrar ulaşabilirsiniz. İyi günler dilerim!"
    }
  ]
}
``` 