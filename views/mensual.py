import tkinter as tk
from tkinter import ttk
from datetime import datetime
from db_context.evento_dao import EventoDao
from themes import config
from views.calendario import Calendario
from views.evento import VistaEvento

class MonthWidget(ttk.Frame):
    def __init__(self, parent, rows=None, controller=None):
        super().__init__(parent, style='WeekFrame.TFrame', padding=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.controller = controller
        self.__cal = Calendario()
        self.rows = rows
        self.column_headers = []
        self.days_header = []
        self.days_content = []
        self.days_events_tables = []
        self.days_frame= []
        self.__cargar_componentes()

    def __cargar_componentes(self):
            """Genera y retorna un frame que contiene cada uno de los widgets que representan los días del mes, incluyendo
            sus respectivas tablas con eventos."""
            #monthFrame = ttk.Frame(frame, style='WeekFrame.TFrame', padding=5)

            for m in range(7):
                labelDay = ttk.Label(self, width=13, text=self.__cal.nombreDelDia(m, 1), font='Helvetica 10 bold', foreground=self.controller.configTema['fgText'],
                                     justify='right', background=self.controller.configTema['bgNombreDia'], borderwidth=2,
                                     relief='solid')
                self.column_headers.append(labelDay)
                if labelDay['text'] == 'Domingo':
                    labelDay['foreground'] = 'red'
                if labelDay['text'] == 'Sábado':
                    labelDay['foreground'] = 'blue'
                labelDay.grid(column=m, row=0, padx=0, pady=0)
            if self.rows == 6:
                pad = (21, 18, 21, 18)
            else:
                pad = (21, 28, 21, 28)

            for week in range(self.rows):
                for day in range(7):
                    frameDay = ttk.Frame(self,width=7,height=7, borderwidth=2, relief='solid', style='DayFrame.TFrame')
                    self.days_frame.append(frameDay)
                    day_header_label = ttk.Label(frameDay, width=7, font='Helvetica 12 bold',
                              background=self.controller.configTema['bgDiaMes'], padding=(30,0,0,0))
                    if day == 6:
                        day_header_label['foreground'] = '#55aa00'
                    if day == 0:
                        day_header_label['foreground'] = '#ff5500'
                    self.days_header.append(day_header_label)
                    day_header_label.grid(padx=0, pady=0)
                    day_content_label = ttk.Label(frameDay, text='SIN\nEVENTOS', font='Helvetica 8', justify='center',
                              padding=pad, background=self.controller.configTema['bgSinEventos'])
                    self.days_content.append(day_content_label)
                    day_content_label.grid()
                    tablaTreeView = ttk.Treeview(frameDay, columns=('id', 'ev'), show='', selectmode="extended", height=3,
                                                 padding=0, )
                    tablaTreeView["displaycolumns"] = 'ev'
                    tablaTreeView.column('ev', width=95, anchor=tk.W)
                    tablaTreeView.heading('ev', text="Eventos", anchor=tk.CENTER)
                    self.days_events_tables.append(tablaTreeView)
                    frameDay.grid(row=week+1, column=day, padx=1, pady=1)






class VistaMensual(ttk.Frame):
    """Clase que representa gráficamente los días de un mes completo y sus eventos"""

    def __init__(self, parent, gui=None):
        super().__init__(parent, padding=(0))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.__gui = gui
        self.__fechaActualDT = datetime.today()
        self.__anioActual = int(self.__fechaActualDT.strftime('%Y'))
        self.__mesActual = int(self.__fechaActualDT.strftime('%m'))
        self.__cal = Calendario()
        self.__mes = self.__cal.matrizMensual(self.__anioActual, self.__mesActual)
        self.__tablas_con_eventos = []
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
        self.__five_row_month = MonthWidget(self.__mesFrame, rows=5, controller=self.__gui)
        self.__six_row_month = MonthWidget(self.__mesFrame, rows=6, controller=self.__gui)
        if len(self.__mes) == 6:
            self.__current_month_widget = self.__six_row_month
        else:
            self.__current_month_widget = self.__five_row_month
        self.__show_month(self.__current_month_widget, height=3)
        self.__mesFrame.grid(column=0, row=1, columnspan=3, pady=0, padx=0)

    def actualizar(self):
        """Vuelve a cargar los widgets de los días del mes y sus tablas con eventos actualizadas desde el archivo .csv"""
        #self.__mesFrame = ttk.Frame(self, padding=5)
        if len(self.__mes) == 6:
            self.__show_month(self.__six_row_month, height=2)
        else:
            self.__show_month(self.__five_row_month, height=3)
        self.__mesFrame.grid(column=0, row=1, columnspan=3, pady=0, padx=0)

    def __show_month(self, month_widget, height):
        self.__tablas_con_eventos = []
        month_days = []
        for week in self.__mes:
            for day in week:
                month_days.append(day)
        widgets = zip(month_widget.days_header,
                      month_widget.days_content,
                      month_widget.days_events_tables,
                      month_widget.days_frame)
        for header, body, table, frame in widgets:
            date = month_days.pop(0)
            header.config(text=f'{date.day}-{date.month}')
            if date.month != self.__mesActual:
                frame.config(style='NoDayFrame.TFrame')
                header['background'] = self.__gui.configTema['bgNoDiaMes']
            if date == self.__fechaActualDT.date():
                header['background'] = self.__gui.configTema['bgHoy']
            eventos_del_dia = EventoDao.seleccionar_fecha(fecha=date.strftime('%Y-%m-%d'))
            if eventos_del_dia:
                body.grid_remove()
                self.__insertarEventosEnTabla(table=table, datos=eventos_del_dia)
            else:
                table.grid_remove()
                body.grid()
        month_widget.grid()


    def __insertarEventosEnTabla(self, table, datos):
        """Crea una tabla tk.TreeView en la que se muestran cada uno de los eventos correspondientes."""
        table.delete(*table.get_children())
        for row in datos:
            valores = (row.id_evento, row.titulo)
            table.insert('', tk.END, tags=str(row.id_importancia), values=valores)
        table.tag_configure(tagname='2', font='Helvetica 8 bold', background='red', foreground='white')
        table.bind("<ButtonPress-1>", self.__onClickCell)
        table.bind("<Double-Button-1>", self.__doubleOnClickCell)
        table.grid(padx=1, pady=1, sticky='nsew')
        self.__tablas_con_eventos.append(table)

    def __onClickCell(self, event):
        """Define el comportamiento ciertos widgets al hacer un click seleccionando un evento de la tabla."""
        tabla = list(filter(lambda x: x.focus() != '', self.__tablas_con_eventos))
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
        tabla = list(filter(lambda x: x.focus() != '', self.__tablas_con_eventos))
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
        self.__current_month_widget.grid_remove()
        if self.__mesActual - 1 < 1:
            self.__anioActual -= 1
            self.__mesActual = 12
        else:
            self.__mesActual -= 1
        self.__mes = self.__cal.matrizMensual(self.__anioActual, self.__mesActual)
        self.__lblNombreMes['text'] = self.__cal.nombreDelMes(self.__mesActual, 1) + ' - ' + str(self.__anioActual)
        if len(self.__mes) == 6:
            self.__current_month_widget = self.__six_row_month
        else:
            self.__current_month_widget = self.__five_row_month
        self.__show_month(self.__current_month_widget, height=3)
        self.__change_colors(self.__current_month_widget)

    def __siguiente(self):
        """Permite generar gráficamente los widgets del mes siguiente."""
        self.__current_month_widget.grid_remove()
        if self.__mesActual + 1 > 12:
            self.__anioActual += 1
            self.__mesActual = 1
        else:
            self.__mesActual += 1
        self.__mes = self.__cal.matrizMensual(self.__anioActual, self.__mesActual)
        self.__lblNombreMes['text'] = self.__cal.nombreDelMes(self.__mesActual, 1) + ' - ' + str(self.__anioActual)
        if len(self.__mes) == 6:
            self.__current_month_widget = self.__six_row_month
        else:
            self.__current_month_widget = self.__five_row_month
        self.__show_month(self.__current_month_widget, height=3)
        self.__change_colors(self.__current_month_widget)

    def set_theme(self):
        self.__change_colors(self.__current_month_widget)

    def __change_colors(self, month_widget):
        for col in month_widget.column_headers:
            col.config(background=self.__gui.configTema['bgNombreDia'])
            col.config(foreground=self.__gui.configTema['fgText'])

        widgets = zip(month_widget.days_header, month_widget.days_content)
        for header, body in widgets:
            if header['text'].split('-')[1] == str(self.__mesActual):
                if header['text'] == self.__fechaActualDT.strftime('%d-%-m'):
                    header.config(background=self.__gui.configTema['bgHoy'])
                else:
                    header.config(background=self.__gui.configTema['bgDiaMes'])
            else:
                header.config(background=self.__gui.configTema['bgNoDiaMes'])
            header.config(foreground=self.__gui.configTema['fgText'])
            body.config(background=self.__gui.configTema['bgSinEventos'])
            body.config(foreground=self.__gui.configTema['fgText'])


if __name__ == '__main__':
        class Gui:
            configTema = config.awdark

        root = tk.Tk()
        VistaMensual(root, Gui()).grid()
        root.eval('tk::PlaceWindow . center')
        root.mainloop()
