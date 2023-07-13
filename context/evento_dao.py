class Evento:
    def __init__(self, id_evento: int, titulo: str, descripcion: str, fecha_hora: str, etiquetas, recordatorio,
                 importancia):
        self._id_evento = id_evento
        self._titulo = titulo
        self._descripcion = descripcion
        self._fecha_hora = fecha_hora
        self._etiquetas = etiquetas
        self._recordatorio = recordatorio,
        self._importancia = importancia

    @property
    def id_evento(self):
        return self._id_evento

    @id_evento.setter
    def id_evento(self, value):
        self._id_evento = value

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, value):
        self._titulo = value

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value):
        self._descripcion = value

    @property
    def fecha_hora(self):
        return self._fecha_hora

    @fecha_hora.setter
    def fecha_hora(self, value):
        self._fecha_hora = value

    @property
    def etiquetas(self):
        return self._etiquetas

    @etiquetas.setter
    def etiquetas(self, value):
        self._etiquetas = value

    @property
    def recordatorio(self):
        return self._recordatorio

    @recordatorio.setter
    def recordatorio(self, value):
        self._recordatorio = value

    @property
    def importancia(self):
        return self._importancia

    @importancia.setter
    def importancia(self, value):
        self._importancia = value

    def __str__(self):
        return f'''
                    Id evento: {self._id_evento}, Titulo: {self._titulo},
                    Descripción: {self._descripcion}, Fecha y hora: {self._fecha_hora},
                    Etiquetas: {self._etiquetas}, Recordatorio: {self._recordatorio},
                    Importancia: {self._importancia}
                '''
