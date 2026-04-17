import numpy as np
import plotly.graph_objects as go
import pandas as pd
from src.nasa_api import get_moon_data
from src.physics import propagate_orbit

def main():
    print("=== Menjalankan Misi Artemis 2: Flyby Lunar ===")
    
    start_date = '2026-04-01'
    end_date = '2026-04-10'

    # 1. Ambil data NASA
    moon_df = get_moon_data(start_date, end_date)

    # 2. Setup State Vector (TLI - Trans Lunar Injection)
    # Posisi awal: 400km di atas permukaan Bumi
    # Kecepatan: ~10.9 km/s dengan sudut arah menuju orbit Bulan
    # Angka ini di-tuning khusus untuk posisi Bulan April 2026
    initial_state = [-6778, 0, 0, 1.25, -10.82, 0.45] 

    print("--- Menghitung Rute Pergi-Pulang (10 Hari) ---")
    orion_traj, t_steps = propagate_orbit(initial_state, moon_df)

    print("--- Membuat Visualisasi 3D Interaktif ---")
    fig = go.Figure()

    # Bumi
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0], mode='markers',
        marker=dict(size=12, color='royalblue', symbol='circle'),
        name='Bumi'
    ))

    # Lintasan Orbit Bulan (Garis Abu-abu)
    fig.add_trace(go.Scatter3d(
        x=moon_df['x'], y=moon_df['y'], z=moon_df['z'],
        mode='lines', line=dict(color='gray', width=2, dash='dash'),
        name='Jalur Orbit Bulan'
    ))

    # Posisi Bulan saat Orion melintas (Estimasi tgl 4-5 April)
    target_idx = 96 # jam ke-96
    fig.add_trace(go.Scatter3d(
        x=[moon_df['x'].iloc[target_idx]], 
        y=[moon_df['y'].iloc[target_idx]], 
        z=[moon_df['z'].iloc[target_idx]],
        mode='markers', marker=dict(size=8, color='silver', symbol='circle'),
        name='Bulan (Titik Temu)'
    ))

    # Rute Orion (Garis Merah)
    fig.add_trace(go.Scatter3d(
        x=orion_traj[:, 0], y=orion_traj[:, 1], z=orion_traj[:, 2],
        mode='lines', line=dict(color='crimson', width=4),
        name='Rute Artemis 2'
    ))

    # Setting Tampilan (Black Space Theme)
    fig.update_layout(
        template="plotly_dark",
        title="Simulasi Akurat Artemis 2: Free Return Trajectory",
        scene=dict(
            xaxis_title="X (km)", yaxis_title="Y (km)", zaxis_title="Z (km)",
            aspectmode='data' # Sangat penting agar skala X, Y, Z sama (tidak gepeng)
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    print("--- Selesai. Silakan cek browser Anda! ---")
    fig.show()

if __name__ == "__main__":
    main()