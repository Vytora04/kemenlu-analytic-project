CREATE DATABASE IF NOT EXISTS kemenlu_test;
USE kemenlu_test;

CREATE TABLE IF NOT EXISTS TbTrade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Negara VARCHAR(100),
    Kode_HS VARCHAR(50),
    Label TEXT,
    Tahun INT,
    Jumlah DECIMAL(18, 2),
    Satuan VARCHAR(50),
    Sumber_Data VARCHAR(50)
);