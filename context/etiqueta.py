class Etiqueta:
    def __init__(self, id_etiqueta: int, nombre: str):
        self._id_etiqueta = id_etiqueta
        self._nombre = nombre

    @property
    def id_etiqueta(self):
        return self._id_etiqueta

    @id_etiqueta.setter
    def id_etiqueta(self, value):
        self._id_etiqueta = value

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    def __str__(self):
        return f'''
                Id Etiqueta: {self._id_etiqueta},
                Nombre: {self._nombre}
                '''
