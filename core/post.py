from .componentes import Estado, PostEngine, Resultado


class Post:
    def __init__(self, engine: PostEngine = None):
        self.engine = engine or PostEngine()
        # Cada paso: (nombre mostrado, mensaje por defecto, id de componente o None)
        self.pasos: list[tuple[str, str, str | None]] = [
            ("BIOS/UEFI", "Inicializando firmware", None),
            ("CPU", "Comprobando procesador", "cpu"),
            ("RAM", "Comprobando memoria RAM", "ram"),
            ("GPU", "Comprobando tarjeta gráfica", "gpu"),
            ("Placa base", "Comprobando placa base", "placa_base"),
            ("Almacenamiento", "Comprobando almacenamiento", "almacenamiento"),
            ("Ventiladores", "Comprobando ventiladores", "ventiladores"),
            ("Periféricos", "Comprobando puertos y periféricos", "usb"),
            ("Red", "Comprobando adaptador de red", "red"),
            ("Resultado", "Evaluando resultados", None),
        ]
        self.fallas_simuladas: set = set()
        self.precauciones_simuladas: set = set()
        self.resultado: Resultado = Resultado.OK

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
        self.resultado = Resultado.OK

    def _aplicar_estados_simulados(self):
        for cid in self.fallas_simuladas:
            c = self.engine.get_componente(cid)
            if c:
                c.set_estado(Estado.FALLA, f"{c.nombre} con falla simulada")
        for cid in self.precauciones_simuladas:
            c = self.engine.get_componente(cid)
            if c:
                c.set_estado(Estado.PRECAUCIÓN, f"{c.nombre} requiere atención")

    def ejecutar(self) -> list[tuple[str, str, Estado]]:
        self._aplicar_estados_simulados()
        eventos: list[tuple[str, str, Estado]] = []
        self.resultado = Resultado.OK

        for nombre, msg, cid in self.pasos:
            estado = Estado.FUNCIONAL
            if cid:
                c = self.engine.get_componente(cid)
                if c:
                    estado = c.estado
                    if c.mensaje:
                        msg = c.mensaje

            eventos.append((nombre, msg, estado))

            if estado == Estado.FALLA and cid:
                c = self.engine.get_componente(cid)
                if c and c.prioridad == "CRITICO":
                    # Un componente crítico impide continuar: el SO no arranca.
                    self.resultado = Resultado.FALLO_CRITICO
                    break
                self.resultado = Resultado.ADVERTENCIA
            elif estado == Estado.PRECAUCIÓN:
                self.resultado = Resultado.ADVERTENCIA

        return eventos
