# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QFrame,QSplitter,QProgressBar,QButtonGroup,QTextEdit)
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QFont
import os
import random
from core import PostEngine,Post,Resultado
from ui.dashboard import DashboardWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador BIOS - POWER ON SELF TEST")
        self.setMinimumSize(1100,760)
        self.engine=PostEngine(); self.post=Post(self.engine)
        self.escenario="TODO_OK"
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
        center=QFrame(); center.setObjectName("center_frame")
        cl=QVBoxLayout(center)
        self.progress=QProgressBar(); self.progress.setMinimum(0); self.progress.setMaximum(100); self.progress.setFormat("POST %p%")
        cl.addWidget(self.progress)
        self.log=QTextEdit(); self.log.setReadOnly(True); self.log.setFont(QFont("Consolas",9)); self.log.setMinimumHeight(420)
        cl.addWidget(self.log)
        sp.addWidget(center)
        self.dashboard=DashboardWidget(self.engine)
        df=QFrame(); dl=QVBoxLayout(df); dl.addWidget(self.dashboard); sp.addWidget(df)
        sp.setSizes([360,760])
        bar=QFrame(); bl=QVBoxLayout(bar)
        sel=QHBoxLayout(); sel.addWidget(QLabel("Escenario:"))
        claves=["TODO_OK","ADVERTENCIAS","FALLA_CRITICA","ALEATORIO"]
        textos=["Caso 1: Todo OK","Caso 2: Advertencias","Caso 3: Falla crítica","Caso 4: Aleatorio"]
        self.btn_caso=[]
        self.grupo_escenario=QButtonGroup(self); self.grupo_escenario.setExclusive(True)
        for i,texto in enumerate(textos):
            b=QPushButton(texto); b.setCheckable(True); self.grupo_escenario.addButton(b,i); sel.addWidget(b)
            b.clicked.connect(lambda _=False,k=claves[i]: self.seleccionar_escenario(k))
            self.btn_caso.append(b)
        self.btn_caso[0].setChecked(True); sel.addStretch()
        acc=QHBoxLayout()
        self.btn_iniciar=QPushButton("▶ INICIAR POST"); self.btn_reset=QPushButton("RESET")
        acc.addWidget(self.btn_iniciar); acc.addWidget(self.btn_reset); acc.addStretch()
        bl.addLayout(sel); bl.addLayout(acc)
        ml.addWidget(bar)
        self.btn_iniciar.clicked.connect(self.iniciar); self.btn_reset.clicked.connect(self.reset_ui)

    def apply_styles(self):
        p=os.path.join(os.path.dirname(os.path.dirname(__file__)),"styles","bios.qss")
        if os.path.exists(p):
            with open(p,encoding="utf-8") as f: self.setStyleSheet(f.read())

    def reset_ui(self):
        self.post.limpiar_fallas(); self.engine.reset(); self.dashboard.refresh()
        self.progress.setValue(0); self.log.clear(); self.log.append("Listo para iniciar POST.")
        self._post_paso=0; self._post_eventos=[]; self.btn_iniciar.setEnabled(True); self.post_timer.stop()

    def seleccionar_escenario(self, clave):
        self.escenario=clave
        self.reset_ui(); self._aplicar_escenario(); self.dashboard.refresh()

    def _aplicar_escenario(self):
        self.post.limpiar_fallas()
        esc=self.escenario
        if esc=="ALEATORIO":
            esc=random.choice(["TODO_OK","ADVERTENCIAS","FALLA_CRITICA"])
            self.log.append(f"Escenario aleatorio seleccionado: {esc}")
        if esc=="ADVERTENCIAS":
            self.post.simular_precaucion("gpu"); self.post.simular_falla("ventiladores")
            self.log.append("Escenario: advertencias en componentes no críticos (GPU / ventiladores).")
        elif esc=="FALLA_CRITICA":
            critico=random.choice(["cpu","ram","placa_base"])
            self.post.simular_falla(critico)
            self.log.append(f"Escenario: falla crítica en componente esencial ({critico}).")
        else:
            self.log.append("Escenario: todos los componentes funcionan correctamente.")

    def iniciar(self):
        self.reset_ui(); self._aplicar_escenario(); self._post_eventos=self.post.ejecutar()
        self._post_paso=0; self.btn_iniciar.setEnabled(False); self.progress.setValue(0); self.post_timer.start(550)

    def _avanzar_post(self):
        if self._post_paso < len(self._post_eventos):
            nombre,msg,estado=self._post_eventos[self._post_paso]
            self.log.append(f"[{self._post_paso+1}/{len(self._post_eventos)}] {nombre}: {msg} -> {estado.value}")
            self.progress.setValue(int((self._post_paso+1)*100/len(self._post_eventos))); self._post_paso+=1; self.dashboard.refresh()
        else:
            self.post_timer.stop(); self._evaluar(); self.btn_iniciar.setEnabled(True)

    def _evaluar(self):
        if self.post.resultado==Resultado.FALLO_CRITICO:
            self.log.append("🔴 ERROR CRÍTICO - EL ARRANQUE SE HA DETENIDO.")
            self.log.append("   No se puede iniciar el sistema operativo por un fallo físico crítico.")
        elif self.post.resultado==Resultado.ADVERTENCIA:
            self.log.append("🟡 POST COMPLETADO CON ADVERTENCIAS - INICIANDO SISTEMA OPERATIVO...")
            self.log.append("   El sistema arrancará, pero se sugiere revisión del equipo.")
        else:
            self.log.append("🟢 SISTEMA CORRECTO (OK) - INICIANDO SISTEMA OPERATIVO...")
