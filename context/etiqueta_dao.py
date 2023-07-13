from cursor import Cursor
from etiqueta import Etiqueta


class EtiquetaDao:
    """
    Contiene los métodos que permiten ejecutar el CRUD sobre la tabla etiquetas de la base de datos
    DAO (Data Access Object)
    CRUD (Create-Read-Update-Delete)
    """
    _SELECCIONAR = 'SELECT * FROM etiquetas ORDER BY id_etiqueta'
    _INSERTAR = 'INSERT INTO etiquetas(nombre) VALUES(%s)'
    _ACTUALIZAR = 'UPDATE etiquetas SET nombre=%s WHERE id_etiqueta=%s'
    _ELIMINAR = 'DELETE FROM etiquetas WHERE id_etiqueta=%s'

    @classmethod
    def seleccionar(cls):
        with Cursor() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            etiquetas = []
            for reg in registros:
                etiquetas.append(Etiqueta(reg[0], reg[1]))
            return etiquetas

    @classmethod
    def insertar(cls, etiqueta: Etiqueta):
        with Cursor() as cursor:
            values = (etiqueta.nombre,)
            cursor.execute(cls._INSERTAR, values)
            print(f'Etiqueta Insertada: {etiqueta}')
            return cursor.rowcount

    @classmethod
    def actualizar(cls, etiqueta: Etiqueta):
        with Cursor() as cursor:
            values = (etiqueta.nombre, etiqueta.id_etiqueta,)
            cursor.execute(cls._ACTUALIZAR, values)
            print(f'Etiqueta Actualizada: {etiqueta}')
            return cursor.rowcount

    @classmethod
    def eliminar(cls, etiqueta: Etiqueta):
        with Cursor() as cursor:
            values = (etiqueta.id_etiqueta,)
            cursor.execute(cls._ELIMINAR, values)
            print(f'Etiqueta eliminada: {etiqueta}')
            return cursor.rowcount
