import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path
import os

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set_style('whitegrid')

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Hanya memanggil main_data.csv yang ada di folder yang sama
    file_path = Path(__file__).parent / "main_data.csv"
    day_df = pd.read_csv(file_path)
    
    # Konversi tipe data
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    return day_df

# Panggil data
day_df = load_data()

# --- HEADER ---
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Analisis Anomali Cuaca Ekstrem & Efek Psikologis Cuaca Kemarin (H-1)")

st.divider()

# --- PERTANYAAN 1 ---
st.subheader("1. Anomali Cuaca Ekstrem & Titik Terendah")
st.markdown("Rata-rata penyewaan harian berdasarkan kondisi cuaca:")

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x='weathersit_label', y='cnt', data=day_df, palette='Blues_d', errorbar=None, ax=ax1)
ax1.set_xlabel('Kondisi Cuaca')
ax1.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig1)
st.info("**Insight:** Penyewaan terendah terjadi saat cuaca *Light Snow/Rain* (pernah menyentuh angka 22 unit).")

st.divider()

# --- PERTANYAAN 2 ---
st.subheader("2. Efek Cuaca Kemarin (H-1) Terhadap Hari Cerah")
st.markdown("Rata-rata penyewaan hari ini saat cuaca **Clear**, dilihat dari cuaca kemarin:")

clear_days = day_df[day_df['weathersit_label'] == 'Clear'].dropna(subset=['weather_prev_day'])
weather_order = ['Light Snow/Rain', 'Mist/Cloudy', 'Clear']
clear_grouped = clear_days.groupby('weather_prev_day')['cnt'].mean().reindex(weather_order).reset_index()

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(data=clear_grouped, x='weather_prev_day', y='cnt', palette='coolwarm', ax=ax2)
ax2.set_xlabel('Kondisi Cuaca Kemarin (H-1)')
ax2.set_ylabel('Rata-rata Penyewaan Hari Ini')
st.pyplot(fig2)
st.info("**Insight:** Hari cerah setelah kemarin hujan ringan memiliki penyewaan lebih rendah dibanding hari cerah setelah kemarin cerah.")

st.divider()

# --- KESIMPULAN ---
st.subheader("Kesimpulan & Rekomendasi")
st.success("""
**Kesimpulan:**
1. Penyewaan mencapai titik terendah mutlak (22 unit) saat cuaca Light Snow/Rain. 
2. Terdapat efek psikologis (trauma cuaca) di mana cuaca buruk kemarin tetap menekan jumlah penyewaan hari ini meskipun cuaca hari ini sedang cerah.

**Rekomendasi:**
- **Mitigasi Cuaca:** Kurangi operasional armada saat cuaca ekstrem, dan fokuskan armada di area transit (seperti stasiun) saat hujan ringan.
- **Strategi Promosi:** Luncurkan promo dadakan pada hari yang cerah setelah hari sebelumnya hujan deras untuk memancing kembali minat pengguna.
""")