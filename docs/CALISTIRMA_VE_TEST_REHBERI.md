# Projeyi Çalıştırma ve Test Etme Rehberi

Bu doküman, her ekibin kendi sorumlu olduğu proje bölümünü lokal bilgisayarında nasıl çalıştıracağını ve test edeceğini adım adım açıklar.

**Ön Koşul:** Bilgisayarınızda [Python](https://www.python.org/downloads/) ve [Visual Studio Code](https://code.visualstudio.com/) kurulu olmalıdır.

---

## Genel Kurulum (Herkes için)

Projenin bağımlılıklarını yönetmek için her zaman bir sanal ortam (virtual environment) kullanacağız. Bu, sisteminizin genel Python kurulumunu temiz tutar.

1.  **Projeyi Klonla:** `GIT_VE_IS_AKISI_REHBERI.md` dokümanındaki adımları izleyerek projeyi bilgisayarınıza klonlayın.
2.  **VS Code'da Aç:** Proje klasörünü VS Code ile açın.
3.  **Terminali Aç:** VS Code içinde `Ctrl + Shift + ~` tuşlarına basarak yeni bir terminal açın.
4.  **Sanal Ortam Oluştur:** Terminalde aşağıdaki komutu çalıştırın. Bu, `.venv` adında bir sanal ortam klasörü oluşturacaktır.
    ```bash
    python -m venv .venv
    ```
5.  **Sanal Ortamı Aktif Et:**
    *   **Windows (PowerShell/CMD):**
        ```powershell
        .venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    Aktif olduğunda, terminal satırının başında `(.venv)` ifadesini göreceksiniz.
6.  **Bağımlılıkları Yükle:** Projenin ana dizinindeki `requirements.txt` dosyasında yer alan tüm kütüphaneleri yükleyin.
    ```bash
    pip install -r requirements.txt
    ```

---

## 1. Frontend (Streamlit) Projesini Çalıştırma

**Sorumlular:** Nisa, Mustafa

1.  Yukarıdaki genel kurulum adımlarını tamamladığınızdan emin olun.
2.  Terminalin hala proje ana dizininde (`/UniqueAi`) olduğundan emin olun.
3.  Aşağıdaki komutu çalıştırın:
    ```bash
    streamlit run frontend/app.py
    ```
4.  Komut, otomatik olarak varsayılan web tarayıcınızda yeni bir sekme açacak ve uygulamayı size gösterecektir. (Genellikle `http://localhost:8501`).
5.  Kodda bir değişiklik yapıp kaydettiğinizde, Streamlit arayüzü size sağ üstte "Source file changed" uyarısı verir ve yeniden çalıştırma seçeneği sunar.

---

## 2. Backend (FastAPI) Projesini Çalıştırma

**Sorumlular:** Enes, Sedat

1.  Genel kurulum adımlarını tamamladığınızdan emin olun.
2.  Backend sunucusunu `hot-reload` (otomatik yeniden başlatma) özelliği ile başlatmak için aşağıdaki komutu çalıştırın. Bu sayede kodda yaptığınız her değişiklik sonrası sunucu kendini yeniden başlatır.
    ```bash
    uvicorn backend.app.main:app --reload
    ```
3.  Sunucu `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.
4.  **Test Etme:**
    *   **Health Check:** Tarayıcınızda `http://127.0.0.1:8000/api/v1/health` adresine gidin. `{"status":"ok"}` mesajını görüyorsanız, sunucu çalışıyor demektir.
    *   **API Dokümantasyonu:** Tarayıcınızda `http://127.0.0.1:8000/docs` adresine gidin. FastAPI'nin otomatik oluşturduğu interaktif API dokümanını (Swagger UI) göreceksiniz. Buradan tüm endpoint'leri görebilir ve doğrudan test edebilirsiniz.

---

## 3. AI/ML (Script'ler) Çalıştırma

**Sorumlular:** Nazif, Ziişan, Erkan

1.  Genel kurulum adımlarını tamamladığınızdan emin olun. AI/ML için ek, büyük kütüphaneler yüklenecektir.
2.  AI/ML script'leri genellikle doğrudan çalıştırılan Python dosyalarıdır.
3.  **Örnek (Fine-tuning script'ini çalıştırmak için):**
    *   *Not: Gerçek fine-tuning işlemi, güçlü bir GPU (tercihen NVIDIA) gerektirir ve saatler sürebilir. Bu adımlar, script'in çalışıp çalışmadığını test etmek içindir.*
    *   Terminalde aşağıdaki komutu çalıştırın:
        ```bash
        python ai_model/scripts/run_finetune.py
        ```
4.  Script, adımları konsola basarak çalışacaktır. Başlangıçta, veri seti yolu veya diğer konfigürasyonlar eksik olduğu için hata verebilir. Göreviniz, bu script'i `PROJE_YONETIM_DOKUMANI.md`'deki görevlere göre doldurmak ve çalışır hale getirmektir. 