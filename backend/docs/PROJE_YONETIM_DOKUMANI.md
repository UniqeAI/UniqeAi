# UniqueAi (Agent-Llama): Proje Yönetim ve Geliştirme Dokümanı

Bu doküman, "UniqueAi (Agent-Llama)" projesinin teknik yapısını, takım rollerini, geliştirme süreçlerini ve yol haritasını tanımlar. Tüm ekip üyelerinin bu dokümanı dikkatlice okuması ve geliştirme süreçlerinde referans alması beklenmektedir.

---

## 1. Proje Yapısı ve Versiyon Kontrolü

Projemiz, tüm kod tabanını tek bir repository altında toplayan **Monorepo** yapısını benimseyecektir. Bu yaklaşım, bileşenler arası entegrasyonu ve bağımlılık yönetimini kolaylaştıracaktır.

### 1.1. Dizin Yapısı

```
UniqueAi/
├── .github/              # GitHub Actions (CI/CD) konfigürasyonları
│   └── workflows/
├── ai_model/             # Yapay zeka modeli, fine-tuning scriptleri, sentetik veri
│   ├── data/
│   │   └── synthetic_data.jsonl
│   ├── notebooks/        # Keşif amaçlı Jupyter notebook'ları
│   └── scripts/          # Fine-tuning, inference ve Zemberek entegrasyon scriptleri
├── backend/              # FastAPI sunucusu
│   ├── app/
│   │   ├── api/          # API endpoint'leri
│   │   ├── core/         # Konfigürasyon, ayarlar
│   │   ├── services/     # Mock API'ler ve iş mantığı
│   │   └── schemas/      # Pydantic modelleri
│   ├── tests/            # Backend testleri
│   └── Dockerfile
├── frontend/             # Streamlit arayüzü
│   ├── assets/           # Resimler, CSS dosyaları
│   ├── components/       # Arayüz bileşenleri (giriş, sohbet ekranı vb.)
│   └── app.py            # Ana Streamlit uygulaması
├── docs/                 # Proje dokümantasyonu
│   └── PROJE_YONETIM_DOKUMANI.md
├── .gitignore
└── README.md
```

### 1.2. GitHub Akışı (Git Flow)

1.  **`main` Branch'i:** Her zaman stabil ve dağıtıma hazır kodu içerir. Doğrudan commit atılmaz.
2.  **`develop` Branch'i:** Geliştirme ortamını temsil eder. Tamamlanan `feature` branch'leri buraya birleştirilir.
3.  **`feature/*` Branch'leri:** Her yeni görev veya özellik için `develop` branch'inden yeni bir branch oluşturulur.
    *   **İsimlendirme Kuralı:** `feature/<ekip>/<gorev-aciklamasi>`
    *   **Örnek:** `feature/frontend/login-page`, `feature/backend/auth-endpoints`, `feature/ai/synthetic-data-generator`
4.  **Pull Request (PR):** Bir `feature` tamamlandığında, `develop` branch'ine birleştirilmek üzere Pull Request açılır. PR, en az bir ekip üyesi tarafından incelenip onaylandıktan sonra birleştirilir.

---

## 2. Takım Rolleri ve Teknolojiler

| Alan | Sorumlular | Teknolojiler |
| :--- | :--- | :--- |
| **Proje Yönetimi & DevOps** | Erkan | GitHub, GitHub Actions, Docker |
| **Frontend** | Nisa, Mustafa | Streamlit, Python |
| **Backend** | Enes, Sedat | FastAPI, Python, Pydantic, Docker |
| **AI / ML** | Nazif, Ziişan, Erkan | PyTorch, Hugging Face Transformers, Llama 3.1, Zemberek |

---

## 3. Backend Mimarisi ve Geliştirme Önceliği

Bu bölümde, projemizdeki API kavramını ve geliştirme sırasını netleştireceğiz.

### Mock API vs. Gerçek API

Projemizde, gerçek bir telekom şirketinin veritabanlarına bağlanan bir **"Gerçek API" olmayacaktır.** Bizim amacımız, böyle bir API'yi kullanabilen bir yapay zeka ajanı geliştirmektir.

Bu nedenle, bizim **FastAPI Backend projemiz, aslında dev bir Mock API (Simülasyon API'si) görevi görür.** İçerisinde, sanki gerçek bir sisteme bağlanıyormuş gibi davranan ama aslında önceden tanımlanmış, sahte (ama gerçekçi) veriler döndüren fonksiyonlar barındırır. Bu fonksiyon setine projemizin **"Araç Kutusu" (Toolbox)** adını veriyoruz.

### Geliştirme Önceliği ve İş Akışı

1.  **ÖNCELİK 1: Backend Ekibi - Araç Kutusunu Oluşturma:** Projenin başlangıcındaki en kritik görev, Backend ekibinin aşağıda belirtilen temel araç (fonksiyon) setini `backend/app/services/mock_tools.py` gibi bir modülde oluşturmasıdır.
2.  **ÖNCELİK 2: AI/ML Ekibi - Sentetik Veri Üretimi:** Backend ekibi bu araçların listesini ve nasıl çalıştığını yayınladıktan sonra, AI/ML ekibi bu araçları kullanarak yapay zekayı eğitecek olan sentetik veriyi üretmeye başlayabilir.
3.  **PARALEL GÖREV: Frontend Ekibi:** Bu sırada Frontend ekibi, arayüz bileşenlerini ve temel sayfa akışını geliştirmeye devam edebilir.

### İlk Geliştirilecek Araç Kutusu (Mock API Fonksiyonları)

| Fonksiyon Adı | Parametreler | Örnek Yanıt |
| :--- | :--- | :--- |
| `getUserInfo` | `user_id: int` | `{"name": "...", "package": "..."}` |
| `getAvailablePackages` | `None` | `[{"name": "...", "price": "...", "speed": "..."}]` |
| `initiatePackageChange` | `user_id: int`, `new_package_name: str` | `{"status": "success", "message": "..."}` |
| `getComplaintStatus` | `complaint_id: str` | `{"status": "in_progress", "details": "..."}` |
| `createComplaint` | `user_id: int`, `complaint_text: str` | `{"status": "success", "complaint_id": "..."}` |

---

## 4. Genel Proje Yol Haritası (Taslak)

-   **Sprint 0 (1. Hafta):** Kurulum, Temel Yapıların Oluşturulması ve **Mock API'nin ilk versiyonunun tamamlanması.**
-   **Sprint 1 (2. Hafta):** Temel Fonksiyonların Geliştirilmesi (Kullanıcı Doğrulama, Sohbet Akışı).
-   **Sprint 2 (3. Hafta):** Yapay Zeka Modelinin İnce Ayarı (Fine-Tuning) ve Entegrasyonu.
-   **Sprint 3 (4. Hafta):** Uçtan Uca Test, Hata Ayıklama ve Performans İyileştirmeleri.
-   **Sprint 4 (5. Hafta):** Final Sunum Hazırlığı, Dokümantasyonun Tamamlanması.

---

## 4. İlk Hafta (Sprint 0) Görev Dağılımı (5 Gün)

Tüm ekiplerin paralel olarak çalışmaya başlaması için ilk 5 günlük görevler aşağıda tanımlanmıştır.

### **Görev: Proje Yönetimi & DevOps (Erkan)**
*   **Gün 1:** GitHub üzerinde `UniqueAi` repository'sini oluşturmak ve yarışma gereksinimlerini karşılamak.
    *   Depoyu (Repository) GitHub ayarlarından **Public** olarak ayarlamak.
    *   Oluşturulan `LICENSE` ve `.gitignore` dosyalarını ilk commit ile repoya eklemek.
    *   `main` ve `develop` branch'lerini yaratıp `main` branch'ini korumalı hale getirmek (Doğrudan commit atılmasını engellemek).
*   **Gün 2:** Yukarıda tanımlanan `Dizin Yapısı`'nı ana hatlarıyla oluşturup `develop` branch'ine push'lamak. Boş `__init__.py` dosyalarını ekleyerek Python modül yapısını hazırlamak.
*   **Gün 3:** Temel bir `README.md` ve bu `PROJE_YONETIM_DOKUMANI.md` dosyasını `docs/` dizinine eklemek.
*   **Gün 4:** Proje için bir `requirements.txt` dosyası oluşturmak ve temel bağımlılıkları (fastapi, uvicorn, streamlit, transformers, torch, zemberek-python) eklemek.
*   **Gün 5:** Ekip için bir iletişim kanalı (Discord/Slack) kurmak ve tüm ekibi davet etmek. Haftalık kısa bir toplantı (daily stand-up) organize etmek.

### **Görev: Frontend Ekibi (Nisa, Mustafa)**
*   **Gün 1:** Lokal geliştirme ortamını kurmak (Python, Streamlit). Boş bir Streamlit projesi oluşturup "Merhaba Agent-Llama" yazdırarak çalıştığını teyit etmek.
*   **Gün 2:** `components` dizini altında `login_screen.py` ve `chat_screen.py` adında iki modül oluşturmak.
*   **Gün 3:** `login_screen.py` içinde kullanıcı adı ve şifre için basit bir giriş formu tasarlamak (sadece arayüz, işlevsellik olmadan).
*   **Gün 4:** `chat_screen.py` içinde bir mesajlaşma arayüzü taslağı oluşturmak: Altta bir metin giriş kutusu ve gönder butonu, üstte ise mesajların gösterileceği bir alan.
*   **Gün 5:** `app.py` ana dosyasında, durum yönetimi (session state) kullanarak giriş yapıldıysa sohbet ekranını, yapılmadıysa giriş ekranını gösteren temel bir mantık kurmak.

### **Görev: Backend Ekibi (Enes, Sedat)**
*   **Gün 1:** Lokal geliştirme ortamını kurmak (Python, FastAPI, Uvicorn). `backend/` dizini altında temel bir FastAPI uygulaması oluşturmak.
*   **Gün 2:** `/api/v1/health` adında bir endpoint oluşturmak. Bu endpoint `{"status": "ok"}` JSON yanıtı dönmeli. Bu, sunucunun ayakta olduğunu test etmek için kullanılacak.
*   **Gün 3:** Şartnamede geçen `getUserInfo`, `getAvailablePackages` gibi fonksiyonları simüle edecek mock fonksiyonları `services/mock_tools.py` içinde oluşturmak. Bu fonksiyonlar şimdilik sabit (hard-coded) veriler dönebilir.
*   **Gün 4:** `/api/v1/chat` adında bir POST endpoint'i için Pydantic şemalarını (`schemas/chat.py`) ve API endpoint tanımını (`api/v1/chat.py`) oluşturmak. Endpoint, kullanıcı mesajını alıp şimdilik sabit bir yanıt dönmelidir.
*   **Gün 5:** Backend projesi için temel bir `Dockerfile` hazırlamak.

### **Görev: AI / ML Ekibi (Nazif, Ziişan, Erkan)**
*   **Gün 1:** Gerekli kütüphaneleri (transformers, torch, accelerate, bitsandbytes) kurarak `meta-llama/Llama-3.1-8B-Instruct` modelini indirip lokalde bir inference (çıkarım) testi yapmak. Modele basit bir soru sorup yanıt alabildiğinizi teyit edin.
*   **Gün 2:** Fine-tuning için kullanılacak sentetik verinin yapısını tasarlamak. Her bir veri noktası `{"instruction": "...", "input": "...", "output": "<tool_code>print(backend_api.some_function(...))</tool_code>"}` formatında olacak şekilde bir JSON yapısı belirlemek.
*   **Gün 3:** Backend ekibinin `services/mock_tools.py` içinde tanımladığı mock araçları temel alarak, **10-15 adet** örnek sentetik veri manuel olarak oluşturmak ve `ai_model/data/synthetic_data.jsonl` dosyasına kaydetmek. **Not:** Bu görev, backend kodu yazmak değil, backend'in araçlarını nasıl çağıracağını modele öğretmek için örnek diyaloglar ve komutlar oluşturmaktır.
*   **Gün 4:** Zemberek kütüphanesini kurmak. Gelen bir kullanıcı girdisini (ör: "İnternetimin hızını yükseltmek istiyorum.") Zemberek ile normalize edip köklerine ayıracak basit bir test script'i yazmak.
*   **Gün 5:** Llama 3.1 için Hugging Face TRL (Transformer Reinforcement Learning) kütüphanesini kullanarak bir fine-tuning iskelet script'i (`scripts/run_finetune.py`) oluşturmaya başlamak. Script sadece veri yükleme ve model hazırlama adımlarını içerebilir. 