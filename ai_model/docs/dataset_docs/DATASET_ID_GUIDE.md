# Eğitim Veri Seti Kimliklendirme (ID) Rehberi

## 1. Giriş: ID (Kimlik) Nedir ve Neden Kullanılır?

Oluşturduğumuz her bir diyalog örneğinin başında yer alan `id` alanı (`"TC-001"`, `"DA-002"` gibi), o diyalog örneğinin **benzersiz kimlik kartıdır**. Bu kimlikler rastgele verilmemiştir; veri setini organize etmek, analiz etmek ve stratejik olarak yönetmek için tasarlanmış anlamlı bir kodlama sistemi içerirler.

Bu sistem, binlerce diyalog arasında kaybolmamızı engeller ve veri setimizi rastgele bir yığından, yönetilebilir ve ölçülebilir bir varlığa dönüştürür.

## 2. ID Yapısı: Anlamlı Kodlama

Her bir ID, iki ana bölümden oluşur: `[STRATEJİ_KODU]-[SIRA_NUMARASI]`

**Örnek:** `PA-001`
*   **`PA`**: Strateji kodudur. Bu örneğin "Proaktif Yardım" (Proactive Assistance) stratejisine ait olduğunu belirtir.
*   **`001`**: Sıra numarasıdır. Bu örneğin, Proaktif Yardım stratejisi için oluşturulan ilk örnek olduğunu gösterir.

### Strateji Kodları Tablosu

Veri üretirken veya analiz ederken aşağıdaki kodları kullanmalısınız:

| Strateji Kodu | İngilizce Karşılığı      | Türkçe Açıklaması                                |
|---------------|--------------------------|--------------------------------------------------|
| `TC`          | Tool Chaining            | **Zincirleme Araç Kullanımı:** Bir işlemin çıktısını diğerinde kullanma. |
| `DA`          | Disambiguation           | **Belirsizliği Giderme:** Eksik bilgiyi netleştirmek için soru sorma.     |
| `PA`          | Proactive Assistance     | **Proaktif Yardım:** Kullanıcının ihtiyacını tahmin edip öneri sunma.   |
| `EH`          | Error Handling           | **Hata Yönetimi:** API'dan dönen hataları anlayıp çözüm önerme.        |
| `MI`          | Multi-Intent             | **Çok Niyetli Görevler:** Tek cümlede birden fazla isteği karşılama.     |
| `NC`          | Natural Chit-Chat        | **Doğal Sohbet:** Araç kullanmadan yapılan genel sohbetler.          |

## 3. Stratejik Avantajlar: Bu Sistem Bize Ne Kazandırır?

Bu basit görünen kimliklendirme sistemi, projenin başarısı için kritik öneme sahip 4 temel avantaj sunar:

### a. Hata Analizi ve Model Zayıflıklarını Giderme
Modeliniz canlıya alındığında veya test aşamasında belirli türde hatalar yaptığını fark edebilirsiniz. Örneğin, modelin API hatalarını yönetmekte zorlandığını düşünelim.

*   **Ne Yaparsınız?** Eğitim verisi içinde `EH-` ile başlayan tüm diyalogları anında filtreleyebilirsiniz.
*   **Sonuç:** Bu verilerin sayısının az mı olduğunu, formatlarının yanlış mı olduğunu veya senaryoların yeterince çeşitli mi olmadığını hızla analiz edebilir ve sorunu kökünden çözmek için doğrudan o kategoriye yönelik yeni veriler üretebilirsiniz.

### b. Dengeli ve Kaliteli Veri Seti
İyi bir yapay zeka, her yetenekte dengeli bir şekilde eğitilmelidir.

*   **Ne Yaparsınız?** Basit bir script ile her bir strateji kodundan (`TC-`, `DA-`, `PA-` vb.) kaçar adet örnek olduğunu sayabilirsiniz.
*   **Sonuç:** "Modelimiz zincirleme araç kullanımında (`TC`) çok iyiyken, belirsizliği gidermede (`DA`) zayıf kalıyor. Çünkü elimizde 5000 `TC` örneğine karşılık sadece 300 `DA` örneği var." gibi somut, veriye dayalı kararlar alarak eğitiminizi dengeleyebilirsiniz.

### c. Tam Takip Edilebilirlik
Binlerce satırlık JSON dosyası içinde belirli bir diyaloğu bulmak imkansızdır.

*   **Ne Yaparsınız?** "Şu `MI-042` numaralı örnekte bir sorun var." dediğinizde, herkesin tam olarak hangi diyalogdan bahsettiği net olur.
*   **Sonuç:** Hataları ayıklamak, belirli örnekleri gözden geçirmek veya bir senaryoyu güncellemek saniyeler sürer.

### d. Organize ve Verimli Ekip Çalışması
Veri üretimi, takım çalışması gerektiren bir süreçtir.

*   **Ne Yaparsınız?** Veri üretme görevini ekip üyeleri arasında kolayca paylaştırabilirsiniz. Örnek:
    *   "Ali, sen `TC-1000`'den `TC-2000`'e kadar olan senaryoları oluştur."
    *   "Ayşe, sen `PA-500`'den `PA-1000`'e kadar olanları devral."
*   **Sonuç:** Herkes ne yapacağını bilir, görevler çakışmaz ve veri üretim süreci son derece organize ve verimli bir şekilde ilerler. 