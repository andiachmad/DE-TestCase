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
docker run --rm -v "${PWD}\..\data:/app/data:ro" cdc-analysis
```

## Output

1. Tabular Table

    Menampilkan semua event dari masing-masing tabel (accounts, cards, savings_accounts).

2. Denormalized Historical View

    Gabungan semua event dari tiga tabel, diurutkan berdasarkan waktu dan urutan event.

3. Transaction Analysis

    Ringkasan transaksi yang mengubah saldo savings (set.balance) dan kredit kartu (set.credit_used).
