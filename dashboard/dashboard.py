import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path
import os

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set_style('whitegrid')

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Path yang aman
    file_path = Path(__file__).parent / "main_data.csv"
    day_df = pd.read_csv(file_path)
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df

day_df = load_data()

# --- HEADER ---
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Analisis Penyewaan Sepeda Berdasarkan Cuaca dan Efek Cuaca H-1")

# --- FITUR INTERAKTIF (FILTER) ---
st.sidebar.header("Filter Data")
# Filter 1: Musim
season_filter = st.sidebar.multiselect(
    "Pilih Musim:", 
    options=day_df['season_label'].unique(), 
    default=day_df['season_label'].unique()
)

# Filter 2: Cuaca
weather_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca:", 
    options=day_df['weathersit_label'].unique(), 
    default=day_df['weathersit_label'].unique()
)

# Terapkan filter
filtered_df = day_df[
    (day_df['season_label'].isin(season_filter)) & 
    (day_df['weathersit_label'].isin(weather_filter))
]

st.divider()

# --- PERTANYAAN 1 (2 GRAFIK) ---
st.subheader("1. Sebaran dan Rata-rata Penyewaan Berdasarkan Cuaca")
st.markdown("Menjawab Pertanyaan 1: Bagaimana sebaran dan titik terendah penyewaan berdasarkan cuaca?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Rata-rata Penyewaan**")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='weathersit_label', y='cnt', data=filtered_df, palette='Blues_d', errorbar=None, ax=ax1)
    ax1.set_xlabel('Kondisi Cuaca')
    ax1.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig1)

with col2:
    st.markdown("**Sebaran dan Titik Terendah**")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='weathersit_label', y='cnt', data=filtered_df, palette='Blues', ax=ax2)
    ax2.set_xlabel('Kondisi Cuaca')
    ax2.set_ylabel('Jumlah Penyewaan (cnt)')
    st.pyplot(fig2)

st.info("**Insight:** Cuaca *Clear* memiliki rata-rata tertinggi. Namun, boxplot menunjukkan titik terendah ekstrem (22 unit) terjadi saat cuaca *Light Snow/Rain*.")

st.divider()

# --- PERTANYAAN 2 ---
st.subheader("2. Efek Cuaca Kemarin (H-1) Saat Hari Ini Cerah")
st.markdown("Menjawab Pertanyaan 2: Bagaimana pengaruh cuaca H-1 terhadap penyewaan hari ini?")

clear_days = filtered_df[filtered_df['weathersit_label'] == 'Clear'].dropna(subset=['weather_prev_day'])
weather_order = ['Light Snow/Rain', 'Mist/Cloudy', 'Clear']
clear_grouped = clear_days.groupby('weather_prev_day')['cnt'].mean().reindex(weather_order).dropna().reset_index()

if not clear_grouped.empty:
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=clear_grouped, x='weather_prev_day', y='cnt', palette='coolwarm', ax=ax3)
    ax3.set_xlabel('Kondisi Cuaca Kemarin (H-1)')
    ax3.set_ylabel('Rata-rata Penyewaan Hari Ini')
    st.pyplot(fig3)
    st.info("**Insight:** Hari cerah setelah kemarin hujan ringan memiliki penyewaan lebih rendah (2.758 unit) dibanding hari cerah setelah kemarin cerah (5.008 unit).")
else:
    st.warning("Data untuk analisis H-1 tidak cukup pada filter yang dipilih.")