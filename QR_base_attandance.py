import tkinter as tk

# --- PYINSTALLER İÇİN pyzbar DLL DOSYALARI EKLEMEK İÇİN NOTLAR ---

# Otomatik olarak pyzbar kütüphanesinin kurulu olduğu dizini tespit etmeniz ve oradaki DLL dosyalarını .exe dosyasına eklemeniz gerekir.
# Bunun için aşağıdaki adımları izleyebilirsiniz:

# 1. pyzbar kurulumu yapılan dizini bulmak için:
import os
import pyzbar
import glob

# pyzbar'ın modul yolunu bul
pyzbar_dir = os.path.dirname(pyzbar.__file__)

# DLL dosyalarını ara
dll_files = glob.glob(os.path.join(pyzbar_dir, "*.dll"))

# Print veya kullanmak için DLL dosyaları listesi
# print("pyzbar DLL dosyaları:", dll_files)

# 2. PyInstaller ile .spec dosyası kullanarak bu dosyaları datas kısmına ekleyin!
#    Aşağıdaki .spec dosyası örneğini kendi projenize göre düzenleyip kullanabilirsiniz:
#
# Aşağıdaki şekilde bir 'QR_base_attandance.spec' dosyası oluşturun:
#
# -------------- QR_base_attandance.spec başlangıç ----------------
# # -*- mode: python ; coding: utf-8 -*-
#
# block_cipher = None
#
# import pyzbar
# import os, glob
# pyzbar_dir = os.path.dirname(pyzbar.__file__)
# dll_files = glob.glob(os.path.join(pyzbar_dir, "*.dll"))
# datas = [(f, ".") for f in dll_files]
#
# a = Analysis(
#     ['QR_base_attandance.py'],
#     pathex=[],
#     binaries=[],
#     datas=datas,
#     hiddenimports=[],
#     hookspath=[],
#     runtime_hooks=[],
#     excludes=[],
#     win_no_prefer_redirects=False,
#     win_private_assemblies=False,
#     cipher=block_cipher,
# )
# pyzbar_app = PYZ(a.pure, a.scripts, a.binaries, a.zipfiles, a.datas, a)
# coll = COLLECT(
#     pyzbar_app,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='QR_base_attandance'
# )
# -------------- QR_base_attandance.spec son ----------------------
#
# 3. Daha sonra terminalde (bulunduğunuz dizinde) şunu çalıştırın:
#
#    pyinstaller QR_base_attandance.spec
#
# veya direkt komut olarak aşağıdaki gibi komut kullanmak isterseniz (DLL yolunu kendi sisteminizde tespit ettiğiniz şekilde yazınız):
#
#    pyinstaller --add-data "<PYZBAR_DIZINI>\\*.dll;." QR_base_attandance.py
#
# <PYZBAR_DIZINI> kısmını otomatik bulmak için yukarıdaki pyzbar_dir değişkenini kullanabilirsiniz.
#
# ÖRNEK Otomatik ve sorunsuz komut:
# (Örneğin, cmd veya powershell altında çalıştırılabilir)
#
# python -c "import pyzbar,os; print(os.path.dirname(pyzbar.__file__))"
#
# Diyelim ki çıktı:  C:\Users\<KULLANICI>\AppData\Local\Programs\Python\Python3x\Lib\site-packages\pyzbar
#
# Ardından şunu çalıştırın:
#
# pyinstaller --add-data "C:\Users\<KULLANICI>\AppData\Local\Programs\Python\Python3x\Lib\site-packages\pyzbar\*.dll;." QR_base_attandance.py
#
# (Yukarıdaki yolu kendi çıktınıza göre uyarlayın)
#
# *** EN GÜVENLİ VE SÜRDÜRÜLEBİLİR YÖNTEM .spec DOSYASI KULLANMAKTIR! ***
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import qrcode
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode as zbar_decode
import threading
from flask import Flask, request, render_template_string
import socket
import datetime
import os

# --- AYARLAR VE LİSTELER ---
ogretmen_isim_listesi = ["Ahmet Hoca", "Mehmet Hoca", "Ali Veli","Nihal Menzi"]
ogrenci_listesi = ["Burak Yılmaz", "Ayşe Kaya", "Fatma Demir", "Can Yıldız","Tunahan Oral","Göktuğ Yıldırım","Hasan Gülsün"]

# Devamsızlık Kuralları
TOPLAM_HAFTA = 13
GECME_SINIRI = 8  # En az 8 kere gelmesi lazım

# Dosya Adı
YOKLAMA_DOSYASI = "yoklama.txt"

# --- FLASK WEB SUNUCUSU (Öğrencilerin Göreceği Ekran) ---
app = Flask(__name__)

# Basit HTML Şablonu
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Yoklama Sistemi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background-color: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
        button:hover { background-color: #218838; }
        .error { color: red; font-weight: bold; }
        .success { color: green; font-weight: bold; }
        .fail-warning { color: darkred; font-weight: bold; margin-top: 10px; border: 1px solid red; padding: 10px; background: #ffe6e6;}
    </style>
</head>
<body>
    <div class="container">
        <h2>Ders Yoklaması</h2>
        {% if message %}
            <p class="{{ status }}">{{ message }}</p>
            {% if kalan_bilgisi %}
                <div class="fail-warning">{{ kalan_bilgisi }}</div>
            {% endif %}
        {% endif %}
        
        {% if not success_flag %}
        <form method="POST" action="/submit">
            <input type="text" name="ad_soyad" placeholder="Ad Soyad Giriniz" required>
            <button type="submit">Yoklamayı Gönder</button>
        </form>
        {% endif %}
    </div>
</body>
</html>
"""

def devamsizlik_kontrol(ad_soyad):
    """Dosyayı okur ve öğrencinin kaç kez geldiğini sayar."""
    sayac = 0
    if os.path.exists(YOKLAMA_DOSYASI):
        with open(YOKLAMA_DOSYASI, "r", encoding="utf-8") as f:
            for line in f:
                if ad_soyad.lower() in line.lower():
                    sayac += 1
    return sayac

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE, message="", status="", success_flag=False)

@app.route('/submit', methods=['POST'])
def submit():
    ad_soyad = request.form.get('ad_soyad').strip()
    
    # İsim Listede Var mı Kontrolü
    isim_bulundu = False
    gercek_isim = ""
    for ogrenci in ogrenci_listesi:
        if ogrenci.lower() == ad_soyad.lower():
            isim_bulundu = True
            gercek_isim = ogrenci
            break
            
    if not isim_bulundu:
        return render_template_string(HTML_TEMPLATE, message="Yanlış girildi, tekrar deneyin.", status="error", success_flag=False)
    
    # Yoklamayı Kaydet
    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(YOKLAMA_DOSYASI, "a", encoding="utf-8") as f:
        f.write(f"{gercek_isim} | {tarih}\n")
    
    # Kaldı/Geçti Kontrolü
    mevcut_katilim = devamsizlik_kontrol(gercek_isim)
    kalan_bilgisi = ""
    
    # Not: Senaryoya göre 13. haftada kontrol yapılıyor varsayıyoruz.
    # Eğer bu sistem sürekli çalışıyorsa, şu anki katılım sayısını gösteririz.
    if mevcut_katilim < GECME_SINIRI:
        kalan_durumu = f"Dikkat! Toplam katılımınız: {mevcut_katilim}. Dersten geçmek için en az {GECME_SINIRI} olmalı."
    else:
        kalan_durumu = f"Tebrikler, katılım şartını sağladınız. (Toplam: {mevcut_katilim})"

    return render_template_string(HTML_TEMPLATE, 
                                  message=f"Hoşgeldin {gercek_isim}, yoklaman alındı.", 
                                  status="success", 
                                  kalan_bilgisi=kalan_durumu,
                                  success_flag=True)

def run_flask():
    # Sunucuyu tüm ağa açar (host='0.0.0.0')
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# --- MASAÜSTÜ ARAYÜZÜ (QRStudio Entegreli) ---
class AttendanceApp:
    def __init__(self, root, teacher_name):
        self.root = root
        self.root.title(f"Yoklama Sistemi - {teacher_name}")
        self.root.geometry("1100x750")
        
        # Flask Sunucusunu Başlat
        self.server_thread = threading.Thread(target=run_flask, daemon=True)
        self.server_thread.start()
        
        # IP Adresi ve Link
        self.local_ip = get_local_ip()
        self.attendance_url = f"http://{self.local_ip}:5000"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Üst Bilgi Paneli
        info_frame = ttk.Frame(self.root, padding=10)
        info_frame.pack(fill="x")
        
        ttk.Label(info_frame, text=f"Yoklama Linki: {self.attendance_url}", font=("Segoe UI", 12, "bold")).pack(side="left")
        ttk.Label(info_frame, text="(Öğrenciler aynı Wi-Fi ağında olmalı)", font=("Segoe UI", 10)).pack(side="left", padx=10)

        # --- QRStudio Arayüzü (Verilen koddan uyarlandı) ---
        self.frame = ttk.Frame(self.root, padding=12)
        self.frame.pack(expand=True, fill="both")
        
        # Sol Panel (Kontroller)
        left_panel = ttk.Frame(self.frame)
        left_panel.pack(side="left", fill="y", padx=10)
        
        ttk.Label(left_panel, text="QR İçeriği (Otomatik):", font=("Segoe UI", 11)).pack(anchor="w")
        self.input_text = ScrolledText(left_panel, width=40, height=5, font=("Segoe UI", 11))
        self.input_text.pack(pady=5)
        self.input_text.insert("1.0", self.attendance_url) # Linki otomatik yaz
        
        btn = ttk.Button(left_panel, text="Yoklama QR'ını Oluştur", command=self.generate_qr)
        btn.pack(pady=10, fill="x")
        
        # Sağ Panel (Önizleme)
        right_panel = ttk.Frame(self.frame)
        right_panel.pack(side="right", expand=True, fill="both")
        
        self.qr_label = ttk.Label(right_panel, text="QR Kod Burada Görünecek")
        self.qr_label.pack(pady=20)
        
        self.status_label = ttk.Label(self.root, text="Sistem Hazır", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", side="bottom")

    def generate_qr(self):
        text = self.input_text.get("1.0", "end").strip()
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        
        # Ekranda Göster
        self.show_qr_preview(img)
        self.status_label.config(text="QR Kod başarıyla oluşturuldu ve öğrenciler bekleniyor...")

    def show_qr_preview(self, pil_img):
        img = pil_img.resize((300, 300), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=self.photo, text="")

# --- GİRİŞ EKRANI ---
class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Öğretmen Girişi")
        self.root.geometry("400x250")
        
        # Ortalamak için
        self.center_window()

        tk.Label(self.root, text="Öğretmen Girişi", font=("Segoe UI", 16, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="İsim Soyisim:").pack()
        self.name_entry = tk.Entry(self.root, font=("Segoe UI", 12))
        self.name_entry.pack(pady=5)
        
        tk.Button(self.root, text="Giriş Yap", command=self.check_login, bg="#007bff", fg="white", font=("Segoe UI", 11)).pack(pady=20)
        
        self.root.mainloop()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def check_login(self):
        name = self.name_entry.get().strip()
        
        if name in ogretmen_isim_listesi:
            self.root.destroy() # Giriş ekranını kapat
            self.open_main_app(name)
        else:
            messagebox.showerror("Hata", "Tekrar deneyiniz. İsim listede bulunamadı.")

    def open_main_app(self, teacher_name):
        new_root = tk.Tk()
        app = AttendanceApp(new_root, teacher_name)
        new_root.mainloop()

# --- PROGRAMI BAŞLAT ---
if __name__ == "__main__":
    # Eğer yoklama dosyası yoksa oluştur
    if not os.path.exists(YOKLAMA_DOSYASI):
        with open(YOKLAMA_DOSYASI, "w", encoding="utf-8") as f:
            pass
            
    LoginWindow()