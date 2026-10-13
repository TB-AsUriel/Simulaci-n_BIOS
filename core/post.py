from .componentes import Estado, Componente, PostEngine
from typing import List, Tuple

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

    def simular_falla(self, comp_id: str):
        if comp_id in self.engine.componentes:
            # find by id
            pass
        self.fallas_simuladas.add(comp_id)

    def limpiar_fallas(self):
        self.fallas_simuladas.clear()

    def ejecutar(self):
        # Devuelve lista de eventos (paso, mensaje, estado)
        eventos = []
        # Aplica fallas
        for cid in self.fallas_simuladas:
            c = self.engine.get_componente(cid)
            if c:
                c.set_estado(Estado.FALLA, f"{c.nombre} con falla simulada")
        # Ejecuta pasos
        for nombre, msg in self.pasos:
            eventos.append((nombre, msg, Estado.FUNCIONAL))
        return eventos
