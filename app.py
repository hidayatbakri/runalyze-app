import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import time

# ====== CONFIG ======
st.set_page_config(page_title="🏃‍♂️ Runalyze Gen-Z", layout="centered")
column_map = {
    'Elapsed Time': 'duration_sec',
    'Waktu Total': 'duration_sec',
    'Distance': 'distance_km',
    'Jarak': 'distance_km',
    'Activity Date': 'date',
    'Tanggal Aktivitas': 'date',
    'Activity Type': 'activity_type',
    'Jenis aktivitas': 'activity_type',
}

# ====== DESKRIPSI LABEL ======
runner_label_desc = {
    "Ghost Jogger": "👻 Pelari misterius yang suka muncul dan hilang tiba-tiba. Konsistensi? Nggak kenal.",
    "Weekend Warrior": "🛌 Senin sampai Jumat rebahan, Sabtu Minggu langsung tancap gas. Balance life banget.",
    "Steady Strider": "🧘‍♂️ Konsisten dan tenang. Gak nge-push, tapi selalu jalan. Pelari mindfulness sejati.",
    "Marathon Maniac": "🔥 Ini gila sih... Tiap minggu kayak latihan buat Ironman. Mungkin kamu punya 2 kaki dan 4 paru-paru."
}

gpa_label_desc = {
    "😵 AFK Runner": "Kamu lebih sering AFK daripada lari. Yuk, mulai gerak biar gak karatan!",
    "😴 Jogger Noob": "Masih pemula, tapi udah mulai. Semangat terus, nanti juga jadi pro!",
    "🧢 Casual Cruiser": "Larinya santai kayak di pantai. Gak dikejar target, tapi tetap enjoy dan konsisten.",
    "🏃‍♂️💨 Tryhard Sprinter": "Wuhuu! Kamu udah niat banget. Tapi jangan lupa istirahat juga ya!",
    "🔥👑 Legendary Strider": "RAJA SEGALANYA! Disiplin, bertenaga, dan lari udah jadi bagian hidupmu!"
}

# ====== HEADER ======
st.title("🏃‍♂️ Runalyze Gen-Z")
st.subheader("Analisis Tipe Pelari + GPA Lari")

st.markdown("---")

# ====== FILE UPLOAD ======
uploaded_file = st.file_uploader("📤 Upload file Strava kamu (.csv)", type=["csv"])


if uploaded_file is not None:
    # Baca CSV
    df_raw = pd.read_csv(uploaded_file)
    st.success("📈 Data berhasil dimuat!")
    
    st.markdown("### 🔍 Preview Data")
    st.dataframe(df_raw.head())

    # Tombol Analisis
    if st.button("🚀 Analisis Sekarang!"):
        with st.spinner("🏃‍♀️ Lagi ngitung langkahmu... sebentar ya!"):
            time.sleep(1)
            st.markdown("## 💡 Hasil Analisis")

            # === Preprocessing Data ===
            df_raw = df_raw.rename(columns={col: column_map[col] for col in df_raw.columns if col in column_map})

            df_raw['distance_km'] = df_raw['distance_km'].astype(str).str.replace(',', '.', regex=False).astype(float)

            df_raw = df_raw[df_raw['activity_type'].isin(['Run', 'Berlari'])]
            df_raw = df_raw[(df_raw['distance_km'] > 0) & (df_raw['duration_sec'] > 0)]

            df_raw['duration_min'] = df_raw['duration_sec'] / 60
            df_raw['date'] = pd.to_datetime(df_raw['date'], errors='coerce')
            df_raw['week'] = df_raw['date'].dt.to_period('W').astype(str)

            weekly = df_raw.groupby('week').agg({
                'distance_km': 'sum',
                'duration_min': 'sum'
            })

            user_features = pd.DataFrame([{
                'dist_mean': weekly['distance_km'].mean(),
                'dist_std': weekly['distance_km'].std(ddof=0),
                'dist_total': weekly['distance_km'].sum(),
                'weeks_active': len(weekly),
                'dur_mean': weekly['duration_min'].mean(),
                'dur_std': weekly['duration_min'].std(ddof=0),
                'dur_total': weekly['duration_min'].sum()
            }])

            # === Load pipeline & predict ===
            pipeline = joblib.load("models/clustering_model.pkl")
            user_features['runner_type'] = pipeline.predict(user_features)

            # === Map runner label ===
            type_map = {
                0: "Ghost Jogger",
                1: "Weekend Warrior",
                2: "Steady Strider",
                3: "Marathon Maniac"
            }
            user_features['runner_label'] = user_features['runner_type'].map(type_map)

            # === Hitung GPA ===
            def calculate_gpa(row):
                gpa = (
                    0.3 * (row['dist_mean'] / 10) +
                    0.3 * (row['dur_mean'] / 60) +
                    0.2 * (row['weeks_active'] / 10) +
                    0.2 * (row['dist_total'] / 100)
                )
                return round(min(gpa, 4.0), 1)

            user_features['running_gpa'] = user_features.apply(calculate_gpa, axis=1)

            def gpa_label_genz(gpa):
                if gpa <= 1.0:
                    return "😵 AFK Runner"
                elif gpa <= 2.0:
                    return "😴 Jogger Noob"
                elif gpa <= 3.0:
                    return "🧢 Casual Cruiser"
                elif gpa <= 3.5:
                    return "🏃‍♂️💨 Tryhard Sprinter"
                else:
                    return "🔥👑 Legendary Strider"

            user_features['gpa_label'] = user_features['running_gpa'].apply(gpa_label_genz)

            # === TAMPILKAN METRIK ===
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🏃‍♂️ Tipe Pelari", user_features['runner_label'].iloc[0])
                st.caption(runner_label_desc[user_features['runner_label'].iloc[0]])
            with col2:
                st.metric("📊 Running GPA", user_features['running_gpa'].iloc[0], help="Skala 0 - 4")
                st.caption(gpa_label_desc[user_features['gpa_label'].iloc[0]])

            st.markdown(f"### 🧠 Kamu adalah: {user_features['gpa_label'].iloc[0]}")
            st.info(gpa_label_desc[user_features['gpa_label'].iloc[0]])

            st.markdown("### 📋 Rangkuman")
            st.dataframe(user_features)

            # === Optional: grafik mingguan pakai data asli ===
            st.markdown("### 📈 Grafik Mingguan")
            if "week" in df_raw.columns:
                try:
                    fig, ax = plt.subplots()
                    weekly['distance_km'].plot(kind='line', marker='o', ax=ax)
                    ax.set_title("Jarak Lari per Minggu")
                    ax.set_ylabel("Km")
                    ax.grid(True)
                    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
                    st.pyplot(fig)
                except Exception as e:
                    st.warning(f"❗ Gagal menampilkan grafik: {e}")

else:
    st.info("Silakan upload file .csv dari Strava kamu dulu. Data tidak akan disimpan di server kami.")
