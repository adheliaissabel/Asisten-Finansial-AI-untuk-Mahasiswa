# 🎓 Asisten Finansial AI untuk Mahasiswa (FuzzyFinance)

Aplikasi web untuk menganalisis kondisi keuangan mahasiswa menggunakan **Fuzzy Logic (Metode Sugeno)**. Masukkan pemasukan dan pengeluaran bulanan, dan aplikasi akan memberikan skor serta status keuanganmu: **Hemat**, **Normal**, atau **Boros**.

---

## 🏗️ Arsitektur

```
Browser → Bun server.ts (port 3000) → Python FastAPI (port 8000)
```

| Bagian | Teknologi | Fungsi |
|---|---|---|
| Frontend | HTML, Tailwind CSS, TypeScript (Bun) | Tampilan dan proxy API |
| Backend | Python, FastAPI, Uvicorn | Kalkulasi fuzzy logic |

---

## ✅ Prasyarat

Pastikan software berikut sudah terinstall di komputermu:

- **Python 3.9+** → [python.org](https://www.python.org/downloads/)
  ```bash
  python --version
  ```
- **Bun** → [bun.sh](https://bun.sh)
  ```bash
  curl -fsSL https://bun.sh/install | bash
  bun --version
  ```
- **Git** → [git-scm.com](https://git-scm.com)
  ```bash
  git --version
  ```

---

## 🚀 Cara Menjalankan

### Langkah 1 — Clone repository

```bash
git clone https://github.com/adheliaissabel/Asisten-Finansial-AI-untuk-Mahasiswa.git
cd Asisten-Finansial-AI-untuk-Mahasiswa
```

---

### Langkah 2 — Jalankan Backend (Terminal 1)

```bash
# Masuk ke folder backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic

# Jalankan server
uvicorn main:app --reload
```

✅ Backend berjalan di `http://127.0.0.1:8000`

> **Biarkan terminal ini tetap terbuka!**

---

### Langkah 3 — Jalankan Frontend (Terminal 2)

Buka **terminal baru** (jangan tutup terminal backend):

```bash
# Masuk ke folder frontend
cd Asisten-Finansial-AI-untuk-Mahasiswa/frontend

# Install dependencies
bun install

# Jalankan server frontend
bun run server.ts
```

✅ Frontend berjalan di `http://localhost:3000`

> **Biarkan terminal ini tetap terbuka juga!**

---

### Langkah 4 — Buka di Browser

Pastikan **kedua terminal** masih berjalan, lalu buka browser dan akses:

```
http://localhost:3000
```

🎉 Aplikasi FuzzyFinance siap digunakan!

---

## 🗂️ Struktur Folder

```
Asisten-Finansial-AI-untuk-Mahasiswa/
├── backend/
│   ├── main.py          # FastAPI app + logika fuzzy logic
│   └── venv/            # Virtual environment (tidak di-push ke GitHub)
└── frontend/
    ├── index.html        # Halaman utama
    ├── server.ts         # Bun server + proxy ke backend
    ├── package.json
    └── tsconfig.json
```

---

## 🔌 API Endpoint

### `POST /api/fuzzy`

Menghitung skor dan status keuangan berdasarkan fuzzy logic.

**Request body:**
```json
{
  "pemasukan": 2000000,
  "pengeluaran": 800000
}
```

**Response:**
```json
{
  "skor": "32.5%",
  "status": "Hemat"
}
```

**Status keuangan:**
| Skor | Status |
|---|---|
| 0% – 35% | Hemat |
| 36% – 65% | Normal |
| 66% – 100% | Boros |

---

## ❗ Troubleshooting

| Error | Solusi |
|---|---|
| `Port already in use` | Tutup aplikasi lain yang memakai port 3000 atau 8000 |
| `ModuleNotFoundError` | Pastikan virtual environment aktif, ulangi `pip install` |
| `uvicorn: command not found` | Aktifkan venv terlebih dahulu |
| `bun: command not found` | Install Bun terlebih dahulu |
| Fitur hitung tidak bekerja | Pastikan backend (Terminal 1) masih berjalan dan tidak error |
| `Failed to fetch` | Cek apakah backend berjalan di `http://127.0.0.1:8000` |

---

## 👩‍💻 Developer

**Adhelia Issabel** — Universitas ...

---

## 📄 Lisensi

Project ini dibuat untuk keperluan akademis.
