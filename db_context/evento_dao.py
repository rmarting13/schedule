from cursor import Cursor
from models.evento import Evento


class EventoDao:
    """
    Contiene los métodos que permiten ejecutar el CRUD sobre la tabla personas de la base de datos
    DAO (Data Access Object)
    CRUD (Create-Read-Update-Delete)
    """
    _SELECCIONAR = 'SELECT * FROM eventos ORDER BY id_evento'
    _INSERTAR = 'INSERT INTO eventos(titulo, fecha_hora, descripcion, duracion, recordatorio, id_importancia) VALUES(' \
                '%s, %s, %s, %s, %s, %s)'
    _ACTUALIZAR = 'UPDATE eventos SET titulo=%s, fecha_hora=%s, descripcion=%s, duracion=%s, recordatorio=%s, ' \
                  'id_importancia=%s WHERE id_evento=%s'
    _ELIMINAR = 'DELETE FROM eventos WHERE id_evento=%s'

    @classmethod
    def seleccionar(cls):
        with Cursor() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            eventos = []
            for reg in registros:
                eventos.append(Evento(
                    id_evento=reg[0],
                    titulo=reg[1],
                    fecha_hora=reg[2],
                    descripcion=reg[3],
                    duracion=reg[4],
                    recordatorio=reg[5],
                    id_importancia=reg[6])
                )
            return eventos

    @classmethod
    def insertar(cls, evento: Evento):
        with Cursor() as cursor:
            values = (
                evento.titulo,
                evento.fecha_hora,
                evento.descripcion,
                evento.duracion,
                evento.recordatorio,
                evento.id_importancia
            )
            cursor.execute(cls._INSERTAR, values)
            print(f'Evento Insertado: {evento}')
            return cursor.rowcount

    @classmethod
    def actualizar(cls, evento: Evento):
        with Cursor() as cursor:
            values = (
                evento.titulo,
                evento.fecha_hora,
                evento.descripcion,
                evento.duracion,
                evento.recordatorio,
                evento.id_importancia,
                evento.id_evento
            )
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
    # evento1 = Evento(
    #     titulo='Desafío de Algorítmica',
    #     fecha_hora='2023-07-14 9:00:00',
    #     duracion=60,
    #     id_importancia=1
    # )
    # insertados = EventoDao.insertar(evento1)
    # print(f'Eventos insertados: {insertados}')

    # evento2 = Evento(
    #     titulo='Entrega del TP1.4 de Programación 2',
    #     descripcion='''La sección de entrega en la plataforma abre este viernes 14/07 y cierra el lunes 17/07''',
    #     fecha_hora='2023-07-17 23:59:59',
    #     duracion=30,
    #     recordatorio='2023-07-14 8:30:00',
    #     id_importancia=2
    # )
    # insertadas = EventoDao.insertar(evento2)
    # print(f'Eventos insertados: {insertadas}')

    #ACTUALIZAR
    evento1 = Evento(
        titulo='Desafío de Algorítmica',
        fecha_hora='2023-07-14 9:00:00',
        descripcion='Estudiar para el examen.',
        recordatorio='2023-07-13 15:00:00',
        duracion=60,
        id_importancia=1,
        id_evento=3
    )
    actualizados = EventoDao.actualizar(evento1)
    print(f'Eventos actualizados: {actualizados}')

    #ELIMINAR
    # evento1 = Evento(
    #     id_evento=2,
    #     titulo='Desafío de Algorítmica',
    #     fecha_hora='2023-07-14 9:00:00',
    #     duracion=60,
    #     id_importancia=1
    # )
    # eliminados = EventoDao.eliminar(evento1)
    # print(f'Eventos eliminados: {eliminados}')

    #SELECCIONAR
    datos = EventoDao.seleccionar()
    for dato in datos:
        print(dato)
