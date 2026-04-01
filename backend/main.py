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
    # 1. FUZZIFIKASI (Sesuai Aturan Baru)
    # ==========================================
    
    # --- Pemasukan (x) ---
    # Rendah: < 500k (1), turun hingga 1000k (0)
    # Sedang: 500k-1000k (naik), 1000k-1500k (turun)
    # Tinggi: > 1500k (1)
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
        mu_p_sedang = (1500000 - x) / 500000.0
        mu_p_tinggi = (x - 1000000) / 500000.0
    else:
        mu_p_rendah = 0.0
        mu_p_sedang = 0.0
        mu_p_tinggi = 1.0

    # --- Pengeluaran (y) ---
    # Kecil: < 500k (1), turun hingga 1200k (0)
    # Wajar: 500k-1200k (naik), 1200k-1500k (turun)
    # Besar: > 1500k (1)
    if y <= 500000:
        mu_e_kecil = 1.0
        mu_e_wajar = 0.0
        mu_e_besar = 0.0
    elif 500000 < y <= 1200000:
        mu_e_kecil = (1200000 - y) / 700000.0
        mu_e_wajar = (y - 500000) / 700000.0
        mu_e_besar = 0.0
    elif 1200000 < y <= 1500000:
        mu_e_kecil = 0.0
        mu_e_wajar = (1500000 - y) / 300000.0
        mu_e_besar = (y - 1200000) / 300000.0
    else:
        mu_e_kecil = 0.0
        mu_e_wajar = 0.0
        mu_e_besar = 1.0

    # ==========================================
    # 2. INFERENSI (Metode Sugeno untuk Persentase)
    # Skor Z: Hemat = 20%, Normal = 50%, Boros = 85%
    # (Semakin tinggi skor, semakin BOROS kondisinya)
    # ==========================================
    z_hemat = 20
    z_normal = 50
    z_boros = 85

    rules = [
        # 1. Rendah & Kecil -> Normal
        {"alpha": min(mu_p_rendah, mu_e_kecil), "z": z_normal},
        # 2. Rendah & Wajar -> Boros
        {"alpha": min(mu_p_rendah, mu_e_wajar), "z": z_boros},
        # 3. Rendah & Besar -> Boros
        {"alpha": min(mu_p_rendah, mu_e_besar), "z": z_boros},
        
        # 4. Sedang & Kecil -> Hemat
        {"alpha": min(mu_p_sedang, mu_e_kecil), "z": z_hemat},
        # 5. Sedang & Wajar -> Normal
        {"alpha": min(mu_p_sedang, mu_e_wajar), "z": z_normal},
        # 6. Sedang & Besar -> Boros
        {"alpha": min(mu_p_sedang, mu_e_besar), "z": z_boros},
        
        # 7. Tinggi & Kecil -> Hemat
        {"alpha": min(mu_p_tinggi, mu_e_kecil), "z": z_hemat},
        # 8. Tinggi & Wajar -> Hemat
        {"alpha": min(mu_p_tinggi, mu_e_wajar), "z": z_hemat},
        # 9. Tinggi & Besar -> Normal
        {"alpha": min(mu_p_tinggi, mu_e_besar), "z": z_normal},
    ]

    # ==========================================
    # 3. DEFUZZIFIKASI (Weighted Average)
    # ==========================================
    total_alpha_z = sum(r["alpha"] * r["z"] for r in rules)
    total_alpha = sum(r["alpha"] for r in rules)

    # Menghitung skor persentase (0 - 100)
    skor_akhir = total_alpha_z / total_alpha if total_alpha > 0 else 0
    
    # Menentukan Status String berdasarkan rentang persentase
    if skor_akhir <= 35: 
        status = "Hemat"
    elif skor_akhir <= 65: 
        status = "Normal"
    else: 
        status = "Boros"

    # Mengirim data ke Frontend (ditambah simbol % agar cantik)
    return {
        "skor": f"{round(skor_akhir, 1)}%", 
        "status": status
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)