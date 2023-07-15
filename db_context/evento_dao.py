from db_context.cursor import Cursor
from models.evento import Evento


class EventoDao:
    """
    Contiene los métodos que permiten ejecutar el CRUD sobre la tabla personas de la base de datos
    DAO (Data Access Object)
    CRUD (Create-Read-Update-Delete)
    """
    _LAST_INSERT_ID = 'SELECT LAST_INSERT_ID() from eventos;'
    _SELECCIONAR_TODO = 'SELECT ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, '\
                        'ev.recordatorio, im.nombre, GROUP_CONCAT(et.nombre) AS "etiquetas" FROM eventos ev '\
                        'LEFT JOIN eventos_etiquetas ee ON ev.id_evento = ee.id_evento '\
                        'LEFT JOIN etiquetas et ON ee.id_etiqueta = et.id_etiqueta '\
                        'LEFT JOIN importancias im ON ev.id_importancia = im.id_importancia '\
                        'GROUP BY ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, ev.recordatorio '\
                        'ORDER BY fecha_hora DESC;'
    _SELECCIONAR_ID = 'SELECT ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, '\
                      'ev.recordatorio, ev.id_importancia, GROUP_CONCAT(et.nombre) AS "etiquetas" FROM eventos ev '\
                      'LEFT JOIN eventos_etiquetas ee ON ev.id_evento = ee.id_evento '\
                      'LEFT JOIN etiquetas et ON ee.id_etiqueta = et.id_etiqueta '\
                      'WHERE ev.id_evento = %s '\
                      'GROUP BY ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, '\
                      'ev.recordatorio ORDER BY fecha_hora DESC;'
    _SELECCIONAR_ETIQUETA = 'SELECT ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, '\
                            'ev.recordatorio, im.nombre, GROUP_CONCAT(et.nombre) AS "etiquetas" FROM eventos ev '\
                            'INNER JOIN eventos_etiquetas ee ON ev.id_evento = ee.id_evento '\
                            'INNER JOIN etiquetas et ON ee.id_etiqueta = et.id_etiqueta '\
                            'INNER JOIN importancias im ON ev.id_importancia = im.id_importancia '\
                            'WHERE et.nombre LIKE %s'\
                            'GROUP BY ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, '\
                            'ev.recordatorio ORDER BY fecha_hora DESC;'
    _SELECCIONAR_TITULO = 'SELECT ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, '\
                          'ev.recordatorio, im.nombre, GROUP_CONCAT(et.nombre) AS "etiquetas" FROM eventos ev '\
                          'LEFT JOIN eventos_etiquetas ee ON ev.id_evento = ee.id_evento '\
                          'LEFT JOIN etiquetas et ON ee.id_etiqueta = et.id_etiqueta '\
                          'LEFT JOIN importancias im ON ev.id_importancia = im.id_importancia '\
                          'WHERE ev.titulo LIKE %s'\
                          'GROUP BY ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, '\
                          'ev.recordatorio ORDER BY fecha_hora DESC;'
    _SELECCIONAR_FECHA_HORA = 'SELECT * FROM eventos WHERE fecha_hora = %s;'
    _SELECCIONAR_FECHA = 'SELECT id_evento, titulo, fecha_hora, id_importancia FROM eventos WHERE fecha_hora LIKE %s ORDER BY fecha_hora;'
    _SELECCIONAR_TITULO_ETIQUETA = 'SELECT ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, ' \
                                   'ev.recordatorio, im.nombre, GROUP_CONCAT(et.nombre) AS "etiquetas" FROM eventos ev ' \
                                   'LEFT JOIN eventos_etiquetas ee ON ev.id_evento = ee.id_evento ' \
                                   'LEFT JOIN etiquetas et ON ee.id_etiqueta = et.id_etiqueta ' \
                                   'LEFT JOIN importancias im ON ev.id_importancia = im.id_importancia ' \
                                   'WHERE ev.titulo LIKE %s AND et.nombre LIKE %s' \
                                   'GROUP BY ev.id_evento, ev.titulo, ev.fecha_hora, ev.descripcion, ev.duracion, ' \
                                   'ev.recordatorio ORDER BY fecha_hora DESC;'
    _INSERTAR = 'INSERT INTO eventos(titulo, fecha_hora, descripcion, duracion, recordatorio, id_importancia) VALUES(' \
                '%s, %s, %s, %s, %s, %s);'
    _ACTUALIZAR = 'UPDATE eventos SET titulo=%s, fecha_hora=%s, descripcion=%s, duracion=%s, recordatorio=%s, ' \
                  'id_importancia=%s WHERE id_evento=%s;'
    _ELIMINAR = 'DELETE FROM eventos WHERE id_evento=%s;'


    @classmethod
    def seleccionar(cls, **kwargs):
        with Cursor() as cursor:
            if kwargs.get('id_evento'):
                values = (kwargs.get('id_evento'),)
                cursor.execute(cls._SELECCIONAR_ID, values)
                reg = cursor.fetchone()
                print(f'Registro = {reg}')
                eventos = Evento(
                            id_evento=reg[0],
                            titulo=reg[1],
                            fecha_hora=reg[2],
                            descripcion=reg[3],
                            duracion=reg[4],
                            recordatorio=reg[5],
                            id_importancia=reg[6],
                            etiquetas=reg[7]
                        )
            else:
                if kwargs.get('titulo') and kwargs.get('etiqueta'):
                    titulo = '%' + kwargs.get('titulo') + '%'
                    etiqueta = '%' + kwargs.get('etiqueta') + '%'
                    values = (titulo, etiqueta)
                    cursor.execute(cls._SELECCIONAR_TITULO_ETIQUETA, values)
                    registros = cursor.fetchall()
                elif kwargs.get('titulo'):
                    values = ('%'+kwargs.get('titulo')+'%', )
                    cursor.execute(cls._SELECCIONAR_TITULO, values)
                    registros = cursor.fetchall()
                elif kwargs.get('etiqueta'):
                    values = ('%'+kwargs.get('etiqueta')+'%', )
                    cursor.execute(cls._SELECCIONAR_ETIQUETA, values)
                    registros = cursor.fetchall()
                else:
                    cursor.execute(cls._SELECCIONAR_TODO)
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
                        id_importancia=reg[6],
                        etiquetas=reg[7]
                        )
                    )
            return eventos

    @classmethod
    # def seleccionar_id(cls, id_evento):
    #     with Cursor() as cursor:
    #         cursor.execute(cls._SELECCIONAR_ID, id_evento)
    #         reg = cursor.fetchone()
    #         evento = Evento(
    #                 id_evento=reg[0],
    #                 titulo=reg[1],
    #                 fecha_hora=reg[2],
    #                 descripcion=reg[3],
    #                 duracion=reg[4],
    #                 recordatorio=reg[5],
    #                 id_importancia=reg[6],
    #                 etiquetas=reg[7]
    #         )
    #         return evento

    @classmethod
    def eixiste_fecha_hora(cls, fecha_hora):
        print(fecha_hora)
        with Cursor() as cursor:
            cursor.execute(cls._SELECCIONAR_FECHA_HORA, (fecha_hora,))
            cursor.fetchone()
            return cursor.rowcount > 0

    @classmethod
    def seleccionar_fecha(cls, fecha):
        with Cursor() as cursor:
            value = (fecha+'%',)
            cursor.execute(cls._SELECCIONAR_FECHA, value)
            registros = cursor.fetchall()
            eventos = []
            for reg in registros:
                eventos.append(Evento(
                        id_evento=reg[0],
                        titulo=reg[1],
                        fecha_hora=reg[2],
                        id_importancia=reg[3],
                    )
                )
            return eventos

    @classmethod
    # def seleccionar_titulo(cls, order_by=None):
    #     with Cursor() as cursor:
    #         cursor.execute(cls._SELECCIONAR_TITULO)
    #         registros = cursor.fetchall()
    #         eventos = []
    #         for reg in registros:
    #             eventos.append(Evento(
    #                 id_evento=reg[0],
    #                 titulo=reg[1],
    #                 fecha_hora=reg[2],
    #                 descripcion=reg[3],
    #                 duracion=reg[4],
    #                 recordatorio=reg[5],
    #                 id_importancia=reg[6],
    #                 etiquetas=reg[7]
    #                 )
    #             )
    #         return eventos

    @classmethod
    # def seleccionar_titulo_etiqueta(cls, **filters):
    #     with Cursor() as cursor:
    #         titulo = '%'+filters.get('titulo')+'%'
    #         etiqueta = '%'+filters.get('etiqueta')+'%'
    #         values = (titulo, etiqueta)
    #         cursor.execute(cls._SELECCIONAR_TITULO_ETIQUETA, values)
    #         registros = cursor.fetchall()
    #         eventos = []
    #         for reg in registros:
    #             eventos.append(Evento(
    #                 id_evento=reg[0],
    #                 titulo=reg[1],
    #                 fecha_hora=reg[2],
    #                 descripcion=reg[3],
    #                 duracion=reg[4],
    #                 recordatorio=reg[5],
    #                 id_importancia=reg[6],
    #                 etiquetas=reg[7]
    #             )
    #             )
    #         return eventos

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
            return cursor.lastrowid

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
            return cursor.lastrowid

    @classmethod
    def eliminar(cls, evento: Evento=None, id_evento=None):
        with Cursor() as cursor:
            if evento:
                values = (evento.id_evento,)
            else:
                values = (id_evento,)
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
    # evento1 = Evento(
    #     titulo='Desafío de Algorítmica',
    #     fecha_hora='2023-07-14 9:00:00',
    #     descripcion='Estudiar para el examen.',
    #     recordatorio='2023-07-13 15:00:00',
    #     duracion=60,
    #     id_importancia=1,
    #     id_evento=3
    # )
    # actualizados = EventoDao.actualizar(evento1)
    # print(f'Eventos actualizados: {actualizados}')

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
    datos = EventoDao.seleccionar_todos()
    for dato in datos:
        print(dato)
