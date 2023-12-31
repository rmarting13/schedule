import tkinter as tk
from tkinter import ttk, END, messagebox
from db_context.evento_dao import EventoDao
from views.evento import VistaEvento


class FiltroDeEventos(ttk.Frame):
    """Clase que representa gráficamente la interfaz de búsqueda y filtro de eventos."""

    def __init__(self, parent, gui):
        super().__init__(parent, padding=(5))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        self.__parent = gui
        self.__inputTitulo = tk.StringVar()
        self.__inputEtiqueta = tk.StringVar()
        self.__checkValueTitulo = tk.StringVar()
        self.__checkValueEtiqueta = tk.StringVar()
        self.__cargarComponentes()

    def __cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a la interfaz de la vista de búsqueda."""
        ttk.Checkbutton(self, text="Filtrar por Título:", padding=5, command=self.__habilitarFiltroPorTitulo,
                        variable=self.__checkValueTitulo).grid(column=0, row=0, columnspan=1, sticky=tk.W)
        ttk.Checkbutton(self, text="Filtrar por Etiquetas:", padding=5, command=self.__habilitarFiltroPorEtiqueta,
                        variable=self.__checkValueEtiqueta).grid(column=0, row=1, columnspan=1, sticky=tk.W)
        self.__inputTit = ttk.Entry(self, font=('Ubuntu', '11'), width=30, textvariable=self.__inputTitulo,
                                    state='disabled')
        self.__inputTit.grid(column=1, row=0, columnspan=1, padx=5, pady=5, sticky=tk.W)
        self.__inputTag = ttk.Entry(self, font=('Ubuntu', '11'), width=30, textvariable=self.__inputEtiqueta,
                                    state='disabled')
        self.__inputTag.grid(column=1, row=1, columnspan=1, padx=5, pady=5, sticky=tk.W)
        self.__btnBuscar = ttk.Button(self, text='Buscar', command=self.__buscar, state='disabled')
        self.__btnBuscar.grid(column=0, row=2, columnspan=3, pady=5, padx=5)
        self.__frameResultados = ttk.Labelframe(self, text='Resultados', padding=5, borderwidth=2, relief='sunken')

        columnas = ('id', 'ti', 'fe', 'et')
        self.__tablaTreeView = ttk.Treeview(self.__frameResultados, columns=columnas, show='headings',
                                            selectmode="extended", displaycolumns=('ti', 'fe', 'et'))

        self.__tablaTreeView.column('id', width=30, anchor=tk.CENTER)
        self.__tablaTreeView.column('ti', width=200, anchor=tk.CENTER)
        self.__tablaTreeView.column('fe', width=100, anchor=tk.CENTER)
        self.__tablaTreeView.column('et', width=200, anchor=tk.CENTER)

        self.__tablaTreeView.heading("id", text="Id", anchor=tk.CENTER)
        self.__tablaTreeView.heading("fe", text="Fecha - Hora", anchor=tk.CENTER)
        self.__tablaTreeView.heading("ti", text="Título", anchor=tk.CENTER)
        self.__tablaTreeView.heading("et", text="Etiquetas", anchor=tk.CENTER)

        self.__sclBar = ttk.Scrollbar(self.__frameResultados, orient=tk.VERTICAL, command=self.__tablaTreeView.yview)
        self.__sclBar.grid(column=1, row=0, sticky=tk.NS)
        self.__tablaTreeView.configure(yscroll=self.__sclBar.set)
        self.__tablaTreeView.grid(column=0, row=0)
        self.__frameResultados.grid(column=0, row=3, columnspan=3)
        self.__tablaTreeView.bind("<ButtonPress-1>", self.__onClickCell)
        self.__tablaTreeView.bind("<Double-Button-1>", self.__doubleOnClickCell)
        self.__insertarElementos(EventoDao.seleccionar())

    def actualizar(self):
        """Vuelve a cargar la tabla con eventos actualizada desde el archivo .csv"""
        self.__buscar()

    def __onClickCell(self, event):
        """Define el comportamiento ciertos widgets al hacer un click seleccionando un evento de la tabla."""
        if self.__tablaTreeView.focus() != "":
            self.__parent.btnElim['state'] = 'enabled'
            self.__parent.btnModif['state'] = 'enabled'
            self.__parent.selectID = self.__tablaTreeView.item(self.__tablaTreeView.focus(), 'values')[0]
        else:
            self.__parent.btnModif['state'] = 'disabled'
            self.__parent.btnElim['state'] = 'disabled'

    def __doubleOnClickCell(self, event):
        """Define el comportamiento ciertos widgets al hacer doble click sobre un evento de la tabla."""
        id = self.__tablaTreeView.item(self.__tablaTreeView.focus(), 'values')[0]
        evento = EventoDao.seleccionar(id_evento=id)
        ventana = tk.Toplevel(self)
        VistaEvento(ventana, evento, self.__parent)
        ventana.grid()

    def __insertarElementos(self, datos):
        """Inserta en una talba tk.TreeView los eventos recibidos por parámetro."""
        for evento in datos:
            values = (
                evento.id_evento,
                evento.titulo,
                evento.fecha_hora,
                evento.etiquetas,
                evento.id_importancia
            )
            self.__tablaTreeView.insert('', tk.END, tags=values, values=values)
            self.__tablaTreeView.tag_configure(tagname='IMPORTANTE', background='#7d0c0c',
                                               foreground='white')

    def __buscar(self):
        """Es llamado al presionar el botón Buscar en la interfaz gráfica, obteniendo los datos
        de los campos de filtro de la interfaz y enviándolos a la clase BaseDeDatos para que filtre dichos datos
        en el archivo csv. Una vez obtenido los eventos filtrados, los inserta en la tabla de eventos."""
        self.__tablaTreeView.delete(*self.__tablaTreeView.get_children())
        filtro = {}
        if self.__checkValueTitulo.get() not in ['0', '']:
            filtro.update({'titulo': self.__inputTitulo.get()})
        if self.__checkValueEtiqueta.get() not in ['0', '']:
            filtro.update({'etiqueta': self.__inputEtiqueta.get()})
        if len(filtro.keys()) != 0:
            listaFiltrada = EventoDao.seleccionar(**filtro)
            print(listaFiltrada)
            if listaFiltrada:
                self.__insertarElementos(listaFiltrada)
            else:
                messagebox.showerror(title='Error', message='No se encontraron eventos relacionados con la búsqueda.')
        else:
            self.__insertarElementos(EventoDao.seleccionar())


    def __habilitarFiltroPorTitulo(self):
        """Es llamado al activar o desactivar el widget CheckButton del label "Filtrar por Título" en la interfa gráfica,
        y define el comportamiento de los widgets relacionados, habilitando/deshabilitando campos y botones."""
        if self.__checkValueTitulo.get() == '1':
            self.__inputTit['state'] = 'enabled'
            self.__btnBuscar['state'] = 'enabled'
        else:
            self.__inputTit.delete(0, END)
            self.__inputTit['state'] = 'disabled'
        self.__habilitarBtnBuscar()

    def __habilitarFiltroPorEtiqueta(self):
        """Es llamado al activar o desactivar el widget CheckButton del label "Filtrar por Etiqueta" en la interfa gráfica,
        y define el comportamiento de los widgets relacionados, habilitando/deshabilitando campos y botones."""
        if self.__checkValueEtiqueta.get() == '1':
            self.__inputTag['state'] = 'enabled'
        else:
            self.__inputTag.delete(0, END)
            self.__inputTag['state'] = 'disabled'
        self.__habilitarBtnBuscar()

    def __habilitarBtnBuscar(self):
        """Habilita o deshabilita el botón 'Buscar' de acuerdo a si al menos uno de los campos de filtrado está
        habilitado o no"""
        if self.__inputTit['state'] == 'enabled' or self.__inputTag['state'] == 'enabled':
            self.__btnBuscar['state'] = 'enabled'
        else:
            self.__btnBuscar['state'] = 'disabled'