import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, END, messagebox
from datetime import datetime
from calendar import Calendar
from tkcalendar import Calendar as tkCalendar
from Archivo import BaseDeDatos
from db_context.importancia_dao import ImportanciaDao
from models.evento import Evento


class VistaEvento(ttk.Frame):
    """Clase que representa gráficamente los datos de un evento."""

    def __init__(self, parent, evento: Evento, gui):
        super().__init__(parent, padding=(20))
        self.__parent = parent
        self.__parent.title('Evento')
        self.__gui = gui
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.__evento = evento
        self.cargarComponentes()

    def cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a cada campo de los datos de un evento."""
        ttk.Label(self, text='TITULO:', style='lblName.TLabel', padding=5, borderwidth=2, relief='raised').grid(
            column=0, row=0, padx=5, pady=5, sticky=tk.W)
        self.__lblTitulo = ttk.Label(self, text=self.__evento.titulo, font=('Ubuntu', '12', 'bold'), padding=5,
                                     background=self.__gui.configTema['bgLabelText'])
        self.__lblTitulo.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text='DESCRIPCION:', style='lblName.TLabel', padding=5, borderwidth=2, relief='raised').grid(
            column=0, row=1, padx=5, pady=5, sticky=tk.W)
        self.__lblDesc = tk.Text(self, font=('Ubuntu', '10'), width=60, height=10,
                                 background=self.__gui.configTema['bgLabelText'],
                                 foreground=self.__gui.configTema['fgText'])
        self.__lblDesc.insert(tk.INSERT, self.__evento.descripcion)
        self.__lblDesc['state'] = 'disabled'
        self.__lblDesc.grid(column=0, row=2, columnspan=4, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text='FECHA Y HORA:', style='lblName.TLabel', padding=5, borderwidth=2, relief='raised').grid(
            column=2, row=0, padx=5, pady=5, sticky=tk.W)
        self.__lblFecha = ttk.Label(self, text=self.__evento.fecha_hora,
                                    font=('Ubuntu', '11', 'bold'), padding=5,
                                    background=self.__gui.configTema['bgLabelText'])
        self.__lblFecha.grid(column=3, row=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text='DURACION:', style='lblName.TLabel', padding=5, borderwidth=2, relief='raised').grid(
            column=0, row=3, padx=5, pady=5, sticky=tk.W)
        self.__lblDura = ttk.Label(self, text=self.__evento.duracion, font=('Ubuntu', '11', 'bold'), padding=5,
                                   background=self.__gui.configTema['bgLabelText'])
        self.__lblDura.grid(column=1, row=3, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text='IMPORTANCIA:', style='lblName.TLabel', padding=5, borderwidth=2, relief='raised').grid(
            column=2, row=3, padx=5, pady=5, sticky=tk.W)
        self.__lblImpor = ttk.Label(self,
                                    text=ImportanciaDao.seleccionar(id_importancia=self.__evento.id_importancia)[1],
                                    font=('Ubuntu', '11', 'bold'), padding=5,
                                    background=self.__gui.configTema['bgLabelText'])
        self.__lblImpor.grid(column=3, row=3, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text='ETIQUETAS: ', style='lblName.TLabel', padding=5, borderwidth=2, relief='raised').grid(
            column=0, row=4, padx=5, pady=5, sticky=tk.W)
        self.__lblTag = ttk.Label(self, text=self.__evento.etiquetas, font=('Ubuntu', '11', 'bold'), padding=5,
                                  background=self.__gui.configTema['bgLabelText'])
        self.__lblTag.grid(column=1, row=4, columnspan=4, padx=5, pady=5, sticky=tk.W)
        canvas = tk.Canvas(self, width=40, height=40, borderwidth=0,
                           highlightbackground=self.__gui.configTema['hlbgCanvas'])
        canvas.grid(column=0, row=5, columnspan=1, sticky=(tk.E), pady=5)
        img = (Image.open(self.__gui.configTema['imagen']))
        resized_image = img.resize((40, 40), Image.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(2, 2, anchor=tk.NW, image=new_image)
        canvas.image = new_image
        self.__lblRecor = ttk.Label(self, text=self.__evento.recordatorio, style='lblName.TLabel', padding=5,
                                    background=self.__gui.configTema['bgLabelText'])
        self.__lblRecor.grid(column=1, row=5, padx=5, pady=5)