# 🚁 LifeScan-Webots: Otonom Arama ve Enkaz Altı Canlı Tespiti Simülasyonu

[![Webots Versiyonu](https://img.shields.io/badge/Webots-R2025a-blue?style=for-the-badge&logo=cyberbotics)](https://cyberbotics.com/)
[![Dil](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![Lisans](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=openedx)](https://opensource.org/licenses/MIT)

---

## 📌 1. Proje Amacı ve Kapsamı
**LifeScan-Webots**, afet sonrası (deprem, sel, göçük vb.) fiziki olarak girilmesi tehlikeli veya imkansız olan enkaz bölgelerinde hızlı keşif ve hayat belirtisi tespiti yapabilen otonom/yarı-otonom bir drone kontrol sistemidir. 

Projenin temel misyonu, arama-kurtarma ekipleri sahaya girmeden önce kritik verileri (canlı türü, anlık koordinatlar ve ulaşım rotaları) güvenli bir mesafeden toplayarak **"altın saatler" (golden hours)** içinde müdahale verimliliğini maksimize etmektir.

---

## ⚙️ 2. Kullanılan Teknolojiler ve Araçlar

* **Simülasyon Platformu:** Cyberbotics Webots R2025a robotik simülasyon ortamı.
* **Hava Aracı Modeli:** DJI Mavic 2 Pro (Fiziksel tork, aerodinamik sürtünme ve motor atalet matrisleri simüle edilmiş quadcopter platformu).
* **Geliştirme Dili:** Python 3.x (Sensör veri işleme, PID kontrol döngüsü ve Supervisor analitiği).
* **Algılama Metodolojisi:** Koordinat Bazlı Yakınlık Analizi (Proximity & Spatial Data Fusion).

---

## 🧠 3. Sistem Mimarisi ve Kararlılık Optimizasyonları

Projenin kararlı uçuş algoritması, geleneksel quadcopter zafiyetlerini ortadan kaldırmak için özelleştirilmiş 4 eksenli (Roll, Pitch, Yaw, Altitude) bir PID denetleyici mimarisine sahiptir:
                                                          ┌──────────────────────────────────────────┐
                                                          
                                                          │          Klavye / Otonom Girdi           │
                                                          
                                                          └────────────────────┬─────────────────────┘
                                                                               │
                                                                               ▼
                                            ┌──────────────────────────────────────────────────────────────────────────────────┐
                                            │                           PID Kontrolör Matrisi                                  │
                                            │   k_vertical_p = 1.0  |  k_roll_p = 40.0  |  k_pitch_p = 25.0  |  k_yaw_p = 1.0  │
                                            └────────────────────────────────────┬─────────────────────────────────────────────┘
                                                                                 │
                                                                                 ▼
                                                            ┌──────────────────────────────────────────┐
                                                            │    Yazılımsal Durum Hafızası (Filter)    │
                                                            └────────────────────┬─────────────────────┘
                                                                                 │
                                                                                 ▼
                                                            ┌──────────────────────────────────────────┐
                                                            │      Doyum ve Limit Kırpma (Clamp)       │
                                                            └────────────────────┬─────────────────────┘
                                                                                 │
                                                                                 ▼
                                                            ┌──────────────────────────────────────────┐
                                                            │    DJI Mavic 2 Pro Motor Sürücüleri      │
                                                            └──────────────────────────────────────────┘

### 🛡️ Kritik Geliştirmeler ve Mühendislik Çözümleri
1. **Vortex Ring State (Girdap Halkası / Türbülans) Koruması:** Dronun dikey alçalma (*descent*) esnasında kendi pervanelerinin ürettiği kirli ve türbülanslı hava akımına gömülerek ani tork kaybı yaşaması ve takla atarak düşmesi engellenmiştir. Dikey eksen kazancı `k_vertical_p = 1.0` seviyesine çekilmiş ve kübik kontrol formülünün alt sınırı `-0.4` olarak maskelenerek dronun paraşüt kararlılığında süzülmesi sağlanmıştır.
2. **Akıllı Klavye Filtreleme (Edge-Triggering):** Webots simülasyon döngüsünün (*timestep*) insani reflekslerden çok daha hızlı akması nedeniyle oluşan mükerrer komut basımları (bouncing etkisi) yazılımsal durum hafızası (`last_key`) kullanılarak çözülmüştür. Yükseklik ve dönüş komutları her basışta tam adımlı (Örn: Tam 2 derece hassas dönüş) işletilir.
3. **Zıt Tork ve Yön Senkronizasyonu:** Saat yönünde (CW) ve tersi yönünde (CCW) dönen motorların dinamik tork salınımları, motor güç dağılım matrisindeki matematiksel işaret sabitlemeleriyle dengelenmiştir.

---

## 🔍 4. Algılama ve Supervisor (Gözlemci) Katmanı

Projede başlangıçta planlanan termal/sıcaklık sensör mimarisi yerine, donanım kısıtları ve simülasyon doğruluğu göz önüne alınarak **Ultrasonic Distance Sensor** tabanlı çalışan ve hava aracına fiziksel yük bindirmeyen harici bir **Supervisor (Gözlemci)** katmanına geçiş yapılmıştır.

* **Enkaz Altı Tespiti:** Canlı modelleri (Kedi, Köpek, İnsan) görsel temasın mümkün olmadığı, çeşitli katı nesnelerin ve enkaz yapılarının altındaki kör noktalara yerleştirilmiştir.
* **Veri Füzyonu:** Supervisor katmanı, dronun GPS ve IMU verilerini anlık okuyarak sahnedeki canlıların mutlak konumlarıyla haritalandırır. Mesafe kritik eşiğin altına düştüğü an sinyal dalga boyu analizini simüle ederek enkaz altındaki canlının türünü raporlar.
* **Tespit Edilen Varlıklar:** Canlılar (İnsan, Kedi, Köpek) ve Tahliye Ekipmanları (Scooter).

---

## 📹 5. Sistem Çalışma Demosu

> Dronun kalkış, havada sabit asılı kalma (*hovering*), eksenel hassas dönüş, süzülerek alçalma ve eş zamanlı enkaz altı canlı algılama aşamalarını içeren güncel uçuş simülasyonu görüntüsü:

  ![LifeScan Dron Uçuş Kontrolü ve Hedef Algılama Gösterimi](media/dron.gif)

---

## 🎮 6. Manuel Kontrol Komutları Matrisi

Simülasyonda manuel müdahale gerçekleştirmek için 3D ekrana bir kez tıkladıktan sonra aşağıdaki tuş takımı kombinasyonları kullanılabilir:

| Komut Sınıfı | Tuş Kombinasyonu | Fonksiyonel Etki | Çalışma Modu |
| :--- | :--- | :--- | :--- |
| **İleri Git 🔼** | `YUKARI OK` | Pitch açısını öne eğer, ileri doğrusal hız üretir. | Dinamik (Basılı Tuttukça) |
| **Geri Git 🔽** | `AŞAĞI OK` | Pitch açısını arkaya eğer, geri doğrusal hız üretir. | Dinamik (Basılı Tuttukça) |
| **Sola Dönüş ↩️** | `SOL OK` | Kendi ekseninde sola hassas **2.3°** açı verir. | Adımsal (Tek Tetikleme) |
| **Sağa Dönüş ↪️** | `SAĞ OK` | Kendi ekseninde sağa hassas **2.3°** açı verir. | Adımsal (Tek Tetikleme) |
| **Yüksel ⏫** | `SHIFT + YUKARI OK` | Hedef irtifayı pürüzsüz şekilde artırır. | Adımsal (Tek Tetikleme) |
| **Alçal ⏬** | `SHIFT + AŞAĞI OK` | Türbülans korumalı, emniyetli çöküş sağlar. | Adımsal (Tek Tetikleme) |
| **Sola Kayma ◀️** | `SHIFT + SOL OK` | Roll açısını sola yatırarak yatay eksende süzülür. | Dinamik (Basılı Tuttukça) |
| **Sağa Kayma ▶️** | `SHIFT + SAĞ OK` | Roll açısını sağa yatırarak yatay eksende süzülür. | Dinamik (Basılı Tuttukça) |

---

## 📊 7. Elde Edilen Bulgular ve Raporlama (Terminal)

Simülasyonun kararlı çalışma döngüsü esnasında telemetri ve supervisor katmanından anlık olarak alınan gerçek zamanlı çıktı akışı aşağıda listelenmiştir:

```log
⌛ Raporlama Merkezi: Dronun kalkması bekleniyor ...
=============================================
--- 🎉✨ GÜVENLİ PID UÇUŞ SİSTEMİ AKTİF ---
🫵 Dronu kontrol etmek için 3D ekrana bir kez tıklayın.
🧾 Komut Listesi:
  - YUKARI OK      🔼 : İleri git
  - AŞAĞI OK       🔽 : Geri git
  - SOL OK         ↩️  : Kendi ekseninde sola 1-2 derece dön 
  - SAĞ OK         ↪️  : Kendi ekseninde sağa 1-2 derece dön 
  - SHIFT + YUKARI ⏫ : Yüksel
  - SHIFT + AŞAĞI  ⏬ : Alçal
  - SHIFT + SOL    ◀️  : Sola yatay kay (Strafe)
  - SHIFT + SAĞ    ▶️  : Sağa yatay kay (Strafe)
=============================================
=============================================
--- 🚀 Raporlama Merkezi: Akıllı Filtreleme Aktif ---
🪁 Dron kalkışını tamamladı.
🎑 Menzil Kontrolü: Dron konum merkezli 4 metre yarıçaplı alan içindeki canlılar tespit ediliyor...
=============================================
🚨 YENİ CANLI TESPİT EDİLDİ:
 🐶 [Köpek] - 🚩 Konum: X=1.0, Z=0.0
🚨 YENİ CANLI TESPİT EDİLDİ:
 🐱 [Kedi] - 🚩 Konum: X=-2.7, Z=0.0
🚨 YENİ CANLI TESPİT EDİLDİ:
 🚵‍♀️ [İnsan / Scooter] - 🚩 Konum: X=4.9, Z=0.2
=============================================
[Komut] Sağa Hassas Dönüş ↪️ Hedef Açı: -2.3°
[Komut] Sağa Hassas Dönüş ↪️ Hedef Açı: -4.6°
[Komut] Sağa Hassas Dönüş ↪️ Hedef Açı: -6.9°
[Komut] Sağa Hassas Dönüş ↪️ Hedef Açı: -9.2°
[Komut] Sola Hassas Dönüş ↩️ Hedef Açı: -6.9°
```        

## 📂 8. Proje Dosya Yapısı (Directory Tree)

Proje deposunun organizasyonu, Webots hazır "City" şablonu üzerine inşa edilen çevre elemanları ve modüler bileşenlerin dağılımı şu şekildedir:

```text
LifeScan-Webots/
│
├── worlds/                          # Simülasyon dünyasını barındıran klasör
│   ├── city_net/
│   ├── .city.jpg
│   ├── .city.wbproj                 # Webots dünyaya ait görünüm ve proje ayarları dosyası
│   └── city.wbt                     # Üzerinde oynama yapılan, enkaz ve canlıların eklendiği ana şehir sahnesi
│
├── controllers/                     # Robot kontrolör kodları (Beyin Katmanı)
│   │
│   ├── dron_klavye/                 # DJI Mavic 2 Pro için geliştirilen ana uçuş kontrolörü
│   │   └── dron_klavye.py           # PID, Edge-Triggering klavye filtrelemesini içeren Python kodu
│   │
│   ├── Robot_kontrol/               # Sahneyi dışarıdan izleyen akıllı gözlemci katmanı
│   │   └── Robot_kontrol.py         # Yakınlık analizi yapan ve terminale alarm basan Python kodu
│   │
│   ├── mavic2pro/                   # DJI Mavic 2 Pro dahili kinematik kütüphane/kontrolör klasörü
│   │
│   # --- Webots City Şablonu ile Gelen Standart Çevre Kontrolörleri ---
│   ├── autonomous_vehicle/          # Sahnedeki otonom araçların hareket kontrol birimi
│   ├── crossroads_traffic_lights/   # Büyük kavşak trafik ışıkları senkronizasyon klasörü
│   └── generic_traffic_light/       # Standart/generic trafik lambası yönetim klasörü
│
│
├── media/                           # Dokümantasyon görselleri ve medya dosyaları
│   └── dron.gif             # README'de görüntülenen sistem çalışma demosu
│
├── plugins/                         # Şehir trafiği ve fizik motoru için Webots eklentileri
│   └── robot_windows/               # Standart araç kontrol pencereleri arayüz eklentileri
│
├── README.md                        # Detaylı proje raporu ve kullanım kılavuzu
└── .gitignore                       # Git takibine takılmaması gereken Webots log/cache dosyaları
