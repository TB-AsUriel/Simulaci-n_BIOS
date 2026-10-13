# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QLabel, QPushButton, QFrame, QStackedWidget, QListWidget, 
                             QListWidgetItem, QSplitter, QProgressBar, QTextEdit)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QIcon, QFont, QPixmap
import sys
import os

from core import Estado, PostEngine, Post

class ComponentItem(QFrame):
    def __init__(self, componente):
        super().__init__()
        self.componente = componente
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setObjectName("comp_item")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(10)

        # Icono
        icon_label = QLabel()
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "icons", f"{componente.id}.svg")
        # mapeo por si id diferente
        if not os.path.exists(icon_path):
            mapping = {
                "cpu": "procesador",
                "ram": "memoria_ram",
                "gpu": "tarjeta_grafica",
                "placa_base": "placa_base",
                "almacenamiento": "almacenamiento",
                "ventiladores": "ventiladores",
                "usb": "puertos_usb",
                "red": "red"
            }
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "icons", f"{mapping.get(componente.id, componente.id)}.svg")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            icon_label.setPixmap(icon.pixmap(24, 24))
        layout.addWidget(icon_label)

        # Nombre
        name_label = QLabel(componente.nombre)
        name_font = QFont("Consolas", 10)
        name_label.setFont(name_font)
        layout.addWidget(name_label)
        layout.addStretch()

        # Estado
        self.estado_label = QLabel(componente.estado.value)
        self.estado_label.setObjectName(f"estado_{componente.id}")
        self.estado_label.setAlignment(Qt.AlignCenter)
        est_font = QFont("Consolas", 9, QFont.Bold)
        self.estado_label.setFont(est_font)
        layout.addWidget(self.estado_label)

    def update_estado(self):
        est = self.componente.estado
        self.estado_label.setText(est.value)
        # Estilos por estado
        if est == Estado.FUNCIONAL:
            self.estado_label.setStyleSheet("color: #22c55e;")
        elif est == Estado.PRECAUCION:
            self.estado_label.setStyleSheet("color: #f59e0b;")
        elif est == Estado.FALLA:
            self.estado_label.setStyleSheet("color: #ef4444;")

class DashboardWidget(QWidget):
    def __init__(self, engine: PostEngine):
        super().__init__()
        self.engine = engine
        self.items = {}
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        header = QLabel("COMPONENTES")
        header_font = QFont("Consolas", 12, QFont.Bold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        for c in self.engine.componentes:
            item = ComponentItem(c)
            self.items[c.id] = item
            layout.addWidget(item)
        layout.addStretch()

    def refresh(self):
        for item in self.items.values():
            item.update_estado()
