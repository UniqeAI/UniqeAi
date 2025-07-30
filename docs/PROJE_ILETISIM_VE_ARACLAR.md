# Proje İletişim ve Görev Yönetim Araçları

Bu doküman, UniqueAi projesinde kullanılacak olan iletişim ve görev yönetimi araçlarını ve kurallarını belirtir.

---

## 1. İletişim Platformu: Slack

Tüm ekip içi anlık iletişim için **Slack** kullanılacaktır. WhatsApp grupları proje tartışmaları için kullanılmayacaktır. Slack, profesyonel ekipler için tasarlanmış, konu bazlı kanallar oluşturmaya olanak tanıyan güçlü bir araçtır.

### Slack Çalışma Alanı Yapısı (Örnek)

*   **Kanallar (Channels):**
    *   `#genel`: Proje dışı sohbet ve genel konular.
    *   `#duyurular`: Proje yöneticisi tarafından yapılacak önemli duyurular.
    *   `#frontend`: Frontend ekibinin kendi arasındaki tartışmaları, soruları ve kod paylaşımları.
    *   `#backend`: Backend ekibinin kendi arasındaki tartışmaları, soruları ve kod paylaşımları.
    *   `#ai-ml`: Yapay zeka ekibinin kendi arasındaki tartışmaları, soruları ve kod paylaşımları.
    *   `#github-log`: Pull Request'ler, commit'ler ve branch'ler ile ilgili otomatik bildirimler için (Slack-GitHub entegrasyonu ile).
*   **İş Akışı:**
    *   Bir soru sorarken, konunun geçtiği kanalda sorun.
    *   Kod paylaşırken mutlaka kod bloğu (` ``` `) kullanın.
    *   Tartışmaları ilgili kanal altında "thread" (konu başlığı) olarak sürdürerek kanal kirliliğini önleyin.

### Kurallar
1.  Teknik bir soru sorarken, ilgili kod bloğunu ve hatayı mutlaka paylaşın.
2.  Acil olmayan konular için ilgili kişiyi `@mention` ile etiketlemekten çekinmeyin.
3.  Tüm önemli kararlar ve duyurular `#duyurular` kanalından takip edilmelidir.

---

## 2. Görev Yönetim Aracı: GitHub Projects

Projedeki görevlerin takibi için ek bir araç (Jira, ClickUp vb.) yerine, doğrudan GitHub reposu içinde yer alan **GitHub Projects** özelliği kullanılacaktır. Bu, öğrenme sürecini hızlandırır ve her şeyi tek bir yerde tutar.

### Kanban Tahtası Yapısı

Proje için `To Do` (Yapılacaklar), `In Progress` (Yapılıyor) ve `Done` (Bitti) sütunlarından oluşan basit bir Kanban tahtası oluşturulacaktır.

### İş Akışı
1.  Proje yöneticisi (Erkan), `PROJE_YONETIM_DOKUMANI.md`'de belirtilen görevleri GitHub Projects'teki `To Do` sütununa kartlar olarak ekler.
2.  Bir ekip üyesi bir göreve başladığında, o kartı `In Progress` sütununa çeker.
3.  Görevle ilgili Pull Request açıldığında, PR bu kart ile ilişkilendirilir.
4.  Pull Request, `develop` branch'ine birleştirildiğinde, görev kartı otomatik olarak (veya manuel) `Done` sütununa taşınır. 