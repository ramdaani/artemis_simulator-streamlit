import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

def propagate_orbit(initial_state, moon_df):
    # Konstanta Gravitasi (GM) km^3/s^2
    MU_EARTH = 398600.44
    MU_MOON = 4902.8
    
    # Persiapan data waktu (per jam) untuk posisi Bulan
    moon_df['t_sec'] = np.arange(len(moon_df)) * 3600
    
    # Interpolasi posisi Bulan agar sinkron dengan waktu t
    get_moon_x = interp1d(moon_df['t_sec'], moon_df['x'], fill_value="extrapolate")
    get_moon_y = interp1d(moon_df['t_sec'], moon_df['y'], fill_value="extrapolate")
    get_moon_z = interp1d(moon_df['t_sec'], moon_df['z'], fill_value="extrapolate")

    def equations(t, state):
        x, y, z, vx, vy, vz = state
        r_sc = np.array([x, y, z])
        r_mag = np.linalg.norm(r_sc)
        
        # Posisi Bulan saat detik ke-t
        r_m = np.array([get_moon_x(t), get_moon_y(t), get_moon_z(t)])
        r_m_sc = r_m - r_sc
        rm_mag = np.linalg.norm(r_m_sc)
        
        # Gravitasi Bumi
        a_earth = -MU_EARTH * r_sc / r_mag**3
        
        # Gravitasi Bulan (Hanya aktif jika Orion cukup dekat atau untuk akurasi penuh)
        a_moon = MU_MOON * r_m_sc / rm_mag**3
        
        ax, ay, az = a_earth + a_moon
        return [vx, vy, vz, ax, ay, az]

    # Simulasi 10 hari (Pergi-Pulang)
    t_span = (0, 10 * 24 * 3600)
    # 8000 titik evaluasi agar garis di Plotly sangat halus saat menikung di Bulan
    t_eval = np.linspace(0, t_span[1], 8000)

    # Gunakan toleransi sangat ketat (atol/rtol) agar rute balik tidak melesat
    sol = solve_ivp(equations, t_span, initial_state, method='RK45', 
                    t_eval=t_eval, rtol=1e-10, atol=1e-12)
    
    return sol.y.T, t_eval