import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path
import os

# Set page config
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set(style='whitegrid')

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Path yang aman untuk Streamlit
    file_path = Path(__file__).parent / "day.csv"
    hour_path = Path(__file__).parent / "hour.csv"
    
    day_df = pd.read_csv(file_path)
    hour_df = pd.read_csv(hour_path)
    
    # Konversi tipe data
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    # Mapping
    hour_df['day_type'] = hour_df['workingday'].map({1: 'Hari Kerja', 0: 'Libur/Weekend'})
    
    return day_df, hour_df

day_df, hour_df = load_data()

# --- HEADER ---
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis Penyewaan Sepeda 2011-2012")

# --- METRIK UTAMA ---
total_rentals = day_df['cnt'].sum()
total_casual = day_df['casual'].sum()
total_registered = day_df['registered'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{total_rentals:,}")
col2.metric("Pengguna Casual", f"{total_casual:,}")
col3.metric("Pengguna Registered", f"{total_registered:,}")

st.divider()

# --- VISUALISASI 1 (Pertanyaan 1) ---
st.subheader("1. Dominasi Tipe Pengguna")
fig1, ax1 = plt.subplots(figsize=(6, 4))
sns.barplot(x=['Casual', 'Registered'], y=[total_casual, total_registered], palette=['#FFA15A', '#19A0AA'], ax=ax1)
ax1.set_ylabel('Total Penyewaan')
ax1.set_title('Total Penyewaan Berdasarkan Tipe Pengguna', fontsize=14)
st.pyplot(fig1)
st.info("**Insight:** Pengguna *Registered* jauh lebih mendominasi dibandingkan *Casual*.")

st.divider()

# --- VISUALISASI 2 (Pertanyaan 2) ---
st.subheader("2. Pola Penyewaan per Jam: Hari Kerja vs Libur")
hourly_avg = hour_df.groupby(['day_type', 'hr'])['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=hourly_avg, x='hr', y='cnt', hue='day_type', marker='o', palette='Set1', ax=ax2)
ax2.set_xticks(range(0, 24))
ax2.set_xlabel('Jam (0-23)')
ax2.set_ylabel('Rata-rata Penyewaan')
ax2.set_title('Rata-rata Penyewaan Sepeda per Jam', fontsize=14)
st.pyplot(fig2)
st.info("**Insight:** Hari kerja memiliki dua puncak tajam (jam 08.00 & 17.00). Hari libur puncaknya landai di siang hari (12.00-15.00).")