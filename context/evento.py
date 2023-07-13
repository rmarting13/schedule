class Evento:
    def __init__(self, titulo, fecha_hora, duracion, id_importancia,
                 descripcion=None,  recordatorio=None, id_evento=None):
        self._id_evento = id_evento
        self._titulo = titulo
        self._descripcion = descripcion
        self._fecha_hora = fecha_hora
        self._duracion = duracion
        self._recordatorio = recordatorio
        self._id_importancia = id_importancia

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
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, value):
        self._duracion = value

    @property
    def recordatorio(self):
        return self._recordatorio

    @recordatorio.setter
    def recordatorio(self, value):
        self._recordatorio = value

    @property
    def id_importancia(self):
        return self._id_importancia

    @id_importancia.setter
    def id_importancia(self, value):
        self._id_importancia = value

    def __str__(self):
        return f'''
                    Id evento: {self._id_evento}, Titulo: {self._titulo},
                    Descripción: {self._descripcion}, Fecha y hora: {self._fecha_hora},
                    Duración: {self._duracion} minutos,
                    Recordatorio: {self._recordatorio}, Importancia: {self._id_importancia}
                '''
