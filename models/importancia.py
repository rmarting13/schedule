class Importancia:
    def __init__(self, nombre: str, id_importancia=None):
        self._id_importancia = id_importancia
        self._nombre = nombre

    @property
    def id_importancia(self):
        return self._id_importancia

    @id_importancia.setter
    def id_importancia(self, value):
        self._id_importancia = value

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    def __str__(self):
        return f'''
                Id Importancia: {self._id_importancia},
                Nombre: {self._nombre}
                '''
