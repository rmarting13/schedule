import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, END, messagebox
from datetime import datetime
from calendar import Calendar
from tkcalendar import Calendar as tkCalendar

from db_context.etiqueta_dao import EtiquetaDao
from db_context.evento_dao import EventoDao
from db_context.eventos_etiquetas_dao import EventoEtiquetaDao
from db_context.importancia_dao import ImportanciaDao
from models.etiqueta import Etiqueta
from models.evento import Evento
from views.popup import PopUp


class NuevoEventoVista(ttk.Frame):
    """Clase que representa gráficamente la interfaz de creación/modificación de un evento de calendario."""

    def __init__(self, parent, gui):
        super().__init__(parent, padding=20)
        self.__guiParent = gui
        self.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.__ventanaCal = None
        self.__tamTag = 0
        self.__rowTag = 0
        self.__columnTag = -1
        self.__listaEtiquetas = []
        self.__tags_in_db = list(map(lambda x: (x.id_etiqueta, x.nombre),EtiquetaDao.seleccionar()))
        self.__tags_in_db_nombres = list(map(lambda x: x.nombre, EtiquetaDao.seleccionar()))
        self.__importancia_options = list(
            map(lambda x: str(x.id_importancia) + ' ' + x.nombre, ImportanciaDao.seleccionar()))
        self.__titulo = tk.StringVar()
        self.__importancia = tk.StringVar()
        self.__fecha = tk.StringVar()
        self.__fechaRecor = tk.StringVar()
        self.__duracion = tk.StringVar()
        self.__hHora = tk.StringVar()
        self.__mHora = tk.StringVar()
        self.__hRecor = tk.StringVar()
        self.__mRecor = tk.StringVar()
        self.__etiqueta = tk.StringVar()
        self.__checkValue = tk.StringVar()
        self.__selectedOptionId = None
        if self.__guiParent.selectID:

            self.__eventoActual = EventoDao.seleccionar(id_evento=self.__guiParent.selectID)
            fecha, hora = self.__eventoActual['fecha_hora'].split(' ')
            self.__id = self.__eventoActual['id_evento']
            self.__titulo.set(self.__eventoActual['titulo'])
            self.__descripcion = self.__eventoActual['descripcion']
            self.__importancia.set(self.__eventoActual['id_importancia'])
            self.__fecha.set(fecha)
            self.__duracion.set(self.__eventoActual['duracion'])
            self.__hHora.set(hora[:2])
            self.__mHora.set(hora[3:5])
        else:
            self.__id = None
            self.__descripcion = ''
            self.__inputDesc = None
            self.__tagFrame = None
            self.__limpiarCampos()

        self.__etiqueta.trace("w", lambda name, index, mode: self.__activarBtnEtiqueta())
        self.__cargarComponentes()

    def __cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a cada campo de los datos de un evento, disponibles para ser
        completados por el usuario."""
        self.__mainBlock = ttk.Frame(self)
        self.__mainBlock.grid_columnconfigure(0, weight=1)
        self.__block1 = ttk.Frame(self.__mainBlock, padding=10)
        self.__block1.grid_columnconfigure(0, weight=1)
        self.__block2 = ttk.Frame(self.__mainBlock, padding=10)
        self.__block2.grid_columnconfigure(0, weight=1)

        # TITULO
        ttk.Label(
            self.__block1,
            font=('Ubuntu', '12', 'bold'),
            text="Título: ",
            justify='left',
            width=6
        ).grid(column=0, row=0, columnspan=1, sticky=tk.W, pady=5)
        self.__inputTit = ttk.Entry(self.__block1, font=('Ubuntu Medium', '12', 'bold'), width=35,
                                    textvariable=self.__titulo, justify='right')
        self.__inputTit.grid(column=1, row=0, columnspan=1, sticky=tk.W, pady=5)

        # DESCRIPCIÓN
        ttk.Label(self.__block1, font=('Ubuntu', '12', 'bold'), text="Descripción:", justify='left').grid(column=0,
                                                                                                          row=1,
                                                                                                          columnspan=3,
                                                                                                          sticky=(tk.W),
                                                                                                          pady=5)
        self.__inputDesc = tk.Text(self.__block1, font=('Ubuntu', '11'), height=10, width=60,
                                   background=self.__guiParent.configTema['bgLabelText'],
                                   foreground=self.__guiParent.configTema['fgText'])
        self.__inputDesc.insert('1.0', self.__descripcion)
        self.__inputDesc.grid(column=0, row=2, columnspan=2, sticky=(tk.E), pady=5)

        # IMPORTANCIA
        ttk.Label(self.__block1, font=('Ubuntu', '12', 'bold'), text="Importancia:", justify='left').grid(column=0,
                                                                                                          row=4,
                                                                                                          columnspan=1,
                                                                                                          sticky=(tk.E),
                                                                                                          pady=5)

        self.__inputImp = ttk.Combobox(self.__block1, textvariable=self.__importancia, font=('Ubuntu', '11', 'bold'),
                                       values=self.__importancia_options, justify='center')
        self.__inputImp.set(self.__importancia.get())
        self.__inputImp.config(state='readonly', width=12)
        self.__inputImp.grid(column=1, row=4, columnspan=1, sticky=(tk.E), pady=5)

        # ETIQUETAS
        self.__tagFrame = ttk.Labelframe(self.__block1, text="Tags", borderwidth=6, relief='sunken')
        self.__tagFrame.grid(column=0, row=7, columnspan=2)
        self.__btnAddTag = ttk.Button(self.__block1, text="Agregar Etiqueta:", command=self.__agregarEtiqueta,
                                      state='disabled')
        self.__btnAddTag.grid(column=0, row=5, columnspan=1, sticky=(tk.W), pady=5)
        ttk.Label(self.__block1, text='Etiquetas Disponibles:', padding=5, font=('Ubuntu', '11', 'bold')).grid(column=0,
                                                                                                               row=6,
                                                                                                               columnspan=1,
                                                                                                               sticky=tk.W)
        self.__lblTagsRest = ttk.Label(self.__block1, text='5', font=('Ubuntu', '12', 'bold'),
                                       foreground=self.__guiParent.configTema['Tags'], padding=5)
        self.__lblTagsRest.grid(column=1, row=6, columnspan=1, sticky=tk.W)
        # self.__inputTag = ttk.Entry(self.__block1, font=('Ubuntu', '11'), width=35, textvariable=self.__etiqueta,
        #                             justify='right')
        self.__inputTag = ttk.Combobox(self.__block1, font=('Ubuntu', '11', 'bold'),
                                       width=35, textvariable=self.__etiqueta, justify='right')
        self.__inputTag.grid(column=1, row=5, columnspan=1, sticky=(tk.E), pady=5)
        self.__inputTag.bind('<KeyRelease>', self.update)
        self.__inputTag.bind("<<ComboboxSelected>>", self.callback)
        self.__inputTag.grid(column=1, row=5, columnspan=1, sticky=(tk.E), pady=5)

        if self.__guiParent.selectID:
            tags = self.__eventoActual['etiquetas'].split(sep=',')
            for tag in tags:
                self.__etiqueta.set(tag)
                self.__agregarEtiqueta()

        # FECHA
        ttk.Label(self.__block2, font=('Ubuntu', '12', 'bold'), text="Fecha:", justify='left').grid(column=0, row=0,
                                                                                                    columnspan=1,
                                                                                                    sticky=(tk.E),
                                                                                                    pady=5)
        self.__inputFecha = ttk.Entry(self.__block2, font=('Ubuntu', '11', 'bold'), textvariable=self.__fecha,
                                      state='readonly')
        self.__inputFecha.config(justify='center', width=15)
        self.__inputFecha.grid(column=1, row=0, columnspan=1, sticky=(tk.E), pady=5)
        self.__inputFecha.bind("<ButtonPress-1>", self.__seleccionarFechaEvento)

        # HORA
        hora = ttk.Label(self.__block2, font=('Ubuntu', '12', 'bold'), text="Hora:", justify="left")
        hora.grid(column=0, row=1, columnspan=1, sticky=(tk.E), pady=5)
        self.__inputHora = ttk.Labelframe(self.__block2)
        diezHoras = list(map(lambda x: '0' + str(x), range(10)))
        self.__horas = diezHoras.copy()
        self.__horas.extend(map(lambda x: str(x), range(10, 24)))
        self.__min = diezHoras
        self.__min.extend(map(lambda x: str(x), range(10, 60)))
        comboHora = ttk.Combobox(self.__inputHora, font=('Ubuntu', '11', 'bold'), textvariable=self.__hHora,
                                 values=self.__horas, width=3, state='readonly', justify='right')
        comboHora.grid(column=0, row=0, columnspan=1, sticky=(tk.N))
        comboMin = ttk.Combobox(self.__inputHora, font=('Ubuntu', '11', 'bold'), textvariable=self.__mHora,
                                values=self.__min, width=3, state='readonly', justify='right')
        comboMin.grid(column=2, row=0, columnspan=1, sticky=(tk.N))
        self.__inputHora.grid(column=1, row=1, sticky=(tk.E), pady=0)
        ttk.Label(self.__inputHora, text=":", font=('Arial', 14), justify='left').grid(column=1, row=0, columnspan=1,
                                                                                       sticky=(tk.N), padx=2)

        # DURACIÓN
        ttk.Label(self.__block2, font=('Ubuntu', '12', 'bold'), text="Duración:", justify='left').grid(column=0, row=2,
                                                                                                       columnspan=1,
                                                                                                       sticky=(tk.E),
                                                                                                       pady=5)
        self.__inputDura = ttk.Combobox(self.__block2, font=('Ubuntu', '11', 'bold'), textvariable=self.__duracion,
                        values=['30 min', '1 hora', ' horas', '6 horas', '8 horas', '12 horas', 'Todo el día'],
                        justify='center')
        self.__inputDura.config(state='readonly', width=12)
        self.__inputDura.grid(column=1, row=2, columnspan=1, sticky=(tk.E), pady=5)

        # AGREGAR RECORDATORIO
        canvas = tk.Canvas(self.__block2, width=40, height=40,
                           highlightbackground=self.__guiParent.configTema['hlbgCanvas'])
        canvas.grid(column=0, row=3, columnspan=1, sticky=(tk.E), pady=5)
        img = (Image.open(self.__guiParent.configTema['imagen']))
        resized_image = img.resize((40, 40), Image.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(2, 2, anchor=tk.NW, image=new_image)
        canvas.image = new_image
        self.__recorChBx = ttk.Checkbutton(self.__block2, text="Recordatorio", command=self.__agregarRecor,
                                           variable=self.__checkValue)
        self.__recorChBx.grid(column=1, row=3, columnspan=1, sticky=(tk.W), pady=5, padx=(5, 0))
        self.__inputRecor = ttk.Labelframe(self.__block2, text="Configurar recordatorio")

        # BOTONES ACEPTAR Y CANCELAR
        btnFrame = ttk.Labelframe(self.__block2)
        btnFrame.grid(column=1, row=5, pady=5, columnspan=2, sticky=tk.E, )
        self.__btnAceptar = ttk.Button(btnFrame, style='btnAceptar.TButton', text="Aceptar",
                                       command=self.__enviarEvento, state='disabled')
        self.__btnAceptar.grid(column=0, row=0, padx=(0, 3))
        btnCancelar = ttk.Button(btnFrame, style='btnCancelar.TButton', text="Cancelar", command=self.__limpiarCampos)
        btnCancelar.grid(column=1, row=0, padx=(3, 0))
        self.__titulo.trace("w", lambda name, index, mode: self.__activarBtnAceptar())
        if self.__titulo.get() != '':
            self.__btnAceptar['state'] = 'enabled'

        self.__block1.grid(column=0, row=0, rowspan=2)
        separator = ttk.Separator(self, orient='vertical', )
        separator.grid(column=1, row=0, rowspan=2, padx=5, sticky=tk.EW)
        self.__block2.grid(column=2, row=0, rowspan=2)
        self.__mainBlock.grid(column=0, row=0)

    def update(self, *args):
        options = []
        typed = self.__inputTag.get()
        if typed == '':
            tags = self.__tags_in_db
        else:
            tags = EtiquetaDao.seleccionar_nombre(typed)
        self.__inputTag['values'] = list(map(lambda x: str(x[0])+' '+x[1], tags))
        self.__inputTag.event_generate('<Down>')
        self.__inputTag.after(100, self.__inputTag.focus_set)

    def callback(self,e):
        selection = self.__inputTag.selection_get().split(' ')
        self.__inputTag.set(selection[1])
        self.__selectedOptionId = int(selection[0])

    def actualizar(self):
        self.__cargarComponentes()

    def __agregarRecor(self):
        """Es llamado al activar el widget CheckButton del label Recordatorio, y genera un frame que contiene
        los widgets relacionados a la fecha y hora del recordatorio para ser configurados por el usuario."""
        if self.__checkValue.get() == '1':
            # FECHA
            ttk.Label(self.__inputRecor, font=('Ubuntu', '12', 'bold'), text="Fecha:", justify='left').grid(column=0,
                                                                                                            row=0,
                                                                                                            columnspan=1,
                                                                                                            sticky=(
                                                                                                                tk.E),
                                                                                                            pady=5,
                                                                                                            padx=(0, 5))
            self.__inputFechaRecor = ttk.Entry(self.__inputRecor, font=('Ubuntu', '11', 'bold'),
                                               textvariable=self.__fechaRecor, state='readonly')
            self.__inputFechaRecor.config(justify='center', width=15)
            self.__inputFechaRecor.grid(column=1, row=0, columnspan=1, sticky=(tk.W), pady=5)
            self.__inputFechaRecor.bind("<ButtonPress-1>", self.__seleccionarFechaRecor)
            # HORA
            ttk.Label(self.__inputRecor, font=('Ubuntu', '12', 'bold'), text="Hora:", justify="left").grid(column=0,
                                                                                                           row=1,
                                                                                                           columnspan=1,
                                                                                                           sticky=(
                                                                                                               tk.E),
                                                                                                           pady=5,
                                                                                                           padx=(0, 5))
            self.__inputHoraRecor = ttk.Labelframe(self.__inputRecor)
            comboRecorHora = ttk.Combobox(self.__inputHoraRecor, font=('Ubuntu', '11', 'bold'),
                                          textvariable=self.__hRecor, values=self.__horas, width=3, state='readonly',
                                          justify='right')
            comboRecorHora.set(datetime.now().strftime('%H'))
            comboRecorHora.grid(column=0, row=0, columnspan=1, sticky=(tk.N))
            comboRecorMin = ttk.Combobox(self.__inputHoraRecor, font=('Ubuntu', '11', 'bold'),
                                         textvariable=self.__mRecor, values=self.__min, width=3, state='readonly',
                                         justify='right')
            comboRecorMin.set(datetime.now().strftime('%M'))
            comboRecorMin.grid(column=2, row=0, columnspan=1, sticky=(tk.N))
            ttk.Label(self.__inputHoraRecor, text=":", font=('Arial', '14', 'bold'), justify='left').grid(column=1,
                                                                                                          row=0,
                                                                                                          columnspan=1,
                                                                                                          sticky=(tk.N),
                                                                                                          padx=2)
            self.__inputHoraRecor.grid(column=1, row=1, sticky=(tk.E), pady=0)
            self.__inputRecor.grid(column=1, row=4, sticky=(tk.E), pady=0)
        else:
            # self.__cerrarCal()
            self.__inputRecor.destroy()
            self.__inputRecor = ttk.Labelframe(self.__block2, text="Configurar recordatorio")

    def __seleccionarFechaRecor(self, event):
        """Es llamado al hacer click en el campo fecha de la interfaz, desplegando un pequeño calendario gráfico que
        permite elegir una determinada fecha para el evento."""
        if self.__ventanaCal == None:
            self.__desplegarCalendarioSeleccionable(self.__obtenerFechaRecor)

    def __seleccionarFechaEvento(self, event):
        """Es llamado al hacer click en el campo fecha del frame Recordatorio , desplegando un pequeño calendario gráfico que
       permite elegir una determinada fecha para el recordatorio."""
        if self.__ventanaCal == None:
            self.__desplegarCalendarioSeleccionable(self.__obtenerFechaEvento)

    def __desplegarCalendarioSeleccionable(self, tipo):
        """Genera gráficamente la interfaz de un calendario que permite explorar y seleccionar fechas."""
        self.__ventanaCal = tkCalendar(self.__mainBlock, selectmode="day", date_pattern="y-mm-dd")
        self.__ventanaCal.grid(column=3, row=0, columnspan=2, padx=5, pady=5, sticky=tk.S)
        self.__btnSel = ttk.Button(self.__mainBlock, text="Seleccionar", command=tipo)
        self.__btnSel.grid(column=3, row=1, pady=5, padx=5, sticky=tk.NE)
        self.__btnCan = ttk.Button(self.__mainBlock, text="Cerrar", command=self.__cerrarCal)
        self.__btnCan.grid(column=4, row=1, pady=5, padx=5, sticky=tk.NW)

    def __cerrarCal(self):
        """Destruye el frame donde se generó el calendario para selección de fechas."""
        self.__ventanaCal.destroy()
        self.__btnSel.destroy()
        self.__btnCan.destroy()
        self.__ventanaCal = None

    def __obtenerFechaRecor(self):
        """Es llamado al presionar el botón "Seleccionar" del frame del calendario de selección de fechas, obteniendo
        del mismo la fecha seleccionada e insertándola en el widget del campo fecha del frame Recordatorio."""
        self.__inputFechaRecor['state'] = 'normal'
        self.__inputFechaRecor.delete(0, tk.END)
        self.__inputFechaRecor.insert(0, self.__ventanaCal.get_date())
        self.__inputFechaRecor['state'] = 'readonly'
        self.__cerrarCal()

    def __obtenerFechaEvento(self):
        """Es llamado al presionar el botón "Seleccionar" del frame del calendario de selección de fechas, obteniendo
        del mismo la fecha seleccionada e insertándola en el widget del campo fecha del frame Evento."""
        self.__inputFecha['state'] = 'normal'
        self.__inputFecha.delete(0, END)
        self.__inputFecha.insert(0, self.__ventanaCal.get_date())
        self.__inputFecha['state'] = 'readonly'
        self.__cerrarCal()

    def __enviarEvento(self):
        """Recoge y almacena en un diccionario todos los strings obenidos de los widgets de la interfaz, enviándolo
        a un objeto de la clase BaseDeDatos para grabar los datos del evento o modificar uno existente."""
        fecha = self.__fecha.get()
        hora = self.__hHora.get() + ':' + self.__mHora.get()+':00'
        if self.__validarFechaYHora(fecha, hora):
            #tags = ", ".join(self.__listaEtiquetas)
            if self.__checkValue.get() == '1':
                stringRecor = self.__fechaRecor.get()+' '+self.__hRecor.get()+':'+self.__mRecor.get()+':00'
            else:
                stringRecor = None
            dur = int(self.__duracion.get().split(' ')[0])
            duracion_en_min = dur*60 if dur != 30 else 30
            values = {
                'id_evento': self.__id,
                'titulo': self.__titulo.get(),
                'descripcion': self.__inputDesc.get("1.0", "end-1c"),
                'id_importancia': int(self.__importancia.get().split(' ')[0]),
                'fecha_hora': self.__fecha.get()+' '+self.__hHora.get()+':'+self.__mHora.get()+':00',
                'duracion': duracion_en_min,
                'etiquetas': None,
                'recordatorio': stringRecor
            }
            evento = Evento(**values)
            print(f'ALL TAGS: {self.__listaEtiquetas}')
            old_tags = list(filter(lambda tg: tg[0] != 0, self.__listaEtiquetas))
            new_tags = list(filter(lambda tg: tg[0] == 0, self.__listaEtiquetas))
            print(f'OLD TAGS: {old_tags}')
            print(f'NEW TAGS: {new_tags}')
            if self.__guiParent.selectID: # actualización de un evento existente
                id_evento = EventoDao.actualizar(evento)
                tags_on_db = list(map(lambda x: x[1], EventoEtiquetaDao.seleccionar(id_evento)))
                # relaciones_actuales = list(map(lambda x: (id_evento, x[0]), self.__listaEtiquetas))
                if sorted(old_tags) != sorted(tags_on_db):  # pregunta si se eliminaron etiquetas al actualizar
                    delete_tags = list(filter(lambda tg: tg not in old_tags, tags_on_db))
                    for tag in delete_tags:  # se eliminan las relaciones de la tabla eventos_etiquetas en la db
                        EventoEtiquetaDao.eliminar(id_evento=id_evento, id_etiqueta=tag)
            else:  # Creación de un evento nuevo
                id_evento = EventoDao.insertar(evento)
                if len(old_tags) > 0:  # si se seleccionaron etiquetas existentes
                    map(lambda x: EventoEtiquetaDao.insertar(id_evento=id_evento, id_etiqueta=x), old_tags)
            print(f'CANTIDAD DE ETIQUETAS NUEVAS: {len(new_tags)}')
            if len(new_tags) > 0: # si se crearon nuevas etiquetas (se ejecuta tanto para actualización como nuevo evento)
                id_etiquetas_insertadas = list(map(lambda x: EtiquetaDao.insertar(Etiqueta(nombre=x[1])), new_tags))  # etiqueta nueva
                print('ID ETIQUETAS INSERTADAS: '+str(id_etiquetas_insertadas))
                map(lambda x: EventoEtiquetaDao.insertar(id_evento=id_evento, id_etiqueta=x), id_etiquetas_insertadas)  # nuevas relaciones en la tabla eventos_etiquetas



            PopUp(self).mensaje('Evento agregado con éxito!')
            self.__limpiarCampos()

    def __activarBtnAceptar(self):
        """Habilita o deshabilita el estado del botón "Aceptar", de acuerdo al seguimiento de la traza del campo del
        widget correspondiente al Título del evento. De esta manera, mientras el usuario no ingrese al menos un caracter
        en el campo de Título entonces el botón no se habilitará."""
        if self.__titulo.get() == '':
            self.__btnAceptar['state'] = 'disabled'
        else:
            self.__btnAceptar['state'] = 'enabled'

    def __validarFechaYHora(self, fecha, hora):
        """Determina si la fecha seleccionada del evento seleccionada por el usuario, coincide o nó con algún evento ya existente.
        En caso de ser cierto, ejecuta una ventana emergente con un cuadro de diálogo indicandole al usuario la situación."""
        if self.__guiParent.selectID == None:
            value = fecha+' '+hora
            if EventoDao.eixiste_fecha_hora(fecha_hora=value):
                rdo = False
                PopUp(self).mensaje('Ya existe un evento en la misma fecha y hora.\nPor favor elija otra fecha/hora.')
            else:
                rdo = True
        else:
            rdo = True
        return rdo

    def __limpiarCampos(self):
        """Elimina el contenido de los widgets de la interfaz que haya completado el usuario o hayan sido autocompletados
        por modificación de un evento."""
        self.__titulo.set('')
        self.__descripcion = ''
        self.__importancia.set(self.__importancia_options[0])
        self.__fecha.set(datetime.today().strftime('%Y-%m-%d'))
        self.__hHora.set(datetime.now().strftime('%H'))
        self.__mHora.set(datetime.now().strftime('%M'))
        self.__duracion.set('1 hora')
        self.__fechaRecor.set(datetime.today().strftime('%Y-%m-%d'))
        if self.__inputDesc != None:
            self.__inputDesc.delete("1.0", "end-1c")
        if self.__checkValue.get() == '1':
            self.__recorChBx.invoke()
        if self.__ventanaCal != None:
            self.__cerrarCal()
        if self.__tagFrame != None:
            self.__tagFrame.destroy()
            self.__tagFrame = ttk.Labelframe(self.__block1, text="Tags", borderwidth=6, relief='sunken')
            self.__tagFrame.grid(column=0, row=6, columnspan=2)
        self.__listaEtiquetas.clear()

    def __activarBtnEtiqueta(self):
        """Habilita o deshabilita el estado del botón Agregar Etiqueta, de acuerdo al seguimiento de la traza
        del campo de entrada de etiquetas. El botón no se habilitará a menos que el usuario ingrese un caracter en el campo."""
        if self.__etiqueta.get() == '' or len(self.__tagFrame.winfo_children()) >= 5:
            self.__btnAddTag['state'] = 'disabled'
        else:
            self.__btnAddTag['state'] = 'enabled'

    def __agregarEtiqueta(self):
        """Es llamado al presionar el botón "Agregar Etiqueta", recogiendo el string del campo de entrada de etiqueta
        agregándolo a una lista de etiquetas del evento y a su vez mostrando gráficamente en la interfaz, las etiquetas agregadas."""
        #deleteTag = lambda tag: self.__listaEtiquetas.remove(tag)
        def deleteTag(tag):
            for tuple in self.__listaEtiquetas:
                if tag in tuple:
                    self.__listaEtiquetas.remove(tuple)
                    break

        cant = int(self.__lblTagsRest['text'])
        self.__lblTagsRest['text'] = str(cant - 1)
        if cant == 1:
            self.__lblTagsRest['foreground'] = 'red'

        def modificar1(event):
            tagLabel['relief'] = 'raised'

        def modificar2(event):
            tagLabel['relief'] = 'ridge'

        def eliminar(event):
            cant = int(self.__lblTagsRest['text'])
            if cant == 0:
                self.__lblTagsRest['foreground'] = self.__guiParent.configTema['Tags']
            self.__lblTagsRest['text'] = str(cant + 1)
            deleteTag(tagLabel["text"])
            tagLabel.destroy()

        if self.__etiqueta.get() not in list(map(lambda x: x[1], self.__listaEtiquetas)):
            if self.__etiqueta.get() not in self.__tags_in_db_nombres:
                self.__listaEtiquetas.append((0, self.__etiqueta.get()))
            elif self.__selectedOptionId:
                self.__listaEtiquetas.append((self.__selectedOptionId, self.__etiqueta.get()))

            tagLabel = ttk.Label(self.__tagFrame, font=('Ubuntu', '10', 'bold'), text=self.__etiqueta.get(),
                                 relief='ridge', padding=5)
            tagLabel.bind("<Enter>", modificar1)
            tagLabel.bind("<Leave>", modificar2)
            tagLabel.bind("<ButtonPress-1>", eliminar)
            if self.__tamTag + tagLabel.winfo_reqwidth() < 270:
                self.__columnTag += 1
                self.__tamTag += tagLabel.winfo_reqwidth()
            else:
                self.__tamTag = 0
                self.__columnTag = 0
                self.__rowTag += 1
            tagLabel.grid(column=self.__columnTag, row=self.__rowTag, pady=5, padx=5)
            if len(self.__tagFrame.winfo_children()) >= 5:  # Deshabilita el botón si se llegó al máximo de 5 etiquetas
                self.__btnAddTag.state(['disabled'])
        self.__inputTag.delete(0, END)