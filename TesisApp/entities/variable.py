class Variable:
    def __init__(self, clave, significado):
        self.clave = clave
        self.significado = significado

    def to_dict(self):
        return {
            'clave': self.clave,
            'significado': self.significado,
        }