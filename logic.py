from database import (
    tambah_aktivitas, ambil_semua_aktivitas, ambil_aktivitas_by_id,
    update_aktivitas, update_status, hapus_aktivitas, ambil_statistik
)

KATEGORI_LIST = ["Kuliah", "Tugas", "Organisasi", "Olahraga", "Hiburan", "Pribadi", "Lainnya"]
PRIORITAS_LIST = ["Tinggi", "Sedang", "Rendah"]
STATUS_LIST = ["Belum Selesai", "Sedang Berlangsung", "Selesai"]


class AktivitasController:
    def validasi_input(self, data: dict) -> tuple[bool, str]:
        """Validasi data input. Mengembalikan (valid, pesan_error)."""
        if not data.get("judul", "").strip():
            return False, "Judul aktivitas tidak boleh kosong."
        if len(data["judul"].strip()) > 100:
            return False, "Judul aktivitas maksimal 100 karakter."
        if not data.get("tanggal", "").strip():
            return False, "Tanggal tidak boleh kosong."
        if not data.get("waktu_mulai", "").strip():
            return False, "Waktu mulai tidak boleh kosong."
        if not data.get("waktu_selesai", "").strip():
            return False, "Waktu selesai tidak boleh kosong."
        if data["waktu_mulai"] >= data["waktu_selesai"]:
            return False, "Waktu selesai harus lebih akhir dari waktu mulai."
        if data.get("kategori") not in KATEGORI_LIST:
            return False, "Kategori tidak valid."
        if data.get("prioritas") not in PRIORITAS_LIST:
            return False, "Prioritas tidak valid."
        return True, ""

    def tambah(self, data: dict) -> tuple[bool, str]:
        valid, pesan = self.validasi_input(data)
        if not valid:
            return False, pesan
        data["judul"] = data["judul"].strip()
        data.setdefault("lokasi", "")
        data.setdefault("deskripsi", "")
        data.setdefault("status", "Belum Selesai")
        tambah_aktivitas(data)
        return True, "Aktivitas berhasil ditambahkan."

    def edit(self, aktivitas_id: int, data: dict) -> tuple[bool, str]:
        valid, pesan = self.validasi_input(data)
        if not valid:
            return False, pesan
        data["judul"] = data["judul"].strip()
        update_aktivitas(aktivitas_id, data)
        return True, "Aktivitas berhasil diperbarui."

    def hapus(self, aktivitas_id: int) -> tuple[bool, str]:
        if not ambil_aktivitas_by_id(aktivitas_id):
            return False, "Aktivitas tidak ditemukan."
        hapus_aktivitas(aktivitas_id)
        return True, "Aktivitas berhasil dihapus."

    def tandai_selesai(self, aktivitas_id: int) -> tuple[bool, str]:
        row = ambil_aktivitas_by_id(aktivitas_id)
        if not row:
            return False, "Aktivitas tidak ditemukan."
        update_status(aktivitas_id, "Selesai")
        return True, "Aktivitas ditandai selesai."

    def ambil_semua(self, filter_tanggal=None, filter_kategori=None, filter_status=None):
        return ambil_semua_aktivitas(filter_tanggal, filter_kategori, filter_status)

    def ambil_by_id(self, aktivitas_id: int):
        return ambil_aktivitas_by_id(aktivitas_id)

    def statistik(self):
        return ambil_statistik()
