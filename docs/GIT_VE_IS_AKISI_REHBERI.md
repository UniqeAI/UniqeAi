# Git ve GitHub İş Akışı Rehberi (VS Code ile)

Bu rehber, Git ve GitHub'ı hiç kullanmamış bir ekip üyesinin projeye nasıl katkı sağlayacağını adım adım anlatır. Tüm işlemler Visual Studio Code (VS Code) üzerinden yapılacaktır.

---

### Temel Kavramlar

*   **Repository (Repo):** Projemizin tüm dosyalarının ve geçmişinin saklandığı yer. (GitHub'daki `agent-llama` projesi).
*   **Commit:** Kodda yaptığın bir grup değişikliği "kaydetme" işlemidir. Her commit'in bir mesajı olur (Örn: "Giriş sayfası butonu eklendi").
*   **Branch (Dal):** Projenin ana kodundan ayrılan bir kopyasıdır. Yeni bir özellik geliştirirken ana koda zarar vermeden güvenli bir alanda çalışmanı sağlar. Bizim ana dallarımız `main` ve `develop` olacak.
*   **Push:** Kendi bilgisayarında yaptığın commit'leri GitHub'daki ortak repoya gönderme işlemidir.
*   **Pull:** Diğerlerinin yaptığı ve GitHub'a gönderdiği değişiklikleri kendi bilgisayarına çekme işlemidir.
*   **Pull Request (PR):** Kendi `feature` branch'inde tamamladığın bir işi, `develop` branch'ine eklenmesi için yaptığın "birleştirme talebi"dir. Bu, kodunun başkaları tarafından incelenmesini (code review) sağlar.

---

### Adım Adım Geliştirme Süreci (Her Yeni Görev İçin)

Tüm bu adımları VS Code'un sol tarafındaki **Source Control** (kaynak kontrolü) sekmesinden (üç noktanın birleştiği ikon) kolayca yapabilirsin.

**1. Projeyi Bilgisayarına Klonla (Sadece ilk başta bir kere)**
*   GitHub'daki `UniqueAi` projesine git.
*   Yeşil `<> Code` butonuna tıkla ve HTTPS linkini kopyala.
*   VS Code'u aç, `Ctrl+Shift+P` ile komut paletini aç ve `Git: Clone` yaz.
*   Kopyaladığın linki yapıştır ve projeyi bilgisayarında kaydetmek istediğin yeri seç.

**2. Her Zaman Güncel Kal**
*   İşe başlamadan önce **her zaman** `develop` branch'ine geç.
    *   VS Code'un sol alt köşesindeki branch ismine tıkla ve listeden `origin/develop` seç.
*   En son değişiklikleri al.
    *   Source Control panelinde, üç noktaya (...) tıkla ve `Pull` komutunu çalıştır.

**3. Yeni Görevin İçin Branch Oluştur**
*   Şimdi `develop` branch'inin en güncel halindesin.
*   VS Code'un sol alt köşesindeki `develop` yazan yere tıkla.
*   Yukarıda açılan menüden `+ Create new branch...` seçeneğine tıkla.
*   Branch'ine kurala uygun bir isim ver: `feature/ekip-adi/gorev-adi`
    *   Örnek: `feature/frontend/login-arayuzu`
    *   Örnek: `feature/backend/kullanici-endpoint`

**4. Kodunu Yaz ve Değişiklikleri Kaydet (Commit)**
*   Artık kendi güvenli dalındasın. Kodunu yaz, dosyaları oluştur.
*   Yaptığın değişiklikler sol taraftaki Source Control panelinde "Changes" altında listelenir.
*   Anlamlı bir bütün oluşturan değişiklikleri kaydetmek için:
    *   Değişikliklerin yanındaki `+` (Stage Changes) ikonuna basarak onları "hazırlık alanına" al.
    *   Yukarıdaki mesaj kutusuna bu değişikliği özetleyen bir commit mesajı yaz (Örn: "Kullanıcı adı ve şifre inputları eklendi").
    *   `Commit` butonuna bas.

**5. Değişikliklerini GitHub'a Gönder (Push)**
*   Commit'lerin hala senin bilgisayarında. Ekibin görmesi için GitHub'a göndermelisin.
*   Source Control panelindeki `Publish Branch` veya `Sync Changes` butonuna bas. Bu, hem `push` hem `pull` yapar.

**6. Pull Request (PR) Aç**
*   İşin bittiğinde, branch'ini `develop` ile birleştirmek için bir talep oluşturmalısın.
*   GitHub.com'daki `UniqueAi` reposuna git. Genellikle "You have recently pushed branches" uyarısı ve yanında bir `Compare & pull request` butonu görürsün. Ona tıkla.
*   Açılan sayfada başlık ve açıklama yazarak PR'ını oluştur. Sağ taraftan "Reviewers" kısmına ekip arkadaşlarını ekle.
*   Ekip arkadaşların kodunu inceleyip onayladıktan sonra, Proje Yöneticisi bu talebi `develop` branch'ine birleştirecektir.

**7. Temizlik**
*   PR'ın birleştirildikten sonra tekrar **Adım 2**'ye dönerek `develop` branch'ine geçip `pull` yaparak projeyi güncelleyebilir ve yeni görevine başlayabilirsin. 