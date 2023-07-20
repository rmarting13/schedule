from db_context.mysql_connection import Connection


class Cursor:
    """
    Clase encargada de administrar el objeto cursor() del pool de conexiones, y las conexiones
    individuales del pool (liberar las conexiones en deshuso y regresarlas al pool de conexiones)
    """
    def __init__(self):
        self._conn = None
        self._cursor = None

# Los siguientes métodos __enter__ y __exit__ se encargan de abrir y cerrar los recursos cuando
# se ejecuta una sintaxis WITH para usar una instancia de esta clase
    def __enter__(self):
        """
        Se ejecuta al iniciar la sentencia WITH
        :return:
        """
        print('Inicio del método with __enter__')
        self._conn = Connection.get_connection()
        self._cursor = self._conn.cursor()
        return self._cursor

    # exc_type = Tipo de excepción
    # exc_val = Valor de la exepción (contenido)
    # exc_tb = Exception traceback o traza de la excepción
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Se ejecuta al finalizar la sentencia WITH
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        print('Se ejecuta el método with __exit__')
        if exc_val: # preguntamos si el valor de la excepción es diferente de None (no está vacía)
            # si no está vacío significa que ocurrió una excepción y debemos hacer un rollback:
            self._conn.rollback()
            # a continuación enviamos a nuestro log los detalles de la excepción:
            print(f'Ocurrió un error: {exc_type} {exc_val} {exc_tb}')
        else:
            # Si no ocurrió ninguna excepción  entonces mandamos a hacer el commit a la base de datos
            self._conn.commit()
            print('Commit de la transacción.')
        self._cursor.close() # Finalizada la transacción cerramos el cursor


if __name__ == '__main__':
    with Cursor() as cursor:
        print('Dentro del bloque with')
