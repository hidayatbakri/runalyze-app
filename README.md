# 🏃‍♂️ Runalyze Gen-Z

> Analisis lari kamu dari Strava untuk mengungkap **Tipe Pelari**, **Running GPA**, dan **motivasi ala AI Gen-Z** 🤖🔥

## 📌 Deskripsi Proyek

**Runalyze Gen-Z** adalah aplikasi berbasis Streamlit yang melakukan analisis terhadap data lari dari Strava. Dengan pendekatan clustering + scoring, aplikasi ini bisa:
- Mengklasifikasikan kamu ke dalam **4 tipe pelari Gen-Z**
- Menghitung **Running GPA** skala 0–4
- Memberikan **motivasi kocak / menyentil** berdasarkan performa (soon)

🎯 Cocok untuk kamu yang lari biar sehat, biar gaya, atau biar bisa flex di Instagram.

---

## 🧪 Fitur Utama

- 📤 Upload file `.csv` dari Strava
- 📊 Preview data mentah
- 🧠 Klasifikasi tipe pelari:
  - **Ghost Jogger**
  - **Weekend Warrior**
  - **Steady Strider**
  - **Marathon Maniac**
- 🎓 Running GPA Score (0.0 – 4.0)
- 🤣 Label motivasi kocak:
  - `😵 AFK Runner`
  - `😴 Jogger Noob`
  - `🧢 Casual Cruiser`
  - `🏃‍♂️💨 Tryhard Sprinter`
  - `🔥👑 Legendary Strider`
- 📈 Grafik progres mingguan

---

## 📂 Cara Pakai

1. **Clone repositori:**
   ```bash
   git clone https://github.com/your-username/runalyze-genz.git
   cd runalyze-genz
   ```

2. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi:**
   ```bash
   streamlit run app.py
   ```

---

## 🧠 Cara Kerja Singkat
1. Data preprocessing:
  - Filter hanya aktivitas Run
  - Hitung durasi (menit), jarak (km), dan agregat mingguan
2. Ekstraksi fitur mingguan:
  - dist_mean, dist_std, dur_mean, dll
3. Inferensi:
  - KMeans clustering untuk deteksi tipe pelari
  - Skoring manual untuk Running GPA
4. Visualisasi & motivasi berdasarkan hasil inferensi (soon)

---

## 🛠 Teknologi yang Digunakan
* Python 🐍
* Streamlit 🎈
* Scikit-learn 🤖
* Pandas & NumPy 📊
* Matplotlib 📈
* Joblib 🔧


---
## ⚠️ Disclaimer
Data kamu tidak disimpan, semua analisis dilakukan di local browser/server.


---
### 📄 License
MIT License © 2025 by Hidayat Bakri
