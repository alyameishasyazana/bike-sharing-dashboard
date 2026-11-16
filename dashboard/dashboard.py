import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

# Set page config
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

sns.set(style='whitegrid')

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Mendapatkan direktori tempat file dashboard.py ini berada
    base_path = os.path.dirname(__file__)
    
    # Membuat path lengkap ke file CSV
    day_path = os.path.join(base_path, 'day.csv')
    hour_path = os.path.join(base_path, 'hour.csv')
    
    # Membaca CSV menggunakan path lengkap
    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)
    
    # Mengubah tipe data tanggal
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    # Mapping Cuaca
    weather_map = {1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
    day_df['weathersit'] = day_df['weathersit'].map(weather_map)
    
    # Feature Engineering: Cuaca H-1
    day_df = day_df.sort_values('dteday').reset_index(drop=True)
    day_df['weathersit_prev_day'] = day_df['weathersit'].shift(1)
    
    return day_df

# Panggil fungsi load data
day_df = load_data()

# --- HEADER ---
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Dashboard ini menjawab dua pertanyaan bisnis utama: **Anomali Cuaca Ekstrem** dan **Efek Psikologis Cuaca Kemarin (H-1)**.")

# --- SIDEBAR (Filter) ---
st.sidebar.header("Filter Data")
# Pastikan tahun diubah ke string agar rapi di dropdown
day_df['yr_str'] = day_df['yr'].map({0: '2011', 1: '2012'})
year_option = st.sidebar.selectbox("Pilih Tahun:", day_df['yr_str'].unique())
weather_option = st.sidebar.multiselect("Pilih Kondisi Cuaca:", day_df['weathersit'].unique(), default=day_df['weathersit'].unique())

# Terapkan filter
filtered_df = day_df[(day_df['yr_str'] == year_option) & (day_df['weathersit'].isin(weather_option))]

# --- PERTANYAAN 1: ANOMALI CUACA EKSTREM ---
st.subheader("1. Anomali Cuaca Ekstrem & Titik Terendah")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Sebaran Penyewaan Berdasarkan Cuaca**")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='weathersit', y='cnt', data=filtered_df, palette='Set3', ax=ax)
    plt.title('Sebaran dan Anomali Penyewaan')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(fig)
    st.caption("Terlihat titik terendah menyentuh angka sangat rendah pada saat cuaca Heavy Rain/Snow.")

with col2:
    st.markdown("**Anomali Penyewaan saat Hujan Ringan**")
    bad_weather_df = filtered_df[filtered_df['weathersit'] == 'Light Snow/Rain']
    
    if not bad_weather_df.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=bad_weather_df, x='temp', y='cnt', hue='hum', size='windspeed', palette='coolwarm', sizes=(20, 200), ax=ax)
        plt.title('Scatter Plot: Hujan Ringan')
        plt.xlabel('Suhu (Temp)')
        plt.ylabel('Jumlah Penyewaan')
        st.pyplot(fig)
        st.caption("Anomali: Saat hujan ringan, penyewaan bisa tetap tinggi (>4000) jika suhu hangat dan angin rendah.")
    else:
        st.info("Tidak ada data cuaca 'Light Snow/Rain' pada filter tahun ini.")

# --- PERTANYAAN 2: EFEK TRAUMA CUACA H-1 ---
st.subheader("2. Efek Psikologis Cuaca Kemarin (H-1)")
st.markdown("Apakah cuaca buruk kemarin menekan penyewaan hari ini meskipun cuaca hari ini cerah?")

clear_days = filtered_df[filtered_df['weathersit'] == 'Clear']
clear_days_grouped = clear_days.dropna(subset=['weathersit_prev_day']).groupby('weathersit_prev_day')['cnt'].mean().reset_index()

if not clear_days_grouped.empty:
    # Mengurutkan data
    weather_order = ['Heavy Rain/Snow', 'Light Snow/Rain', 'Mist/Cloudy', 'Clear']
    # Filter urutan yang hanya ada di data
    weather_order = [w for w in weather_order if w in clear_days_grouped['weathersit_prev_day'].values]
    
    clear_days_grouped['weathersit_prev_day'] = pd.Categorical(clear_days_grouped['weathersit_prev_day'], categories=weather_order, ordered=True)
    clear_days_grouped = clear_days_grouped.sort_values('weathersit_prev_day')

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=clear_days_grouped, x='weathersit_prev_day', y='cnt', palette='coolwarm', ax=ax)
    plt.title('Rata-rata Penyewaan Saat Cuaca HARI INI Cerah (Berdasarkan Cuaca Kemarin)', fontsize=14)
    plt.xlabel('Kondisi Cuaca Kemarin (H-1)')
    plt.ylabel('Rata-rata Penyewaan Hari Ini')
    st.pyplot(fig)

    st.markdown("""
    **Insight:**
    *   Grafik di atas membuktikan adanya **efek trauma cuaca**. 
    *   Meskipun cuaca **hari ini cerah**, rata-rata penyewaan tertinggi terjadi jika **kemarin juga cerah**. 
    *   Namun, jika kemarin cuaca buruk (Heavy Rain/Snow), minat pengguna untuk bersepeda di hari yang cerah tetap tertinggal lebih rendah.
    """)
else:
    st.info("Tidak cukup data untuk menampilkan analisis efek trauma cuaca pada filter ini.")

# --- KESIMPULAN ---
st.subheader("Kesimpulan & Rekomendasi")
st.success("""
**Kesimpulan:**
1. Penyewaan mencapai titik terendah (mendekati 0) saat cuaca Heavy Rain/Snow. Namun, ada anomali di mana cuaca Light Snow/Rain tidak menyurutkan minat jika suhu hangat dan angin rendah.
2. Terdapat *lagging effect* (efek trauma) di mana cuaca buruk kemarin tetap menekan jumlah penyewaan hari ini meskipun cuaca hari ini sedang cerah.

**Rekomendasi:**
*   **Mitigasi Stok:** Kurangi operasional armada saat cuaca ekstrem (Heavy Rain/Snow), tapi tetap sediakan armada saat hujan ringan dengan suhu hangat.
*   **Strategi Marketing:** Luncurkan promo *flash sale* atau notifikasi push ("Cuaca hari ini cerah! Yuk bersepeda lagi") pada hari yang cerah setelah hari sebelumnya hujan deras untuk memancing kembali minat pengguna.
""")