import csv
from datetime import datetime
class BaseDeDatos:
    """Clase que representa un archivo .csv y permite leer y escribir datos en el mismo."""
    def __init__(self, ruta):
        self.__archivo = ruta
        self.__encabezado=("ID","TITULO","FECHA","HORA","DESCRIPCION","IMPORTANCIA",'DURACION','RECORDATORIO',"ETIQUETA")

    def grabarDato(self, dato):
        """Recibe por parámetro un diccionario que contiene los campos (claves) y contenido (valores) de un
        evento, y lo escribe en el archivo csv."""
        with open (self.__archivo, "r+", newline="") as archivo: 
            lector = list(csv.DictReader(archivo, fieldnames=self.__encabezado,delimiter=",")) 
            if dato['ID'] == '':
                listaID = list(map(lambda x: int(x['ID']),lector))
                listaID.sort()
                id = listaID.pop() + 1
                escritor = csv.DictWriter(archivo, fieldnames=self.__encabezado,delimiter=",")
                dato.update({'ID': id})
                escritor.writerow(dato)
            else:
                listaID = list(map(lambda x: x['ID'],lector))
                ind = listaID.index(dato['ID'])
                lector[ind].update(dato)
                self.grabarArchivoCompleto(lector)

    def grabarArchivoCompleto(self,datos):
        """Recibe por parámetro una colección de diccionarios que contienen los datos de eventos, y lo escribe
        en el archivo csv."""
        with open (self.__archivo, "w", newline="") as archivo:
            escritor= csv.DictWriter(archivo, fieldnames=self.__encabezado)
            escritor.writerows(datos)

    def borrarEvento(self,datos):
        """Recibe por parámetro un diccionario que contiene un evento, obtiene su ID y lo elimina del arhivo."""
        lista = self.leerArchivoCompleto()
        evento = list(filter(lambda x: x['ID']==datos[0], lista))
        lista.remove(evento[0])
        self.grabarArchivoCompleto(lista)
        

    def leerArchivoCompleto(self):
        """Retorna una lista de diccionarios que representa todas las filas escritas en el archivo csv."""
        with open(self.__archivo, "r", newline="") as archivo:
            lista=list(csv.DictReader(archivo, fieldnames=self.__encabezado, delimiter=","))
        lista.sort(key=lambda x: datetime.strptime(x['HORA'], "%H:%M"))
        lista.sort(key=lambda x: datetime.strptime(x['FECHA'], "%d/%m/%Y"))
        return lista

    def leerDatosFiltrados(self,filtro):
        """Recibe por parámetro un diccionario que contiene las claves y valores para filtrar el archivo, luego
        retorna una lista con los eventos filtrados."""
        with open(self.__archivo, "r", newline="") as archivo:
            lista=list(csv.DictReader(archivo, fieldnames=self.__encabezado, delimiter=","))
            filtrada = []; resultado = []
            if 'FECHA' in filtro.keys():
                filtrada.append(filter(lambda x: x['FECHA'] == filtro['FECHA'], lista))
            if 'TITULO' in filtro.keys():
                filtrada.append(filter(lambda x: x['TITULO'].lower() == filtro['TITULO'].lower(), lista))
            if 'ETIQUETA' in filtro.keys():
                for row in lista:
                    tag = row['ETIQUETA'].split(sep=', ')
                    tag = map(lambda x: x.lower(), tag)
                    row.update({'ETIQUETA':tag})
                filtrada.append(filter(lambda x: filtro['ETIQUETA'].lower() in x['ETIQUETA'], lista))
            if len(filtrada) > 1:
                for evento in filtrada[0]:
                    if evento in filtrada[1]:
                        resultado.append(evento)
            else:
                resultado.extend(filtrada[0])
            resultado.sort(key=lambda x: datetime.strptime(x['HORA'], "%H:%M"))
            resultado.sort(key=lambda x: datetime.strptime(x['FECHA'], "%d/%m/%Y"))
        return resultado
    
    def filtrarPorID(self,id):
        """Recibe el valor de la clave ID para filtrar el archivo, luego retorna el evento correspondiente a
        la clave ID filtrada."""
        with open(self.__archivo, "r", newline="") as archivo:
            lista=list(csv.DictReader(archivo, fieldnames=self.__encabezado, delimiter=","))
            listaID = list(map(lambda x: x['ID'],lista))
            ind = listaID.index(id)
        return lista[ind]

    def mapearFechas(self):
        """Retorna una lista de tuplas (fecha , ID), en formato string correspondientes a todos los eventos del archivo."""
        with open(self.__archivo, "r", newline="") as archivo:
            lista=list(csv.DictReader(archivo, fieldnames=self.__encabezado, delimiter=","))
            fechas = list(map(lambda x: (x['ID'],x['FECHA']),lista))
        return fechas

    def mapearFechasYHoras(self):
        """Retorna una lista de tuplas (fecha, hora) en formato string, correspondientes a todos los eventos del archivo."""
        with open(self.__archivo, "r", newline="") as archivo:
            lista=list(csv.DictReader(archivo, fieldnames=self.__encabezado, delimiter=","))
            fechas = list(map(lambda x: x['FECHA'],lista))
            horas = list(map(lambda x: x['HORA'],lista))
        return list(map(lambda x,y: (x,y),fechas,horas))
    
            

