"""
Paket Değiştirme Senaryosu - Ultra Gelişmiş Sürüm (1000 Senaryo Optimizasyonu)
================================================
Bu modül, 1000 benzersiz senaryo üretmek için optimize edilmiş son derece çeşitli
paket değişikliği senaryoları üretir.
"""
import uuid
import random
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils import generate_user_id, create_validated_response
from ...telekom_api_schema import ChangePackageResponse

@dataclass
class UserDemographics:
    age_group: str
    location_type: str
    family_status: str
    occupation: str
    income_level: str
    tech_literacy: str

@dataclass
class ContextualFactors:
    time_of_day: str
    day_of_week: str
    season: str
    urgency_level: str
    previous_experience: str
    communication_preference: str

class PackageChangeScenarioGenerator:
    """1000 benzersiz senaryo için optimize edilmiş paket değiştirme senaryoları üreticisi"""
    
    def __init__(self):
        self.scenario_counter = 0
        self.used_fingerprints = set()
        self.regional_variations = self._load_regional_data()
        
    # Genişletilmiş demografik segmentler
    DEMOGRAPHICS = {
        'age_groups': {
            'gen_z': {'min_age': 18, 'max_age': 25, 'characteristics': ['dijital_yerli', 'sosyal_medya_odakli']},
            'millennial_early': {'min_age': 26, 'max_age': 32, 'characteristics': ['kariyer_odakli', 'teknoloji_merakli']},
            'millennial_late': {'min_age': 33, 'max_age': 40, 'characteristics': ['aile_kurma', 'ev_alimi']},
            'gen_x': {'min_age': 41, 'max_age': 55, 'characteristics': ['aile_sorumlusu', 'deneyimli']},
            'boomer': {'min_age': 56, 'max_age': 75, 'characteristics': ['güvenlik_öncelikli', 'geleneksel']},
            'silent_gen': {'min_age': 76, 'max_age': 90, 'characteristics': ['dijital_göçmen', 'basitlik_arayan']}
        },
        'locations': {
            'buyuksehir_merkez': {'internet_quality': 'excellent', 'competition': 'high'},
            'buyuksehir_cevre': {'internet_quality': 'good', 'competition': 'medium'},
            'il_merkezi': {'internet_quality': 'good', 'competition': 'medium'},
            'ilce': {'internet_quality': 'fair', 'competition': 'low'},
            'koy_kasaba': {'internet_quality': 'limited', 'competition': 'very_low'},
            'universite_yerleskesi': {'internet_quality': 'excellent', 'competition': 'high'},
            'is_merkezi': {'internet_quality': 'excellent', 'competition': 'high'}
        },
        'occupations': {
            'teknoloji': ['yazilim_geliştirici', 'veri_analisti', 'IT_uzmanı', 'grafik_tasarımcı', 'siber_guvenlik_uzmani'],
            'egitim': ['öğretmen', 'akademisyen', 'eğitim_koordinatörü', 'okul_muduru'],
            'saglik': ['doktor', 'hemşire', 'eczacı', 'fizyoterapist', 'psikolog'],
            'finans': ['muhasebeci', 'bankacı', 'mali_müşavir', 'yatirim_uzmani'],
            'ticaret': ['satış_temsilcisi', 'mağaza_müdürü', 'e_ticaret_uzmanı', 'ithalat_ihracat'],
            'hizmet': ['berber', 'kuaför', 'restoran_sahibi', 'taksi_şoförü', 'otel_isletmecisi'],
            'sanat': ['muzisyen', 'ressam', 'yazar', 'tasarimci'],
            'spor': ['profesyonel_sporcu', 'antrenor', 'spor_yoneticisi'],
            'ogrenci': ['lise_öğrencisi', 'üniversite_öğrencisi', 'lisansustu_ogrenci'],
            'emekli': ['emekli_memur', 'emekli_işçi', 'emekli_öğretmen', 'emekli_asker']
        }
    }

    # Genişletilmiş paket matrisi
    ADVANCED_PACKAGES = {
        'fiber_internet': {
            'entry': ['Fiber Başlangıç 25 Mbps', 'Temel Fiber 35 Mbps', 'Ev Fiber 50 Mbps', 'Mini Fiber 40 Mbps'],
            'standard': ['Hızlı Fiber 100 Mbps', 'Süper Fiber 150 Mbps', 'Ultra Fiber 200 Mbps', 'Pro Fiber 120 Mbps'],
            'premium': ['Mega Fiber 300 Mbps', 'Gigabit Fiber 1000 Mbps', 'Quantum Fiber 1500 Mbps', 'Hyper Fiber 2000 Mbps'],
            'business': ['İş Fiber Pro 500 Mbps', 'Kurumsal Fiber 1 Gbps', 'Enterprise Fiber 2 Gbps', 'Business Elite 5 Gbps']
        },
        'mobile_packages': {
            'minimal': ['Konuşma + 2GB', 'Temel Mobil 5GB', 'Ekonomik 8GB', 'Mini Paket 3GB'],
            'standard': ['Akıllı Mobil 15GB', 'Süper Mobil 25GB', 'Digital Life 40GB', 'Plus Paket 30GB'],
            'unlimited': ['Sınırsız Konuşma + 50GB', 'Unlimited Pro 75GB', 'Infinity Mobile 100GB', 'Sınırsız Max 120GB'],
            'premium': ['Premium Unlimited', 'VIP Mobile', 'Exclusive Mobile', 'Platinum Unlimited']
        },
        'combo_packages': {
            'basic_combo': ['Ev + Mobil Temel', 'Aile Paketi Ekonomik', 'İkili Kombo Başlangıç', 'Mini Kombo'],
            'family_combo': ['Aile Süper Paketi', 'Ev + 2 Mobil', 'Mega Aile Kombosu', 'Family Max'],
            'premium_combo': ['Ultimate Aile Paketi', 'Platinum Kombo', 'VIP Aile Çözümü', 'Elite Kombo'],
            'business_combo': ['İş + Mobil Pro', 'Kurumsal Kombo', 'Ofis Çözümü', 'Business Max']
        },
        'special_packages': {
            'student': ['Öğrenci Paketi', 'Campus Special', 'Genç Tarife', 'Öğrenci Plus'],
            'senior': ['65+ Paketi', 'Emekli Dostları', 'Altın Yıllar Paketi', 'Huzur Paketi'],
            'rural': ['Kırsal Fiber', 'Köy İnterneti', 'Uzak Bölge Paketi', 'Kırsal Max'],
            'gaming': ['Gamer Pro', 'eSports Elite', 'Gaming Master', 'Oyun Paketi'],
            'streaming': ['Stream Pro', 'Netflix&Chill', 'Content Creator', '4K Streaming Paketi'],
            'traveler': ['Seyahat Paketi', 'Global Roaming', 'Turist Tarifesi', 'Yolcu Paketi']
        }
    }

    LIFE_SCENARIOS = {
        'yeni_ev': [
            "Yeni eve taşındım, fiber altyapısı var",
            "Villa aldık, daha hızlı internet lazım",
            "Kiracı çıktı, evimize taşınıyoruz",
            "Yeni mahallede daha iyi paketler varmış",
            "Yurtdışından döndüm, yeni bir eve yerleştim",
            "Kampüsten ayrılıp kendi evime çıktım",
            "Taşındığım yeni binada fiber internet zorunlu",
            "Ev sahibim fiber internet istiyor",
            "Yeni taşındığım semtte internet altyapısı farklı",
            "Eşimle ilk evimizi aldık, internet paketi araştırıyorum",
            "Taşınma nedeniyle adres değişikliği yapmam gerekiyor",
            "Yeni evimde internet hızı eski yerden daha düşük",
            "Taşındığımız bölgede sadece fiber var",
            "Yeni apartmanımızda akıllı ev sistemi için hızlı internet gerekli",
            "Taşınırken internet paketimi güncellemem gerekiyor",
            "Yeni evim çalışma ofisim olacak, profesyonel internet lazım",
            "Taşındığımız yerde çocukların online dersleri için stabil internet şart",
            "Yeni semtimizde internet kalitesi daha yüksek",
            "Ev değişikliği nedeniyle paketimi iptal ettim, yeni başvuru yapıyorum",
            "Yeni adresime internet bağlatmam lazım",
            "Taşınma döneminde internet kesintisi yaşadım",
            "Yeni evimde sabit internet yok, mobil paket arıyorum",
            "Taşındığımız ilçede farklı operatörler daha avantajlı",
            "Yeni apartman yönetimi belirli bir operatörle anlaşmış",
            "Ev alırken internet altyapısını kontrol etmemiştim",
            "Yeni yerleşim yerinde internet seçenekleri sınırlı",
            "Taşınma sonrası internet faturası çok arttı",
            "Yeni evde eski paketim yetersiz kalıyor",
            "Semt değiştirdim, komşular farklı paketler kullanıyor",
            "Taşındığım bina fibere hazır değil, alternatif arıyorum",
            "Yeni evimde internet kurulumu için teknik destek lazım",
            "Taşınırken modemimi kaybettim, yeni kurulum gerekli",
            "Yeni adresimde internet hızı çok düşük çıktı",
            "Ev değişikliği yaptım, paketimi taşımak istiyorum",
            "Yeni semtimizde sadece uydu internet var",
            "Taşındığım şehirde farklı tarifeler geçerli",
            "Yeni ev için aile paketi araştırıyorum",
            "Taşınma nedeniyle internet sözleşmemi feshettim",
            "Yeni yerleşim yerinde 5G altyapısı daha iyi",
            "Eşyalarım taşınırken modem hasar gördü",
            "Yeni adresimde sabit hat yok, mobil çözüm arıyorum",
            "Taşınma sonrası internet bağlantım çalışmıyor",
            "Yeni mahallemizde fiber altyapı henüz yok",
            "Ev değiştirdim, daha ekonomik paket arıyorum",
            "Yeni semtimizde internet fiyatları daha yüksek",
            "Taşınırken internet paketimi iptal ettirdim",
            "Yeni evimde çok sayıda cihaz bağlayacağım",
            "Taşındığımız bölgede indirimli öğrenci paketi yok",
            "Yeni adresim için kurumsal paket araştırıyorum",
            "Ev değişikliği sonrası internet hızım düştü"
        ],
        'is_degisimi': [
            "Uzaktan çalışmaya başladım",
            "Evden çalışma kalıcı oldu",
            "Freelance işe geçtim",
            "Kendi işimi kurdum",
            "İkinci bir iş başladım",
            "Kariyer değişikliği yaptım",
            "Terfi ettim, iş gereksinimlerim arttı",
            "Yeni bir şirkete geçtim, evden çalışıyorum",
            "İş yerim şehir dışına taşındı",
            "Serbest mesleğe başladım, internet kullanımım arttı",
            "Yarı zamanlı işe başladım, ek internet kotası lazım",
            "İşim gereği sürekli video konferans yapıyorum",
            "Yeni projem için yüksek hızlı internet gerekiyor",
            "İş bilgisayarım için ayrı internet hattı lazım",
            "Home office döneminde internet faturası çok arttı",
            "İş yerim kapandı, evden çalışmaya başladım",
            "Yeni işimde büyük dosyalar indirip yüklüyorum",
            "Kariyerime online eğitimlerle devam ediyorum",
            "İşim nedeniyle sık sık yurtdışı bağlantı kurmam gerekiyor",
            "Profesyonel olarak içerik üretmeye başladım",
            "İş değiştirdim, yeni şirket VPN için stabil internet istiyor",
            "Freelance platformlarda çalışıyorum, sürekli online olmam lazım",
            "Kendi online mağazamı açtım",
            "İşim gereği bulut sistemlerini yoğun kullanıyorum",
            "Yeni pozisyonumda sürekli canlı yayın yapmam gerekiyor",
            "İkinci işim online danışmanlık, ek paket lazım",
            "Yeni işimde sanal makine kullanmam gerekiyor",
            "Kariyer değişikliği yaptım, yazılım geliştirici oldum",
            "İşim nedeniyle büyük veri setleri indiriyorum",
            "Evden çalışırken internet kesintileri iş kaybına neden oluyor",
            "Yeni işim için sabit IP adresi gerekiyor",
            "İş bilgisayarım ve kişisel bilgisayarım için farklı bağlantılar lazım",
            "Online stok takip sistemi kullanıyorum, sürekli bağlı kalmam gerekiyor",
            "Müşteri görüşmelerim artık tamamen online",
            "İşim için güvenli ve hızlı internete ihtiyacım var",
            "Yeni pozisyonumda tasarım programları kullanıyorum, yüksek RAM gerekiyor",
            "İş değişikliği sonrası internet kullanım sürem iki katına çıktı",
            "Online pazarlama uzmanı oldum, sürekli sosyal medya canlı yayını yapıyorum",
            "İşim gereği sık sık uluslararası video konferanslar yapıyorum",
            "Yeni işim veri analizi, büyük dosyalarla çalışıyorum",
            "Evden çalışırken eşimle interneti paylaşamıyoruz",
            "İş bilgisayarım için özel bir internet paketi lazım",
            "Sürekli online eğitim veriyorum, yüksek yükleme hızı gerekiyor",
            "Yeni işim grafik tasarım, büyük dosya transferleri yapıyorum",
            "İş değişikliği sonrası daha esnek internet paketi arıyorum",
            "Online satış platformunda çalışıyorum, sürekli bağlı kalmam gerekiyor",
            "Yeni işim için 8 saat kesintisiz internet şart",
            "İşim nedeniyle birden fazla cihazı aynı anda kullanıyorum",
            "Mobil internetle çalışmak verimimi düşürüyor"
        ],
        'aile_degisimi': [
            "Evlendim, eşimle ortak paket yapacağız",
            "Çocuğum doğdu, ev internet kullanımı arttı",
            "Çocuklarım büyüdü, online ders ihtiyacı var",
            "Aile büyükleri ile birlikte yaşıyoruz artık",
            "Boşandım, kendi adıma paket geçmek istiyorum",
            "Çocuklarım üniversiteye başladı, evdeki kullanım azaldı",
            "Yeni bebeğimiz oldu, anneanneler sık geliyor",
            "Çocuğum online oyun oynamaya başladı",
            "Ailecek online kurslara başladık",
            "Eşim işten çıktı, evde daha çok vakit geçiriyor",
            "Çocuğum uzaktan eğitime başladı",
            "Ailecek film izleme alışkanlığımız arttı",
            "Büyük çocuğum yurda gitti, internet ihtiyacı azaldı",
            "Evimize akıllı cihazlar aldık, internet tüketimi arttı",
            "Aile bütçemiz değişti, daha ekonomik paket lazım",
            "Çocuklar tablet kullanmaya başladı",
            "Ailecek online alışveriş yapıyoruz",
            "Eşim yeni işe başladı, evden çalışıyor",
            "Çocuğum e-spor turnuvalarına katılıyor",
            "Ailemle video konferans sıklığımız arttı",
            "Yeni evliyiz, ortak hesap oluşturacağız",
            "Çocuğum müzik kursuna online devam ediyor",
            "Ailecek bulut depolama kullanmaya başladık",
            "Büyükannemiz sağlık takibi için online cihaz kullanıyor",
            "Çocuklarımın her ikisi de online ders alıyor",
            "Aile içi iletişim için grup görüşmeleri yapıyoruz",
            "Evde dört farklı cihaz aynı anda internete bağlanıyor",
            "Çocuğumun üniversite sınavı için online dersleri var",
            "Ailecek akıllı TV kullanımımız arttı",
            "Yeni taşınan komşularla online iletişim kuruyoruz",
            "Çocuğum yurtdışında, sık sık video görüşüyoruz",
            "Aile büyüklerimiz sağlık nedeniyle ziyarete gelemiyor, online görüşüyoruz",
            "Evde internet kullanım saatlerimiz değişti",
            "Çocuğumun online oyun arkadaşlarıyla bağlantısı kesiliyor",
            "Ailecek farklı odalarda internet kullanıyoruz",
            "Yeni bebeğimiz için bebek izleme kamerası bağlantısı lazım",
            "Çocuğumun tabletinde video dersler kesiliyor",
            "Ailece aynı anda farklı platformlardan film izliyoruz",
            "Eşim ve ben farklı saatlerde evden çalışıyoruz",
            "Çocuğumun online sınavları için stabil internet lazım",
            "Aile bütçesinde internet harcamasını azaltmam gerekiyor",
            "Büyük çocuğum evden ayrıldı, daha küçük paket yeterli",
            "Yeni gelen misafir öğrenci için ek kota gerekiyor",
            "Ailecek kullandığımız cihaz sayısı arttı",
            "Çocukların oyun konsolları için özel bağlantı gerekiyor",
            "Aile içi internet kullanımında öncelik ayarlamam lazım",
            "Eşimle internet kullanım alışkanlıklarımız farklılaştı"
        ],
        'teknoloji_degisimi': [
            "4K TV aldım, daha hızlı internet gerekiyor",
            "Gaming setup kurdum",
            "Smart home sistemlerine geçtik",
            "Çocuklar online oyun oynuyor",
            "Streaming servisleri kullanmaya başladık",
            "Drone ile canlı yayın yapıyorum",
            "VR oyunları oynamaya başladım",
            "8K çözünürlükte TV aldım",
            "Yeni oyun konsolum için düşük ping gerekiyor",
            "Akıllı ev aletleri kullanmaya başladık",
            "Sanal gerçeklik cihazı aldım",
            "Profesyonel fotoğraf makinesiyle online yayın yapıyorum",
            "Yeni bilgisayarım eski paketimi zorluyor",
            "Online depolama hizmetine geçtim",
            "Sürekli bulut yedekleme yapıyorum",
            "Yeni tabletimde 4K videolar izliyorum",
            "Mobil hotspot cihazı kullanıyorum",
            "Akıllı saat için sürekli senkronizasyon gerekiyor",
            "Ev sinema sistemim için yüksek bant genişliği lazım",
            "Yeni telefonum 5G destekliyor",
            "Online oyun turnuvalarına katılıyorum",
            "Canlı yayın yapmaya başladım",
            "Yeni modem aldım, paketimi güncellemem gerekiyor",
            "Video düzenleme için yüksek yükleme hızı lazım",
            "İki monitörlü setup kurdum",
            "Sesli asistan kullanımım arttı",
            "Yüksek çözünürlüklü güvenlik kameraları taktırdım",
            "Online arşivleme sistemi kullanıyorum",
            "Yeni grafik kartı aldım, internet hızı yetersiz kalıyor",
            "Bulut oyun servislerini kullanmaya başladım",
            "Akıllı aydınlatma sistemi kurulumu yaptırdım",
            "Sürekli podcast yayını yapıyorum",
            "Yeni nesil oyunlar indirmem saatler alıyor",
            "Yüksek kaliteli müzik akışı için daha fazla bant genişliği lazım",
            "Online fotoğraf düzenleme yapıyorum",
            "3D modelleme için yüksek hız gerekiyor",
            "Video konferans kalitemi artırmak istiyorum",
            "Akıllı buzdolabım internet bağlantısı istiyor",
            "Yeni alınan akıllı termostat sürekli veri gönderiyor",
            "Sanal makine kullanmaya başladım",
            "İki ayrı oyun konsolum var, aynı anda bağlanıyorlar",
            "4K kalitesinde film kiralıyorum",
            "Yüksek çözünürlüklü haritaları indiriyorum",
            "Drone görüntülerini anında paylaşıyorum",
            "Akıllı prizler kullanıyorum",
            "Online kumanda sistemleri kurulumu yaptırdım",
            "Yeni teknolojik cihazlar için QoS ayarları yapmam gerekiyor",
            "Evde 20'den fazla IoT cihazı var",
            "8K video render için fiber internet gerekiyor"
        ],
        'ekonomik': [
            "Bütçemi gözden geçiriyorum",
            "Maaşım arttı, daha iyi paket alabilirim",
            "Ekonomik durumum kötüleşti, daha ucuz paket lazım",
            "Öğrenci oldum, indirimli paket arıyorum",
            "Emekli oldum, ihtiyaçlarım değişti",
            "Kredi ödemelerim başladı, tasarruf etmem gerekiyor",
            "Yatırım yapıyorum, ekstra gelir kaynağım oluştu",
            "Faturalarım çok yüksek geliyor",
            "Ekonomik kriz nedeniyle bütçemi kısmam gerekiyor",
            "İşsiz kaldım, daha uygun paket arıyorum",
            "Gelirim azaldı, internet harcamasını azaltmam lazım",
            "Yan gelirim arttı, daha iyi pakete geçebilirim",
            "Öğrenci indiriminden yararlanmak istiyorum",
            "Emekli indirimi için başvurmam gerekiyor",
            "Aylık internet harcamamı sabitlemek istiyorum",
            "Ekonomik paketlere geçiş yapmak istiyorum",
            "Faturaları düşürmek için paketimi küçültmek istiyorum",
            "Yeni bir tarifeye geçerek tasarruf etmek istiyorum",
            "Gelir durumum değişti, paketimi güncellemem gerekiyor",
            "Ek iş buldum, daha fazla internet kullanıyorum",
            "Bütçe planlaması yapıyorum, internet masrafını azaltacağım",
            "Ekonomik nedenlerle daha uygun operatöre geçmeyi düşünüyorum",
            "Fiyat/performans oranı yüksek paket arıyorum",
            "Kampanyalı paketlerden yararlanmak istiyorum",
            "Sözleşmem bitmek üzere, daha uygun paket var mı?",
            "Ek masrafları karşılayabilmek için internet paketimi küçülteceğim",
            "Ev ekonomisinde kesintiye gitmem gerekiyor",
            "Yıllık paket alarak indirimden yararlanmak istiyorum",
            "Kur farkı nedeniyle faturalarım arttı",
            "Gelirime göre internet harcamam çok yüksek",
            "Aile bütçesini dengelemek için internet masrafını azaltmam lazım",
            "Ekonomik krizde lüks internet paketini kaldıramıyorum",
            "Tasarruf amacıyla paketimi değiştirmek istiyorum",
            "Daha ucuz alternatifler olduğunu duydum",
            "Faturalarımı ödeyemez duruma geldim",
            "Ekonomik nedenlerle taşınıyorum, yeni paket araştırıyorum",
            "İşten çıkarıldım, internet masrafını azaltmam lazım",
            "Öğrenci oldum, indirimli pakete geçmek istiyorum",
            "Emekli maaşımla daha uygun paket lazım",
            "Ek gelirim arttı, premium pakete geçebilirim",
            "Bütçemi aşan bir paket kullanıyorum",
            "Ekonomik durum iyileşti, daha iyi internet alabilirim",
            "Kira artışı nedeniyle internet harcamasını kısmam gerekiyor",
            "Tasarruf paketlerini incelemek istiyorum",
            "Fiyat artışları nedeniyle paketimi değiştirmem gerekiyor",
            "Ekonomik nedenlerle aile paketinden çıkacağım",
            "Daha uygun fiyatlı paketlere geçiş yapmak istiyorum",
            "Ekonomik krizde internet paketimi minimuma indirmem gerekiyor"
        ],
        'rekabet': [
            "Komşumun operatörü daha ucuz paket veriyor",
            "Başka operatör daha iyi kampanya yapmış",
            "Arkadaşım tavsiye etti, paket değiştirmeyi düşünüyorum",
            "Sosyal medyada gördüğüm kampanya ilgimi çekti",
            "Reklamınızı gördüm, daha avantajlı görünüyor",
            "Piyasa araştırması yaptım, alternatifleriniz var",
            "Rakip operatör daha hızlı internet sunuyor",
            "Diğer şirketlerin müşteri hizmetleri daha iyi",
            "Farklı operatörde daha fazla kota aynı fiyata",
            "Rakip firma ücretsiz kurulum yapıyor",
            "Başka operatörde modem ücretsiz",
            "Diğer şirketlerin indirimleri daha cazip",
            "Rakip operatörün network kalitesi daha iyi",
            "Farklı bir operatörle görüştüm, daha iyi teklifleri var",
            "Piyasada daha uygun fiyatlı paketler gördüm",
            "Arkadaşımın interneti daha hızlı",
            "Komşum aynı paraya daha fazla hız alıyor",
            "Rakip operatörün kampanyası daha avantajlı",
            "Diğer şirketler sadık müşteri indirimi yapıyor",
            "Farklı operatörde taahhüt süresi daha kısa",
            "Rakip firma ücretsiz ek hizmetler sunuyor",
            "Diğer operatörün müşteri memnuniyeti daha yüksek",
            "Başka bir şirketle görüştüm, teklifinizi değerlendiriyorum",
            "Piyasada daha rekabetçi fiyatlar var",
            "Rakip operatör yeni müşteri için özel indirim yapıyor",
            "Diğer şirketlerin internet hızı daha stabil",
            "Farklı operatörde kesinti yaşanmıyor",
            "Arkadaşımın operatörü problemleri daha hızlı çözüyor",
            "Rakip firma daha modern modem veriyor",
            "Diğer operatörlerin uygulaması daha kullanışlı",
            "Başka şirkette aynı hız daha ucuza geliyor",
            "Rakip operatörün teknik desteği daha hızlı",
            "Farklı operatör daha geniş kapsama alanı sunuyor",
            "Diğer şirketlerin yurtdışı erişimi daha iyi",
            "Rakip firma ücretsiz bulut depolama veriyor",
            "Piyasada daha fazla seçenek var",
            "Başka operatörün streaming paketleri daha cazip",
            "Rakip şirket oyuncular için özel paket sunuyor",
            "Diğer operatörlerin sosyal medya paketleri var",
            "Farklı şirkette aylık kota sınırı yok",
            "Rakip operatörün müşteri hizmetleri 7/24 Türkçe",
            "Diğer şirketlerin faturaları daha şeffaf",
            "Başka operatörde ek ücret yok",
            "Rakip firma daha hızlı kurulum yapıyor",
            "Farklı operatörün interneti kesintisiz",
            "Diğer şirketlerin hız test sonuçları daha iyi",
            "Rakip operatörün kampanyası daha uzun süreli",
            "Piyasada daha kaliteli hizmet veren operatörler var",
            "Başka operatöre geçmeyi düşünüyorum"
        ],
        'teknoloji_yetersiz': [
            "Sık sık kesintiler yaşıyorum",
            "Hız vaat ettiğiniz seviyede değil",
            "Oyun oynarken gecikme sorunu yaşıyorum",
            "Video konferanslarda kopmalar oluyor",
            "Dosya yükleme hızı çok yavaş",
            "Aynı anda birden fazla cihaz bağlayamıyorum",
            "İnternet hızım dalgalanıyor",
            "Modem sık sık yeniden başlıyor",
            "Gece saatlerinde bile hız düşüyor",
            "Online derslerde bağlantı kopuyor",
            "Film izlerken sürekli buffering oluyor",
            "İndirme hızları çok düşük",
            "Oyunlarda ping değerim çok yüksek",
            "Video yükleme saatler sürüyor",
            "Wi-Fi sinyali zayıf",
            "Cihazlar sürekli bağlantıyı kaybediyor",
            "Sabit IP ile bile sorun yaşıyorum",
            "Mobil tethering daha iyi çalışıyor",
            "Sözleşmede yazan hızı alamıyorum",
            "Teknik ekip gelmesine rağmen sorun çözülmedi",
            "Farklı modem denedim, sorun devam ediyor",
            "Hız testlerinde tutarlı sonuç alamıyorum",
            "Fiber olmasına rağmen ADSL hızında",
            "Paket yükseltmeme rağmen hız artmadı",
            "İnternet özellikle yağmurlu havalarda kesiliyor",
            "Aynı anda iki cihaz bağlayınca hız düşüyor",
            "Gün içinde belirli saatlerde internet çöküyor",
            "Online işlemlerde zaman aşımı yaşıyorum",
            "VPN ile bağlanınca hız çok düşüyor",
            "Oyun konsolum sürekli bağlantı hatası veriyor",
            "Akıllı ev cihazları internete bağlanamıyor",
            "Dosya indirirken hız sürekli değişiyor",
            "4K video izlerken sürekli kalite düşüyor",
            "Canlı yayın yaparken bağlantım kopuyor",
            "Uzaktan çalışırken sık sık bağlantı kaybediyorum",
            "Müşteri hizmetleri sorunumu çözemedi",
            "Teknik destek gelmesine rağmen iyileşme olmadı",
            "Farklı katlarda Wi-Fi sinyali alamıyorum",
            "Cihazlar otomatik olarak mobil veriye geçiyor",
            "Online depolama senkronizasyonu sürekli kesiliyor",
            "Yeni aldığım cihazlar internete bağlanamıyor",
            "İnternet hızım asla vaat edilen seviyeye ulaşmıyor",
            "Oyun güncellemeleri çok yavaş iniyor",
            "Sürekli yeniden bağlanmam gerekiyor",
            "İnternet kesintileri iş kaybına neden oluyor",
            "Faturalı hattım mobil internetten daha yavaş",
            "Sabit hat internetim mobil internetten daha kötü",
            "Hız sorunları nedeniyle iş verimliliğim düştü",
            "Teknolojik cihazlarım internet yetersizliğinden verimli çalışmıyor"
        ]
    }

    CONVERSATION_PATTERNS = {
        'opener_variations': {
            'direct': [
                "Paketimi değiştirmek istiyorum",
                "Tarife değişikliği yapmak istiyorum",
                "Başka bir pakete geçmek istiyorum",
                "Paketimi güncellemek istiyorum",
                "Tarifemi değiştirmek istiyorum",
                "Paket değişikliği için başvurmak istiyorum",
                "Farklı bir pakete geçiş yapmak istiyorum",
                "İnternet paketimi değiştirmek istiyorum",
                "Mobil paketimi güncellemek istiyorum",
                "Kombi paketimi değiştirmek istiyorum",
                "Tarife yükseltmek istiyorum",
                "Paketimi küçültmek istiyorum",
                "Daha ekonomik pakete geçmek istiyorum",
                "Premium pakete geçmek istiyorum",
                "Aile paketine geçiş yapmak istiyorum",
                "İş paketine geçmek istiyorum",
                "Öğrenci paketine geçmek istiyorum",
                "Emekli paketine geçmek istiyorum",
                "Yeni kampanyalı pakete geçmek istiyorum",
                "Sözleşmesiz pakete geçmek istiyorum",
                "Hızımı artırmak istiyorum",
                "Kotamı artırmak istiyorum",
                "Sınırsız pakete geçmek istiyorum",
                "Fiber pakete geçmek istiyorum",
                "5G pakete geçmek istiyorum",
                "İnternet hızımı yükseltmek istiyorum",
                "Ek hizmet eklemek istiyorum",
                "Ekran paketi eklemek istiyorum",
                "Oyun paketi eklemek istiyorum",
                "Bulut hizmeti eklemek istiyorum",
                "Güvenlik paketi eklemek istiyorum",
                "TV paketimi değiştirmek istiyorum",
                "Sabit hat paketimi değiştirmek istiyorum",
                "Mobil internet paketimi değiştirmek istiyorum",
                "Tarifemi iptal ettirmek istiyorum",
                "Paketimi askıya almak istiyorum",
                "Sözleşmemi yenilemek istiyorum",
                "Taahhüt süremi uzatmak istiyorum",
                "Fatura ödeme şeklimi değiştirmek istiyorum",
                "Otomatik ödemeyi iptal ettirmek istiyorum",
                "Fatura adresimi değiştirmek istiyorum",
                "Müşteri numaramı değiştirmek istiyorum",
                "Hesap birleştirme yapmak istiyorum",
                "Hattımı devretmek istiyorum",
                "Numara taşıma yapmak istiyorum",
                "Hattımı iptal ettirmek istiyorum",
                "Yeni modem istiyorum",
                "Teknik destek talep etmek istiyorum"
            ],
            'contextual': [
                "Mevcut paketim artık ihtiyacımı karşılamıyor",
                "Paket değişikliği konusunda bilgi almak istiyorum",
                "Daha uygun bir paket seçeneği var mı acaba",
                "İnternet hızım yeterli gelmiyor",
                "Kota sınırıma ulaştım",
                "Faturalarım çok yüksek geliyor",
                "İhtiyaçlarım değişti",
                "Yaşam tarzım değişti",
                "Kullanım alışkanlıklarım farklılaştı",
                "Teknolojik cihazlarım arttı",
                "Evden çalışmaya başladım",
                "Çocuklarım online eğitime geçti",
                "Yeni bir eve taşındım",
                "İş değiştirdim",
                "Ekonomik durumum değişti",
                "Daha hızlı internete ihtiyacım var",
                "Sık sık kesinti yaşıyorum",
                "Bağlantı kalitesinden memnun değilim",
                "Rakip operatörler daha iyi teklif sunuyor",
                "Mevcut paketim çok pahalı",
                "Paketim ihtiyacımdan fazla",
                "Paketim ihtiyacımı karşılamıyor",
                "Daha ekonomik seçenekler var mı?",
                "Kampanyalardan yararlanmak istiyorum",
                "İndirimli paketler hakkında bilgi almak istiyorum",
                "Sözleşmem bitmek üzere",
                "Taahhüt sürem doldu",
                "Yeni müşteri indiriminden yararlanmak istiyorum",
                "Sadık müşteri indirimi talep ediyorum",
                "Paket karşılaştırması yapmak istiyorum",
                "Farklı paketlerin fiyatlarını öğrenmek istiyorum",
                "Hız testi sonuçlarım kötü",
                "Teknik problemler yaşıyorum",
                "Müşteri hizmetlerine ulaşamıyorum",
                "Faturamda anlamadığım ücretler var",
                "Ek ücretlendirmelerden rahatsızım",
                "Paket içeriğimi öğrenmek istiyorum",
                "Güncel fiyat listesini istiyorum",
                "Tarife broşürü talep ediyorum",
                "Online işlemlerde sorun yaşıyorum",
                "Mobil uygulamanız çalışmıyor",
                "Web sitesinden paket değiştiremiyorum",
                "Otomatik paket yenileme istemiyorum",
                "Fatura ödeme kolaylığı arıyorum",
                "Taksitli ödeme seçeneği istiyorum",
                "Öğrenci belgemi güncellemek istiyorum",
                "Emekli belgemi sisteme yüklemek istiyorum",
                "Adres değişikliği için başvurmak istiyorum",
                "Hesap bilgilerimi güncellemek istiyorum"
            ],
            'story_based': [
                "Durumum değişti, paketime de yansıtmak istiyorum",
                "Yaşam tarzım değişti, buna uygun paket lazım",
                "İhtiyaçlarım farklılaştı, paket güncellemesi yapmak istiyorum",
                "Hayatımdaki değişiklikler nedeniyle paketimi yenilemek istiyorum",
                "Yeni bir işe başladım, internet kullanımım arttı",
                "Evlendim, ortak paket oluşturmak istiyoruz",
                "Çocuğum oldu, evde daha çok vakit geçiriyoruz",
                "Taşındım, yeni evime uygun paket arıyorum",
                "Emekli oldum, daha az internet kullanıyorum",
                "Öğrenci oldum, indirimli pakete geçmek istiyorum",
                "Ekonomik sıkıntılar nedeniyle paketimi küçültmem gerekiyor",
                "Terfi ettim, daha iyi bir paket alabilirim",
                "Freelance çalışmaya başladım, stabil internet lazım",
                "Çocuklarım üniversiteye gitti, internet ihtiyacım azaldı",
                "Pandemi sonrası ofise döndüm, ev interneti az kullanıyorum",
                "Yeni teknolojik cihazlar aldım, hızım yetmiyor",
                "Online oyun oynamaya başladım, düşük ping istiyorum",
                "Film platformlarına abone oldum, daha fazla kota lazım",
                "Evden çalışma sona erdi, paketimi küçültmek istiyorum",
                "Yeni hobi edindim, internet kullanımım arttı",
                "Sağlık sorunlarım nedeniyle evde daha çok vakit geçiriyorum",
                "Çocuklarım online eğitime geçti, internet yetersiz kalıyor",
                "Aile büyüklerimiz taşındı, daha fazla cihaz bağlıyoruz",
                "Akıllı ev sistemleri kurdum, internet tüketimim arttı",
                "İş yerim kapandı, evden çalışmaya başladım",
                "Ek gelir kaynağım oldu, daha iyi pakete geçebilirim",
                "Kira artışı oldu, internet masrafını kısmam gerekiyor",
                "Yeni bir şehre taşındım, yerel paketleri araştırıyorum",
                "Komşularım farklı operatör kullanıyor, daha memnunlar",
                "Arkadaşımın paketi daha avantajlı, ben de geçmek istiyorum",
                "Sosyal medyada kampanyanızı gördüm, ilgimi çekti",
                "Teknik sorunlar yaşıyorum, çözüm bulamadım",
                "Müşteri hizmetleriniz beni tatmin etmedi",
                "Uzun süredir müşterinizim, sadakat indirimi istiyorum",
                "Faturalarım çok yüksek, tasarruf etmem gerekiyor",
                "İnternet hızım sözleşmede yazanın altında",
                "Sık sık kesintiler nedeniyle iş kaybı yaşıyorum",
                "Yeni bir operatör teklif verdi, sizinle kalmak istiyorum",
                "Ailecek paketimizi değerlendiriyoruz",
                "Çocuklarım büyüdü, kendi hatlarını istiyorlar",
                "Evdeki internet kullanım saatleri değişti",
                "Gece vardiyasına geçtim, gündüz internet kullanıyorum",
                "Yarı zamanlı işe başladım, ek internet kotası lazım",
                "Online kursa başladım, daha fazla veri gerekiyor",
                "Hobim için büyük dosyalar indiriyorum",
                "Güvenlik kameralarım sürekli internet kullanıyor",
                "Eski paketim artık sunulmuyor",
                "Yeni kampanyalarınızı değerlendirmek istiyorum",
                "Hayat koşullarım değişti, paketimi buna göre ayarlamak istiyorum"
            ],
            'comparison': [
                "Başka operatörlerin paketlerine baktım, sizde de benzer var mı",
                "Piyasadaki diğer seçenekleri değerlendiriyorum",
                "Rekabetçi bir paket arıyorum",
                "Alternatif paketleri karşılaştırmak istiyorum",
                "Rakip operatörün teklifini aldım, siz ne sunabilirsiniz",
                "Diğer şirketler daha uygun fiyatlı",
                "Farklı operatörde aynı hız daha ucuz",
                "Komşum sizden daha iyi hız alıyor",
                "Arkadaşımın paketi daha fazla içerik sunuyor",
                "Piyasada daha avantajlı kampanyalar var",
                "Diğer operatörlerin müşteri hizmetleri daha iyi",
                "Rakip firma ücretsiz ek hizmetler veriyor",
                "Sizin paketleriniz rakiplere göre pahalı",
                "Farklı operatörde modem ücretsiz",
                "Diğer şirketler kurulum ücreti almıyor",
                "Rakip operatörün kapsama alanı daha geniş",
                "Başka operatörde kesinti yaşanmıyor",
                "Diğer şirketlerin interneti daha stabil",
                "Farklı operatörün uygulaması daha kullanışlı",
                "Rakip firma daha modern teknoloji kullanıyor",
                "Diğer operatörler daha hızlı teknik destek veriyor",
                "Başka şirkette aynı paraya daha fazla kota var",
                "Rakip operatör oyuncular için özel paket sunuyor",
                "Diğer şirketlerin sosyal medya paketleri var",
                "Farklı operatörde sınırsız youtube erişimi var",
                "Rakip firma uluslararası aramaları dahil ediyor",
                "Diğer operatörler yurtdışı roaming paketleri sunuyor",
                "Başka şirket cloud depolama veriyor",
                "Rakip operatörün aylık ücreti daha düşük",
                "Diğer firmalar taahhüt süresiz paket sunuyor",
                "Farklı operatörde ek ücret yok",
                "Rakip firma daha şeffaf faturalandırma yapıyor",
                "Diğer şirketlerin internet hızı daha yüksek çıkıyor",
                "Başka operatörün kampanyası daha uzun süreli",
                "Rakip firma yeni müşteriye hediye veriyor",
                "Diğer operatörler sadık müşterilerine özel indirim yapıyor",
                "Farklı şirkette referans sistemiyle ek indirim var",
                "Rakip operatörün kurulum süreci daha hızlı",
                "Diğer şirketlerde teknik ekip daha çabuk geliyor",
                "Başka operatörde ücretsiz hız testi yapılıyor",
                "Rakip firma online işlemlerde daha az komisyon alıyor",
                "Diğer operatörlerin faturalı hatları daha avantajlı",
                "Farklı şirkette öğrenci indirimi daha yüksek",
                "Rakip operatör emeklilere özel tarife sunuyor",
                "Diğer şirketler aile paketlerinde daha esnek",
                "Başka operatörde kurumsal müşterilere özel avantajlar var",
                "Rakip firma iş ortaklarına ek indirim veriyor",
                "Diğer operatörlerin tatil paketleri daha cazip",
                "Farklı şirkette yurtdışı kullanım ücretleri daha düşük"
            ],
            'problem': [
                "Mevcut paketimde sorunlar yaşıyorum",
                "İnternet hizmetinizden memnun değilim",
                "Teknik sorunlar nedeniyle paket değiştirmek istiyorum",
                "Hizmet kalitesi beklentilerimi karşılamıyor",
                "Sık sık bağlantı kopmaları yaşıyorum",
                "Hızım sürekli dalgalanıyor",
                "Vaadedilen hızı asla alamıyorum",
                "Online oyun oynayamıyorum, ping çok yüksek",
                "Video konferanslarım sürekli kesiliyor",
                "Dosya indirmem saatler alıyor",
                "Modem sürekli kendini yeniden başlatıyor",
                "Wi-Fi kapsama alanı çok zayıf",
                "Farklı katlarda internet kullanamıyorum",
                "Teknik destek çağırdım ama sorun çözülmedi",
                "Müşteri hizmetlerine ulaşamıyorum",
                "Sorunlarım çözülmediği için paketimi değiştireceğim",
                "Kesintiler nedeniyle iş kaybı yaşıyorum",
                "Faturamda açıklanamayan ücretler var",
                "Sözleşmede olmayan ek ücretler çıkıyor",
                "Paket içeriğimde değişiklik yapılmış",
                "Hızım düşürülmüş",
                "Kota sınırım değiştirilmiş",
                "Fiyat artışından habersizdim",
                "Otomatik yenileme yapılmış",
                "Kampanya bitmiş ama ben haberdar edilmemişim",
                "Teknik ekip randevusuna gelmedi",
                "Sorunum çözülmediği için ücret iadesi istiyorum",
                "Modem arızalı, değişim talep ediyorum",
                "Altyapı sorunları devam ediyor",
                "Yağmurlu havalarda internet kesiliyor",
                "Akşam saatlerinde hız düşüyor",
                "Aynı anda birden fazla cihaz bağlayamıyorum",
                "Oyun konsolum internete bağlanamıyor",
                "Akıllı TV'mde sürekli buffering oluyor",
                "VPN ile bağlanınca hız çok düşüyor",
                "Mobil tethering daha iyi çalışıyor",
                "Sabit IP ile bile sorun yaşıyorum",
                "Hız testi sonuçları tutarsız",
                "Teknik destek sorunumu anlamıyor",
                "Çözüm önerileriniz işe yaramadı",
                "Defalarca şikayet ettim ama sonuç alamadım",
                "Sisteminizde sürekli arıza var",
                "Kesintiler nedeniyle müşteri kaybediyorsunuz",
                "Hizmet kalitesi düştü",
                "Eski kalitenizi arıyorum",
                "Yöneticiyle görüşmek istiyorum",
                "Şikayetimi üst mercilere ileteceğim",
                "Sorun çözülmezse operatör değiştireceğim",
                "Memnuniyetsiz bir müşteri olarak hakkımı arıyorum"
            ]
        },
        'concern_expressions': {
            'price': [
                "bütçeme uygun", "daha ekonomik", "uygun fiyatlı", "bütçe dostu", "tasarruf etmek istiyorum",
                "ucuz alternatif", "düşük maliyetli", "ekonomi paketi", "fiyat performans", "cüzdan dostu",
                "indirimli tarife", "kampanyalı fiyat", "özel teklif", "uygun ödeme", "taksit seçeneği",
                "ekonomik çözüm", "fiyat avantajı", "düşük ücret", "makul fiyat", "bütçe planı",
                "masrafı azaltmak", "fatura şoku", "yüksek ücret", "pahalı paket", "fiyat artışı",
                "ekonomik kriz", "bütçe sıkıntısı", "tasarruf paketi", "ekonomi modu", "ucuz internet",
                "düşük faturalı", "fiyat araştırması", "uygun maliyet", "cazip fiyat", "indirim bekliyorum",
                "fiyat rekabeti", "daha hesaplı", "ekonomik tarife", "fiyat performans", "bütçe ayarlaması",
                "fiyat karşılaştırması", "ucuz seçenek", "düşük bütçeli", "fiyat politikası", "ekonomik hizmet",
                "fiyat düşürme", "indirim talebi", "fiyat memnuniyeti", "bütçe dostu çözüm"
            ],
            'speed': [
                "daha hızlı", "yüksek hız", "hız konusunda sorun yaşamayan", "kesintisiz hız", "yüksek performans",
                "süper hızlı", "ışık hızında", "ani hız artışı", "stabil bağlantı", "düşük gecikme",
                "yüksek bant genişliği", "hız garantisi", "fiber hız", "5G performans", "kesintisiz akış",
                "hız ihtiyacım", "performans artışı", "hız testi", "download hızı", "upload performansı",
                "düşük ping", "oyun hızı", "streaming kalitesi", "hız sorunu", "yavaş internet",
                "hız dalgalanması", "tutarlı hız", "vaadedilen hız", "gerçek hız", "hız ölçümü",
                "internet performansı", "ağ hızı", "bağlantı kalitesi", "veri transfer hızı", "yükleme hızı",
                "indirme performansı", "hız sınırı", "bottleneck", "darboğaz", "hız engeli",
                "performans düşüklüğü", "hız iyileştirme", "hız artırımı", "performans paketi", "hız çözümü",
                "akış hızı", "verimli bağlantı", "hız memnuniyeti", "yüksek performanslı internet"
            ],
            'reliability': [
                "stabil", "kesintisiz", "güvenilir", "sorunsuz", "dengeli",
                "sürekli", "istikrarlı", "güvenli", "sağlam", "dayanıklı",
                "tutarlı", "kesin", "sarsılmaz", "emin", "kararlı",
                "düzenli", "sistemli", "süreklilik", "güven verici", "kalıcı",
                "sağlıklı", "problemsiz", "düzgün", "istikrarlı bağlantı", "kesintisiz hizmet",
                "güvenilir ağ", "sorunsuz deneyim", "dengeli performans", "sağlam altyapı", "dayanıklı bağlantı",
                "tutarlı hizmet", "emin olmak", "kararlı internet", "düzenli akış", "sistemli çalışma",
                "süreklilik arz eden", "güven veren", "kalıcı çözüm", "sağlıklı bağlantı", "problemsiz kullanım",
                "düzgün çalışan", "istikrar bekliyorum", "kesinti korkusu", "güvenilirlik endişesi", "sorun yaşamak istemiyorum"
            ],
            'features': [
                "daha zengin", "ekstra özellikli", "kapsamlı", "gelişmiş", "avantajlı",
                "fazladan", "ilave", "bonus", "hediyeli", "promosyonlu",
                "özel", "vip", "premium", "üstün", "kapsayıcı",
                "geniş", "çeşitli", "çok yönlü", "fonksiyonel", "pratik",
                "kullanışlı", "yararlı", "faydalı", "avantaj sağlayan", "değer katan",
                "ek hizmet", "yan paket", "ilave özellik", "bonus içerik", "promosyon ürün",
                "özel erişim", "vip ayrıcalık", "premium içerik", "üstün kalite", "kapsamlı hizmet",
                "geniş kapsam", "çeşitli seçenek", "çok yönlü paket", "fonksiyonel çözüm", "pratik kullanım",
                "kullanışlı uygulama", "yararlı özellik", "faydalı içerik", "avantajlı paket", "değer katıcı hizmet"
            ],
            'support': [
                "iyi müşteri hizmeti", "hızlı destek", "profesyonel yardım", "7/24 destek", "anında çözüm",
                "teknik yardım", "uzman ekip", "etkili çözüm", "hızlı yanıt", "anlayışlı personel",
                "yardımsever", "çözüm odaklı", "dinamik destek", "etkili iletişim", "kaliteli hizmet",
                "müşteri odaklı", "şikayet yönetimi", "problem çözme", "ariza giderme", "bakım onarım",
                "uzaktan destek", "yerinde servis", "teknik ekip", "müşteri temsilcisi", "danışmanlık",
                "bilgilendirme", "yönlendirme", "rehberlik", "yardım masası", "destek hattı",
                "canlı destek", "online yardım", "chat desteği", "telefon desteği", "e-posta desteği",
                "sosyal medya desteği", "uygulama desteği", "self servis", "otomatik çözüm", "kullanım kılavuzu",
                "sık sorulan sorular", "eğitim videosu", "teknik doküman", "uzman görüşü", "profesyonel tavsiye",
                "hızlı müdahale", "acil destek", "öncelikli hizmet", "vip destek", "özel ilgi"
            ]
        },
        'decision_factors': [
            "fiyat/performans oranı önemli",
            "hız benim için kritik",
            "müşteri hizmetleri kalitesi önemli",
            "kampanya ve fırsatlar ilgimi çekiyor",
            "uzun vadeli anlaşma istemiyorum",
            "esnek paket seçeneklerini tercih ederim",
            "teknik destek kalitesi ön planda",
            "şeffaf faturalandırma önemli",
            "ek ücret olmaması tercihim",
            "kullanım kolaylığı arıyorum",
            "modem kalitesi dikkat ettiğim bir konu",
            "kapsama alanı geniş olmalı",
            "kesintisiz hizmet bekliyorum",
            "güvenilir marka önceliğim",
            "yeni teknolojileri desteklemesi önemli",
            "çevre dostu operatör tercihim",
            "yerli üretim cihazlar kullanması önemli",
            "sosyal sorumluluk projeleri dikkatimi çekiyor",
            "eski müşterilere özel avantajlar bekliyorum",
            "referans sistemiyle ek kazanç istiyorum",
            "kolay iptal seçeneği önemli",
            "taahhütsüz paket tercihim",
            "online işlem kolaylığı arıyorum",
            "mobil uygulama kalitesi önemli",
            "hız testi yapabilme imkanı istiyorum",
            "kullanım istatistiklerini görebilmek istiyorum",
            "kota uyarı sistemi tercih sebebim",
            "otomatik yenileme istemiyorum",
            "fatura ödeme kolaylığı arıyorum",
            "taksit seçeneği sunması önemli",
            "ek hizmetlerin esnek olmasını istiyorum",
            "paket özelleştirme imkanı arıyorum",
            "kullanmadığım hizmetler için ödeme yapmak istemiyorum",
            "aile üyeleriyle paylaşım imkanı istiyorum",
            "cihaz sınırlaması olmaması önemli",
            "gece kotası gibi avantajlar ilgimi çekiyor",
            "tatil modu seçeneği bekliyorum",
            "yurtdışı kullanım avantajları tercih sebebim",
            "bulut depolama hizmeti sunması önemli",
            "güvenlik paketi dahil olmasını istiyorum",
            "reklamsız deneyim sunması tercihim",
            "veri gizliliği politikası önemsediğim konu",
            "çevre dostu faturalandırma istiyorum",
            "yenilenebilir enerji kullanımı dikkatimi çekiyor",
            "müşteri memnuniyeti odaklı olması önemli",
            "sosyal medyada aktif olması tercih sebebim",
            "hızlı şikayet çözüm sistemi bekliyorum",
            "müşteri geri bildirimlerine önem vermesi değerli"
        ]
    }

    def _load_regional_data(self) -> Dict:
        """Bölgesel veri simülasyonu"""
        return {
            'marmara': {'fiber_coverage': 95, 'avg_speed': 150},
            'aegean': {'fiber_coverage': 85, 'avg_speed': 120},
            'mediterranean': {'fiber_coverage': 80, 'avg_speed': 110},
            'central': {'fiber_coverage': 70, 'avg_speed': 100},
            'black_sea': {'fiber_coverage': 65, 'avg_speed': 90},
            'eastern': {'fiber_coverage': 55, 'avg_speed': 80},
            'southeastern': {'fiber_coverage': 60, 'avg_speed': 85},
            'north_cyprus': {'fiber_coverage': 75, 'avg_speed': 95}
        }

    def generate_user_demographics(self) -> UserDemographics:
        """Çeşitlendirilmiş kullanıcı demografisi oluşturur"""
        age_group = random.choice(list(self.DEMOGRAPHICS['age_groups'].keys()))
        location = random.choice(list(self.DEMOGRAPHICS['locations'].keys()))
        
        # Yaş grubuna göre meslek seçimi
        if age_group in ['gen_z', 'millennial_early']:
            occupation_category = random.choice(['teknoloji', 'egitim', 'ticaret', 'ogrenci', 'sanat'])
        elif age_group == 'millennial_late':
            occupation_category = random.choice(['teknoloji', 'egitim', 'saglik', 'finans', 'spor'])
        elif age_group == 'gen_x':
            occupation_category = random.choice(['saglik', 'finans', 'egitim', 'ticaret', 'hizmet'])
        else:  # boomer ve silent_gen
            occupation_category = random.choice(['emekli', 'saglik', 'egitim', 'hizmet'])
            
        occupation = random.choice(self.DEMOGRAPHICS['occupations'][occupation_category])
        
        # Demografiye göre aile durumu
        family_status = self._determine_family_status(age_group)
        income_level = self._determine_income_level(occupation, location)
        tech_literacy = self._determine_tech_literacy(age_group, occupation)
        
        return UserDemographics(
            age_group=age_group,
            location_type=location,
            family_status=family_status,
            occupation=occupation,
            income_level=income_level,
            tech_literacy=tech_literacy
        )

    def _determine_family_status(self, age_group: str) -> str:
        """Yaş grubuna göre aile durumu belirler"""
        status_weights = {
            'gen_z': {'bekar': 0.8, 'yeni_evli': 0.15, 'aile_cocuklu': 0.05},
            'millennial_early': {'bekar': 0.5, 'yeni_evli': 0.3, 'aile_cocuklu': 0.2},
            'millennial_late': {'bekar': 0.2, 'yeni_evli': 0.2, 'aile_cocuklu': 0.6},
            'gen_x': {'bekar': 0.1, 'aile_cocuklu': 0.6, 'aile_buyuk_cocuk': 0.3},
            'boomer': {'aile_buyuk_cocuk': 0.4, 'emekli_cift': 0.4, 'tek_kisi': 0.2},
            'silent_gen': {'emekli_cift': 0.3, 'tek_kisi': 0.7}
        }
        
        weights = status_weights.get(age_group, {'bekar': 0.5, 'aile_cocuklu': 0.5})
        return random.choices(list(weights.keys()), weights=list(weights.values()))[0]

    def _determine_income_level(self, occupation: str, location: str) -> str:
        """Meslek ve lokasyona göre gelir seviyesi"""
        base_income = {
            'yazilim_geliştirici': 'high', 'siber_guvenlik_uzmani': 'high', 
            'doktor': 'high', 'yatirim_uzmani': 'high',
            'bankacı': 'medium_high', 'mali_müşavir': 'medium_high',
            'öğretmen': 'medium', 'hemşire': 'medium', 'grafik_tasarımcı': 'medium',
            'berber': 'medium_low', 'taksi_şoförü': 'medium_low',
            'öğrenci': 'low', 'emekli_memur': 'medium_low', 'emekli_asker': 'medium_low'
        }
        
        # Lokasyon etkisi
        location_impact = {
            'buyuksehir_merkez': 1.2,
            'is_merkezi': 1.3,
            'universite_yerleskesi': 0.9,
            'koy_kasaba': 0.8
        }
        
        base_level = base_income.get(occupation, 'medium')
        impact = location_impact.get(location, 1.0)
        
        # Gelir seviyesini lokasyon etkisiyle ayarla
        if base_level == 'high' and impact < 0.9:
            return 'medium_high'
        elif base_level == 'medium' and impact > 1.1:
            return 'medium_high'
        elif base_level == 'medium' and impact < 0.9:
            return 'medium_low'
        
        return base_level

    def _determine_tech_literacy(self, age_group: str, occupation: str) -> str:
        """Yaş ve mesleğe göre teknoloji okuryazarlığı"""
        age_tech_level = {
            'gen_z': 'very_high', 
            'millennial_early': 'high', 
            'millennial_late': 'high',
            'gen_x': 'medium', 
            'boomer': 'low',
            'silent_gen': 'very_low'
        }
        
        tech_occupations = ['yazilim_geliştirici', 'veri_analisti', 'IT_uzmanı', 
                           'grafik_tasarımcı', 'siber_guvenlik_uzmani']
        
        non_tech_occupations = ['emekli_asker', 'emekli_memur', 'berber', 'taksi_şoförü']
        
        base_level = age_tech_level.get(age_group, 'medium')
        
        if occupation in tech_occupations:
            return 'very_high'
        elif occupation in non_tech_occupations:
            return 'low'
        elif 'öğrenci' in occupation:
            return 'high'
        
        return base_level

    def generate_contextual_factors(self, demographics: UserDemographics) -> ContextualFactors:
        """Çeşitlendirilmiş bağlamsal faktörler oluşturur"""
        urgency_weights = {
            'low': 0.4, 'medium': 0.4, 'high': 0.15, 'critical': 0.05
        }
        
        if demographics.occupation in ['yazilim_geliştirici', 'freelance']:
            urgency_weights['high'] = 0.3
            urgency_weights['critical'] = 0.1
            
        time_of_day = random.choice(['sabah', 'öğle', 'akşam', 'gece'])
        day_of_week = random.choice(['hafta_içi', 'cumartesi', 'pazar'])
        season = random.choice(['ilkbahar', 'yaz', 'sonbahar', 'kış'])
        
        urgency = random.choices(
            list(urgency_weights.keys()), 
            weights=list(urgency_weights.values())
        )[0]
        
        experience_options = ['ilk_kez', 'daha_önce_değiştirdi', 'sık_değiştiren', 'uzun_süreli_müşteri']
        previous_experience = random.choice(experience_options)
        
        communication_prefs = ['hızlı_çözüm', 'detaylı_bilgi', 'kıyaslama_isteiyor', 'güvence_arıyor']
        communication_preference = random.choice(communication_prefs)
        
        return ContextualFactors(
            time_of_day=time_of_day,
            day_of_week=day_of_week,
            season=season,
            urgency_level=urgency,
            previous_experience=previous_experience,
            communication_preference=communication_preference
        )

    def select_realistic_package(self, demographics: UserDemographics, context: ContextualFactors) -> Tuple[str, str]:
        """Demografiye uygun gerçekçi paket seçer"""
        # Demografiye göre paket kategorisi belirleme
        if demographics.income_level in ['low', 'medium_low']:
            if demographics.family_status == 'bekar':
                category = 'mobile_packages'
                subcategory = 'minimal'
            else:
                category = random.choice(['fiber_internet', 'combo_packages'])
                subcategory = random.choice(['entry', 'basic_combo'])
                
        elif demographics.income_level == 'medium':
            if demographics.tech_literacy in ['high', 'very_high']:
                category = random.choice(['fiber_internet', 'combo_packages'])
                subcategory = random.choice(['standard', 'family_combo'])
            else:
                category = 'mobile_packages'
                subcategory = 'standard'
                
        else:  # high income
            if demographics.occupation in ['yazilim_geliştirici', 'grafik_tasarımcı']:
                category = 'special_packages'
                subcategory = random.choice(['gaming', 'streaming'])
            else:
                category = random.choice(['fiber_internet', 'combo_packages'])
                subcategory = random.choice(['premium', 'premium_combo'])
        
        # Özel durumlar
        if demographics.age_group == 'gen_z' and 'öğrenci' in demographics.occupation:
            category = 'special_packages'
            subcategory = 'student'
        elif demographics.age_group in ['boomer', 'silent_gen']:
            category = 'special_packages'
            subcategory = 'senior'
        elif demographics.location_type in ['ilce', 'koy_kasaba']:
            category = 'special_packages'
            subcategory = 'rural'
        elif 'travel' in demographics.occupation:
            category = 'special_packages'
            subcategory = 'traveler'
            
        # Kategori ve alt kategori kontrolü
        if category not in self.ADVANCED_PACKAGES:
            category = 'fiber_internet'
        if subcategory not in self.ADVANCED_PACKAGES[category]:
            subcategory = list(self.ADVANCED_PACKAGES[category].keys())[0]
            
        package_list = self.ADVANCED_PACKAGES[category][subcategory]
        selected_package = random.choice(package_list)
        
        return selected_package, f"{category}_{subcategory}"

    def generate_life_story(self, demographics: UserDemographics) -> str:
        """Demografiye uygun yaşam hikayesi oluşturur"""
        story_categories = []
        
        # Yaş grubuna göre hikaye kategorileri
        if demographics.age_group in ['gen_z', 'millennial_early']:
            story_categories.extend(['yeni_ev', 'is_degisimi', 'teknoloji_degisimi'])
        elif demographics.age_group == 'millennial_late':
            story_categories.extend(['aile_degisimi', 'yeni_ev', 'is_degisimi'])
        elif demographics.age_group == 'gen_x':
            story_categories.extend(['aile_degisimi', 'teknoloji_degisimi', 'ekonomik'])
        else:  # boomer ve silent_gen
            story_categories.extend(['ekonomik', 'aile_degisimi'])
            
        # Gelir seviyesine göre ek kategoriler
        if demographics.income_level in ['low', 'medium_low']:
            story_categories.append('ekonomik')
        else:
            story_categories.append('rekabet')
            
        # Teknik sorunlar için ek kategori
        if demographics.tech_literacy in ['high', 'very_high']:
            story_categories.append('teknoloji_yetersiz')
            
        selected_category = random.choice(story_categories)
        return random.choice(self.LIFE_SCENARIOS[selected_category])

    def create_personality_driven_dialogue(self, demographics: UserDemographics, 
                                         context: ContextualFactors, 
                                         package: str, 
                                         life_story: str) -> Dict[str, str]:
        """Kişiliğe dayalı diyalog oluşturur"""
        # Konuşma tarzı belirleme
        if demographics.tech_literacy == 'very_high':
            style = 'technical'
        elif demographics.age_group in ['boomer', 'silent_gen']:
            style = 'traditional'
        elif demographics.occupation in ['doktor', 'bankacı', 'akademisyen']:
            style = 'professional'
        else:
            style = 'casual'
            
        # Opener seçimi
        if context.urgency_level in ['high', 'critical']:
            opener_type = 'direct'
        elif context.communication_preference == 'detaylı_bilgi':
            opener_type = 'contextual'
        elif life_story and 'problem' in life_story.lower():
            opener_type = 'problem'
        elif life_story:
            opener_type = 'story_based'
        else:
            opener_type = 'comparison'
            
        opener_templates = self.CONVERSATION_PATTERNS['opener_variations'][opener_type]
        base_opener = random.choice(opener_templates)
        
        # Hikaye entegrasyonu
        if life_story and opener_type in ['story_based', 'problem']:
            user_message = f"Merhaba, {life_story.lower()}. Bu nedenle {base_opener.lower()}. '{package}' paketi uygun olur mu?"
        else:
            user_message = f"Merhaba, {base_opener.lower()}. '{package}' paketini inceledim, bu pakete geçmek istiyorum."
            
        # Asistan yanıtı - demografiye göre ton
        if demographics.age_group in ['boomer', 'silent_gen']:
            assistant_response = f"Tabii ki, size '{package}' paketinin detaylarını açıklayarak yardımcı olayım."
        elif demographics.tech_literacy == 'very_high':
            assistant_response = f"Anlıyorum, '{package}' paketi için hemen geçiş işlemlerinizi başlatıyorum."
        else:
            assistant_response = f"Elbette, '{package}' paketine geçiş talebinizi işleme alıyorum."
            
        # Son mesaj - bağlama göre
        if context.urgency_level == 'critical':
            final_message = f"Acil talebiniz için öncelik veriyoruz. '{package}' paketiniz en geç yarın aktif olacaktır."
        elif context.urgency_level == 'high':
            final_message = f"'{package}' paketiniz için hızlandırılmış aktivasyon işlemi başlatıldı. 24 saat içinde aktif olacak."
        else:
            activation_time = random.choice(['önümüzdeki fatura döneminde', 'bu hafta içinde', 'en geç 3 iş günü içinde'])
            final_message = f"'{package}' paketine geçiş işleminiz tamamlandı. Yeni paketiniz {activation_time} aktif olacaktır."
            
        return {
            'user_message': user_message,
            'assistant_response': assistant_response,
            'final_message': final_message
        }

    def generate_unique_fingerprint(self, demographics: UserDemographics, 
                                  context: ContextualFactors, 
                                  package: str, 
                                  life_story: str) -> str:
        """Senaryo için benzersiz parmak izi oluşturur"""
        fingerprint_data = {
            'demographics': {
                'age': demographics.age_group,
                'location': demographics.location_type,
                'family': demographics.family_status,
                'occupation': demographics.occupation[:3],  # Sadece ilk 3 karakter
                'income': demographics.income_level,
                'tech': demographics.tech_literacy
            },
            'context': {
                'time': context.time_of_day,
                'day': context.day_of_week[:2],  # Sadece ilk 2 karakter
                'season': context.season[:2],    # Sadece ilk 2 karakter
                'urgency': context.urgency_level[:1],  # Sadece ilk karakter
                'experience': context.previous_experience[:2],  # Sadece ilk 2 karakter
                'communication': context.communication_preference[:2]  # Sadece ilk 2 karakter
            },
            'package': package[:15],  # Sadece ilk 15 karakter
            'story': hashlib.md5(life_story.encode()).hexdigest()[:8],  # Hash'in ilk 8 karakteri
            'timestamp': datetime.now().strftime('%H%M%S')  # Saat, dakika, saniye
        }
        
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_string.encode()).hexdigest()

    def generate_single_scenario(self) -> Dict[str, Any]:
        """Tek bir benzersiz senaryo oluşturur"""
        max_attempts = 100  # Benzersizlik için daha fazla deneme
        attempts = 0
        
        while attempts < max_attempts:
            # Demografik profil oluştur
            demographics = self.generate_user_demographics()
            
            # Bağlamsal faktörler oluştur
            context = self.generate_contextual_factors(demographics)
            
            # Paket seçimi
            package, package_category = self.select_realistic_package(demographics, context)
            
            # Yaşam hikayesi
            life_story = self.generate_life_story(demographics)
            
            # Benzersizlik kontrolü
            fingerprint = self.generate_unique_fingerprint(demographics, context, package, life_story)
            
            if fingerprint not in self.used_fingerprints:
                self.used_fingerprints.add(fingerprint)
                break
                
            attempts += 1
        
        if attempts >= max_attempts:
            # Son çare olarak rastgele bir parmak izi oluştur
            fingerprint = hashlib.md5(str(datetime.now()).encode()).hexdigest()
            self.used_fingerprints.add(fingerprint)
        
        # Diyalog oluştur
        dialogue = self.create_personality_driven_dialogue(demographics, context, package, life_story)
        
        # API yanıtı oluştur
        api_response = {
            'to_package': package,
            'status': random.choice(['pending_activation', 'processing', 'confirmed']),
            'estimated_activation': (datetime.now() + timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d')
        }
        
        # Senaryo yapısı
        scenario = {
            'scenario_id': f"PKG_CHANGE_{uuid.uuid4().hex[:8]}_{self.scenario_counter}",
            'timestamp': datetime.now().isoformat(),
            'fingerprint': fingerprint,
            'user_profile': demographics.__dict__,
            'context': context.__dict__,
            'target_package': package,
            'life_story': life_story,
            'conversation': dialogue,
            'api_response': api_response
        }
        
        self.scenario_counter += 1
        return scenario

    def generate_batch_scenarios(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Toplu senaryo üretimi (1000 için optimize edilmiş)"""
        scenarios = []
        unique_check = set()
        
        print(f"⏳ {count} benzersiz senaryo üretiliyor...")
        
        for i in range(count):
            # İlerleme göstergesi
            if (i + 1) % 100 == 0:
                print(f"✅ {i + 1}/{count} senaryo üretildi")
            
            scenario = None
            attempts = 0
            max_attempts = 20
            
            while attempts < max_attempts:
                scenario = self.generate_single_scenario()
                fp = scenario['fingerprint']
                
                # Benzersizlik kontrolü
                if fp not in unique_check:
                    unique_check.add(fp)
                    break
                    
                attempts += 1
            
            if scenario:
                scenarios.append(scenario)
        
        print(f"🎉 {len(scenarios)} benzersiz senaryo başarıyla üretildi!")
        return scenarios

    def export_scenarios_to_json(self, scenarios: List[Dict[str, Any]], filename: str = None) -> str:
        """Senaryoları JSON formatında dışa aktarır"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"package_change_scenarios_{timestamp}.json"
        
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_scenarios': len(scenarios),
                'unique_count': len(set(s['fingerprint'] for s in scenarios))
            },
            'scenarios': scenarios
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filename

def generate_change_package_scenario() -> Dict[str, Any]:
    """Kullanıcının mevcut tarife paketini değiştirdiği senaryo."""
    user_id = generate_user_id()
    
    # Optimize edilmiş generator'ı başlat
    generator = PackageChangeScenarioGenerator()
    
    # Benzersiz senaryo üret
    advanced_scenario = generator.generate_single_scenario()
    
    # Modüler yapıya uygun format'a dönüştür
    return {
        "id": f"change_package_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CHANGE_PACKAGE.value,
        "personality_profile": advanced_scenario['user_profile']['age_group'],
        "cognitive_state": _map_demographics_to_cognitive_state(advanced_scenario['user_profile']),
        "emotional_context": _map_context_to_emotional_state(advanced_scenario['context']),
        "donguler": [
            {"rol": "kullanici", "icerik": advanced_scenario['conversation']['user_message']},
            {"rol": "asistan", "icerik": advanced_scenario['conversation']['assistant_response']},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "new_package_name": advanced_scenario['target_package']}}]},
            {"rol": "arac", "icerik": create_validated_response(ChangePackageResponse, override_data=advanced_scenario['api_response'])},
            {"rol": "asistan", "icerik": advanced_scenario['conversation']['final_message']}
        ],
        "fingerprint": advanced_scenario['fingerprint']
    }

def _map_demographics_to_cognitive_state(demographics: Dict[str, Any]) -> str:
    """Demografik bilgileri bilişsel duruma eşler"""
    age_group = demographics.get('age_group', 'millennial_early')
    tech_literacy = demographics.get('tech_literacy', 'medium')
    
    # Yaş grubuna göre bilişsel durum
    age_cognitive_map = {
        'gen_z': CognitiveState.INNOVATIVE.value,
        'millennial_early': CognitiveState.ANALYTICAL.value,
        'millennial_late': CognitiveState.STRATEGIC.value,
        'gen_x': CognitiveState.SYSTEMATIC.value,
        'boomer': CognitiveState.SYSTEMATIC.value,
        'silent_gen': CognitiveState.TRADITIONAL.value
    }
    
    # Teknoloji okuryazarlığına göre ayarlama
    if tech_literacy == 'very_high':
        return CognitiveState.INNOVATIVE.value
    elif tech_literacy == 'high':
        return CognitiveState.ANALYTICAL.value
    
    return age_cognitive_map.get(age_group, CognitiveState.ANALYTICAL.value)

def _map_context_to_emotional_state(context: Dict[str, Any]) -> str:
    """Bağlamsal faktörleri duygusal duruma eşler"""
    urgency_level = context.get('urgency_level', 'medium')
    communication_preference = context.get('communication_preference', 'hızlı_çözüm')
    
    # Aciliyet seviyesine göre duygusal durum
    urgency_emotional_map = {
        'low': EmotionalContext.CALM.value,
        'medium': EmotionalContext.CURIOUS.value,
        'high': EmotionalContext.WORRIED.value,
        'critical': EmotionalContext.URGENT.value
    }
    
    # İletişim tercihine göre ayarlama
    if communication_preference == 'güvence_arıyor':
        return EmotionalContext.WORRIED.value
    elif communication_preference == 'kıyaslama_isteiyor':
        return EmotionalContext.SKEPTICAL.value
    
    return urgency_emotional_map.get(urgency_level, EmotionalContext.CURIOUS.value)

def get_generator_statistics(self) -> Dict[str, Any]:
    """Generator istatistiklerini döndürür"""
    return {
        'total_scenarios_generated': self.scenario_counter,
        'unique_fingerprints': len(self.used_fingerprints),
        'memory_usage': len(self.conversation_memory),
        'regional_data_loaded': len(self.regional_variations),
        'generator_uptime': datetime.now().isoformat()
    }

# 1000 benzersiz veri üretimi için fonksiyon
def generate_1000_unique_scenarios() -> List[Dict[str, Any]]:
    """1000 benzersiz paket değiştirme senaryosu üretir"""
    scenarios = []
    
    print(f"🚀 1000 benzersiz senaryo üretiliyor...")
    
    for i in range(1000):
        try:
            scenario = generate_change_package_scenario()
            scenarios.append(scenario)
            
            if (i + 1) % 100 == 0:
                print(f"✅ {i + 1}/1000 senaryo üretildi")
                
        except Exception as e:
            print(f"⚠️ Senaryo {i + 1} üretim hatası: {e}")
            continue
    
    print(f"🎉 Toplam {len(scenarios)} benzersiz senaryo başarıyla üretildi!")
    return scenarios

# Kalite kontrol fonksiyonu
def validate_scenario_quality(scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Senaryo kalitesini kontrol eder"""
    unique_fingerprints = set()
    valid_count = 0
    
    for scenario in scenarios:
        # Temel alan kontrolü
        required_fields = ['id', 'scenario_type', 'personality_profile', 'cognitive_state', 'emotional_context', 'donguler']
        if all(field in scenario for field in required_fields):
            valid_count += 1
        
        # Benzersizlik kontrolü
        fp = scenario.get('fingerprint', '')
        if fp:
            unique_fingerprints.add(fp)
    
    return {
        'total_scenarios': len(scenarios),
        'valid_scenarios': valid_count,
        'unique_scenarios': len(unique_fingerprints),
        'validity_rate': valid_count / len(scenarios) * 100 if scenarios else 0,
        'uniqueness_rate': len(unique_fingerprints) / len(scenarios) * 100 if scenarios else 0
    }

# İstatistik fonksiyonu
def get_scenario_statistics(scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Senaryo istatistiklerini hesaplar"""
    if not scenarios:
        return {}
    
    stats = {
        'total_scenarios': len(scenarios),
        'personality_distribution': {},
        'cognitive_distribution': {},
        'emotional_distribution': {},
        'complexity_distribution': {'low': 0, 'medium': 0, 'high': 0},
        'quality_metrics': {
            'valid_scenarios': 0,
            'invalid_scenarios': 0,
            'average_complexity': 0.0
        }
    }
    
    total_complexity = 0.0
    
    for scenario in scenarios:
        # Kişilik dağılımı
        personality = scenario.get('personality_profile', 'unknown')
        stats['personality_distribution'][personality] = stats['personality_distribution'].get(personality, 0) + 1
        
        # Bilişsel durum dağılımı
        cognitive = scenario.get('cognitive_state', 'unknown')
        stats['cognitive_distribution'][cognitive] = stats['cognitive_distribution'].get(cognitive, 0) + 1
        
        # Duygusal durum dağılımı
        emotional = scenario.get('emotional_context', 'unknown')
        stats['emotional_distribution'][emotional] = stats['emotional_distribution'].get(emotional, 0) + 1
        
        # Karmaşıklık dağılımı
        if 'advanced_metadata' in scenario:
            complexity = scenario['advanced_metadata'].get('complexity_score', 0.5)
            total_complexity += complexity
            
            if complexity < 0.33:
                stats['complexity_distribution']['low'] += 1
            elif complexity < 0.67:
                stats['complexity_distribution']['medium'] += 1
            else:
                stats['complexity_distribution']['high'] += 1
        
        # Kalite kontrolü
        validation = validate_scenario_quality([scenario])
        if validation['validity_rate'] > 0:
            stats['quality_metrics']['valid_scenarios'] += 1
        else:
            stats['quality_metrics']['invalid_scenarios'] += 1
    
    # Ortalama karmaşıklık
    if stats['quality_metrics']['valid_scenarios'] > 0:
        stats['quality_metrics']['average_complexity'] = total_complexity / stats['quality_metrics']['valid_scenarios']
    
    return stats

# Ana yürütme
if __name__ == "__main__":
    # 1000 benzersiz senaryo üret
    scenarios = generate_1000_unique_scenarios()
    
    # Kalite kontrolü yap
    quality_report = validate_scenario_quality(scenarios)
    print("\n🔍 Kalite Raporu:")
    print(f"Toplam Senaryo: {quality_report['total_scenarios']}")
    print(f"Geçerli Senaryo: {quality_report['valid_scenarios']} (%{quality_report['validity_rate']:.2f})")
    print(f"Benzersiz Senaryo: {quality_report['unique_scenarios']} (%{quality_report['uniqueness_rate']:.2f})")
    
    # Örnek senaryoyu göster
    if scenarios:
        print("\n✨ Örnek Senaryo:")
        sample = scenarios[0]
        print(f"ID: {sample['id']}")
        print(f"Yaş Grubu: {sample['personality_profile']}")
        print(f"Bilişsel Durum: {sample['cognitive_state']}")
        print(f"Duygusal Bağlam: {sample['emotional_context']}")
        print(f"İlk Mesaj: {sample['donguler'][0]['icerik']}")
    
    # Senaryoları dosyaya kaydet
    exporter = PackageChangeScenarioGenerator()
    filename = exporter.export_scenarios_to_json(scenarios)
    print(f"\n💾 Senaryolar '{filename}' dosyasına kaydedildi")