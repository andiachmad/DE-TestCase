# coding: utf-8
# !/usr/bin/env python

import os
import glob
import json
import pandas as pd

# Mencari file JSON Terlebih dahulu
def load_json_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
    return all_files

# Membaca isi file dari setiap file JSON 
def load_json_list_to_df(filelist):
    all_records = []
    for file in filelist:
        with open(file, "r") as f:
            data = json.load(f)
            all_records.append(data)
    df = pd.json_normalize(all_records)
    if "ts" in df.columns:
        df = df.sort_values("ts").reset_index(drop=True)
    return df

def merge_cdc_dataframes_with_sequence(accounts_df, cards_df, savings_df):

    # Step 1: Buat copy untuk tidak memodifikasi original
    accounts = accounts_df.copy()
    cards = cards_df.copy()
    savings = savings_df.copy()
    
    # Step 2: Tambahkan sequence number ke setiap DataFrame
    # Sequence ini akan menjaga urutan original dalam setiap source
    accounts['seq'] = range(len(accounts))
    cards['seq'] = range(len(cards))
    savings['seq'] = range(len(savings))
    
    # Step 3: Tambahkan source identifier untuk tracking
    accounts['source'] = 'accounts'
    cards['source'] = 'cards'
    savings['source'] = 'savings'
    
    # Step 4: Gabungkan semua DataFrame
    combined_df = pd.concat(
        [accounts, cards, savings], 
        ignore_index=True
    )
    
    # Step 5: Sort berdasarkan timestamp, kemudian sequence
    # Gunakan stable sort untuk mempertahankan urutan relatif
    final_df = combined_df.sort_values(
        by=['ts', 'seq'],
        ascending=[True, True],
        kind='stable'  # Stable sort algorithm
    ).reset_index(drop=True)
    
    return final_df

if __name__ == "__main__":
    
    if os.path.exists('/app/data'):
        base_path = '/app/data'  # Docker environment
        print("Running in Docker container")
    else:
        base_path = os.path.join(os.path.dirname(__file__), '..', 'data')  # Local environment
        print("Running locally")
    
    print(f"Data path: {base_path}")

    accounts = load_json_files(os.path.join(base_path, 'accounts'))
    cards = load_json_files(os.path.join(base_path, 'cards'))
    savings_accounts = load_json_files(os.path.join(base_path, 'savings_accounts'))

    accounts_df = load_json_list_to_df(accounts)
    cards_df = load_json_list_to_df(cards)
    savings_df = load_json_list_to_df(savings_accounts)

    # Case 1
    print("Accounts DataFrame:")
    print(accounts_df.to_string())
    print("\nCards DataFrame:")
    print(cards_df.to_string())
    print("\nSavings Accounts DataFrame:")
    print(savings_df.to_string())

    # Case 2
    result_df = merge_cdc_dataframes_with_sequence(accounts_df, cards_df, savings_df)
    print("Complete Historical Table View - Denormalized")
    print(result_df.head(50).to_string())

    # Case 3
    # Transaction Summary
    # | No | Timestamp       | Jenis   | Nilai Transaksi |
    # |----|-----------------|---------|-----------------|
    # | 1  | 1577955600000   | Savings | 15000.0         |
    # | 2  | 1578313800000   | Card    | 12000.0         |
    # | 3  | 1578420000000   | Card    | 19000.0         |
    # | 4  | 1578648600000   | Savings | 40000.0         |
    # | 5  | 1578654000000   | Card    | 0.0             |
    # | 6  | 1578654000000   | Savings | 21000.0         |
    # | 7  | 1579361400000   | Card    | 37000.0         |
    # | 8  | 1579505400000   | Savings | 33000.0         |
    # Total transaksi: 8
