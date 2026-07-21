# 🏛️ Dashboard Analisis Perdagangan & Diplomasi Ekonomi - Kemenlu RI

Aplikasi web interaktif dan data pipeline yang dikembangkan untuk tes kompetensi rekrutmen magang posisi **Analytic Engineer (Data Engineer + Data Scientist)** di Pusat Strategi Kebijakan Isu Khusus dan Analisis Data (BSKLN Kemenlu).

## 🚀 Fitur Utama

### 1. Analisis Perdagangan (TradeMap Data)

- KPI Card Metrics: jumlah ekspor, impor, neraca perdagangan, dan volume perdagangan tahun terakhir.
- Grafik tren perdagangan 2020–2024 untuk ekspor, impor, neraca, dan volume perdagangan.
- Top 10 komoditas berdasarkan nilai transaksi.
- Filter dinamis berdasarkan tahun, negara mitra, dan komoditas/label.

### 2. Machine Learning Clustering (K-Means)

- Clustering perdagangan untuk mengelompokkan negara mitra berdasarkan profil ekspor vs impor.
- Clustering pariwisata untuk mengelompokkan negara asal wisatawan berdasarkan jumlah wisatawan vs rata-rata pengeluaran.
- Label deskriptif seperti High-Value Tourists, Mass Tourism, dan kategori serupa.

### 3. AI Diplomacy Assistant (Powered by Groq & Llama 3)

- Integrasi LLM chatbot berbasis Groq API dengan model `llama-3.3-70b-versatile`.
- Memberikan insight diplomasi ekonomi, rekomendasi kebijakan strategis, dan analisis data secara real-time.

### 4. Raw Data Database View

- Tampilan tabel data mentah transaksi perdagangan langsung dari basis data MySQL (`TbTrade`).

## 🛠️ Tech Stack & Library

- **Language:** Python 3.x
- **Database:** MySQL
- **Frontend / Framework:** Streamlit
- **Data Manipulation:** Pandas, NumPy
- **Data Visualization:** Plotly
- **Machine Learning:** Scikit-Learn (StandardScaler & KMeans)
- **AI Integration:** Groq API

## ⚙️ Cara Menjalankan Proyek di Lokal

### 1. Clone Repositori

```bash
git clone https://github.com/Vytora04/kemenlu-analytic-project.git
cd kemenlu-analytic-project
```

### 2. Setup Virtual Environment & Dependencies

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 3. Eksekusi Script Pipeline

```bash
python scripts/01_data_ingestion.py
python scripts/02_machine_learning.py
```

### 4. Jalankan Aplikasi Streamlit

```bash
streamlit run app.py
```

## 📁 Struktur Proyek

```text
app.py
populate_data.py
README.md
requirements.txt
data/
   processed/
      clustered_tourism.csv
      clustered_trade.csv
   raw/
      data_tambahan_wa.xslx
      trademap_data.xslx
db/
   schema.sql
scripts/
   01_data_ingestion.py
   02_machine_learning.py
   generate_dummy.py
```

## 👤 Pengembangan

Proyek ini dikembangkan untuk kebutuhan analisis perdagangan, pariwisata, dan diplomasi ekonomi berbasis data dengan antarmuka interaktif.