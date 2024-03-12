class Caracteristica:
    def __init__(self, clave, significado, porcentaje):
        self.clave = clave
        self.significado = significado
        self.porcentaje = porcentaje

    def to_dict(self):
        return {
            'clave': self.clave,
            'significado': self.significado,
            'porcentaje': self.porcentaje
        }
