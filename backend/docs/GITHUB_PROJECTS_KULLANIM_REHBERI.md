# GitHub Projects ve Görev Yönetimi Kullanım Rehberi

Bu rehber, projemizdeki görevleri (task/issue) yönetmek ve takım içi iş akışını standartlaştırmak için GitHub Projects ve Issues özelliklerini nasıl kullanacağımızı açıklar. Tüm ekibin bu kurallara uyması, projenin şeffaf ve düzenli ilerlemesi için kritik öneme sahiptir.

## Altın Kural: Tek Proje Panosu (Single Project Board)

Tüm proje `frontend`, `backend` ve `ai-model` işleri için **TEK BİR** proje panosu kullanılacaktır. İşleri birbirinden ayırmak için panoları değil, **Etiketleri (Labels)** kullanacağız. Bu, herkesin projenin genel durumunu tek bir yerden görmesini sağlar ve ekipler arası koordinasyonu kolaylaştırır.

## İş Akışı: Fikirden Tamamlanmış Göreve

Her iş, aşağıdaki 4 adımlık döngüyü takip etmelidir:

### Adım 1: Görev (Issue) Oluşturma

Yapılması gereken her yeni iş, bir hata (`bug`) veya yeni bir özellik (`feature`) mutlaka bir **Issue** olarak oluşturulmalıdır.

1.  Projenin ana sayfasındaki **"Issues"** sekmesine gidin.
2.  Yeşil renkli **"New issue"** butonuna tıklayın.
3.  **Başlık (Title):** Görevi net bir şekilde özetleyen bir başlık yazın.
    *   **Kötü:** *Login Butonu*
    *   **İyi:** *Kullanıcı Giriş Sayfası için Login Butonu Fonksiyonelliği*
4.  **Açıklama (Leave a comment):** Görevle ilgili tüm detayları, gereksinimleri ve varsa ilgili belgeleri buraya yazın.

### Adım 2: Görevi Yapılandırma ve Atama (En Önemli Adım!)

Bir `Issue` oluşturduktan sonra, sağ taraftaki menüyü kullanarak görevi yapılandırmalısınız:

1.  **Assignees (Atananlar):** Bu görevi kimin yapacağını buradan seçin. Bir görev **asla** atanmamış (`unassigned`) bırakılmamalıdır.
2.  **Labels (Etiketler):** Görevi kategorize etmek için uygun etiketleri seçin. Bir görevin birden fazla etiketi olabilir.
    *   **Alan Etiketleri:** `frontend`, `backend`, `ai-model`, `docs`
    *   **Tür Etiketleri:** `bug` (hata), `feature` (yeni özellik), `enhancement` (iyileştirme), `documentation` (dokümantasyon)
3.  **Projects (Projeler):** Görevin proje panomuzda görünmesi için buradan ana proje panomuzu (`TDDI Proje Panosu` gibi) seçin. **Bu adım atlanırsa, görev panoda görünmez!**

Bu adımlardan sonra **"Submit new issue"** diyerek görevi oluşturun.

### Adım 3: Proje Panosunu (Kanban) Kullanma

Proje panosuna **"Projects"** sekmesinden ulaşabilirsiniz. Panomuzda 3 ana sütun bulunur:

*   **To Do (Yapılacaklar):** Oluşturulan ve atanan tüm yeni görevler otomatik olarak bu sütuna düşer. Bu, sıradaki işleri gösterir.
*   **In Progress (Yapılıyor):** Bir göreve başladığınızda, yapmanız gereken ilk şey kartınızı bu sütuna sürüklemektir. Böylece tüm ekip, sizin o anda ne üzerinde çalıştığınızı bilir.
*   **Done (Tamamlandı):** Görevle ilgili kodunuzu yazıp `pull request` (PR) açtıktan ve PR'ınız ana dala (`main` veya `develop`) birleştirildikten sonra, kartınızı bu sütuna taşıyın.

### Özet Akış (TL;DR)

**Fikir/İhtiyaç** -> **Issue Oluştur** -> **Ata, Etiketle, Projeye Ekle** -> **Panoda "In Progress"e Çek** -> **İşi Bitirince "Done"a Çek**

Bu basit kurallara uyarak projemizi çok daha verimli ve düzenli bir şekilde yönetebiliriz. 