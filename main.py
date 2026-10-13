
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIOS Simulator - POWER ON SELF TEST")
        self.setMinimumSize(1024, 768)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("BIOS SIMULATOR")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont("Consolas", 32, QFont.Bold)
        title.setFont(title_font)

        subtitle = QLabel("POST - Power On Self Test")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont("Consolas", 16)
        subtitle.setFont(subtitle_font)

        status = QLabel("SISTEMA LISTO")
        status.setAlignment(Qt.AlignCenter)
        status_font = QFont("Consolas", 18, QFont.Bold)
        status.setFont(status_font)
        status.setObjectName("status_label")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(status)

    def apply_styles(self):
        style_path = os.path.join(os.path.dirname(__file__), "styles", "bios.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()