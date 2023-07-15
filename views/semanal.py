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


class VistaSemanal(ttk.Frame):
    """Clase que representa gráficamente los días de una semana y sus eventos"""

    def __init__(self, parent, gui):
        super().__init__(parent, padding=(5))
        self.__gui = gui
        self.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.__cal = Calendario()
        self.__fechaActualDT = datetime.today()
        self.__anioActual = int(self.__fechaActualDT.strftime('%Y'))
        self.__mesActual = int(self.__fechaActualDT.strftime('%m'))
        self.__semanaActual = None
        self.__db = BaseDeDatos('EventosDB.csv')
        self.cargarComponentes()

    def cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a la interfaz de la vista semanal."""
        ttk.Button(self, style='btnSigAnt.TButton', text="Anterior", command=self.__retroceder).grid(column=0, row=0,
                                                                                                     pady=5, padx=5)
        ttk.Button(self, style='btnSigAnt.TButton', text="Siguiente", command=self.__avanzar).grid(column=2, row=0,
                                                                                                   pady=5, padx=5)
        self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)

        for week in self.__semanas:
            if self.__fechaActualDT.date() in week:
                self.__semanaActual = self.__semanas.index(week)
                break

        self.__lblMes = ttk.Label(self,
                                  text=self.__cal.nombreDelMes(self.__mesActual, 1) + ' - ' + str(self.__anioActual),
                                  font=('Century Gothic', '12', 'bold'), padding=5)
        self.__lblMes.grid(column=1, row=0, columnspan=1, pady=5)
        self.actualizar()

    def actualizar(self):
        """Vuelve a cargar los widgets de los días de la semana y sus tablas con eventos actualizada desde el archivo .csv"""
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0, row=1, columnspan=3, pady=5)

    def __mostrarSemana(self, semana):
        """Genera y retorna un frame que contiene cada uno de los widgets que representan los días de la semana,
        incluyendo sus respectivas tablas con eventos."""
        self.__listaTablas = []
        fechasConEventos = self.__db.mapearFechas()
        weekFrame = ttk.Frame(self, style='WeekFrame.TFrame', padding=5)
        for col, dia in enumerate(semana):
            eventFrame = ttk.Frame(weekFrame, borderwidth=2, relief="solid")
            lblDia = ttk.Label(eventFrame, width=14,
                               text=self.__cal.nombreDelDia(col, 1) + '  ' + dia.strftime('%d/%m'),
                               font='Ubuntu 12 bold', padding=5, background=self.__gui.configTema['bgNombreDia'])
            lblDia.grid(column=0, row=0, pady=5, padx=0)
            if col == 0:
                lblDia['foreground'] = 'red'
            if col == 6:
                lblDia['foreground'] = 'blue'
            if dia == self.__fechaActualDT.date():
                lblDia['background'] = self.__gui.configTema['bgHoy']
            eventFrame.grid(column=col, row=1, pady=0, padx=1)
            self.__frameEventos = ttk.Frame(eventFrame)
            diaFormat = dia.strftime('%Y-%m-%d')
            eventosDelDia = EventoDao.seleccionar_fecha(fecha=diaFormat)
            if eventosDelDia:
                self.__crearTablaTreeView(self.__frameEventos, eventosDelDia)
            else:
                ttk.Label(self.__frameEventos, text='SIN EVENTOS', font='Ubuntu 12', padding=(15, 75, 15, 75),
                          background=self.__gui.configTema['bgSinEventos']).grid()
            self.__frameEventos.grid(column=0, row=1, pady=2, padx=2)
        return weekFrame

    def __crearTablaTreeView(self, frame, datos):
        """Crea una tabla tk.TreeView en la que se muestran cada uno de los eventos correspondientes."""
        tablaTreeView = ttk.Treeview(frame, columns=('id', 'ev'), show="headings", selectmode="extended", height=7,
                                     padding=5)
        tablaTreeView["displaycolumns"] = ('ev')
        tablaTreeView.column('ev', width=120, anchor=(tk.NW))
        tablaTreeView.heading('ev', text="Eventos", anchor=tk.CENTER)
        tablaTreeView.grid(column=0, row=0,sticky=tk.W)
        tablaTreeView.bind("<ButtonPress-1>", self.__onClickCell)
        tablaTreeView.bind("<Double-Button-1>", self.__doubleOnClickCell)
        for row in datos:
            cad = row.fecha_hora.strftime('%H:%M') + '  ' + row.titulo
            valores = (row.id_evento, cad)
            tablaTreeView.insert('', tk.END, tags=str(row.id_importancia), values=valores)
        tablaTreeView.tag_configure(tagname='2', background='#7d0c0c', foreground='white')
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
            id = item[0]
            evento = EventoDao.seleccionar(id_evento=id)
            ventana = tk.Toplevel(self)
            VistaEvento(ventana, evento, self.__gui)
            ventana.grid()
            tabla[0].selection_remove(tabla[0].selection()[0])
            tabla[0].focus("")

    def __retroceder(self):
        """Permite generar gráficamente los widgets la semana anterior."""
        self.__frameWeek.destroy()
        if self.__semanaActual - 1 < 0:
            if self.__mesActual - 1 < 1:
                self.__anioActual -= 1
                self.__mesActual = 12
            else:
                self.__mesActual -= 1
            self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)
            self.__semanaActual = len(self.__semanas) - 2
        else:
            self.__semanaActual -= 1
        self.__lblMes['text'] = self.__cal.nombreDelMes(self.__mesActual, 1) + ' - ' + str(self.__anioActual)
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0, row=1, columnspan=3, pady=5)

    def __avanzar(self):
        """Permite generar gráficamente los widgets la semana siguiente."""
        self.__frameWeek.destroy()
        if self.__semanaActual + 1 >= len(self.__semanas) - 1:
            if self.__mesActual + 1 > 12:
                self.__anioActual += 1
                self.__mesActual = 1
            else:
                self.__mesActual += 1
            self.__lblMes['text'] = self.__cal.nombreDelMes(self.__mesActual, 1) + ' - ' + str(self.__anioActual)
            self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)
            self.__semanaActual = 0
        else:
            self.__semanaActual += 1
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0, row=1, columnspan=3, pady=5)