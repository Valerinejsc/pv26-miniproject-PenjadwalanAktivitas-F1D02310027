# pv26-miniproject-PenjadwalanAktivitas-F1D02310027

# Penjadwal Aktivitas

Aplikasi desktop berbasis GUI untuk mengelola dan menjadwalkan aktivitas harian secara terstruktur. Pengguna dapat menambah, mengedit, menghapus, serta memantau status aktivitas dengan tampilan yang bersih dan intuitif.

---

## Identitas Mahasiswa

| | |
|---|---|
| **Nama** | Valerine Jesika Dewi |
| **NIM**  | F1D02310027 |

---

## Cara Menjalankan

**1. Pastikan Python sudah terinstal** (versi 3.10 atau lebih baru)

**2. Install dependensi**
```bash
pip install PySide6
```

**3. Masuk ke folder project**
```bash
cd penjadwal_aktivitas
```

**4. Jalankan aplikasi**
```bash
python main.py
```

> Database `penjadwal.db` akan dibuat otomatis saat pertama kali aplikasi dijalankan.

---

## Panduan Penggunaan Aplikasi

### Menambah Aktivitas Baru

1. Klik tombol **➕ Tambah** pada toolbar, atau pilih menu **Aktivitas → Tambah Aktivitas** (Ctrl+N).
2. Jendela dialog **Tambah Aktivitas Baru** akan terbuka. Isi setiap field berikut:

| Field | Cara Pengisian | Keterangan |
|-------|---------------|------------|
| **Judul** | Ketik nama aktivitas | Wajib diisi, maksimal 100 karakter. Contoh: `Kuliah Pemrograman Visual` |
| **Tanggal** | Klik ikon kalender lalu pilih tanggal | Wajib diisi. Default: tanggal hari ini |
| **Waktu Mulai** | Klik angka jam/menit lalu scroll atau ketik | Wajib diisi. Format 24 jam. Contoh: `08:00` |
| **Waktu Selesai** | Sama seperti Waktu Mulai | Wajib diisi. Harus lebih akhir dari Waktu Mulai |
| **Kategori** | Klik dropdown, pilih salah satu | Wajib diisi. Pilihan: Kuliah, Tugas, Organisasi, Olahraga, Hiburan, Pribadi, Lainnya |
| **Prioritas** | Klik dropdown, pilih salah satu | Wajib diisi. Pilihan: Tinggi, Sedang, Rendah |
| **Lokasi** | Ketik nama tempat | Opsional. Contoh: `Ruang Kelas A`, `Online / Zoom` |
| **Deskripsi** | Ketik catatan tambahan | Opsional. Untuk keterangan detail aktivitas |

3. Klik **Tambah Aktivitas** untuk menyimpan, atau **Batal** untuk membatalkan.

---

### Mengedit Aktivitas

1. Klik satu baris aktivitas di tabel untuk memilihnya.
2. Klik tombol **✏️ Edit** atau tekan **Ctrl+E**.
3. Form akan terbuka dengan data yang sudah terisi — ubah field yang diinginkan.
4. Pada mode edit, terdapat field tambahan **Status** untuk mengubah status aktivitas (Belum Selesai / Sedang Berlangsung / Selesai).
5. Klik **Simpan Perubahan** untuk menyimpan.

---

### Menghapus Aktivitas

1. Klik baris aktivitas yang ingin dihapus di tabel.
2. Klik tombol **🗑️ Hapus** atau tekan **Delete**.
3. Konfirmasi penghapusan pada dialog yang muncul — klik **Yes** untuk melanjutkan.

> ⚠️ Data yang dihapus tidak dapat dikembalikan.

---

### Menandai Aktivitas Selesai

1. Klik baris aktivitas di tabel.
2. Klik tombol **✅ Tandai Selesai**.
3. Konfirmasi pada dialog yang muncul — klik **Yes**.
4. Status aktivitas akan berubah menjadi **Selesai** dan angka pada stat card akan diperbarui.

---

### Filter & Pencarian

Gunakan bagian **Filter & Pencarian** di toolbar untuk menyaring data:

- **Tanggal** — Pilih tanggal tertentu, lalu klik **🔍 Cari**. Klik **✕** untuk mereset ke hari ini.
- **Kategori** — Pilih kategori spesifik atau pilih **Semua** untuk menampilkan semua kategori.
- **Status** — Saring berdasarkan status aktivitas (Semua / Belum Selesai / Sedang Berlangsung / Selesai).
- Klik **Semua Data** untuk menghapus semua filter dan menampilkan seluruh aktivitas.

---

## Teknologi yang Digunakan

| Teknologi | Versi | Kegunaan |
|-----------|-------|----------|
| **Python** | 3.10+ | Bahasa pemrograman utama |
| **PySide6** | 6.x | Framework GUI (Qt for Python) |
| **SQLite** | bawaan Python | Database lokal penyimpanan data |
| **Qt Style Sheets (QSS)** | — | Styling antarmuka dari file eksternal |

### Komponen PySide6 yang digunakan
`QMainWindow` · `QDialog` · `QTableWidget` · `QFormLayout` · `QVBoxLayout` · `QHBoxLayout` · `QDateEdit` · `QTimeEdit` · `QComboBox` · `QLineEdit` · `QTextEdit` · `QMessageBox` · `QMenuBar` · `QStatusBar`

---

## Struktur Project

```
penjadwal_aktivitas/
├── main.py          # Entry point — inisialisasi app & load stylesheet
├── database.py      # Layer Database — operasi SQLite (CRUD)
├── logic.py         # Layer Logika — validasi & business logic
├── ui_main.py       # Layer UI — jendela utama
├── ui_dialog.py     # Layer UI — dialog tambah/edit aktivitas
├── style.qss        # Stylesheet QSS eksternal
└── penjadwal.db     # Database SQLite (dibuat otomatis)
```
