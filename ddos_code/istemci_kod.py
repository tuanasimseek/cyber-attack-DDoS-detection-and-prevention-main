from flask import Flask, request, jsonify
import pandas as pd
import requests
import random
import time
import os

app = Flask(_name_)

# Trafik dosyalarının tam yolları
NORMAL_DOSYA = "C:/Users/user/Desktop/normal_trafik_numeric.xlsx"
SALDIRI_DOSYA = "C:/Users/user/Desktop/dos_saldiri_numeric.xlsx"

# Sunucu adresi
SUNUCU_URL = "http://138.38.23.99:5000/gelen_paket"

# Dosya yollarını kontrol et
if not os.path.exists(NORMAL_DOSYA):
    print(f"Dosya bulunamadı: {NORMAL_DOSYA}")
if not os.path.exists(SALDIRI_DOSYA):
    print(f"Dosya bulunamadı: {SALDIRI_DOSYA}")

# Dosyaları oku
df_normal = pd.read_excel(NORMAL_DOSYA)
df_saldiri = pd.read_excel(SALDIRI_DOSYA)

@app.route('/gelen_paket', methods=['POST'])
def gelen_paket():
    try:
        # JSON verisi al
        veri = request.get_json()
        print(f"Gelen veri: {veri}")



        return jsonify({"message": "Veri alındı", "status": "success"}), 200

    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({"message": "Hata oluştu", "status": "error"}), 500

def excelden_karisik_paket_gonder():
    while True:
        # %50 ihtimalle saldırı ya da normal trafik seç
        if random.random() < 0.5:
            secilen_df = df_normal
        else:
            secilen_df = df_saldiri

        satir = secilen_df.sample(n=1).iloc[0].to_dict()

        try:
            response = requests.post(SUNUCU_URL, json=satir)
            print(f"Gönderilen etiket: {satir.get('label')} → Cevap: {response.status_code}")
        except Exception as e:
            print(f"Hata: {e}")

        time.sleep(random.uniform(0.5, 2))

if _name_ == "_main_":
    # Flask server'ını başlat
    from threading import Thread
    thread = Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False})
    thread.start()

    # Veri gönderme fonksiyonunu başlat
    excelden_karisik_paket_gonder()