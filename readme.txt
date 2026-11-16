# Bike Sharing Data Analysis Dashboard 🚲

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis dataset penyewaan sepeda (Bike Sharing Dataset) untuk menemukan *insight* tersembunyi (out of the box) terkait perilaku pengguna terhadap kondisi cuaca.

## Pertanyaan Bisnis
1. Pada kondisi cuaca ekstrem seperti apa penyewaan sepeda mencapai titik terendah, dan apakah ada anomali di mana penyewaan tetap tinggi meskipun cuaca sedang buruk?
2. Apakah kondisi cuaca buruk pada hari sebelumnya (H-1) memiliki efek psikologis yang menekan jumlah penyewaan sepeda pada hari ini (H), meskipun cuaca hari ini sedang cerah?

## Struktur Direktori
- `dashboard/`
  - `dashboard.py` (File utama Streamlit)
  - `day.csv` (Dataset harian)
  - `hour.csv` (Dataset per jam)
- `notebook.ipynb` (Proses analisis data & EDA)
- `requirements.txt` (Library yang dibutuhkan)
- `README.md` (Dokumentasi)

## Cara Menjalankan Dashboard di Lokal
1. Pastikan Anda memiliki Python (versi 3.8+).
2. Clone repository ini atau download foldernya.
3. Buka terminal/command prompt, arahkan ke folder proyek.
4. Install library yang dibutuhkan:
   ```bash
   pip install -r requirements.txt