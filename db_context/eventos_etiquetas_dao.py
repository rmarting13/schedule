from db_context.cursor import Cursor


class EventoEtiquetaDao:
    """
    Contiene los métodos que permiten ejecutar el CRUD sobre la tabla etiquetas de la base de datos
    DAO (Data Access Object)
    CRUD (Create-Read-Update-Delete)
    """
    _SELECCIONAR = 'SELECT id_evento, id_etiqueta FROM eventos_etiquetas WHERE id_evento = %s'
    _INSERTAR = 'INSERT INTO evenetos_etiquetas(id_evento, id_etiqueta) VALUES(%s, %s)'
    _ACTUALIZAR = 'UPDATE etiquetas SET id_evento=%s, id_etiqueta=%s WHERE id_evento_etiqueta=%s'
    _ELIMINAR_ID = 'DELETE FROM eventos_etiquetas WHERE id_evento_etiqueta=%s'
    _ELIMINAR_ID_EVENTO_ID_ETIQUETA = 'DELETE FROM eventos_etiquetas WHERE id_evento=%s AND id_etiqueta=%s'

    @classmethod
    def seleccionar(cls, id_evento):
        with Cursor() as cursor:
            cursor.execute(cls._SELECCIONAR, id_evento)
            registros = cursor.fetchall()
            return registros

    @classmethod
    def insertar(cls, id_evento, id_etiqueta):
        with Cursor() as cursor:
            values = (id_evento, id_etiqueta)
            cursor.execute(cls._INSERTAR, values)
            print(f'Relación evento-etiqueta insertada: {(id_evento,id_etiqueta)}')
            return cursor.rowcount

    @classmethod
    def actualizar(cls, id_evento_etiqueta):
        with Cursor() as cursor:
            values = (id_evento_etiqueta,)
            cursor.execute(cls._ACTUALIZAR, values)
            print(f'Relación evento-etiqueta Actualizada: {id_evento_etiqueta}')
            return cursor.rowcount

    @classmethod
    def eliminar(cls, **kwargs):
        with Cursor() as cursor:
            if kwargs.get('id_evento_etiqueta', None):
                cursor.execute(cls._ELIMINAR_ID, kwargs.get('id_evento_etiqueta'))
            elif kwargs.get('id_evento', None) and kwargs.get('id_etiqueta', None):
                values = (kwargs.get('id_etiqueta', None), kwargs.get('id_evento'),)
                cursor.execute(cls._ELIMINAR_ID_EVENTO_ID_ETIQUETA, values)
            return cursor.lastrowid


if __name__ == '__main__':
    pass
