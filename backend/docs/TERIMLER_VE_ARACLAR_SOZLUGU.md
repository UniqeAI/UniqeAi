# Terimler ve Araçlar Sözlüğü

Bu doküman, projemizde kullandığımız temel teknolojileri, araçları ve kavramları basit bir dille açıklamaktadır.

---

## Genel Araçlar

*   **Visual Studio Code (VS Code):** Projeyi yazmak için kullanacağımız kod editörümüz. Entegre terminali, Git yönetimi ve eklentileri sayesinde hepsi bir arada bir geliştirme ortamı sunar.
*   **Git:** Kodumuzun versiyonlarını ve değişiklik geçmişini takip eden sistem. Kimin, ne zaman, hangi değişikliği yaptığını kaydeder.
*   **GitHub:** Git ile yönettiğimiz projemizi internet üzerinde sakladığımız ve ekip olarak üzerinde çalıştığımız platform. Pull Request'ler burada yapılır.
*   **Docker:** Bir uygulamanın, tüm bağımlılıklarıyla birlikte paketlenip her bilgisayarda aynı şekilde çalışmasını sağlayan bir teknolojidir. Projemizin backend'ini "dockerize" ederek, "benim bilgisayarımda çalışıyordu" sorununu ortadan kaldıracağız. İlerleyen aşamalarda kullanılacaktır.

---

## Backend Teknolojileri

*   **FastAPI:** Backend API'ımızı oluşturmak için kullandığımız modern, çok hızlı bir Python web çatısıdır (framework). Performansı ve otomatik interaktif doküman oluşturma özelliği (`/docs`) için seçilmiştir.
*   **Uvicorn:** FastAPI uygulamamızı çalıştıran ve web'den gelen isteklere yanıt vermesini sağlayan sunucudur.

---

## Frontend Teknolojileri

*   **Streamlit:** Özellikle yapay zeka ve veri bilimi projeleri için tasarlanmış, çok hızlı bir şekilde interaktif web arayüzleri oluşturmamızı sağlayan bir Python kütüphanesidir. Sadece Python bilerek karmaşık arayüzler yapmamızı sağlar.

---

## AI / ML Teknolojileri

*   **PyTorch:** Google ve Meta gibi devlerin kullandığı temel bir derin öğrenme (deep learning) kütüphanesidir. Llama 3.1 modeli bu çatı üzerine kurulmuştur.
*   **Hugging Face Transformers:** Son teknoloji yapay zeka modellerini (Llama, GPT gibi) kolayca indirip kullanmamızı ve eğitmemizi sağlayan, sektör standardı haline gelmiş bir kütüphanedir.
*   **Fine-Tuning (İnce Ayar):** Önceden eğitilmiş devasa bir modeli (Llama 3.1 gibi), kendi özel görevimiz (bizim durumumuzda, API araçlarını kullanmayı öğrenmesi) için küçük bir veri setiyle yeniden eğitme işlemidir. Bu, modeli sıfırdan eğitmekten çok daha verimlidir.
*   **PEFT / LoRA:** Fine-tuning işlemini çok daha az bellek ve işlem gücü kullanarak yapmamızı sağlayan bir tekniktir. Modelin tamamı yerine sadece küçük, eklenti gibi parçalarını eğitir.
*   **Zemberek:** Türkçe metinler üzerinde işlem yapmak (kök bulma, normalleştirme vb.) için geliştirilmiş, en popüler Türkçe Doğal Dil İşleme (NLP) kütüphanesidir. Modelimizin Türkçe'yi daha iyi anlamasına yardımcı olacaktır. 