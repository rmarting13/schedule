from cursor import Cursor
from importancia import Importancia


class ImportanciaDao:
    """
    Contiene los métodos que permiten ejecutar el CRUD sobre la tabla importancias de la base de datos
    DAO (Data Acces Object)
    CRUD (Create-Read-Update-Delete)
    """
    _SELECCIONAR = 'SELECT * FROM importancias ORDER BY id_importancia'
    _INSERTAR = 'INSERT INTO importancias(nombre) VALUES(%s)'
    _ACTUALIZAR = 'UPDATE importancias SET nombre=%s WHERE id_importancia=%s'
    _ELIMINAR = 'DELETE FROM importancias WHERE id_importancia=%s'

    @classmethod
    def seleccionar(cls):
        with Cursor() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            importancias = []
            for reg in registros:
                importancias.append(Importancia(reg[0], reg[1]))
    @classmethod
    def insertar(cls, importancia: Importancia):
        with Cursor() as cursor:
            values = (importancia.nombre,)
            cursor.execute(cls._INSERTAR, values)
            print(f'Importancia Insertada: {importancia}')
            return cursor.rowcount

    @classmethod
    def actualizar(cls, importancia: Importancia):
        with Cursor() as cursor:
            values = (importancia.nombre, importancia.id_importancia,)
            cursor.execute(cls._ACTUALIZAR, values)
            print(f'Importancia Actualizada: {importancia}')
            return cursor.rowcount

    @classmethod
    def eliminar(cls, importancia: Importancia):
        with Cursor() as cursor:
            values = (importancia.id_importancia,)
            cursor.execute(cls._ELIMINAR, values)
            print(f'Importancia eliminada: {importancia}')

