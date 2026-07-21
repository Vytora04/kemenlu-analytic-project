import pandas as pd
import mysql.connector
import os

RAW_FILE_PATH = os.path.join("data", "raw", "trademap_data.xlsx")

print("Membaca file Excel TradeMap...")
xls = pd.ExcelFile(RAW_FILE_PATH)
df_raw = pd.read_excel(xls, sheet_name=0, header=None)

# 1. Cari baris header yang memuat kolom tahun
header_row_idx = None
for idx, row in df_raw.iterrows():
    row_str = " ".join(row.dropna().astype(str))
    if any(str(yr) in row_str for yr in [2020, 2021, 2022, 2023, 2024]):
        header_row_idx = idx
        break

if header_row_idx is None:
    header_row_idx = 0

# 2. Baca Excel tepat pada baris header
df = pd.read_excel(RAW_FILE_PATH, skiprows=header_row_idx)
df.columns = [str(c).strip() for c in df.columns]

# 3. Cari kolom spesifik
tahun_cols = [c for c in df.columns if any(str(yr) in str(c) for yr in [2020, 2021, 2022, 2023, 2024])]

# Cari kolom HS Code (bisa 'Code', 'HS', 'reporterCd', dll)
code_col = None
for c in df.columns:
    if any(k in c.lower() for k in ['code', 'hs', 'kode', 'product cd']):
        code_col = c
        break
if not code_col:
    code_col = df.columns[0]

# Cari kolom Label Komoditas (bukan nama negara/reporter!)
label_col = None
for c in df.columns:
    # Cari kolom deskripsi produk/komoditas
    if any(k in c.lower() for k in ['label', 'product', 'deskripsi', 'description', 'komoditas']) and 'reporter' not in c.lower():
        label_col = c
        break

# Jika tidak ketemu, biasanya kolom label produk berada tepat di sebelah kanan kolom Code
if not label_col:
    code_idx = list(df.columns).index(code_col)
    label_col = df.columns[code_idx + 1]

print(f"Kolom Kode HS : {code_col}")
print(f"Kolom Label   : {label_col}")

# 4. Filter & Rename
df_selected = df[[code_col, label_col] + tahun_cols].copy()
df_selected = df_selected.rename(columns={code_col: 'Kode_HS', label_col: 'Label'})

# 5. Unpivot / Melt Data
df_melted = pd.melt(
    df_selected, 
    id_vars=['Kode_HS', 'Label'], 
    value_vars=tahun_cols,
    var_name='Tahun_Raw', 
    value_name='Jumlah'
)

df_melted['Tahun'] = df_melted['Tahun_Raw'].astype(str).str.extract(r'(\d{4})').astype(int)
df_melted['Negara'] = 'Indonesia'
df_melted['Satuan'] = '-'
df_melted['Sumber_Data'] = 'Trademap'

# Format angka
df_melted['Jumlah'] = pd.to_numeric(
    df_melted['Jumlah'].astype(str).str.replace(',', '').str.replace(' ', ''), 
    errors='coerce'
).fillna(0)

# Clean baris TOTAL & Indonesia
df_clean = df_melted[
    ~df_melted['Kode_HS'].astype(str).str.upper().str.contains('TOTAL|ALL', na=False) &
    ~df_melted['Label'].astype(str).str.upper().str.contains('TOTAL|ALL PRODUCTS|INDONESIA', na=False)
].dropna(subset=['Kode_HS']).reset_index(drop=True)

# 6. Insert Ulang ke MySQL
print("Memasukkan data baru ke MySQL...")
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="kemenlu_test"
)
cursor = db.cursor()

cursor.execute("TRUNCATE TABLE TbTrade") # Kosongkan data lama

sql = """
INSERT INTO TbTrade (Negara, Kode_HS, Label, Tahun, Jumlah, Satuan, Sumber_Data)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

count = 0
for _, row in df_clean.iterrows():
    val = (
        str(row['Negara']),
        str(row['Kode_HS']),
        str(row['Label']),
        int(row['Tahun']),
        float(row['Jumlah']),
        str(row['Satuan']),
        str(row['Sumber_Data'])
    )
    cursor.execute(sql, val)
    count += 1

db.commit()
print(f"🎉 SUKSES! {count} baris komoditas berhasil dimasukkan ke MySQL.")

cursor.close()
db.close()