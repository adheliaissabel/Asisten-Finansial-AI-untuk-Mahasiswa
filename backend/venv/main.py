from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Keuangan(BaseModel):
    pemasukan: float
    pengeluaran: float

@app.post("/api/fuzzy")
def hitung_fuzzy(data: Keuangan):
    # Konversi ke Juta Rupiah
    x = data.pemasukan / 1000000.0
    y = data.pengeluaran / 1000000.0

    # ==========================================
    # 1. FUZZIFIKASI (Input Mahasiswa)
    # ==========================================
    
    # --- Pemasukan (x) ---
    if x <= 0.5: mu_p_rendah = 1.0
    elif 0.5 < x < 1.0: mu_p_rendah = (1.0 - x) / 0.5
    else: mu_p_rendah = 0.0

    if x <= 0.5 or x >= 1.5: mu_p_sedang = 0.0
    elif 0.5 < x <= 1.0: mu_p_sedang = (x - 0.5) / 0.5
    elif 1.0 < x < 1.5: mu_p_sedang = (1.5 - x) / 0.5

    if x <= 1.0: mu_p_tinggi = 0.0
    elif 1.0 < x < 1.5: mu_p_tinggi = (x - 1.0) / 0.5
    else: mu_p_tinggi = 1.0

    # --- Pengeluaran (y) ---
    if y <= 0.5: mu_e_kecil = 1.0
    elif 0.5 < y < 1.2: mu_e_kecil = (1.2 - y) / 0.7
    else: mu_e_kecil = 0.0

    if y <= 0.5 or y >= 1.5: mu_e_wajar = 0.0
    elif 0.5 < y <= 1.2: mu_e_wajar = (y - 0.5) / 0.7
    elif 1.2 < y < 1.5: mu_e_wajar = (1.5 - y) / 0.3

    if y <= 1.2: mu_e_besar = 0.0
    elif 1.2 < y < 1.5: mu_e_besar = (y - 1.2) / 0.3
    else: mu_e_besar = 1.0

    # ==========================================
    # 2. INFERENSI (9 Rule Base)
    # Sugeno: Boros=0, Normal=50, Hemat=100
    # ==========================================
    rules = [
        {"alpha": min(mu_p_rendah, mu_e_kecil), "z": 50},  # R1: Rendah & Kecil -> Normal
        {"alpha": min(mu_p_rendah, mu_e_wajar), "z": 0},   # R2: Rendah & Wajar -> Boros
        {"alpha": min(mu_p_rendah, mu_e_besar), "z": 0},   # R3: Rendah & Besar -> Boros
        {"alpha": min(mu_p_sedang, mu_e_kecil), "z": 100}, # R4: Sedang & Kecil -> Hemat
        {"alpha": min(mu_p_sedang, mu_e_wajar), "z": 50},  # R5: Sedang & Wajar -> Normal
        {"alpha": min(mu_p_sedang, mu_e_besar), "z": 0},   # R6: Sedang & Besar -> Boros
        {"alpha": min(mu_p_tinggi, mu_e_kecil), "z": 100}, # R7: Tinggi & Kecil -> Hemat
        {"alpha": min(mu_p_tinggi, mu_e_wajar), "z": 100}, # R8: Tinggi & Wajar -> Hemat
        {"alpha": min(mu_p_tinggi, mu_e_besar), "z": 50},  # R9: Tinggi & Besar -> Normal
    ]

    # ==========================================
    # 3. DEFUZZIFIKASI (Weighted Average)
    # ==========================================
    total_alpha_z = sum(r["alpha"] * r["z"] for r in rules)
    total_alpha = sum(r["alpha"] for r in rules)

    skor_akhir = total_alpha_z / total_alpha if total_alpha > 0 else 0
    
    if skor_akhir >= 70: status = "Hemat"
    elif skor_akhir >= 40: status = "Normal"
    else: status = "Boros"

    return {"skor": round(skor_akhir, 2), "status": status}