from cursor import Cursor
from models.importancia import Importancia


class ImportanciaDao:
    """
    Contiene los métodos que permiten ejecutar el CRUD sobre la tabla importancias de la base de datos
    DAO (Data Access Object)
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
            return importancias
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
            return cursor.rowcount

if __name__ == '__main__':
    pass
    # INSERTAR
    imp1 = Importancia(nombre='NORMAL')
    insertadas = ImportanciaDao.insertar(imp1)
    print(f'Importancias insertadas: {insertadas}')
    # imp2 = Importancia(nombre='IMPORTANTE')
    # insertadas = ImportanciaDao.insertar(imp1)
    # print(f'Importancias insertadas: {insertadas}')

    #ACTUALIZAR
    # imp1 = Importancia(id_importancia=2, nombre='IMPORTANTE')
    # actualizadas = ImportanciaDao.actualizar(imp1)
    # print(f'Importancias actualizadas: {actualizadas}')

    #ELIMINAR
    # imp1 = Importancia(id_importancia=4, nombre='NORMAL')
    # eliminadas = ImportanciaDao.eliminar(imp1)
    # print(f'Importancias eliminadas: {eliminadas}')

    #SELECCIONAR
    datos = ImportanciaDao.seleccionar()
    for dato in datos:
       print(dato)
