## Deskripsi 
Solusi ini digunakan untuk menganalisis event log Change Data Capture (CDC) dari tiga sumber data (accounts, cards, savings_accounts) dalam format JSON. 

```
project/
├── data/ # Folder data JSON, dipisah jadi 3 subfolder
│ ├── accounts/ 
│ ├── cards/ 
│ └── savings_accounts/ 
├── solution/ 
│ ├── case.py # Script utama Anda (harus disubmit)
│ ├── case.ipynb 
│ ├── Dockerfile # Buat container
│ ├── requirements.txt # Libraries yang diperlukan
│ ├── deploy.sh # Script otomatis build & run di Docker
│ └── README.md 
```

## Penjelasan Solusi
Penjelasan Metode dan Alur Analisis
1. load_json_files(filepath)

    - Mencari semua file JSON di folder data secara rekursif.

    - Tujuannya agar data event dari berbagai sumber bisa langsung diambil tanpa manual.

2. load_json_list_to_df(filelist)

    - Membaca isi file JSON dan mengubahnya menjadi DataFrame pandas.

    - Data diurutkan berdasarkan timestamp agar analisis historis lebih akurat.

3. merge_cdc_dataframes_with_sequence(accounts_df, cards_df, savings_df)

    - Menambahkan sequence number untuk menjaga urutan event dari masing-masing tabel.

    - Menambahkan kolom source agar asal event jelas.

    - Menggabungkan semua event ke satu tabel lebar (denormalized), lalu diurutkan berdasarkan waktu dan urutan event.

    - Ini penting agar event dengan timestamp sama tetap urut sesuai sumber aslinya.

4. Bagian Main

    - Menentukan path data secara otomatis (Docker atau lokal).

    - Menampilkan tabular table (Case 1).

    - Menampilkan tabel gabungan (Case 2).

    - Diskusi berapa banyak transaksi yang terjadi (Case 3).


## Cara menjalankan Docker Local

- Docker sudah terinstall

- Pastikan Docker sudah berjalan, agar bisa bisa terhubung ke Docker Engine
    
- Folder data/ dengan subfolder accounts/, cards/, savings_accounts/

- File JSON tersedia di masing-masing subfolder

Step-by-Step

```
cd solution
docker build -t cdc-analysis .

## Jalankan container dengan mount folder data
ex : docker run --rm -v "F:\...\testcase\DE-TestCase\data:/app/data:ro" cdc-analysis

> Catatan: Ganti path `F:\...\testcase\DE-TestCase\data` sesuai lokasi folder data berada

```

## Output

1. Tabular Table

    Menampilkan semua event dari masing-masing tabel (accounts, cards, savings_accounts).

2. Denormalized Historical View

    Gabungan semua event dari tiga tabel, diurutkan berdasarkan waktu dan urutan event.

3. Transaction Analysis (Case 3)

   **Lokasi Analisis:** File `solution/case.py`

## Hasil Analsis

| No | Timestamp       | Jenis   | Nilai Transaksi |
|----|-----------------|---------|-----------------|
| 1  | 1577955600000   | Savings | 15000.0         |
| 2  | 1578313800000   | Card    | 12000.0         |
| 3  | 1578420000000   | Card    | 19000.0         |
| 4  | 1578648600000   | Savings | 40000.0         |
| 5  | 1578654000000   | Card    | 0.0             |
| 6  | 1578654000000   | Savings | 21000.0         |
| 7  | 1579361400000   | Card    | 37000.0         |
| 8  | 1579505400000   | Savings | 33000.0         |

**Ringkasan:**
- **Total transaksi**: 8 transaksi
- **Transaksi Savings**: 4 transaksi (perubahan saldo tabungan)
- **Transaksi Card**: 4 transaksi (perubahan penggunaan kredit)
- **Total perubahan saldo savings**: +-109,000.0
- **Total perubahan credit card**: +-68,000.0 (sebelum pelunasan)
