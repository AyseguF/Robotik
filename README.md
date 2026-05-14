# 🚁 LifeScan-Webots: Otonom Arama ve Enkaz Altı Canlı Tespiti Simülasyonu

# 1. Proje Amacı ve Kapsamı

Bu proje, afet sonrası (deprem, sel vb.) ulaşılması zor enkaz bölgelerinde hızlı keşif ve hayat belirtisi tespiti yapabilen otonom bir drone sisteminin simülasyonudur. Projenin temel amacı, arama-kurtarma ekiplerinin riskli bölgelere girmeden önce kritik verileri (canlı konumu, ulaşım yolları) güvenli bir mesafeden toplamasını sağlamaktır.

# 2. Kullanılan Teknolojiler ve Araçlar
*Simülasyon Ortamı: Webots R2023b

* Hava Aracı: DJI Mavic 2 Pro (Dengelenmiş uçuş dinamikleri ile)

* Programlama Dilleri:

  * C: Dronun stabilizasyonu ve klavye/otonom uçuş kontrolleri.

  * Python: Veri analizi, mesafe hesaplamaları ve raporlama birimi (Supervisor).

* Algılama Metodolojisi: Koordinat Bazlı Yakınlık Analizi (Proximity Analysis).

# 3. Sistem Mimarisi ve Sensörler
Proje, donanım verimliliğini maksimize etmek için hiyerarşik bir yapıda tasarlanmıştır:

* Mesafe ve Engel Algılama: Projede başlangıçta planlanan sıcaklık sensörü yerine, donanım kısıtları ve simülasyon doğruluğu göz önüne alınarak Ultrasonic Distance Sensor mantığına geçiş yapılmıştır. Bu sayede dron, çevresindeki engelleri ve hedef nesneleri hassas bir şekilde konumlandırabilmektedir.

* Supervisor (Gözlemci) Katmanı: Dronun üzerine fiziksel yük bindirmeyen, sahneyi dışarıdan takip eden bir Python modülü geliştirilmiştir. Bu modül:

Dronun GPS verilerini okur.

Sahnedeki canlıların (Kedi, Köpek) ve ekipmanların (Scooter) mutlak konumlarını takip eder.

Mesafe kritik eşiğin altına düştüğünde tespit uyarısı üretir.

# 4. Uygulama Senaryosu: Enkaz Altı Tespiti
Projenin en özgün kısmı, görsel temasın mümkün olmadığı durumları simüle etmesidir:

Canlı modelleri (Kedi/Köpek) çeşitli nesnelerin ve enkazların altına yerleştirilmiştir.

Dron, görsel (kamera) verisine ihtiyaç duymadan, ultrasonik ve koordinat bazlı veri füzyonu ile enkaz altındaki varlıkları tespit edebilmektedir.

Tespit Edilen Varlıklar: İnsan, Evcil Hayvan (Kedi/Köpek) ve Ulaşım Araçları (Scooter).

# 5. Elde Edilen Bulgular (Terminal Çıktıları)
Simülasyon sırasında elde edilen gerçek zamanlı veriler şu formattadır:

```!!! CANLI TESPİT EDİLDİ: [Dog] - Koordinat: (X: 1.2, Y: -0.8)```

```!!! YAŞAM BELİRTİSİ: Enkaz altı sinyali alındı. !!!```

```--- EKİPMAN TESPİT EDİLDİ: [ScooterSimple] ---```

# 6. Sonuç
Bu çalışma ile robotik sistemlerde Supervisor kullanımının, düşük donanım maliyetiyle nasıl yüksek doğrulukta raporlama yapabileceği kanıtlanmıştır. Proje, özellikle karmaşık afet sahnelerinde otonom sistemlerin karar verme süreçlerine dair önemli bir temel oluşturmaktadır.
