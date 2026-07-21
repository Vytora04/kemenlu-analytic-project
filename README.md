# 🏛️ Dashboard Analisis Perdagangan & Diplomasi Ekonomi - Kemenlu RI

Aplikasi web interaktif dan *data pipeline* yang dikembangkan untuk tes kompetensi rekrutmen magang posisi **Analytic Engineer (Data Engineer + Data Scientist)** di Pusat Strategi Kebijakan Isu Khusus dan Analisis Data (BSKLN Kemenlu).

---

## 🚀 Fitur Utama

1. **Analisis Perdagangan (TradeMap Data):**
   * Visualisasi tren nilai impor Indonesia (2020–2024).
   * Grafik *Top 10 Komoditas Utama* impor Indonesia.
   * Ringkasan indikator performa utama (KPI Metrics) serta tabel data dinamis dengan *filter/slicer*.

2. **Machine Learning Clustering (K-Means):**
   * Pengelompokan negara mitra berdasarkan data Perdagangan (*Ekspor vs Impor*).
   * Pengelompokan negara asal wisatawan berdasarkan data Pariwisata (*Jumlah Wisatawan vs Rata-rata Pengeluaran*).
   * Labeling kategori deskriptif (*High-Value Tourists, Mass Tourism, Surplus Utama, dll.*).

3. **AI Diplomacy Assistant (Groq & Llama 3):**
   * Integration *LLM Chatbot* berbasis **Groq API** (`llama-3.3-70b-versatile`).
   * Memberikan insight diplomasi ekonomi dan rekomendasi kebijakan strategis secara *real-time*.

4. **Raw Data Database View:**
   * Tampilan tabel utuh data transaksi perdagangan langsung dari basis data MySQL (`TbTrade`).

---

## 🛠️ Tech Stack & Library

* **Language:** Python 3.x
* **Database:** MySQL
* **Frontend / Framework:** Streamlit
* **Data Manipulation:** Pandas, NumPy, openpyxl
* **Data Visualization:** Plotly
* **Machine Learning:** Scikit-Learn (StandardScaler & KMeans)
* **AI Integration:** Groq API

---

## ⚙️ Cara Menjalankan Proyek di Lokal

### 1. Clone Repositori
```bash
git clone [https://github.com/Vytora04/kemenlu-analytic-project.git](https://github.com/Vytora04/kemenlu-analytic-project.git)
cd kemenlu-analytic-project