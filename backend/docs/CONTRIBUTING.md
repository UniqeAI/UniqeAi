# UniqueAi Projesine Katkıda Bulunma Rehberi

Projeye katkıda bulunan herkese teşekkür ederiz! Bu doküman, geliştirme sürecini tutarlı ve verimli hale getirmek için uymamız gereken kuralları özetlemektedir.

---

## 1. İletişim

*   Tüm proje tartışmaları için **Slack** kullanıyoruz. Lütfen ilgili kanalları kullanın.
*   Detaylar için `docs/PROJE_ILETISIM_VE_ARACLAR.md` dosyasına bakın.

## 2. Görev Takibi

*   Görevlerimiz **GitHub Projects** üzerindeki Kanban tahtasında yönetilmektedir.
*   Bir göreve başlamadan önce kartı `In Progress` sütununa çekin.

## 3. Geliştirme İş Akışı

*   Projeye her yeni katkı, `feature` branch'i üzerinden yapılmalıdır.
*   İşe başlamadan önce **her zaman** `develop` branch'ini güncelleyin (`pull`).
*   İşiniz bittiğinde, `develop` branch'ine bir **Pull Request (PR)** açın.
*   Detaylı adımlar için `docs/GIT_VE_IS_AKISI_REHBERI.md` dosyasına bakın.

---

## 4. Kodlama Standartları

Proje genelinde temiz ve okunabilir bir kod yapısı sağlamak için tüm Python kodları **Black** kod formatlayıcısı ile formatlanmalıdır.

### Black Kurulumu ve Kullanımı

1.  **Kurulum:** Henüz yapmadıysanız, projenin sanal ortamı (`.venv`) aktifken Black'i kurun:
    ```bash
    pip install black
    ```
2.  **Kullanım:** Kodunuzu commit'lemeden hemen önce, projenin ana dizinindeyken terminalde aşağıdaki komutu çalıştırın. Bu komut, projedeki tüm `.py` dosyalarını otomatik olarak standart formata getirecektir.
    ```bash
    black .
    ```
3.  **VS Code Entegrasyonu (Tavsiye Edilir):**
    *   VS Code'da Python eklentisinin kurulu olduğundan emin olun.
    *   `Ctrl + Shift + P` ile komut paletini açın ve `Preferences: Open User Settings (JSON)` seçeneğini aratıp açın.
    *   Aşağıdaki ayarları ekleyin. Bu, her Python dosyasını kaydettiğinizde Black'in otomatik olarak çalışmasını sağlar.
        ```json
        {
            "python.formatting.provider": "black",
            "[python]": {
                "editor.formatOnSave": true
            }
        }
        ```

## 5. Pull Request (PR) Kuralları

*   PR başlığınız, yaptığınız değişikliği net bir şekilde özetlemelidir (Örn: "Feat: Kullanıcı giriş arayüzü eklendi").
*   PR açıklamasına, eğer varsa, ilgili GitHub Projects kartının linkini ekleyin.
*   PR'ınızı açtıktan sonra, kodunuzu incelemesi için Slack'teki ilgili kanaldan ekibinize haber verin. 