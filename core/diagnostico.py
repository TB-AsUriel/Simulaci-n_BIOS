from .componentes import Estado, Componente

class Diagnostico:
    def evaluar(self, componente: Componente) -> Estado:
        # Por defecto, todo funcional
        return Estado.FUNCIONAL

    def evaluar_todos(self, componentes):
        resultados = {}
        for c in componentes:
            resultados[c.id] = self.evaluar(c)
        return resultados
