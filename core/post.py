from .componentes import Estado, Componente, PostEngine
from typing import List, Tuple
import random

class Post:
    def __init__(self, engine: PostEngine = None):
        self.engine = engine or PostEngine()
        self.pasos: List[Tuple[str, str]] = [
            ("BIOS/UEFI", "Inicializando firmware"),
            ("CPU", "Comprobando procesador"),
            ("RAM", "Comprobando memoria RAM"),
            ("GPU", "Comprobando tarjeta gráfica"),
            ("Placa base", "Comprobando placa base"),
            ("Almacenamiento", "Comprobando almacenamiento"),
            ("Ventiladores", "Comprobando ventiladores"),
            ("Periféricos", "Comprobando periféricos"),
            ("Resultado", "Evaluando resultados"),
        ]
        self.fallas_simuladas: set = set()
        self.precauciones_simuladas: set = set()

    def simular_falla(self, comp_id: str):
        self.fallas_simuladas.add(comp_id)
        if comp_id in self.precauciones_simuladas:
            self.precauciones_simuladas.discard(comp_id)

    def simular_precaucion(self, comp_id: str):
        self.precauciones_simuladas.add(comp_id)
        if comp_id in self.fallas_simuladas:
            self.fallas_simuladas.discard(comp_id)

    def limpiar_fallas(self):
        self.fallas_simuladas.clear()
        self.precauciones_simuladas.clear()

    def ejecutar(self):
        eventos = []
        # Aplicar estados simulados
        for cid in self.fallas_simuladas:
            c = self.engine.get_componente(cid)
            if c:
                c.set_estado(Estado.FALLA, f"{c.nombre} con falla simulada")
        for cid in self.precauciones_simuladas:
            c = self.engine.get_componente(cid)
            if c:
                c.set_estado(Estado.PRECAUCION, f"{c.nombre} requiere atención")
        return eventos
