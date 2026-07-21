import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

file_path = os.path.join("data", "raw", "data_tambahan_wa.xlsx")
df_trade = pd.read_excel(file_path, sheet_name='Perdagangan')
df_tourism = pd.read_excel(file_path, sheet_name='Pariwisata')

# 1. Clustering Perdagangan
agg_trade = df_trade.groupby('Negara').agg({
    'Nilai_Ekspor_USD_Juta': 'mean',
    'Nilai_Impor_USD_Juta': 'mean',
    'Volume_Perdagangan': 'mean'
}).reset_index()

features_trade = agg_trade[['Nilai_Ekspor_USD_Juta', 'Nilai_Impor_USD_Juta']]
scaler = StandardScaler()
scaled_trade = scaler.fit_transform(features_trade)

kmeans_trade = KMeans(n_clusters=3, random_state=42, n_init=10)
agg_trade['Cluster_ID'] = kmeans_trade.fit_predict(scaled_trade)

# Mapping Label Deskriptif Perdagangan
trade_label_map = {
    0: 'Defisit / Impor Tinggi',
    1: 'Surplus Utama / Ekspor Tinggi',
    2: 'Volume & Pasar Besar'
}
agg_trade['Kategori_Perdagangan'] = agg_trade['Cluster_ID'].map(trade_label_map)

# 2. Clustering Pariwisata
agg_tourism = df_tourism.groupby('Negara_Asal').agg({
    'Jumlah_Wisatawan': 'mean',
    'Rata_Pengeluaran_USD': 'mean'
}).reset_index()

features_tourism = agg_tourism[['Jumlah_Wisatawan', 'Rata_Pengeluaran_USD']]
scaled_tourism = scaler.fit_transform(features_tourism)

kmeans_tourism = KMeans(n_clusters=3, random_state=42, n_init=10)
agg_tourism['Cluster_ID'] = kmeans_tourism.fit_predict(scaled_tourism)

# Mapping Label Deskriptif Pariwisata
tourism_label_map = {
    0: 'High-Value Tourists (Pengeluaran Tinggi)',
    1: 'Budget Tourists',
    2: 'Mass Tourism (Jumlah Wisatawan Banyak)'
}
agg_tourism['Kategori_Pariwisata'] = agg_tourism['Cluster_ID'].map(tourism_label_map)

# Simpan ke CSV
os.makedirs(os.path.join("data", "processed"), exist_ok=True)
agg_trade.to_csv(os.path.join("data", "processed", "clustered_trade.csv"), index=False)
agg_tourism.to_csv(os.path.join("data", "processed", "clustered_tourism.csv"), index=False)

print("🎉 Script ML Berhasil Diperbarui dengan Label Deskriptif!")