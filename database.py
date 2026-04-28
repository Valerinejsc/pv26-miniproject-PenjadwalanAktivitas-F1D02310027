import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "penjadwal.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aktivitas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            judul       TEXT    NOT NULL,
            tanggal     TEXT    NOT NULL,
            waktu_mulai TEXT    NOT NULL,
            waktu_selesai TEXT  NOT NULL,
            kategori    TEXT    NOT NULL,
            prioritas   TEXT    NOT NULL,
            lokasi      TEXT,
            deskripsi   TEXT,
            status      TEXT    NOT NULL DEFAULT 'Belum Selesai',
            dibuat_pada TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()

def tambah_aktivitas(data: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO aktivitas
            (judul, tanggal, waktu_mulai, waktu_selesai,
             kategori, prioritas, lokasi, deskripsi, status)
        VALUES
            (:judul, :tanggal, :waktu_mulai, :waktu_selesai,
             :kategori, :prioritas, :lokasi, :deskripsi, :status)
    """, data)
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def ambil_semua_aktivitas(filter_tanggal=None, filter_kategori=None, filter_status=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM aktivitas WHERE 1=1"
    params = []

    if filter_tanggal:
        query += " AND tanggal = ?"
        params.append(filter_tanggal)
    if filter_kategori and filter_kategori != "Semua":
        query += " AND kategori = ?"
        params.append(filter_kategori)
    if filter_status and filter_status != "Semua":
        query += " AND status = ?"
        params.append(filter_status)

    query += " ORDER BY tanggal ASC, waktu_mulai ASC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def ambil_aktivitas_by_id(aktivitas_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aktivitas WHERE id = ?", (aktivitas_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_aktivitas(aktivitas_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE aktivitas SET
            judul         = :judul,
            tanggal       = :tanggal,
            waktu_mulai   = :waktu_mulai,
            waktu_selesai = :waktu_selesai,
            kategori      = :kategori,
            prioritas     = :prioritas,
            lokasi        = :lokasi,
            deskripsi     = :deskripsi,
            status        = :status
        WHERE id = :id
    """, {**data, "id": aktivitas_id})
    conn.commit()
    conn.close()

def update_status(aktivitas_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE aktivitas SET status = ? WHERE id = ?", (status, aktivitas_id))
    conn.commit()
    conn.close()

def hapus_aktivitas(aktivitas_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aktivitas WHERE id = ?", (aktivitas_id,))
    conn.commit()
    conn.close()

def ambil_statistik():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM aktivitas")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM aktivitas WHERE status = 'Selesai'")
    selesai = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM aktivitas WHERE status = 'Belum Selesai'")
    belum = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM aktivitas WHERE tanggal = date('now','localtime')")
    hari_ini = cursor.fetchone()[0]
    conn.close()
    return {"total": total, "selesai": selesai, "belum": belum, "hari_ini": hari_ini}
