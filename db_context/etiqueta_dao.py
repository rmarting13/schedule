from db_context.cursor import Cursor
from models.etiqueta import Etiqueta


class EtiquetaDao:
    """
    Contiene los métodos que permiten ejecutar el CRUD sobre la tabla etiquetas de la base de datos
    DAO (Data Access Object)
    CRUD (Create-Read-Update-Delete)
    """
    _SELECCIONAR = 'SELECT * FROM etiquetas ORDER BY id_etiqueta'
    _SELECCIONAR_NOMBRE = 'SELECT * FROM etiquetas WHERE nombre LIKE %s ORDER BY nombre'
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
                etiquetas.append(Etiqueta(id_etiqueta=reg[0], nombre=reg[1]))
            return etiquetas

    @classmethod
    def seleccionar_nombre(cls, name):
        with Cursor() as cursor:
            value = '%'+name+'%'
            cursor.execute(cls._SELECCIONAR_NOMBRE, (value,))
            registros = cursor.fetchall()
            etiquetas = []
            for reg in registros:
                etiquetas.append(Etiqueta(id_etiqueta=reg[0], nombre=reg[1]))
            return etiquetas

    @classmethod
    def insertar(cls, etiqueta: Etiqueta):
        with Cursor() as cursor:
            values = (etiqueta.nombre,)
            cursor.execute(cls._INSERTAR, values)
            print(f'Etiqueta Insertada: {etiqueta}')
            return cursor.lastrowid

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

if __name__ == '__main__':
    pass
    # INSERTAR
    # et1 = Etiqueta(nombre='test')
    # insertadas = EtiquetaDao.insertar(et1)
    # print(f'Etiquetas insertadas: {insertadas}')
    # et2 = Etiqueta(nombre='estudiar')
    # insertadas = EtiquetaDao.insertar(et2)
    # print(f'Etiquetas insertadas: {insertadas}')

    #ACTUALIZAR
    # et1 = Etiqueta(id_etiqueta=1, nombre='examen')
    # actualizadas = EtiquetaDao.actualizar(et1)
    # print(f'Etiquetas actualizadas: {actualizadas}')

    #ELIMINAR
    et1 = Etiqueta(id_etiqueta=2, nombre='estudiar')
    eliminadas = EtiquetaDao.eliminar(et1)
    print(f'Etiquetas eliminadas: {eliminadas}')

    #SELECCIONAR
    datos = EtiquetaDao.seleccionar()
    for dato in datos:
       print(dato)
