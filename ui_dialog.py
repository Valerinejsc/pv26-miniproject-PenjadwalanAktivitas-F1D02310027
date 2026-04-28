from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QDateEdit, QTimeEdit,
    QTextEdit, QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QDate, QTime
from logic import KATEGORI_LIST, PRIORITAS_LIST, STATUS_LIST


class DialogAktivitas(QDialog):
    #dialog untuk menambah atau mengedit aktivitas
    def __init__(self, parent=None, data_awal=None):
        super().__init__(parent)
        self.data_awal = data_awal
        self.is_edit = data_awal is not None
        self._setup_ui()
        if self.is_edit:
            self._isi_form(data_awal)

    def _setup_ui(self):
        judul = "Edit Aktivitas" if self.is_edit else "Tambah Aktivitas Baru"
        self.setWindowTitle(judul)
        self.setMinimumWidth(480)
        self.setModal(True)

        layout_utama = QVBoxLayout(self)
        layout_utama.setSpacing(16)
        layout_utama.setContentsMargins(24, 20, 24, 20)

        # header
        lbl_header = QLabel(judul)
        lbl_header.setObjectName("labelJudul")
        lbl_header.setStyleSheet("font-size: 16px; font-weight: 700; color: #ffffff;")
        layout_utama.addWidget(lbl_header)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.HLine)
        layout_utama.addWidget(sep)

        # form
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # judul
        self.input_judul = QLineEdit()
        self.input_judul.setPlaceholderText("Contoh: Kuliah Pemrograman Visual")
        self.input_judul.setMaxLength(100)
        form.addRow("Judul *", self.input_judul)

        # tanggal
        self.input_tanggal = QDateEdit()
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setDate(QDate.currentDate())
        self.input_tanggal.setDisplayFormat("dd/MM/yyyy")
        form.addRow("Tanggal *", self.input_tanggal)

        # waktu 
        waktu_widget = QFrame()
        waktu_layout = QHBoxLayout(waktu_widget)
        waktu_layout.setContentsMargins(0, 0, 0, 0)
        waktu_layout.setSpacing(8)

        self.input_mulai = QTimeEdit()
        self.input_mulai.setDisplayFormat("HH:mm")
        self.input_mulai.setTime(QTime(8, 0))

        lbl_sampai = QLabel("s/d")
        lbl_sampai.setAlignment(Qt.AlignCenter)
        lbl_sampai.setFixedWidth(24)

        self.input_selesai = QTimeEdit()
        self.input_selesai.setDisplayFormat("HH:mm")
        self.input_selesai.setTime(QTime(9, 0))

        waktu_layout.addWidget(self.input_mulai)
        waktu_layout.addWidget(lbl_sampai)
        waktu_layout.addWidget(self.input_selesai)
        form.addRow("Waktu *", waktu_widget)

        # kategori
        self.input_kategori = QComboBox()
        self.input_kategori.addItems(KATEGORI_LIST)
        form.addRow("Kategori *", self.input_kategori)

        # prioritas
        self.input_prioritas = QComboBox()
        self.input_prioritas.addItems(PRIORITAS_LIST)
        form.addRow("Prioritas *", self.input_prioritas)

        # lokasi
        self.input_lokasi = QLineEdit()
        self.input_lokasi.setPlaceholderText("Contoh: Ruang Kelas A, Online, dll.")
        form.addRow("Lokasi", self.input_lokasi)

        # deskripsi
        self.input_deskripsi = QTextEdit()
        self.input_deskripsi.setPlaceholderText("Catatan atau deskripsi tambahan...")
        self.input_deskripsi.setMaximumHeight(90)
        form.addRow("Deskripsi", self.input_deskripsi)
        if self.is_edit:
            self.input_status = QComboBox()
            self.input_status.addItems(STATUS_LIST)
            form.addRow("Status *", self.input_status)

        layout_utama.addLayout(form)

        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.HLine)
        layout_utama.addWidget(sep2)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnSecondary")
        self.btn_batal.setFixedHeight(38)

        label_simpan = "Simpan Perubahan" if self.is_edit else "Tambah Aktivitas"
        self.btn_simpan = QPushButton(label_simpan)
        self.btn_simpan.setFixedHeight(38)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_simpan)
        layout_utama.addLayout(btn_layout)

        self.btn_batal.clicked.connect(self.reject)
        self.btn_simpan.clicked.connect(self._on_simpan)

    def _isi_form(self, data):
        self.input_judul.setText(data["judul"])
        tgl = QDate.fromString(data["tanggal"], "yyyy-MM-dd")
        if tgl.isValid():
            self.input_tanggal.setDate(tgl)
        self.input_mulai.setTime(QTime.fromString(data["waktu_mulai"], "HH:mm"))
        self.input_selesai.setTime(QTime.fromString(data["waktu_selesai"], "HH:mm"))
        idx_kat = self.input_kategori.findText(data["kategori"])
        if idx_kat >= 0:
            self.input_kategori.setCurrentIndex(idx_kat)
        idx_pri = self.input_prioritas.findText(data["prioritas"])
        if idx_pri >= 0:
            self.input_prioritas.setCurrentIndex(idx_pri)
        self.input_lokasi.setText(data["lokasi"] or "")
        self.input_deskripsi.setPlainText(data["deskripsi"] or "")
        if self.is_edit:
            idx_sta = self.input_status.findText(data["status"])
            if idx_sta >= 0:
                self.input_status.setCurrentIndex(idx_sta)

    def _on_simpan(self):
        if not self.input_judul.text().strip():
            QMessageBox.warning(self, "Validasi", "Judul aktivitas tidak boleh kosong.")
            self.input_judul.setFocus()
            return
        self.accept()

    def ambil_data(self) -> dict:
        data = {
            "judul": self.input_judul.text().strip(),
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd"),
            "waktu_mulai": self.input_mulai.time().toString("HH:mm"),
            "waktu_selesai": self.input_selesai.time().toString("HH:mm"),
            "kategori": self.input_kategori.currentText(),
            "prioritas": self.input_prioritas.currentText(),
            "lokasi": self.input_lokasi.text().strip(),
            "deskripsi": self.input_deskripsi.toPlainText().strip(),
            "status": self.input_status.currentText() if self.is_edit else "Belum Selesai",
        }
        return data


class DialogTentang(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tentang Aplikasi")
        self.setFixedSize(420, 320)
        self.setModal(True)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(28, 24, 28, 20)

        lbl_nama_app = QLabel("📅  Penjadwal Aktivitas")
        lbl_nama_app.setStyleSheet("font-size: 20px; font-weight: 700; color: #ffffff;")

        lbl_versi = QLabel("Versi 1.0.0")
        lbl_versi.setStyleSheet("color: #6b6f8a; font-size: 12px;")

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.HLine)

        lbl_deskripsi = QLabel(
            "Aplikasi manajemen jadwal harian berbasis GUI PySide6.\n"
            "Memungkinkan pengguna mencatat, memonitor, dan mengelola\n"
            "aktivitas sehari-hari dengan mudah dan terstruktur."
        )
        lbl_deskripsi.setWordWrap(True)
        lbl_deskripsi.setStyleSheet("color: #c8cad8; line-height: 1.6; font-size: 13px;")

        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.HLine)

        info_frame = QFrame()
        info_frame.setStyleSheet(
            "background:#1a1d2e; border:1px solid #2a2d3e; border-radius:8px; padding:10px;"
        )
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(4)

        lbl_mhs = QLabel("👤  Dibuat oleh:")
        lbl_mhs.setStyleSheet("color:#6b6f8a; font-size:11px; font-weight:600;")
        lbl_nm = QLabel("Valerine Jesika Dewi")
        lbl_nm.setStyleSheet("color:#e8eaf0; font-size:14px; font-weight:700;")
        lbl_nim = QLabel("NIM: F1D02310027")
        lbl_nim.setStyleSheet("color:#5865f2; font-size:12px; font-weight:600;")

        info_layout.addWidget(lbl_mhs)
        info_layout.addWidget(lbl_nm)
        info_layout.addWidget(lbl_nim)

        btn_tutup = QPushButton("Tutup")
        btn_tutup.setFixedHeight(36)
        btn_tutup.clicked.connect(self.accept)

        layout.addWidget(lbl_nama_app)
        layout.addWidget(lbl_versi)
        layout.addWidget(sep)
        layout.addWidget(lbl_deskripsi)
        layout.addWidget(sep2)
        layout.addWidget(info_frame)
        layout.addStretch()
        layout.addWidget(btn_tutup)
