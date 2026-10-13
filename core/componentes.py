# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class Estado(Enum):
    FUNCIONAL = "FUNCIONAL"
    PRECAUCION = "PRECAUCIÓN"
    FALLA = "FALLA"

@dataclass
class Componente:
    id: str
    nombre: str  # Nombre en español para UI
    estado: Estado = Estado.FUNCIONAL
    descripcion: str = ""
    temperatura: Optional[float] = None
    mensaje: str = ""
    prioridad: str = "NORMAL"  # CRITICO | IMPORTANTE | NORMAL

    def set_estado(self, estado: Estado, mensaje: str = ""):
        self.estado = estado
        self.mensaje = mensaje

class PostEngine:
    def __init__(self):
        self.componentes: List[Componente] = self._crear_componentes()

    def _crear_componentes(self) -> List[Componente]:
        return [
            Componente(id="cpu", nombre="Procesador", descripcion="Unidad central de procesamiento", prioridad="CRITICO"),
            Componente(id="ram", nombre="Memoria RAM", descripcion="Memoria de acceso aleatorio", prioridad="CRITICO"),
            Componente(id="gpu", nombre="Tarjeta gráfica", descripcion="Unidad de procesamiento gráfico", prioridad="IMPORTANTE"),
            Componente(id="almacenamiento", nombre="Almacenamiento", descripcion="Dispositivos de almacenamiento", prioridad="CRITICO"),
            Componente(id="placa_base", nombre="Placa base", descripcion="Placa base del sistema", prioridad="CRITICO"),
            Componente(id="ventiladores", nombre="Ventiladores", descripcion="Sistema de refrigeración", prioridad="IMPORTANTE"),
            Componente(id="usb", nombre="Puertos USB", descripcion="Puertos de entrada/salida", prioridad="NORMAL"),
            Componente(id="red", nombre="Red", descripcion="Conectividad de red", prioridad="NORMAL"),
        ]

    def get_componente(self, comp_id: str) -> Optional[Componente]:
        for c in self.componentes:
            if c.id == comp_id:
                return c
        return None

    def reset(self):
        for c in self.componentes:
            c.estado = Estado.FUNCIONAL
            c.mensaje = ""
            c.temperatura = None