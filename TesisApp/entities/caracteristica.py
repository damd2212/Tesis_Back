class Caracteristica:
    def __init__(self, clave, significado, porcentaje, respuesta):
        self.clave = clave
        self.significado = significado
        self.porcentaje = porcentaje
        self.respuesta = respuesta

    def to_dict(self):
        return {
            'clave': self.clave,
            'significado': self.significado,
            'porcentaje': self.porcentaje,
            'respuesta': self.respuesta
        }
