import mysql.connector
conn = mysql.connector.connect(
    user='admin',
    password='admin',
    host='localhost',
    database='calendario'
)

conn.close()
