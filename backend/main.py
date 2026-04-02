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
    # 1. FUZZIFIKASI (Sesuai Rumus di Excel Anda)
    # ==========================================
    
    # --- Pemasukan Tinggi (μ P_Tinggi) ---
    if x <= 750000:
        mu_p_tinggi = 0.0
    elif x >= 1500000:
        mu_p_tinggi = 1.0
    else:
        mu_p_tinggi = (x - 750000) / 750000.0

    # --- Pengeluaran Wajar (μ E_Wajar) ---
    # Rumus: MAX(0, MIN((1000-y)/500, (y-500)/500))
    val1 = (1000000 - y) / 500000.0
    val2 = (y - 500000) / 500000.0
    mu_e_wajar = max(0.0, min(val1, val2))

    # --- Pengeluaran Besar (μ E_Besar) ---
    if y <= 750000:
        mu_e_besar = 0.0
    elif y >= 1500000:
        mu_e_besar = 1.0
    else:
        mu_e_besar = (y - 750000) / 750000.0

    # ==========================================
    # 2. INFERENSI & DEFUZZIFIKASI (Sugeno)
    # ==========================================
    
    # Mencari Alpha Predikat untuk Rule 8 dan Rule 9
    alpha8 = min(mu_p_tinggi, mu_e_wajar) # R8: Tinggi & Wajar
    z8 = 32 # Singleton Hemat
    
    alpha9 = min(mu_p_tinggi, mu_e_besar) # R9: Tinggi & Besar
    z9 = 68 # Singleton Normal

    # Weighted Average (Hanya hitung jika ada rule yang aktif)
    total_alpha = alpha8 + alpha9
    
    if total_alpha > 0:
        # Rumus: ((a8*z8) + (a9*z9)) / (a8+a9)
        skor_akhir = ((alpha8 * z8) + (alpha9 * z9)) / total_alpha
    else:
        # Logika tambahan jika input di luar jangkauan (Default)
        if y > x:
            skor_akhir = 100.0 # Boros
        else:
            skor_akhir = 32.0  # Hemat

    # ==========================================
    # 3. OUTPUT STATUS
    # ==========================================
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