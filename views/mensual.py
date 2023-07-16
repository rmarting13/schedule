import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, END, messagebox
from datetime import datetime
from calendar import Calendar
from tkcalendar import Calendar as tkCalendar
from Archivo import BaseDeDatos
from db_context.evento_dao import EventoDao
from views.calendario import Calendario
from views.evento import VistaEvento


class VistaMensual(ttk.Frame):
    """Clase que representa gráficamente los días de un mes completo y sus eventos"""

    def __init__(self, parent, gui):
        super().__init__(parent, padding=(0))
        self.grid(row=0, column=0, sticky='nsew')
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.__gui = gui
        self.__fechaActualDT = datetime.today()
        self.__anioActual = int(self.__fechaActualDT.strftime('%Y'))
        self.__mesActual = int(self.__fechaActualDT.strftime('%m'))
        self.__db = BaseDeDatos('EventosDB.csv')
        self.__cal = Calendario()
        self.__mes = self.__cal.matrizMensual(self.__anioActual, self.__mesActual)
        self.__cargarComponentes()

    def __cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a la interfaz de la vista mensual."""
        ttk.Button(self, style='btnSigAnt.TButton', text="Anterior", command=self.__anterior).grid(column=0, row=0,
                                                                                                   pady=5,
                                                                                                   padx=(5, 0), )
        ttk.Button(self, style='btnSigAnt.TButton', text="Siguiente", command=self.__siguiente).grid(column=2, row=0,
                                                                                                     pady=5,
                                                                                                     padx=(0, 5))
        self.__lblNombreMes = ttk.Label(self, text=self.__cal.nombreDelMes(self.__mesActual, 1) + ' - ' + str(
            self.__anioActual), font=('Century Gothic', '12', 'bold'), padding=5, borderwidth=2, relief="sunken")
        self.__lblNombreMes.grid(column=1, row=0, columnspan=1, padx=0, pady=5)
        self.__mesFrame = ttk.Frame(self, padding=5)
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0, row=1, columnspan=3, pady=0, padx=0)

    def actualizar(self):
        """Vuelve a cargar los widgets de los días del mes y sus tablas con eventos actualizadas desde el archivo .csv"""
        self.__mesFrame = ttk.Frame(self, padding=5)
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0, row=1, columnspan=3, pady=0, padx=0)

    def __mostrarMes(self, frame, mes):
        """Genera y retorna un frame que contiene cada uno de los widgets que representan los días del mes, incluyendo
        sus respectivas tablas con eventos."""
        self.__listaTablas = []
        fechasConEventos = self.__db.mapearFechas()
        monthFrame = ttk.Frame(frame, style='WeekFrame.TFrame', padding=5)
        self.labels = []
        dias = []
        for m in range(7):
            labelDay = ttk.Label(monthFrame, width=9, text=self.__cal.nombreDelDia(m, 1), font='Helvetica 12 bold',
                                 padding=(18, 0, 5, 0), background=self.__gui.configTema['bgNombreDia'], borderwidth=2,
                                 relief='solid')
            if labelDay['text'] == 'Domingo':
                labelDay['foreground'] = 'red'
            if labelDay['text'] == 'Sábado':
                labelDay['foreground'] = 'blue'
            labelDay.grid(column=m, row=0, padx=2, pady=2)
            dias.append(labelDay)
        self.labels.append(dias)
        if len(self.__mes) == 6:
            pad = (21, 18, 21, 18)
            height = 2
        else:
            pad = (21, 28, 21, 28)
            height = 3
        for week in self.__mes:
            labels_row = []
            for c, date in enumerate(week):
                frameDay = ttk.Frame(monthFrame, borderwidth=2, relief='solid')
                label = ttk.Label(frameDay, width=10, text=str(date.day), font='Helvetica 12 bold',
                                  padding=(5, 0, 5, 0), background=self.__gui.configTema['bgDiaMes'])
                label.grid(padx=2, pady=2)
                diaFormat = date.strftime('%Y-%m-%d')
                eventosDelDia = EventoDao.seleccionar_fecha(fecha=diaFormat)
                if eventosDelDia:
                    self.__crearTablaTreeView(frameDay, eventosDelDia, height)
                else:
                    ttk.Label(frameDay, text='SIN EVENTOS', font='Helvetica 8', width=10, padding=pad,
                              background=self.__gui.configTema['bgSinEventos']).grid()
                frameDay.grid(row=self.__mes.index(week) + 1, column=c, padx=2, pady=2)
                if date.month != mes:
                    label['background'] = self.__gui.configTema['bgNoDiaMes']
                if c == 6:
                    label['foreground'] = 'blue'
                if c == 0:
                    label['foreground'] = 'red'
                if date == self.__fechaActualDT.date():
                    label['background'] = self.__gui.configTema['bgHoy']
                labels_row.append(label)
            self.labels.append(labels_row)
        return monthFrame

    def __crearTablaTreeView(self, frame, datos, altura):
        """Crea una tabla tk.TreeView en la que se muestran cada uno de los eventos correspondientes."""
        tablaTreeView = ttk.Treeview(frame, columns=('id', 'ev'), show='', selectmode="extended", height=altura,
                                     padding=5)
        tablaTreeView["displaycolumns"] = ('ev')
        tablaTreeView.column('ev', width=95, anchor=tk.W)
        tablaTreeView.heading('ev', text="Eventos", anchor=tk.CENTER)
        tablaTreeView.grid(column=0, row=1)
        tablaTreeView.bind("<ButtonPress-1>", self.__onClickCell)
        tablaTreeView.bind("<Double-Button-1>", self.__doubleOnClickCell)
        for row in datos:
            valores = (row.id_evento, row.titulo)
            tablaTreeView.insert('', tk.END, tags=str(row.id_importancia), values=valores)
        tablaTreeView.tag_configure(tagname='2', font='Helvetica 8 bold', background='red', foreground='white')
        self.__listaTablas.append(tablaTreeView)

    def __onClickCell(self, event):
        """Define el comportamiento ciertos widgets al hacer un click seleccionando un evento de la tabla."""
        tabla = list(filter(lambda x: x.focus() != '', self.__listaTablas))
        if len(tabla) != 0 and tabla[0] != None:
            self.__gui.btnElim['state'] = 'enabled'
            self.__gui.btnModif['state'] = 'enabled'
            item = tabla[0].item(tabla[0].focus(), 'values')
            self.__gui.selectID = item[0]
            tabla[0].selection_remove(tabla[0].selection()[0])
            tabla[0].focus("")
        else:
            self.__gui.btnModif['state'] = 'disabled'
            self.__gui.btnElim['state'] = 'disabled'

    def __doubleOnClickCell(self, event):
        """Define el comportamiento ciertos widgets al hacer doble click sobre un evento de la tabla."""
        tabla = list(filter(lambda x: x.focus() != '', self.__listaTablas))
        if len(tabla) != 0 and tabla != None:
            item = tabla[0].item(tabla[0].focus(), 'values')
            id = int(item[0])
            evento = EventoDao.seleccionar(id_evento=id)
            ventana = tk.Toplevel(self)
            VistaEvento(ventana, evento, self.__gui)
            ventana.grid()
            tabla[0].selection_remove(tabla[0].selection()[0])
            tabla[0].focus("")

    def __anterior(self):
        """Permite generar gráficamente los widgets del mes anterior."""
        self.__mesFrame.destroy()
        if self.__mesActual - 1 < 1:
            self.__anioActual -= 1
            self.__mesActual = 12
        else:
            self.__mesActual -= 1
        self.__mes = self.__cal.matrizMensual(self.__anioActual, self.__mesActual)
        self.__lblNombreMes['text'] = self.__cal.nombreDelMes(self.__mesActual, 1) + ' - ' + str(self.__anioActual)
        self.__mesFrame = ttk.Frame(self, padding=5, borderwidth=2, relief="groove")
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0, row=1, columnspan=3, pady=5, padx=5)

    def __siguiente(self):
        """Permite generar gráficamente los widgets del mes siguiente."""
        self.__mesFrame.destroy()
        if self.__mesActual + 1 > 12:
            self.__anioActual += 1
            self.__mesActual = 1
        else:
            self.__mesActual += 1
        self.__mes = self.__cal.matrizMensual(self.__anioActual, self.__mesActual)
        self.__lblNombreMes['text'] = self.__cal.nombreDelMes(self.__mesActual, 1) + ' - ' + str(self.__anioActual)
        self.__mesFrame = ttk.Frame(self, padding=5, borderwidth=2, relief="groove")
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0, row=1, columnspan=3, pady=5, padx=5)