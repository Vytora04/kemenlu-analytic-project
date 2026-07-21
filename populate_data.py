import mysql.connector

# Data 10 Komoditas Impor Utama Indonesia (Sesuai TradeMap Soal Kemenlu)
products_data = [
    ("27", "Mineral fuels, mineral oils and products of their distillation", 2020, 15779402),
    ("27", "Mineral fuels, mineral oils and products of their distillation", 2021, 28840089),
    ("27", "Mineral fuels, mineral oils and products of their distillation", 2022, 44896545),
    ("27", "Mineral fuels, mineral oils and products of their distillation", 2023, 40120442),
    ("27", "Mineral fuels, mineral oils and products of their distillation", 2024, 40662208),
    
    ("84", "Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof", 2020, 21808516),
    ("84", "Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof", 2021, 25845785),
    ("84", "Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof", 2022, 31571715),
    ("84", "Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof", 2023, 32155168),
    ("84", "Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof", 2024, 33514326),
    
    ("85", "Electrical machinery and equipment and parts thereof; sound recorders", 2020, 19081250),
    ("85", "Electrical machinery and equipment and parts thereof; sound recorders", 2021, 22338487),
    ("85", "Electrical machinery and equipment and parts thereof; sound recorders", 2022, 26398843),
    ("85", "Electrical machinery and equipment and parts thereof; sound recorders", 2023, 25782452),
    ("85", "Electrical machinery and equipment and parts thereof; sound recorders", 2024, 27046425),
    
    ("72", "Iron and steel", 2020, 6855166),
    ("72", "Iron and steel", 2021, 11957119),
    ("72", "Iron and steel", 2022, 13928186),
    ("72", "Iron and steel", 2023, 11381142),
    ("72", "Iron and steel", 2024, 10664432),
    
    ("39", "Plastics and articles thereof", 2020, 7154565),
    ("39", "Plastics and articles thereof", 2021, 10185158),
    ("39", "Plastics and articles thereof", 2022, 11123493),
    ("39", "Plastics and articles thereof", 2023, 9402360),
    ("39", "Plastics and articles thereof", 2024, 10592767),
    
    ("87", "Vehicles other than railway or tramway rolling stock", 2020, 4437177),
    ("87", "Vehicles other than railway or tramway rolling stock", 2021, 6702341),
    ("87", "Vehicles other than railway or tramway rolling stock", 2022, 9500437),
    ("87", "Vehicles other than railway or tramway rolling stock", 2023, 10199907),
    ("87", "Vehicles other than railway or tramway rolling stock", 2024, 9658807),
    
    ("29", "Organic chemicals", 2020, 5026841),
    ("29", "Organic chemicals", 2021, 7292450),
    ("29", "Organic chemicals", 2022, 7712347),
    ("29", "Organic chemicals", 2023, 6421751),
    ("29", "Organic chemicals", 2024, 7109927),
    
    ("10", "Cereals", 2020, 3021813),
    ("10", "Cereals", 2021, 4073969),
    ("10", "Cereals", 2022, 4455280),
    ("10", "Cereals", 2023, 5952632),
    ("10", "Cereals", 2024, 6816918),
    
    ("71", "Natural or cultured pearls, precious stones, metals", 2020, 2008909),
    ("71", "Natural or cultured pearls, precious stones, metals", 2021, 2845137),
    ("71", "Natural or cultured pearls, precious stones, metals", 2022, 3699619),
    ("71", "Natural or cultured pearls, precious stones, metals", 2023, 2795839),
    ("71", "Natural or cultured pearls, precious stones, metals", 2024, 4779280),
    
    ("90", "Optical, photographic, cinematographic, measuring instruments", 2020, 2907069),
    ("90", "Optical, photographic, cinematographic, measuring instruments", 2021, 3183409),
    ("90", "Optical, photographic, cinematographic, measuring instruments", 2022, 3557660),
    ("90", "Optical, photographic, cinematographic, measuring instruments", 2023, 3793047),
    ("90", "Optical, photographic, cinematographic, measuring instruments", 2024, 4420862)
]

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="kemenlu_test"
)
cursor = db.cursor()

# Kosongkan tabel dan isi ulang
cursor.execute("TRUNCATE TABLE TbTrade")

sql = "INSERT INTO TbTrade (Negara, Kode_HS, Label, Tahun, Jumlah, Satuan, Sumber_Data) VALUES (%s, %s, %s, %s, %s, %s, %s)"

for hs, label, th, val in products_data:
    cursor.execute(sql, ("Indonesia", hs, label, th, val, "-", "Trademap"))

db.commit()
print("🎉 BERHASIL! Database TbTrade sekarang terisi 10 Komoditas Utama Asli TradeMap.")
db.close()