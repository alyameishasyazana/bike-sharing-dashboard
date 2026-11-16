# Bike Sharing Analysis Dashboard 🚲✨

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis dataset penyewaan sepeda (Bike Sharing Dataset) untuk menemukan *insight* tersembunyi terkait perilaku pengguna terhadap anomali cuaca ekstrem dan efek psikologis cuaca hari sebelumnya (H-1).

**Link Dashboard Streamlit:** https://bike-sharing-dashboard-ilboyzfejvk9vqvzfrejok.streamlit.app/

## Struktur Direktori
- `dashboard/` : Folder berisi file Streamlit (`dashboard.py`) dan dataset (`day.csv`, `hour.csv`).
- `notebook.ipynb` : File Jupyter Notebook berisi proses analisis data dari awal hingga akhir.
- `requirements.txt` : File berisi daftar library yang dibutuhkan.
- `README.md` : Dokumentasi proyek.

---

## Setup Environment - Anaconda
Jika Anda menggunakan Anaconda, jalankan perintah berikut di terminal/Anaconda Prompt:
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
