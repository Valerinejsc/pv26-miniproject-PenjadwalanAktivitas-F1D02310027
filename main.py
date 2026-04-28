import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from database import init_db
from ui_main import MainWindow


def load_stylesheet(app: QApplication) -> None:
    # memuat QSS dari file style.qss eksternal
    qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"[PERINGATAN] File style.qss tidak ditemukan di: {qss_path}")


def main():
    # inisialisasi database jika belum ada
    init_db()

    app = QApplication(sys.argv)
    app.setApplicationName("Penjadwal Aktivitas")
    app.setOrganizationName("Valerine Jesika Dewi")

    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
