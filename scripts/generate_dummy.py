import pandas as pd
import numpy as np
import os

# Buat folder data/raw jika belum ada
os.makedirs(os.path.join("data", "raw"), exist_ok=True)

# 1. Dummy Data Perdagangan (10 Negara Mitra)
negara = ['China', 'Amerika Serikat', 'Jepang', 'Singapura', 'India', 'Malaysia', 'Korea Selatan', 'Australia', 'Jerman', 'Thailand']

data_perdagangan = []
for n in negara:
    for th in range(2020, 2025):
        ekspor = np.random.uniform(500, 5000)
        impor = np.random.uniform(400, 4500)
        data_perdagangan.append({
            'Negara': n,
            'Tahun': th,
            'Nilai_Ekspor_USD_Juta': round(ekspor, 2),
            'Nilai_Impor_USD_Juta': round(impor, 2),
            'Volume_Perdagangan': round(ekspor + impor, 2)
        })

df_perdagangan = pd.DataFrame(data_perdagangan)

# 2. Dummy Data Pariwisata
data_pariwisata = []
for n in negara:
    for th in range(2020, 2025):
        wisatawan = np.random.randint(10000, 500000)
        pengeluaran = np.random.uniform(800, 2000) # USD per kunjungan
        data_pariwisata.append({
            'Negara_Asal': n,
            'Tahun': th,
            'Jumlah_Wisatawan': wisatawan,
            'Rata_Pengeluaran_USD': round(pengeluaran, 2)
        })

df_pariwisata = pd.DataFrame(data_pariwisata)

# 3. Simpan ke Excel 2 Sheet
output_path = os.path.join("data", "raw", "data_tambahan_wa.xlsx")
with pd.ExcelWriter(output_path) as writer:
    df_perdagangan.to_excel(writer, sheet_name='Perdagangan', index=False)
    df_pariwisata.to_excel(writer, sheet_name='Pariwisata', index=False)

print(f"File dummy berhasil dibuat di: {output_path}")