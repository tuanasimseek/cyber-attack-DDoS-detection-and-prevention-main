from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
from datetime import datetime
from tensorflow.keras.models import load_model
import os


app = Flask(__name__)

# Modelin yolu
MODEL_YOLU = r"C:\Users\Lenovo\Desktop\DDOS_tespiti\codes\ddos_model.h5"

# Modeli yükle
print("🤖 Model yükleniyor...")
model = load_model(MODEL_YOLU)
print("✅ Model yüklendi.\n")

def tahmin_yap(gelen_veri):
    try:
        ozellikler = [gelen_veri[key] for key in gelen_veri if key != "label"]

        if len(ozellikler) < 45:
            ozellikler += [0] * (45 - len(ozellikler))

        girdi = np.array([ozellikler])
        tahmin = model.predict(girdi)[0][0]
        return tahmin
    except Exception as e:
        print(f"HATA - Tahmin yapılırken sorun oluştu: {e}")
        return None

@app.route("/gelen_paket", methods=["POST"])
def gelen_paket():
    veri = request.get_json()

    if not veri:
        return jsonify({"hata": "Veri alınamadı"}), 400

    zaman = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    ip = request.remote_addr

    print(f"{ip} - [{zaman}] \"POST /gelen_paket HTTP/1.1\" 200 -")
    print(f"Gelen veri etiketi: {veri.get('label')}")

    tahmin = tahmin_yap(veri)

    if tahmin is None:
        return jsonify({"sonuc": "tahmin hatası"}), 500

    if tahmin > 0.5:
        print("❌ Saldırı Paketi Engellendi!\n")
        return jsonify({"sonuc": "saldiri"})
    else:
        print("✅ Normal Paket Alındı.\n")
        return jsonify({"sonuc": "normal"})

@app.route("/", methods=["GET"])
def home():
    return "Flask Sunucusu Çalışıyor!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == "__main__":
    print("🚀 Flask sunucusu başlatılıyor...")
    print("🔍 Gelen trafik dinleniyor...\n")
    app.run(host="0.0.0.0", port=5000, debug=True,use_reloader=False)
