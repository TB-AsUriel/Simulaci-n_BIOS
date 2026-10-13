
import os

from core import Estado, Post, PostEngine
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ui.dashboard import DashboardWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIOS Simulator - POWER ON SELF TEST")
        self.setMinimumSize(1200, 800)
        self.engine = PostEngine()
        self.post = Post(self.engine)
        self.post_timer = QTimer(self)
        self.post_timer.timeout.connect(self._avanzar_post)
        self._post_paso = 0
        self._post_eventos = []
        self.setup_ui()
        self.apply_styles()
        self.reset_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_layout = QVBoxLayout(header_frame)
        title = QLabel("BIOS SIMULATOR")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Consolas", 28, QFont.Bold))
        subtitle = QLabel("POST - Power On Self Test | UEFI v1.0")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Consolas", 11))
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_frame)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        self.dashboard = DashboardWidget(self.engine)
        dashboard_frame = QFrame()
        db_layout = QVBoxLayout(dashboard_frame)
        db_layout.addWidget(self.dashboard)
        splitter.addWidget(dashboard_frame)

        center_frame = QFrame()
        center_frame.setObjectName("center_frame")
        center_layout = QVBoxLayout(center_frame)
        center_layout.setSpacing(10)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("POST %p%")
        center_layout.addWidget(self.progress_bar)
        self.log_label = QLabel("Listo para iniciar POST")
        self.log_label.setFont(QFont("Consolas", 10))
        self.log_label.setWordWrap(True)
        log_frame = QFrame()
        log_frame.setObjectName("log_frame")
        log_l = QVBoxLayout(log_frame)
        log_l.addWidget(self.log_label)
        center_layout.addWidget(log_frame)
        center_layout.addStretch()
        splitter.addWidget(center_frame)

        right_frame = QFrame()
        right_frame.setObjectName("right_frame")
        right_layout = QVBoxLayout(right_frame)
        info_header = QLabel("INFORMACIÓN")
        info_header.setFont(QFont("Consolas", 12, QFont.Bold))
        info_header.setAlignment(Qt.AlignCenter)
        self.info_label = QLabel("Sistema en modo simulación")
        self.info_label.setFont(QFont("Consolas", 9))
        self.info_label.setWordWrap(True)
        right_layout.addWidget(info_header)
        right_layout.addWidget(self.info_label)
        right_layout.addStretch()
        splitter.addWidget(right_frame)
        splitter.setSizes([280, 640, 280])

        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        self.btn_iniciar = QPushButton("▶ INICIAR POST")
        self.btn_reset = QPushButton("RESET")
        self.btn_falla_cpu = QPushButton("SIMULAR FALLA CPU")
        self.btn_falla_ram = QPushButton("SIMULAR FALLA RAM")
        buttons_layout.addWidget(self.btn_iniciar)
        buttons_layout.addWidget(self.btn_reset)
        buttons_layout.addWidget(self.btn_falla_cpu)
        buttons_layout.addWidget(self.btn_falla_ram)
        buttons_layout.addStretch()
        main_layout.addWidget(buttons_frame)

        self.btn_iniciar.clicked.connect(self.iniciar_post)
        self.btn_reset.clicked.connect(self.reset_ui)
        self.btn_falla_cpu.clicked.connect(lambda: self.simular_falla("cpu"))
        self.btn_falla_ram.clicked.connect(lambda: self.simular_falla("ram"))

    def apply_styles(self):
        style_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "bios.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def reset_ui(self):
        self.post.limpiar_fallas()
        self.engine.reset()
        self.dashboard.refresh()
        self.progress_bar.setValue(0)
        self.log_label.setText("Listo para iniciar POST")
        self._post_paso = 0
        self._post_eventos = []
        self.btn_iniciar.setEnabled(True)
        self.post_timer.stop()

    def iniciar_post(self):
        self.reset_ui()
        self._post_eventos = self.post.ejecutar()
        self._post_paso = 0
        self.btn_iniciar.setEnabled(False)
        self.progress_bar.setValue(0)
        self.post_timer.start(500)

    def _avanzar_post(self):
        if self._post_paso < len(self._post_eventos):
            nombre, msg, estado = self._post_eventos[self._post_paso]
            self.log_label.setText(f"{nombre}: {msg}")
            pct = int((self._post_paso + 1) * 100 / len(self._post_eventos))
            self.progress_bar.setValue(pct)
            self._post_paso += 1
            self.dashboard.refresh()
        else:
            self.post_timer.stop()
            self._evaluar_resultado()
            self.btn_iniciar.setEnabled(True)

    def _evaluar_resultado(self):
        hay_falla = any(c.estado == Estado.FALLA for c in self.engine.componentes)
        hay_precaucion = any(c.estado == Estado.PRECAUCION for c in self.engine.componentes)
        if hay_falla:
            criticos = [c.nombre for c in self.engine.componentes if c.estado == Estado.FALLA and c.prioridad == "CRITICO"]
            if criticos:
                self.log_label.setText("🔴 SISTEMA NO PUEDE ARRANCAR\nFallas críticas detectadas.")
            else:
                self.log_label.setText("🔴 SISTEMA NO PUEDE ARRANCAR\nSe detectaron fallas.")
        elif hay_precaucion:
            self.log_label.setText("🟡 SISTEMA CON PRECAUCIÓN\nSe detectaron advertencias.")
        else:
            self.log_label.setText("🟢 SISTEMA OK\nPOST completado correctamente. Sistema listo para iniciar.")

    def simular_falla(self, comp_id: str):
        c = self.engine.get_componente(comp_id)
        if c:
            c.set_estado(Estado.FALLA, f"{c.nombre} no responde")
        self.dashboard.refresh()
