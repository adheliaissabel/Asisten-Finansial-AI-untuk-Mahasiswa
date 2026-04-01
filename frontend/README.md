# FuzzyFinance 💰
> Asisten Keuangan AI berbasis Fuzzy Logic untuk menganalisis kesehatan finansial bulanan.

---

## Cara Kerja
Masukkan **pemasukan** dan **pengeluaran** bulanan, sistem akan menganalisis menggunakan 9 aturan Fuzzy Logic (Metode Sugeno) dan menampilkan status keuangan:

| Status | Keterangan |
|--------|------------|
| 🟢 Hemat | Pengeluaran jauh di bawah pemasukan |
| 🟡 Normal | Pengeluaran dalam batas wajar |
| 🔴 Boros | Pengeluaran terlalu tinggi |

---

## Teknologi
- **Backend**: Python + FastAPI + Uvicorn
- **Frontend**: HTML + TypeScript + Bun
- **Logika**: Fuzzy Logic metode Sugeno (9 rules)

---

## Prasyarat
Pastikan sudah terinstall di komputer:
- [Python 3.11+](https://www.python.org/downloads/)
- [Bun](https://bun.sh) — install dengan perintah:
  ```bash
  # Windows (PowerShell)
  powershell -c "irm bun.sh/install.ps1 | iex"

  # Mac / Linux
  curl -fsSL https://bun.sh/install | bash
  ```

---

## Instalasi & Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/username/Asisten-Finansial-AI-untuk-Mahasiswa.git
cd Asisten-Finansial-AI-untuk-Mahasiswa
```

### 2. Jalankan Backend (Terminal 1)
```bash
cd backend
pip install fastapi uvicorn
python main.py
```
Berhasil jika muncul:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 3. Jalankan Frontend (Terminal 2)
```bash
cd frontend
bun install
bun start
```
Berhasil jika muncul:
```
✅ FuzzyFinance frontend berjalan di http://localhost:3000
🔗 Proxy /api/* → http://127.0.0.1:8000
```

### 4. Buka di Browser
```
http://localhost:3000
```

---

## Struktur Project
```
Asisten-Finansial-AI-untuk-Mahasiswa/
├── backend/
│   └── main.py          # FastAPI + Fuzzy Logic
└── frontend/
    ├── index.html        # Tampilan web
    ├── server.ts         # Bun server + proxy ke backend
    ├── package.json      # Konfigurasi project
    └── index.ts          # (tidak dipakai sebagai entry point)
```

---

## Troubleshooting

**Port 3000 atau 8000 sudah dipakai:**
```bash
# Cari PID yang menggunakan port (contoh port 3000)
netstat -ano | findstr :3000

# Matikan prosesnya (ganti 12345 dengan PID yang ditemukan)
taskkill /PID 12345 /F
```

**`ModuleNotFoundError: No module named 'fastapi'`:**
```bash
pip install fastapi uvicorn
```

**Error merah di VS Code pada server.ts (bukan error sebenarnya):**
```bash
cd frontend
npm i --save-dev @types/bun
```