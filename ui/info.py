# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        header = QLabel("INFORMACIÃ“N DEL SISTEMA")
        header.setFont(QFont("Consolas", 10, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setFont(QFont("Consolas", 8))
        self.text.setFixedHeight(220)
        self.text.setPlainText("Modo: SIMULACIÃ“N\nCPU: Intel Core (simulado)\nRAM: 16 GB (simulado)\nAlmacenamiento: 512 GB SSD (simulado)\nPlaca base: (simulado)\nGPU: (simulado)\n")
        layout.addWidget(header)
        layout.addWidget(self.text)
        layout.addStretch()

    def set_modo(self, modo: str):
        self.text.setPlainText(f"Modo: {modo}\nCPU: (simulado)\nRAM: 16 GB (simulado)\nAlmacenamiento: (simulado)\nGPU: (simulado)\nPlaca base: (simulado)\nRed: (simulado)")

