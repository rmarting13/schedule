import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, END, messagebox
from datetime import datetime
from calendar import Calendar
from tkcalendar import Calendar as tkCalendar
from Archivo import BaseDeDatos

class Calendario(Calendar):
    """Clase que representa un calendario."""

    def __init__(self):
        super().__init__(firstweekday=6)
        self.__strMesLargo = (
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
        'Diciembre')
        self.__strMesCorto = ('Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic')
        self.__strDiaLargo = ('Lúnes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo')
        self.__strDiaCorto = ('Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'Do')

    def nombreDelMes(self, mes, tipo=0):
        """Retorna un string indicando el nombre del Mes de acuerdo al número ingresado por parámetro. El parámetro tipo
        indica si el nombre es formato largo o formato corto."""
        if tipo == 0:
            cad = self.__strMesCorto[mes - 1]
        else:
            cad = self.__strMesLargo[mes - 1]
        return cad

    def nombreDelDia(self, dia, tipo=0):
        """Retorna un string indicando el nombre del Día de la semana, de acuerdo al número ingresado por parámetro.
        El parámetro tipo indica si el nombre es formato largo o formato corto."""
        if tipo == 0:
            cad = self.__strDiaCorto[dia - 1]
        else:
            cad = self.__strDiaLargo[dia - 1]
        return cad

    def matrizMensual(self, anio, mes):
        """Retorna una matriz con los días del mes y año pasados por parámetro. Cada fila de la matriz
        representa una semana, cuyos días son valores enteros y los días fuera del mes se representan con un 0."""
        return self.monthdatescalendar(anio, mes)

    def listaDeSemanas(self, anio, mes):
        """"Retorna una lista cuyos elementos son listas de valores del tipo datetime.date(), las cuales
        representan cada semana del mes. La primer y ultima lista puede contener los ultimos días del mes
        anterior y/o los primeros días posterior que se incluyen en la primer y ultima semana respectivamente."""
        iterableDias = list(self.itermonthdates(anio, mes))
        listaSemanas = []
        ini = 0
        fin = 7
        for i in range(6):
            if len(iterableDias[ini:fin]) != 0:
                listaSemanas.append(iterableDias[ini:fin])
                ini += 7
                fin += 7
        return listaSemanas


if __name__ == '__main__':
    cal = Calendario()
    days = cal.listaDeSemanas(anio=2023, mes=7)
    for day in days:
        print(day)