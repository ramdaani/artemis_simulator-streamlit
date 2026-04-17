import os
import pandas as pd
from astroquery.jplhorizons import Horizons

def get_moon_data(start_date, end_date):
    """
    Mengambil data posisi dan kecepatan Bulan dari NASA JPL Horizons.
    Data disimpan ke folder data/ agar tidak download ulang.
    """
    cache_path = "data/moon_ephemeris_2026.csv"
    
    # Cek apakah data sudah pernah di-download sebelumnya
    if os.path.exists(cache_path):
        print("--- Mengambil data Bulan dari Cache (Lokal) ---")
        return pd.read_csv(cache_path)

    print("--- Menghubungi Server NASA JPL Horizons... ---")
    
    # 301 adalah ID untuk Bulan, 500@399 artinya posisi dilihat dari pusat Bumi
    obj = Horizons(id='301', location='500@399', 
                   epochs={'start': start_date, 'stop': end_date, 'step': '1h'})
    
    vec = obj.vectors()
    
    # Pilih kolom penting: Waktu, Posisi (x,y,z), Kecepatan (vx,vy,vz)
    df = vec['datetime_str', 'x', 'y', 'z', 'vx', 'vy', 'vz'].to_pandas()
    
    # Buat folder data jika belum ada
    os.makedirs("data", exist_ok=True)
    
    # Simpan ke CSV
    df.to_csv(cache_path, index=False)
    print(f"--- Data berhasil disimpan ke {cache_path} ---")
    
    return df

if __name__ == "__main__":
    # Test jalankan script ini sendiri
    data = get_moon_data('2026-04-01', '2026-04-10')
    print(data.head())