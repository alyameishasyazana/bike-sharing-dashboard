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
    file_path = Path(__file__).parent / "main_data.csv"
    day_df = pd.read_csv(file_path)
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df

day_df = load_data()

# --- HEADER ---
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Analisis Penyewaan Sepeda Berdasarkan Cuaca dan Efek Cuaca H-1")

# --- FITUR FILTERING (WAJIB) ---
st.sidebar.header("Filter Data")
# Filter 1: Berdasarkan Musim
season_filter = st.sidebar.multiselect(
    "Pilih Musim:", 
    options=day_df['season_label'].unique(), 
    default=day_df['season_label'].unique()
)

# Filter 2: Berdasarkan Kondisi Cuaca
weather_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca:", 
    options=day_df['weathersit_label'].unique(), 
    default=day_df['weathersit_label'].unique()
)

# Menerapkan filter ke dataframe
filtered_df = day_df[
    (day_df['season_label'].isin(season_filter)) & 
    (day_df['weathersit_label'].isin(weather_filter))
]

st.divider()

# --- PERTANYAAN 1 ---
st.subheader("1. Rata-rata Penyewaan Berdasarkan Cuaca")
st.markdown("Menjawab Pertanyaan 1: Sebaran penyewaan berdasarkan cuaca.")

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x='weathersit_label', y='cnt', data=filtered_df, palette='Blues_d', errorbar=None, ax=ax1)
ax1.set_xlabel('Kondisi Cuaca')
ax1.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig1)
st.info("**Insight:** Kondisi cuaca *Clear* memiliki rata-rata penyewaan tertinggi, sedangkan *Light Snow/Rain* terendah.")

st.divider()

# --- PERTANYAAN 2 ---
st.subheader("2. Efek Cuaca Kemarin (H-1) Saat Hari Ini Cerah")
st.markdown("Menjawab Pertanyaan 2: Rata-rata penyewaan hari ini (Clear) berdasarkan cuaca kemarin.")

clear_days = filtered_df[filtered_df['weathersit_label'] == 'Clear'].dropna(subset=['weather_prev_day'])
weather_order = ['Light Snow/Rain', 'Mist/Cloudy', 'Clear']
# Reindex hanya untuk urutan, jika data kosong akan diabaikan
clear_grouped = clear_days.groupby('weather_prev_day')['cnt'].mean().reindex(weather_order).dropna().reset_index()

if not clear_grouped.empty:
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=clear_grouped, x='weather_prev_day', y='cnt', palette='coolwarm', ax=ax2)
    ax2.set_xlabel('Kondisi Cuaca Kemarin (H-1)')
    ax2.set_ylabel('Rata-rata Penyewaan Hari Ini')
    st.pyplot(fig2)
    st.info("**Insight:** Hari cerah setelah kemarin hujan ringan memiliki rata-rata penyewaan lebih rendah dibanding hari cerah setelah kemarin cerah.")
else:
    st.warning("Data untuk analisis H-1 tidak cukup pada filter yang dipilih.")