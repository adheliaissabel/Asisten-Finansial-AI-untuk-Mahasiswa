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
    # 1. FUZZIFIKASI 
    # (Disesuaikan dengan batas nilai pada PDF)
    # ==========================================
    
    # --- Pemasukan (x) --- [cite: 11-14, 19-20]
    if x <= 500000:
        mu_p_rendah = 1.0
        mu_p_sedang = 0.0
        mu_p_tinggi = 0.0
    elif 500000 < x <= 1000000:
        mu_p_rendah = (1000000 - x) / 500000.0
        mu_p_sedang = (x - 500000) / 500000.0
        mu_p_tinggi = 0.0
    elif 1000000 < x <= 1500000:
        mu_p_rendah = 0.0
        # Perbaikan: Mengikuti rumus PDF (1200 - 750) / (1500 - 750) untuk Tinggi
        mu_p_sedang = (1500000 - x) / 500000.0
        mu_p_tinggi = (x - 750000) / 750000.0 # Sesuai titik potong di PDF
    else:
        mu_p_rendah = 0.0
        mu_p_sedang = 0.0
        mu_p_tinggi = 1.0

    # --- Pengeluaran (y) --- [cite: 16-18, 21-28]
    if y <= 500000:
        mu_e_kecil = 1.0
        mu_e_wajar = 0.0
        mu_e_besar = 0.0
    elif 500000 < y <= 1000000:
        mu_e_kecil = (1000000 - y) / 500000.0
        mu_e_wajar = (y - 500000) / 500000.0
        mu_e_besar = 0.0
    elif 1000000 < y <= 1500000:
        mu_e_kecil = 0.0
        mu_e_wajar = (1500000 - y) / 500000.0
        mu_e_besar = (y - 750000) / 750000.0 # Sesuai titik potong di PDF
    else:
        mu_e_kecil = 0.0
        mu_e_wajar = 0.0
        mu_e_besar = 1.0

    # ==========================================
    # 2. INFERENSI (Metode Sugeno)
    # Nilai Z disesuaikan dengan Singleton pada PDF [cite: 36, 43, 49, 55, 61, 68, 74, 84, 91]
    # ==========================================
    z_hemat = 32   # Berdasarkan R8 di PDF
    z_normal = 68  # Berdasarkan R9 di PDF (Tinggi-Besar)
    z_boros = 100  # Berdasarkan R2, R3, R6 di PDF

    rules = [
        {"alpha": min(mu_p_rendah, mu_e_kecil), "z": 50},       # R1 [cite: 30-36]
        {"alpha": min(mu_p_rendah, mu_e_wajar), "z": z_boros},  # R2 [cite: 37-43]
        {"alpha": min(mu_p_rendah, mu_e_besar), "z": z_boros},  # R3 [cite: 44-49]
        {"alpha": min(mu_p_sedang, mu_e_kecil), "z": 20},       # R4 [cite: 50-55]
        {"alpha": min(mu_p_sedang, mu_e_wajar), "z": 50},       # R5 [cite: 56-61]
        {"alpha": min(mu_p_sedang, mu_e_besar), "z": z_boros},  # R6 [cite: 63-68]
        {"alpha": min(mu_p_tinggi, mu_e_kecil), "z": 20},       # R7 [cite: 69-74]
        {"alpha": min(mu_p_tinggi, mu_e_wajar), "z": z_hemat},  # R8 [cite: 75-84]
        {"alpha": min(mu_p_tinggi, mu_e_besar), "z": z_normal}, # R9 [cite: 85-91]
    ]

    # ==========================================
    # 3. DEFUZZIFIKASI (Weighted Average) [cite: 93]
    # ==========================================
    total_alpha_z = sum(r["alpha"] * r["z"] for r in rules)
    total_alpha = sum(r["alpha"] for r in rules)

    skor_akhir = total_alpha_z / total_alpha if total_alpha > 0 else 0
    
    # Penentuan status string sesuai skor
    if skor_akhir <= 40: 
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