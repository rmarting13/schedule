from mysql import connector as con
class Connection:
    """
    Clase encargada de la creación del pool de conexiones con la base de datos
    """
    _DATABASE = 'calendario'
    _USERNAME = 'admin'
    _PASSWORD = 'admin'
    _DB_PORT = '3306'
    _HOST = 'localhost'
    _conn = None

    @classmethod
    def get_connection(cls):
        if cls._conn is None:
            try:
                cls._conn = con.connect(
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    host=cls._HOST,
                    port=cls._DB_PORT,
                    database=cls._DATABASE,
                )
                print(f'Creación del pool exitosa: {cls._conn}')
                return cls._conn
            except Exception as e:
                print(f'Ocurrió un error: {e}')
        else:
            return cls._conn


if __name__ == '__main__':
    # Al ser métodos de clase podemos llamarlos sin necesidad de instanciarlos.
    Connection.get_connection()

