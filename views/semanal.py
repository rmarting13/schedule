import tkinter as tk
from tkinter import ttk
from datetime import datetime

from db_context.evento_dao import EventoDao
from views.calendario import Calendario
from views.evento import VistaEvento


class WeekWidget(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, style='WeekFrame.TFrame', padding=2)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.controller = controller
        self.__cal = Calendario()
        self.days_header = []
        self.days_content = []
        self.days_events_tables = []
        self.days_frame = []
        self.__cargar_componentes()

    def __cargar_componentes(self):
        #self.__weekFrame = ttk.Frame(self, style='WeekFrame.TFrame', padding=5)
        for dia in range(7):
            dayFrame = ttk.Frame(self, borderwidth=2, relief="solid")
            lblDia = ttk.Label(dayFrame, width=14,
                               font='Ubuntu 12 bold', padding=5, background=self.controller.configTema['bgNombreDia'])
            self.days_header.append(lblDia)
            lblDia.grid(column=0, row=0, pady=5, padx=0)
            if dia == 0:
                lblDia['foreground'] = 'red'
            if dia == 6:
                lblDia['foreground'] = 'blue'
            event_frame = ttk.Frame(dayFrame, padding=0)
            label_content = ttk.Label(event_frame,text='SIN EVENTOS', font='Ubuntu 12', padding=(15, 75, 15, 75),
                          background=self.controller.configTema['bgSinEventos'])
            self.days_content.append(label_content)
            label_content.grid()
            #self.__frameEventos.grid(column=0, row=1, pady=2, padx=2)
            tablaTreeView = ttk.Treeview(event_frame, columns=('id', 'ev'), show="headings", selectmode="extended", height=7,
                                         padding=0)
            tablaTreeView["displaycolumns"] = ('ev')
            tablaTreeView.column('ev', width=120, anchor=(tk.NW))
            tablaTreeView.heading('ev', text="Eventos", anchor=tk.CENTER)
            tablaTreeView.tag_configure(tagname='2', background='#7d0c0c', foreground='white')
            self.days_events_tables.append(tablaTreeView)
            event_frame.grid(column=0, row=1)
            dayFrame.grid(column=dia, row=1, pady=0, padx=1)

class VistaSemanal(ttk.Frame):
    """Clase que representa gráficamente los días de una semana y sus eventos"""
    def __init__(self, parent, gui):
        super().__init__(parent, padding=5)
        self.__gui = gui
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        self.__cal = Calendario()
        self.__fechaActualDT = datetime.today()
        self.__anioActual = int(self.__fechaActualDT.strftime('%Y'))
        self.__mesActual = int(self.__fechaActualDT.strftime('%m'))
        self.__semanaActual = None
        self.__cargarComponentes()

    def __cargarComponentes(self):
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
        self.__week_frame = ttk.Frame(self)
        self.__week_widget = WeekWidget(self.__week_frame, controller=self.__gui)
        self.actualizar()
        self.__week_frame.grid(column=0, row=1, columnspan=3, pady=5)

    def actualizar(self):
        """Vuelve a cargar los widgets de los días de la semana y sus tablas con eventos actualizada desde el archivo .csv"""
        self.__showWeek(self.__week_widget)
        # self.__frameWeek.grid(column=0, row=1, columnspan=3, pady=5)

    def __showWeek(self, week_widget):
        """Genera y retorna un frame que contiene cada uno de los widgets que representan los días de la semana,
        incluyendo sus respectivas tablas con eventos."""
        self.__listaTablas = []
        widgets = zip(self.__semanas[self.__semanaActual],
                      week_widget.days_header,
                      week_widget.days_content,
                      week_widget.days_events_tables
                      )
        i = 0
        for date, header, body, table in widgets:
            header.config(text=self.__cal.nombreDelDia(i, 1)+' '+date.strftime('%d-%m'))
            if date == self.__fechaActualDT.date():
                header.config(background=self.__gui.configTema['bgHoy'])
            else:
                header.config(background=self.__gui.configTema['bgNombreDia'])
            diaFormat = date.strftime('%Y-%m-%d')
            eventosDelDia = EventoDao.seleccionar_fecha(fecha=diaFormat)
            if eventosDelDia:
                body.grid_remove()
                self.__insertarEventosEnTabla(table=table, datos=eventosDelDia)
            else:
                table.grid_remove()
                body.grid()
            i += 1
        week_widget.grid()

    def __insertarEventosEnTabla(self, table: ttk.Treeview, datos):
        """Crea una tabla tk.TreeView en la que se muestran cada uno de los eventos correspondientes."""
        table.delete(*table.get_children())
        for row in datos:
            cad = row.fecha_hora.strftime('%H:%M') + '  ' + row.titulo
            valores = (row.id_evento, cad)
            table.insert('', tk.END, tags=str(row.id_importancia), values=valores)
        table.bind("<ButtonPress-1>", self.__onClickCell)
        table.bind("<Double-Button-1>", self.__doubleOnClickCell)
        table.grid(padx=0, pady=0, sticky='nsew')
        self.__listaTablas.append(table)

    def __onClickCell(self, event):
        """Define el comportamiento ciertos widgets al hacer un click seleccionando un evento de la tabla."""
        tabla = list(filter(lambda x: x.focus() != '', self.__listaTablas))
        if len(tabla) != 0 and tabla[0] is not None:
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
        if len(tabla) != 0 and tabla is not None:
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
        self.__week_widget.grid_remove()
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
        self.actualizar()

    def __avanzar(self):
        """Permite generar gráficamente los widgets la semana siguiente."""
        self.__week_widget.grid_remove()
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
        self.actualizar()


    def set_theme(self):
        widgets = zip(self.__week_widget.days_header,
                      self.__week_widget.days_content,
                      )
        for  header, body in widgets:
            if header['text'].split(' ')[1] == self.__fechaActualDT.strftime('%d-%m'):
                header.config(background=self.__gui.configTema['bgHoy'])
            else:
                header.config(background=self.__gui.configTema['bgNombreDia'])
            header.config(foreground=self.__gui.configTema['fgText'])
            body.config(background=self.__gui.configTema['bgSinEventos'])
            body.config(foreground=self.__gui.configTema['fgText'])