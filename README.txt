
# QR Base Attendance System
Bu proje, geleneksel yoklama süreçlerini dijitalleştirmek ve hızlandırmak amacıyla geliştirilmiş bir Öğrenci Yoklama Sistemi Simülasyonudur. Sistem, öğretmenlerin dinamik bir QR kod üretmesine ve öğrencilerin bu kodu taratarak katılım sağlamasına olanak tanır.

👨‍💻 Proje Ekibi
Hasan Gülsün 

...
🚀 Sistemi Çalıştırma (Hızlı Kurulum)
1. Hazır (.exe) Sürümü ile Çalıştırma
Projeyi Python veya kütüphane kurulumu ile uğraşmadan test etmek için:

Proje ana dizinindeki dist/ klasörüne girin.

İçeride bulunan QR_Yoklama_Sistemi.exe dosyasını çalıştırın.

Uygulama açıldığında Windows Güvenlik Duvarı izni istenirse, ağ haberleşmesi için "Erişime İzin Ver" butonuna tıklayın.

2. Kaynak Kodundan (.py) Çalıştırma
Geliştirici ortamında çalıştırmak isterseniz:

Gerekli kütüphaneleri yükleyin: pip install -r requirements.txt

Ana dosyayı başlatın: python QR_base_attandance.py

📂 Proje Klasör Yapısı ve Teslim Dosyaları
Hocamızın belirttiği kriterlere uygun olarak hazırlanan dosya yapısı aşağıdadır:

/dist: Hazır çalıştırılabilir .exe dosyasının bulunduğu klasör.

/src: Kaynak kodları (QR_base_attandance.py, qr_utils.py).

/models: Online eğitim platformu tasarımı için hazırlanan PlantUML Sekans Diyagramı ve sistem mimarisi modelleri.

/docs: İhtiyaç Analizi Dokümanı (Sourcing analizi dahil) ve Usability Test raporu.

yoklama.txt: Sistemin ürettiği tarih ve isim bazlı katılım kayıtları.

📊 Akademik Arka Plan
Bu çalışma, ders kapsamında işlenen aşağıdaki temel konular üzerine inşa edilmiştir:

Sistem Geliştirme Yaşam Döngüsü (SDLC): Projenin analiz, tasarım (UML) ve uygulama (Python) aşamaları bu döngüye uygun yönetilmiştir.

Kaynak Yönetimi (Sourcing): Proje, veri güvenliği ve kurum içi ihtiyaçlara yönelik olarak Insourcing stratejisiyle geliştirilmiştir.

Veri Yapıları: Öğretmen ve öğrenci listeleri ile yoklama kayıtları Python sözlükleri (dictionaries) ve dosya işlemleri (file operations) kullanılarak yönetilmektedir.

⚠️ Önemli Notlar
Programın çalışabilmesi için öğretmen bilgisayarı ile öğrenci cihazlarının aynı Wi-Fi ağına bağlı olması gerekir.

Yoklama sonuçları, program kapatıldığında .exe dosyası ile aynı konumda (veya bir üst dizinde) yoklama.txt olarak güncellenecektir.