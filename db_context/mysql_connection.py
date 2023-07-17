from mysql import connector as con
from mysql.connector import errorcode
import sys
import os

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
    def create_database(cls):
        try:
            cls._conn = con.connect(
                user=cls._USERNAME,
                password=cls._PASSWORD,
                host=cls._HOST,
                port=cls._DB_PORT,
            )
            with cls._conn.cursor() as cursor:
                with open('db_context/db_backup.sql', 'r') as sql_file:
                    result_iterator = cursor.execute(sql_file.read(), multi=True)
                    for res in result_iterator:
                        print("Running query: ", res)  # Will print out a short representation of the query
                        print(f"Affected {res.rowcount} rows")
        except con.Error as err:
            print(err)
            sys.exit()
        except Exception as e:
            print(f'Ocurrió un error: {e}')
            sys.exit()
        finally:
            cls._conn.close()

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
                print(f'Conexión exitosa: {cls._conn}')
                return cls._conn
            except con.Error as err:
                if err.errno == errorcode.ER_BAD_DB_ERROR:
                    cls.create_database()
                    cls._conn = None
                    return cls.get_connection()
                else:
                    print(err)
                    sys.exit()
            except Exception as e:
                print(f'Ocurrió un error: {e}')
                sys.exit()
        else:
            return cls._conn


if __name__ == '__main__':
    # Al ser métodos de clase podemos llamarlos sin necesidad de instanciarlos.
    Connection.get_connection()

