import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QComboBox, QDateEdit, QFrame, QHeaderView, QMessageBox,
    QStatusBar, QSizePolicy, QAbstractItemView
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QAction, QFont, QColor

from logic import AktivitasController
from ui_dialog import DialogAktivitas, DialogTentang

NAMA_MAHASISWA = "Valerine Jesika Dewi"
NIM_MAHASISWA  = "F1D02310027"

WARNA_PRIORITAS = {
    "Tinggi": "#ed4245",
    "Sedang": "#f0a500",
    "Rendah": "#3ba55c",
}
WARNA_STATUS = {
    "Selesai":            "#3ba55c",
    "Sedang Berlangsung": "#5865f2",
    "Belum Selesai":      "#6b6f8a",
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = AktivitasController()
        self._setup_ui()
        self._setup_menubar()
        self._muat_data()
        self._perbarui_statistik()

    def _setup_ui(self):
        self.setWindowTitle("Penjadwal Aktivitas")
        self.setMinimumSize(1000, 700) 

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        root.addWidget(self._buat_header())

        konten = QWidget()
        konten_layout = QVBoxLayout(konten)
        konten_layout.setSpacing(15)
        konten_layout.setContentsMargins(20, 20, 20, 20)

        konten_layout.addWidget(self._buat_stat_cards())
        konten_layout.addWidget(self._buat_toolbar())
        konten_layout.addWidget(self._buat_tabel(), stretch=1)

        root.addWidget(konten, stretch=1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Siap")

    def _buat_header(self):
        header = QFrame()
        header.setStyleSheet("background-color: #1a1d2e; border-bottom: 1px solid #2a2d3e;")
        header.setFixedHeight(80) 
        h = QHBoxLayout(header)
        h.setContentsMargins(25, 0, 25, 0)

        teks_frame = QWidget()
        teks_v = QVBoxLayout(teks_frame)
        teks_v.setContentsMargins(0, 0, 0, 0)
        
        lbl_judul = QLabel("📅  Penjadwal Aktivitas")
        lbl_judul.setStyleSheet("color: white; font-size: 22px; font-weight: bold; border: none;")
        lbl_sub = QLabel("Kelola jadwal harianmu dengan mudah")
        lbl_sub.setStyleSheet("color: #8b8fa8; font-size: 13px; border: none;")
        
        teks_v.addWidget(lbl_judul)
        teks_v.addWidget(lbl_sub)

        h.addWidget(teks_frame)
        h.addStretch()

        lbl_id = QLabel(f"👤 {NAMA_MAHASISWA}  |  NIM: {NIM_MAHASISWA}")
        lbl_id.setStyleSheet("color: #5865f2; font-weight: 600; border: none;")
        h.addWidget(lbl_id)

        return header

    def _buat_stat_cards(self):
        frame = QWidget()
        layout = QHBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stat_total   = self._buat_kartu("0", "Total Aktivitas",   "statCardBlue")
        self.stat_selesai = self._buat_kartu("0", "Selesai",            "statCardGreen")
        self.stat_belum   = self._buat_kartu("0", "Belum Selesai",      "statCard")
        self.stat_hariini = self._buat_kartu("0", "Jadwal Hari Ini",    "statCardOrange")

        for kartu in [self.stat_total, self.stat_selesai, self.stat_belum, self.stat_hariini]:
            layout.addWidget(kartu)

        return frame

    def _buat_kartu(self, nilai, caption, object_name):
        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setMinimumHeight(90)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        v = QVBoxLayout(frame)
        
        lbl_nilai = QLabel(nilai)
        lbl_nilai.setAlignment(Qt.AlignCenter)
        lbl_nilai.setStyleSheet("font-size: 24px; font-weight: bold; color: white; border: none;")
        
        lbl_cap = QLabel(caption)
        lbl_cap.setAlignment(Qt.AlignCenter)
        lbl_cap.setStyleSheet("font-size: 12px; color: #8b8fa8; border: none;")

        v.addWidget(lbl_nilai)
        v.addWidget(lbl_cap)
        frame._lbl_nilai = lbl_nilai
        return frame

    def _buat_toolbar(self):
        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        toolbar.setStyleSheet("QFrame#toolbar { background-color: #1e2233; border-radius: 8px; border: 1px solid #2a2d3e; }")

        main_v = QVBoxLayout(toolbar)
        main_v.setContentsMargins(15, 15, 15, 15)
        main_v.setSpacing(15)

        # filter
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        row1.addWidget(QLabel("Tanggal:"))
        self.filter_tanggal = QDateEdit()
        self.filter_tanggal.setCalendarPopup(True)
        self.filter_tanggal.setDate(QDate.currentDate())
        self.filter_tanggal.setMinimumWidth(110)
        self.filter_tanggal.setFixedHeight(32)
        row1.addWidget(self.filter_tanggal)

        btn_reset_tgl = QPushButton("✕")
        btn_reset_tgl.setFixedSize(32, 32)
        row1.addWidget(btn_reset_tgl)

        row1.addSpacing(10)

        # kategori
        row1.addWidget(QLabel("Kategori:"))
        self.filter_kategori = QComboBox()
        self.filter_kategori.addItems(["Semua", "Kuliah", "Tugas", "Organisasi", "Olahraga", "Hiburan", "Pribadi", "Lainnya"])
        self.filter_kategori.setMinimumWidth(120)
        self.filter_kategori.setFixedHeight(32)
        row1.addWidget(self.filter_kategori)

        # status
        row1.addWidget(QLabel("Status:"))
        self.filter_status = QComboBox()
        self.filter_status.addItems(["Semua", "Belum Selesai", "Sedang Berlangsung", "Selesai"])
        self.filter_status.setMinimumWidth(140)
        self.filter_status.setFixedHeight(32)
        row1.addWidget(self.filter_status)

        row1.addStretch() 

        btn_cari = QPushButton("🔍 Cari")
        btn_cari.setMinimumSize(100, 32)
        row1.addWidget(btn_cari)

        btn_tampil_semua = QPushButton("Semua Data")
        btn_tampil_semua.setObjectName("btnSecondary")
        btn_tampil_semua.setMinimumSize(100, 32)
        row1.addWidget(btn_tampil_semua)

        # aksi
        row2 = QHBoxLayout()
        row2.setSpacing(10)

        self.btn_tambah = QPushButton("➕ Tambah")
        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_selesai = QPushButton("✅ Selesai")
        self.btn_hapus = QPushButton("🗑️ Hapus")
        
        self.btn_tambah.setMinimumHeight(35)
        self.btn_edit.setMinimumHeight(35)
        self.btn_selesai.setMinimumHeight(35)
        self.btn_hapus.setMinimumHeight(35)

        row2.addWidget(self.btn_tambah)
        row2.addWidget(self.btn_edit)
        row2.addWidget(self.btn_selesai)
        row2.addWidget(self.btn_hapus)
        row2.addStretch()

        lbl_hint = QLabel("Pilih baris untuk mengelola data")
        lbl_hint.setStyleSheet("color: #4a4d60; font-style: italic;")
        row2.addWidget(lbl_hint)

        main_v.addLayout(row1)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #2a2d3e;")
        main_v.addWidget(line)
        main_v.addLayout(row2)

        btn_cari.clicked.connect(self._on_cari)
        btn_reset_tgl.clicked.connect(self._on_reset_tanggal)
        btn_tampil_semua.clicked.connect(self._on_tampil_semua)
        self.btn_tambah.clicked.connect(self._on_tambah)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_selesai.clicked.connect(self._on_tandai_selesai)
        self.btn_hapus.clicked.connect(self._on_hapus)

        return toolbar

    def _buat_tabel(self):
        self.tabel = QTableWidget()
        kolom = ["#", "Judul", "Tanggal", "Waktu", "Kategori", "Prioritas", "Lokasi", "Status"]
        self.tabel.setColumnCount(len(kolom))
        self.tabel.setHorizontalHeaderLabels(kolom)
        self.tabel.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabel.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabel.verticalHeader().setVisible(False)
        self.tabel.setAlternatingRowColors(True)

        hh = self.tabel.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Interactive) 
        hh.setSectionResizeMode(1, QHeaderView.Stretch) 
        
        self.tabel.setColumnWidth(0, 45)
        self.tabel.setColumnWidth(2, 110)
        self.tabel.setColumnWidth(3, 150)
        self.tabel.setColumnWidth(4, 110)
        self.tabel.setColumnWidth(5, 100)
        self.tabel.setColumnWidth(6, 150)
        self.tabel.setColumnWidth(7, 150)

        return self.tabel

    # menu bar
    def _setup_menubar(self):
        mb = self.menuBar()

        # menu File
        menu_file = mb.addMenu("&File")
        act_refresh = QAction("🔄  Muat Ulang Data", self)
        act_refresh.setShortcut("F5")
        act_refresh.triggered.connect(self._on_tampil_semua)
        menu_file.addAction(act_refresh)
        menu_file.addSeparator()
        act_keluar = QAction("❌  Keluar", self)
        act_keluar.setShortcut("Ctrl+Q")
        act_keluar.triggered.connect(self.close)
        menu_file.addAction(act_keluar)

        # menu Aktivitas
        menu_akt = mb.addMenu("&Aktivitas")
        act_tambah = QAction("➕  Tambah Aktivitas", self)
        act_tambah.setShortcut("Ctrl+N")
        act_tambah.triggered.connect(self._on_tambah)
        menu_akt.addAction(act_tambah)

        act_edit = QAction("✏️  Edit Aktivitas", self)
        act_edit.setShortcut("Ctrl+E")
        act_edit.triggered.connect(self._on_edit)
        menu_akt.addAction(act_edit)

        act_selesai = QAction("✅  Tandai Selesai", self)
        act_selesai.triggered.connect(self._on_tandai_selesai)
        menu_akt.addAction(act_selesai)

        menu_akt.addSeparator()
        act_hapus = QAction("🗑️  Hapus Aktivitas", self)
        act_hapus.setShortcut("Delete")
        act_hapus.triggered.connect(self._on_hapus)
        menu_akt.addAction(act_hapus)

        # menu Bantuan
        menu_bantuan = mb.addMenu("&Bantuan")
        act_tentang = QAction("ℹ️  Tentang Aplikasi", self)
        act_tentang.triggered.connect(self._on_tentang)
        menu_bantuan.addAction(act_tentang)

    # helpers
    def _muat_data(self, filter_tanggal=None, filter_kategori=None, filter_status=None):
        rows = self.controller.ambil_semua(filter_tanggal, filter_kategori, filter_status)
        self.tabel.setRowCount(0)
        for i, row in enumerate(rows):
            self.tabel.insertRow(i)
            self.tabel.setRowHeight(i, 40)

            self._set_item(i, 0, str(i + 1), Qt.AlignCenter)
            self._set_item(i, 1, row["judul"])
            tgl = QDate.fromString(row["tanggal"], "yyyy-MM-dd")
            tgl_str = tgl.toString("dd/MM/yyyy") if tgl.isValid() else row["tanggal"]
            self._set_item(i, 2, tgl_str, Qt.AlignCenter)
            self._set_item(i, 3, f"{row['waktu_mulai']} – {row['waktu_selesai']}", Qt.AlignCenter)
            self._set_item(i, 4, row["kategori"], Qt.AlignCenter)

            item_pri = QTableWidgetItem(row["prioritas"])
            item_pri.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            warna = WARNA_PRIORITAS.get(row["prioritas"], "#c8cad8")
            item_pri.setForeground(QColor(warna))
            item_pri.setData(Qt.UserRole, row["id"])
            self.tabel.setItem(i, 5, item_pri)

            self._set_item(i, 6, row["lokasi"] or "-")

            item_sta = QTableWidgetItem(row["status"])
            item_sta.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            warna_s = WARNA_STATUS.get(row["status"], "#c8cad8")
            item_sta.setForeground(QColor(warna_s))
            self.tabel.setItem(i, 7, item_sta)

            self.tabel.item(i, 0).setData(Qt.UserRole, row["id"])

        self.status_bar.showMessage(f"{len(rows)} aktivitas ditampilkan")

    def _set_item(self, row, col, text, align=Qt.AlignLeft | Qt.AlignVCenter):
        item = QTableWidgetItem(text)
        item.setTextAlignment(align)
        self.tabel.setItem(row, col, item)

    def _get_selected_id(self):
        rows = self.tabel.selectedItems()
        if not rows:
            return None
        row = self.tabel.currentRow()
        item = self.tabel.item(row, 0)
        return item.data(Qt.UserRole) if item else None

    def _perbarui_statistik(self):
        stat = self.controller.statistik()
        self.stat_total._lbl_nilai.setText(str(stat["total"]))
        self.stat_selesai._lbl_nilai.setText(str(stat["selesai"]))
        self.stat_belum._lbl_nilai.setText(str(stat["belum"]))
        self.stat_hariini._lbl_nilai.setText(str(stat["hari_ini"]))

    def _on_cari(self):
        tgl = self.filter_tanggal.date().toString("yyyy-MM-dd")
        kat = self.filter_kategori.currentText()
        sta = self.filter_status.currentText()
        self._muat_data(tgl, kat, sta)

    def _on_reset_tanggal(self):
        self.filter_tanggal.setDate(QDate.currentDate())

    def _on_tampil_semua(self):
        self.filter_kategori.setCurrentIndex(0)
        self.filter_status.setCurrentIndex(0)
        self._muat_data()
        self._perbarui_statistik()

    def _on_tambah(self):
        dialog = DialogAktivitas(self)
        if dialog.exec():
            data = dialog.ambil_data()
            ok, pesan = self.controller.tambah(data)
            if ok:
                self._muat_data()
                self._perbarui_statistik()
                self.status_bar.showMessage(pesan)
            else:
                QMessageBox.warning(self, "Gagal Tambah", pesan)

    def _on_edit(self):
        aktivitas_id = self._get_selected_id()
        if not aktivitas_id:
            QMessageBox.information(self, "Pilih Data", "Silakan pilih aktivitas yang ingin diedit.")
            return
        row = self.controller.ambil_by_id(aktivitas_id)
        if not row:
            return
        dialog = DialogAktivitas(self, data_awal=dict(row))
        if dialog.exec():
            data = dialog.ambil_data()
            ok, pesan = self.controller.edit(aktivitas_id, data)
            if ok:
                self._muat_data()
                self._perbarui_statistik()
                self.status_bar.showMessage(pesan)
            else:
                QMessageBox.warning(self, "Gagal Edit", pesan)

    def _on_tandai_selesai(self):
        aktivitas_id = self._get_selected_id()
        if not aktivitas_id:
            QMessageBox.information(self, "Pilih Data", "Silakan pilih aktivitas terlebih dahulu.")
            return
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi",
            "Tandai aktivitas ini sebagai Selesai?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            ok, pesan = self.controller.tandai_selesai(aktivitas_id)
            if ok:
                self._muat_data()
                self._perbarui_statistik()
                self.status_bar.showMessage(pesan)

    def _on_hapus(self):
        aktivitas_id = self._get_selected_id()
        if not aktivitas_id:
            QMessageBox.information(self, "Pilih Data", "Silakan pilih aktivitas yang ingin dihapus.")
            return
        row = self.tabel.currentRow()
        judul = self.tabel.item(row, 1).text() if self.tabel.item(row, 1) else ""
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus aktivitas:\n\n\"{judul}\"?\n\nData tidak dapat dikembalikan.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            ok, pesan = self.controller.hapus(aktivitas_id)
            if ok:
                self._muat_data()
                self._perbarui_statistik()
                self.status_bar.showMessage(pesan)

    def _on_tentang(self):
        dialog = DialogTentang(self)
        dialog.exec()
