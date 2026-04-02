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
    x = data.pemasukan
    y = data.pengeluaran

    # ==========================================
    # 1. FUZZIFIKASI (Sesuai Grafik & PDF Tugas 3)
    # ==========================================
    
    # --- Pemasukan (x) --- [cite: 19-20]
    mu_p_rendah = 0.0
    mu_p_sedang = 0.0
    mu_p_tinggi = 0.0

    if x <= 500000:
        mu_p_rendah = 1.0
    elif 500000 < x < 1000000:
        mu_p_rendah = (1000000 - x) / 500000.0
        mu_p_sedang = (x - 500000) / 500000.0
    elif 1000000 <= x <= 1500000:
        # Sesuai Rumus PDF: (1200-750)/(1500-750) = 0.6 [cite: 20]
        mu_p_tinggi = (x - 750000) / 750000.0 
        mu_p_sedang = (1500000 - x) / 500000.0 if x < 1500000 else 0.0
    else:
        mu_p_tinggi = 1.0

    # --- Pengeluaran (y) --- [cite: 22, 27-28]
    mu_e_kecil = 0.0
    mu_e_wajar = 0.0
    mu_e_besar = 0.0

    if y <= 500000:
        mu_e_kecil = 1.0
    elif 500000 < y <= 1000000:
        # Sesuai Rumus PDF: (1000-900)/(1000-500) = 0.2 [cite: 22]
        mu_e_wajar = (1000000 - y) / 500000.0
        # Sesuai Rumus PDF: (900-750)/(1500-750) = 0.2 [cite: 27-28]
        mu_e_besar = (y - 750000) / 750000.0
    elif 1000000 < y <= 1500000:
        mu_e_besar = (y - 750000) / 750000.0
    else:
        mu_e_besar = 1.0

    # ==========================================
    # 2. INFERENSI (Metode Sugeno)
    # Nilai Z disesuaikan dengan PDF halaman 4 [cite: 93]
    # ==========================================
    
    # Aturan yang aktif pada kasus 1.2jt & 900rb adalah R8 dan R9 [cite: 79, 89]
    # Nilai z dari PDF: Hemat=32, Normal=68 
    
    rules = [
        {"alpha": min(mu_p_rendah, mu_e_kecil), "z": 50},  # R1
        {"alpha": min(mu_p_rendah, mu_e_wajar), "z": 100}, # R2
        {"alpha": min(mu_p_rendah, mu_e_besar), "z": 100}, # R3
        {"alpha": min(mu_p_sedang, mu_e_kecil), "z": 20},  # R4
        {"alpha": min(mu_p_sedang, mu_e_wajar), "z": 50},  # R5
        {"alpha": min(mu_p_sedang, mu_e_besar), "z": 100}, # R6
        {"alpha": min(mu_p_tinggi, mu_e_kecil), "z": 20},  # R7
        {"alpha": min(mu_p_tinggi, mu_e_wajar), "z": 32},  # R8 [cite: 84, 93]
        {"alpha": min(mu_p_tinggi, mu_e_besar), "z": 68},  # R9 [cite: 91, 93]
    ]

    # ==========================================
    # 3. DEFUZZIFIKASI (Weighted Average) [cite: 93]
    # ==========================================
    total_alpha_z = sum(r["alpha"] * r["z"] for r in rules)
    total_alpha = sum(r["alpha"] for r in rules)

    skor_akhir = total_alpha_z / total_alpha if total_alpha > 0 else 0
    
    # Status berdasarkan PDF (Skor 50 = Normal) 
    if skor_akhir < 40: 
        status = "Hemat"
    elif skor_akhir <= 70: 
        status = "Normal"
    else: 
        status = "Boros"

    return {
        "skor": f"{round(skor_akhir, 1)}%", 
        "status": status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)