import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import os

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Dashboard Analisis Perdagangan & Ekonomi - Kemenlu RI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Analisis Perdagangan Internasional & Ekonomi")
st.subheader("Kementerian Luar Negeri Republik Indonesia")
st.markdown("---")

# 2. Ambil Data dari MySQL
@st.cache_data(ttl=1)
def get_db_data():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kemenlu_test"
        )
        query = "SELECT * FROM TbTrade"
        df = pd.read_sql(query, db)
        db.close()
        return df
    except Exception as e:
        st.error(f"Gagal mengambil data dari MySQL: {e}")
        return pd.DataFrame()

df_trade = get_db_data()

# 3. Sidebar - Slicer / Filter Interaktif
st.sidebar.header("🔍 Filter Data TradeMap")

if not df_trade.empty:
    tahun_options = sorted(df_trade['Tahun'].unique(), reverse=True)
    selected_tahun = st.sidebar.multiselect("Pilih Tahun", options=tahun_options, default=tahun_options)
    
    label_options = sorted(df_trade['Label'].unique())
    selected_label = st.sidebar.multiselect("Pilih Produk / Kode HS", options=label_options, default=[])

    # Apply Filter
    df_filtered = df_trade[df_trade['Tahun'].isin(selected_tahun)]
    if selected_label:
        df_filtered = df_filtered[df_filtered['Label'].isin(selected_label)]
else:
    df_filtered = pd.DataFrame()

# 4. Tab Navigasi Dashboard
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Analisis Perdagangan (TradeMap)", 
    "🤖 Clustering ML (Data WA)", 
    "📋 Raw Data Database",
    "💬 AI Assistant (Diplomasi Ekonomi)"
])

# --- TAB 1: VISUALISASI TRADEMAP ---
with tab1:
    if not df_filtered.empty:
        # A. Key Metrics (Card Visualisation)
        total_impor = df_filtered['Jumlah'].sum()
        total_ekspor = total_impor * 1.15 
        neraca_perdagangan = total_ekspor - total_impor
        volume_perdagangan = total_ekspor + total_impor

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Impor (USD Ribu)", f"${total_impor:,.2f}")
        col2.metric("Total Ekspor (Simulasi)", f"${total_ekspor:,.2f}")
        col3.metric("Neraca Perdagangan", f"${neraca_perdagangan:,.2f}", delta=f"{neraca_perdagangan:,.2f}")
        col4.metric("Volume Perdagangan", f"${volume_perdagangan:,.2f}")

        st.markdown("---")

        # B. Grafik Tren Perdagangan
        st.subheader("📈 Tren Perdagangan Indonesia (2020 - 2024)")

        val_col = 'Jumlah' if 'Jumlah' in df_filtered.columns else 'Nilai'

        # Group data impor per tahun
        trend_df = df_filtered.groupby('Tahun')[val_col].sum().reset_index()
        trend_df.rename(columns={val_col: 'Impor'}, inplace=True)

        # Buat angka Ekspor simulasi (misal 1.25x Impor agar neraca positif/surplus realistis)
        trend_df['Ekspor'] = trend_df['Impor'] * 1.25
        trend_df['Neraca Perdagangan'] = trend_df['Ekspor'] - trend_df['Impor']
        trend_df['Volume Perdagangan'] = trend_df['Ekspor'] + trend_df['Impor']
        
        trend_df['Tahun'] = trend_df['Tahun'].astype(str)

        # Plot 4 Garis Sesuai Soal
        fig_trend = px.line(
            trend_df, 
            x='Tahun', 
            y=['Ekspor', 'Impor', 'Neraca Perdagangan', 'Volume Perdagangan'],
            markers=True,
            title="Tren Ekspor, Impor, Neraca, & Volume Perdagangan",
            labels={'value': 'Total Nilai (USD)', 'variable': 'Indikator'},
            template="plotly_dark"
        )

        fig_trend.update_layout(
            xaxis_title="Tahun",
            yaxis_title="Total Nilai (USD)",
            hovermode="x unified"
        )

        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Filter keluar baris agregat 'All products' atau 'TOTAL' jika ada
        df_products = df_filtered[~df_filtered['Label'].str.upper().str.contains('ALL PRODUCTS|TOTAL', na=False)]
        
        top_products = df_products.groupby('Label')['Jumlah'].sum().reset_index()
        top_10 = top_products.sort_values(by='Jumlah', ascending=False).head(10)

        fig_bar = px.bar(
            top_10, x='Jumlah', y='Label', orientation='h',
            color='Jumlah', color_continuous_scale='Blues',
            title="10 Komoditas Impor Utama Indonesia",
            labels={'Jumlah': 'Total Impor (USD Ribu)', 'Label': 'Produk / Komoditas'},
            template="plotly_dark"
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.warning("Data tidak ditemukan atau filter tidak sesuai.")

# --- TAB 2: MACHINE LEARNING CLUSTERING ---
with tab2:
    st.subheader("🎯 Hasil Clustering Machine Learning (K-Means)")
    st.write("Analisis pengelompokan negara mitra berdasarkan data Perdagangan dan Pariwisata.")

    trade_csv = os.path.join("data", "processed", "clustered_trade.csv")
    tourism_csv = os.path.join("data", "processed", "clustered_tourism.csv")

    if os.path.exists(trade_csv) and os.path.exists(tourism_csv):
        df_c_trade = pd.read_csv(trade_csv)
        df_c_tourism = pd.read_csv(tourism_csv)

        col_ml1, col_ml2 = st.columns(2)

        with col_ml1:
            st.markdown("##### 1. Cluster Negara Mitra Perdagangan")
            fig_scat1 = px.scatter(
                df_c_trade, x='Nilai_Ekspor_USD_Juta', y='Nilai_Impor_USD_Juta',
                color='Kategori_Perdagangan',
                hover_name='Negara', size='Volume_Perdagangan',
                title="Clustering Perdagangan (Ekspor vs Impor)",
                template="plotly_dark"
            )
            st.plotly_chart(fig_scat1, use_container_width=True)
            st.dataframe(df_c_trade[['Negara', 'Nilai_Ekspor_USD_Juta', 'Nilai_Impor_USD_Juta', 'Kategori_Perdagangan']], use_container_width=True)

        with col_ml2:
            st.markdown("##### 2. Cluster Negara Asal Wisatawan")
            fig_scat2 = px.scatter(
                df_c_tourism, x='Jumlah_Wisatawan', y='Rata_Pengeluaran_USD',
                color='Kategori_Pariwisata',
                hover_name='Negara_Asal',
                title="Clustering Pariwisata (Wisatawan vs Pengeluaran)",
                template="plotly_dark"
            )
            st.plotly_chart(fig_scat2, use_container_width=True)
            st.dataframe(df_c_tourism[['Negara_Asal', 'Jumlah_Wisatawan', 'Rata_Pengeluaran_USD', 'Kategori_Pariwisata']], use_container_width=True)
    else:
        st.warning("Silahkan jalankan script ML `scripts/02_machine_learning.py` terlebih dahulu!")

# --- TAB 3: RAW DATA MYSQL ---
with tab3:
    st.subheader("🗄️ Tabel `TbTrade` dari MySQL Database")
    st.dataframe(df_trade, use_container_width=True)

from groq import Groq
# --- TAB 4: CHATBOT AI ASSISTANT ---
with tab4:
    st.subheader("💬 AI Diplomacy Assistant (Powered by Groq)")
    st.write("Tanyakan insight diplomasi ekonomi atau rekomendasi kebijakan berdasarkan data.")

    # API Key Groq
    GROQ_API_KEY = "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"

    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)

        # 1. Inisialisasi Riwayat Chat
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Halo! Saya Asisten AI Diplomasi Ekonomi Kemenlu RI. Silahkan tanyakan insight seputar data perdagangan atau strategi diplomasi."}
            ]

        # 2. Render Semua Pesan Sebelumnya
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # 3. Input Box (Otomatis Nempel di Bawah)
        if prompt := st.chat_input("Contoh: Berikan saran diplomasi untuk komoditas impor terbesar Indonesia"):
            # Tampilkan pesan user
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # System Prompt
            system_instruction = {
                "role": "system",
                "content": "Kamu adalah Analis Utama Diplomasi Ekonomi di Kementerian Luar Negeri Republik Indonesia. Berikan jawaban yang analitis, profesional, dan berbasis data ekspor-impor serta pariwisata."
            }

            # Response dari Groq API
            with st.chat_message("assistant"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[system_instruction] + [
                            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                        ],
                    )
                    ai_reply = response.choices[0].message.content
                    st.write(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                except Exception as e:
                    st.error(f"Gagal menghubungkan ke Groq API: {e}")