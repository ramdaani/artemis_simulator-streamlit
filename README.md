# 🚀 Artemis 2 Lunar Flyby Simulator

Projek ini adalah simulator trajektori penerbangan luar angkasa yang merekonstruksi rute misi **Artemis 2** menggunakan data *real-time* dari **NASA JPL Horizons API**. Program ini menghitung bagaimana pesawat Orion berinteraksi dengan gravitasi Bumi dan Bulan untuk menciptakan rute *Free Return Trajectory*.

## 📌 Gambaran Umum
Simulator ini menggunakan integrasi numerik **Runge-Kutta (RK45)** untuk menyelesaikan persamaan gerak Newton. Tidak seperti simulasi game biasa, projek ini memperhitungkan perubahan posisi Bulan yang dinamis selama misi berlangsung (1-10 April 2026).

## 🛠️ Struktur Project
```text
artemis_sim/
├── data/               # Cache data posisi Bulan dari NASA (.csv)
├── src/
│   ├── nasa_api.py     # Integrasi dengan NASA JPL Horizons API
│   └── physics.py      # Engine Fisika (RK45 & Gravitasi Ganda)
├── main.py             # Entry point & Visualisasi 3D Plotly
├── .gitignore          
├── requirements.txt    
└── README.md           
```

## 🚀 Fitur Utama
Data NASA Asli: Mengambil vektor posisi dan kecepatan (state vectors) Bulan secara presisi.

Double-Body Gravity: Menghitung pengaruh gravitasi Bumi dan Bulan secara bersamaan.

Visualisasi Interaktif: Grafik 3D menggunakan Plotly yang memungkinkan user untuk melakukan zoom, rotate, dan pan pada rute.

Caching System: Data dari NASA disimpan secara lokal untuk mempercepat eksekusi berikutnya.

## 📊 Penjelasan Output & Rute

![Artemis 2 Simulation Output](/src/assets/newplot.png)

Hasil output visualisasi menampilkan tiga komponen utama:

- Titik Biru (Bumi): Pusat koordinat (0,0,0).
- Garis Putus-putus Abu-abu: Jalur orbit Bulan selama 10 hari misi.
- Garis Merah (Rute Orion): Menunjukkan lintasan pesawat dari Bumi menuju Bulan.

## Analisis Lintasan (Free Return Trajectory)
Dalam simulasi ini, Orion diluncurkan dengan kecepatan sekitar 10.8 - 10.9 km/s (Trans-Lunar Injection).

- Fase Pergi: Garis merah akan terlihat lurus memanjang sejauh ~380.000 km.
- Fase Flyby: Saat mendekati titik perak (Bulan), gravitasi Bulan akan menarik pesawat. Jika navigasi presisi, rute akan membengkok tajam di belakang Bulan.

## 📚 Library yang Digunakan
astroquery: Menghubungi server NASA JPL Horizons.
scipy: Melakukan integrasi numerik kompleks (RK45).
plotly: Membuat dashboard visualisasi 3D yang interaktif.
pandas & numpy: Pengolahan data numerik.