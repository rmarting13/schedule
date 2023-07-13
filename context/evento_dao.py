from cursor import Cursor
from evento import Evento


class EventoDao:
    """
    Contiene los métodos que permiten ejecutar el CRUD sobre la tabla personas de la base de datos
    DAO (Data Acces Object)
    CRUD (Create-Read-Update-Delete)
    """
    _SELECCIONAR = 'SELECT * FROM eventos ORDER BY id_evento'
    _INSERTAR = 'INSERT INTO eventos(titulo, descripcion, fecha_hora, etiquetas, recordatorio, importancia) VALUES(' \
                '%s, %s, %s, %s, %s, %s)'
    _ACTUALIZAR = 'UPDATE eventos SET titulo=%s, descripcion=%s, fecha_hora=%s WHERE id_evento=%s'
    _ELIMINAR = 'DELETE FROM eventos WHERE id_evento=%s'

    @classmethod
    def seleccionar(cls):
        with Cursor() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            eventos = []
            for reg in registros:
                eventos.append(Evento(reg[0], reg[1], reg[2], reg[3], reg[4], reg[5], reg[6]))
    @classmethod
    def insertar(cls, evento: Evento):
        with Cursor() as cursor:
            values = (evento.titulo, evento.descripcion, evento.fecha_hora)
            cursor.execute(cls._INSERTAR, values)
            print(f'Evento Insertado: {evento}')
            return cursor.rowcount

    @classmethod
    def actualizar(cls, evento: Evento):
        with Cursor() as cursor:
            values = (evento.titulo, evento.descripcion, evento.fecha_hora, evento.id_evento)
            cursor.execute(cls._ACTUALIZAR, values)
            print(f'Evento Actualizado: {evento}')
            return cursor.rowcount

    @classmethod
    def eliminar(cls, evento: Evento):
        with Cursor() as cursor:
            values = (evento.id_evento,)
            cursor.execute(cls._ELIMINAR, values)
            print(f'Evento eliminado: {evento}')


if __name__ == '__main__':
    pass
    # INSERTAR
    # persona1 = Persona(nombre='Michael', apellido='Jackson', email='mjson@mail.com')
    # insertadas = EventoDao.insertar(persona1)
    # log.debug(f'Personas insertadas: {insertadas}')
    #
    # #ACTUALIZAR
    # persona1 = Persona(7, 'Angel Esteban', 'Robles', 'aerobles@mail.com')
    # actualizadas = EventoDao.actualizar(persona1)
    # log.debug(f'Personas actualizadas: {actualizadas}')
    #
    # #ELIMINAR
    # persona1 = Persona(9, 'Maria', 'Esparza', 'mesparza@mail.com')
    # eliminadas = EventoDao.eliminar(persona1)
    # log.debug(f'Personas eliminadas: {eliminadas}')
    #
    # #SELECCIONAR
    # datos = EventoDao.seleccionar()
    # for dato in datos:
    #     log.debug(dato)