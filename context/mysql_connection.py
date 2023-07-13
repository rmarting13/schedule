from mysql.connector import pooling
class Conexion:
    """
    Clase encargada de la creación del pool de conexiones con la base de datos
    """
    _DATABASE = 'calendario'
    _USERNAME = 'admin'
    _PASSWORD = 'admin'
    _DB_PORT = '3306'
    _HOST = 'localhost'
    _MAX_CON = 5 # define el máximo de objetos de conexión en memoria
    _pool = None

    @classmethod
    def obtenerPool(cls):
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    host=cls._HOST,
                    port=cls._DB_PORT,
                    database=cls._DATABASE,
                    pool_size=cls._MAX_CON
                )
                print(f'Creación del pool exitosa: {cls._pool}')
                return cls._pool
            except Exception as e:
                print(f'Ocurrió un error: {e}')
        else:
            return cls._pool

    @classmethod
    def obtenerConexion(cls):
        # el método get_connection() devuelve un objeto de conexión del pool de conexiones.
        conexion = cls.obtenerPool().get_connection()
        print(f'Conexión obtenida del pool: {conexion}')
        return conexion


if __name__ == '__main__':
    # Al ser métodos de clase podemos llamarlos sin necesidad de instanciarlos.
    Conexion.obtenerConexion()

