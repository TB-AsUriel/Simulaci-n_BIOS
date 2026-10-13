# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QFrame,QSplitter,QProgressBar,QComboBox,QTextEdit)
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QFont
import os
from core import PostEngine,Post,Estado
from ui.dashboard import DashboardWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIOS Simulator - POWER ON SELF TEST")
        self.setMinimumSize(1100,760)
        self.engine=PostEngine(); self.post=Post(self.engine)
        self.post_timer=QTimer(self); self.post_timer.timeout.connect(self._avanzar_post)
        self._post_paso=0; self._post_eventos=[]
        self.setup_ui(); self.apply_styles(); self.reset_ui()

    def setup_ui(self):
        central=QWidget(); self.setCentralWidget(central)
        ml=QVBoxLayout(central); ml.setContentsMargins(10,10,10,10); ml.setSpacing(10)
        header=QFrame(); header.setObjectName("header_frame")
        hl=QVBoxLayout(header)
        t=QLabel("BIOS SIMULATOR"); t.setAlignment(Qt.AlignCenter); t.setFont(QFont("Consolas",28,QFont.Bold))
        s=QLabel("POST - Power On Self Test"); s.setAlignment(Qt.AlignCenter); s.setFont(QFont("Consolas",12))
        hl.addWidget(t); hl.addWidget(s); ml.addWidget(header)
        sp=QSplitter(Qt.Horizontal); ml.addWidget(sp)
        self.dashboard=DashboardWidget(self.engine)
        df=QFrame(); dl=QVBoxLayout(df); dl.addWidget(self.dashboard); sp.addWidget(df)
        center=QFrame(); center.setObjectName("center_frame")
        cl=QVBoxLayout(center)
        self.progress=QProgressBar(); self.progress.setMinimum(0); self.progress.setMaximum(100); self.progress.setFormat("POST %p%")
        cl.addWidget(self.progress)
        self.log=QTextEdit(); self.log.setReadOnly(True); self.log.setFont(QFont("Consolas",9)); self.log.setMinimumHeight(420)
        cl.addWidget(self.log)
        sp.addWidget(center); sp.setSizes([320,760])
        bar=QFrame(); bl=QHBoxLayout(bar)
        self.btn_iniciar=QPushButton("▶ INICIAR POST"); self.btn_reset=QPushButton("RESET")
        self.combo_falla=QComboBox(); self.combo_falla.addItem("Sin falla",None)
        for c in self.engine.componentes: self.combo_falla.addItem(f"Falla: {c.nombre}",c.id)
        self.combo_prec=QComboBox(); self.combo_prec.addItem("Sin precaución",None)
        for c in self.engine.componentes: self.combo_prec.addItem(f"Precaución: {c.nombre}",c.id)
        bl.addWidget(self.btn_iniciar); bl.addWidget(self.btn_reset); bl.addWidget(self.combo_falla); bl.addWidget(self.combo_prec); bl.addStretch()
        ml.addWidget(bar)
        self.btn_iniciar.clicked.connect(self.iniciar); self.btn_reset.clicked.connect(self.reset_ui)
        self.combo_falla.currentIndexChanged.connect(self.aplicar_falla); self.combo_prec.currentIndexChanged.connect(self.aplicar_prec)

    def apply_styles(self):
        p=os.path.join(os.path.dirname(os.path.dirname(__file__)),"styles","bios.qss")
        if os.path.exists(p):
            with open(p,encoding="utf-8") as f: self.setStyleSheet(f.read())

    def reset_ui(self):
        self.post.limpiar_fallas(); self.engine.reset(); self.dashboard.refresh()
        self.progress.setValue(0); self.log.clear(); self.log.append("Listo para iniciar POST.")
        self._post_paso=0; self._post_eventos=[]; self.btn_iniciar.setEnabled(True); self.post_timer.stop()
        self.combo_falla.setCurrentIndex(0); self.combo_prec.setCurrentIndex(0)

    def iniciar(self):
        self.reset_ui(); self._post_eventos=self.post.ejecutar(); self._post_paso=0; self.btn_iniciar.setEnabled(False); self.progress.setValue(0); self.post_timer.start(550)

    def _avanzar_post(self):
        if self._post_paso < len(self._post_eventos):
            nombre,msg,_e=self._post_eventos[self._post_paso]
            self.log.append(f"[{self._post_paso+1}/{len(self._post_eventos)}] {nombre}: {msg}")
            self.progress.setValue(int((self._post_paso+1)*100/len(self._post_eventos))); self._post_paso+=1; self.dashboard.refresh()
        else:
            self.post_timer.stop(); self._evaluar(); self.btn_iniciar.setEnabled(True)

    def _evaluar(self):
        hay_f=any(c.estado==Estado.FALLA for c in self.engine.componentes); hay_p=any(c.estado==Estado.PRECAUCION for c in self.engine.componentes)
        if hay_f: self.log.append("🔴 SISTEMA NO PUEDE ARRANCAR - Se detectaron fallas críticas.")
        elif hay_p: self.log.append("🟡 SISTEMA CON PRECAUCIÓN - Se detectaron advertencias.")
        else: self.log.append("🟢 SISTEMA OK - POST completado correctamente.")

    def aplicar_falla(self):
        cid=self.combo_falla.currentData()
        if cid: self.post.simular_falla(cid); self.combo_prec.setCurrentIndex(0); self.dashboard.refresh()

    def aplicar_prec(self):
        cid=self.combo_prec.currentData()
        if cid: self.post.simular_precaucion(cid); self.combo_falla.setCurrentIndex(0); self.dashboard.refresh()
