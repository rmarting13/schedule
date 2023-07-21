import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, END, messagebox
from datetime import datetime
from tkcalendar import Calendar as tkCalendar
from db_context.etiqueta_dao import EtiquetaDao
from db_context.evento_dao import EventoDao
from db_context.eventos_etiquetas_dao import EventoEtiquetaDao
from db_context.importancia_dao import ImportanciaDao
from models.etiqueta import Etiqueta
from models.evento import Evento

class NuevoEventoVista(ttk.Frame):
    """Clase que representa gráficamente la interfaz de creación/modificación de un evento de calendario."""

    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.__controller = controller
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        self.__parent = parent
        self.__ventanaCal = None
        self.__tamTag = 0
        self.__rowTag = 0
        self.__columnTag = -1
        self.__listaEtiquetas = []
        self.__tags_in_db = EtiquetaDao.seleccionar()
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
        if self.__controller.selectID:
            self.__eventoActual = EventoDao.seleccionar(id_evento=self.__controller.selectID)
            imp = ImportanciaDao.seleccionar(id_importancia=self.__eventoActual.id_importancia)
            self.__id = self.__eventoActual.id_evento
            self.__titulo.set(self.__eventoActual.titulo)
            self.__descripcion = self.__eventoActual.descripcion
            self.__importancia.set(str(imp[0])+' '+imp[1])
            self.__fecha.set(self.__eventoActual.fecha_hora.strftime('%Y-%m-%d'))
            self.__duracion.set(self.__eventoActual.duracion)
            self.__hHora.set(self.__eventoActual.fecha_hora.strftime('%H'))
            self.__mHora.set(self.__eventoActual.fecha_hora.strftime('%M'))
        else:
            self.__id = None
            self.__descripcion = ''
            self.__inputDesc = None
            self.__tagFrame = None
            self.__limpiarCampos()

        self.__etiqueta.trace("w", lambda name, index, mode: self.__activarBtnEtiqueta())
        self.__cargarComponentes()
        if self.__controller.selectID:
            self.grid(column=0, row=0, sticky='nsew')


    def __cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a cada campo de los datos de un evento, disponibles para ser
        completados por el usuario."""
        self.__mainBlock = ttk.Frame(self)
        self.__mainBlock.columnconfigure([0,1], weight=1)
        self.__mainBlock.rowconfigure([0,1], weight=1)
        self.__block1 = ttk.Frame(self.__mainBlock, padding=1)
        self.__block1.columnconfigure([0,1], weight=1)
        self.__block1.rowconfigure([0,1,2,3,4,5,6,7], weight=1)
        self.__block2 = ttk.Frame(self.__mainBlock, padding=10)
        self.__block2.columnconfigure([0,1,3], weight=1)
        self.__block2.rowconfigure([0,1,2,3,4,5,6], weight=1)
        self.__block3 = ttk.Frame(self.__mainBlock, padding=1)
        self.__block3.columnconfigure(0, weight=1)
        self.__block3.rowconfigure(0, weight=1)

        # TITULO
        self.__title_label = ttk.Label(
            self.__block1,
            font=('Ubuntu', '12', 'bold'),
            text="Título: ",
            background=self.__controller.configTema['bgLabelTextNewEvent'],
            justify='center',
            width=5,
            padding= (5,0,0,0)
        )
        self.__title_label.grid(column=0, row=0, sticky='nsew', pady=5)
        vcmd_title = (self.__block1.register(self.__validate_title), '%P')
        ivcmd_title = (self.__block1.register(self.__on_invalid_title),)
        self.__inputTit = ttk.Entry(self.__block1,
                                    validate='focus', validatecommand=vcmd_title,
                                    invalidcommand=ivcmd_title,
                                    font=('Ubuntu Medium', '12', 'bold'), width=15,
                                    textvariable=self.__titulo, justify='right')
        self.__inputTit.grid(column=1, row=0, sticky='nsew', pady=5, padx=1)
        self.label_error_title = ttk.Label(self.__block1, foreground='red')
        self.label_error_title.grid(row=1, column=1, columnspan=1,sticky='nsew', padx=5)

        # DESCRIPCIÓN
        self.__content_label = ttk.Label(self.__block1, font=('Ubuntu', '12', 'bold'),
                                         background=self.__controller.configTema['bgLabelTextNewEvent'],
                                         padding=(5, 0, 0, 0), width=5, text="Descripción:",
                                         justify='left')
        self.__content_label.grid(column=0,
                                    row=2,
                                    columnspan=2,
                                    sticky='nsew',
                                    pady=5, padx=1)
        self.__inputDesc = tk.Text(self.__block1, font=('Ubuntu', '11'), height=10, width=10,
                                   background=self.__controller.configTema['bgLabelText'],
                                   foreground=self.__controller.configTema['fgText'])
        self.__inputDesc.insert('1.0', self.__descripcion)
        self.__inputDesc.grid(column=0, row=3, columnspan=2, sticky='nsew', pady=5, padx=1)

        # IMPORTANCIA
        self.__import_label = ttk.Label(self.__block1, font=('Ubuntu', '12', 'bold'),
                                        width=15, padding=(5,0,0,0),
                                        background=self.__controller.configTema['bgLabelTextNewEvent'],
                                        text="Importancia:", justify='left')
        self.__import_label.grid(column=0,
                                   row=4,
                                   sticky='nsew',
                                   pady=5, padx=1)

        self.__inputImp = ttk.Combobox(self.__block1, width=15, textvariable=self.__importancia, font=('Ubuntu', '11', 'bold'),
                                       values=self.__importancia_options, justify='center')
        self.__inputImp.set(self.__importancia.get())
        self.__inputImp.config(state='readonly')
        self.__inputImp.grid(column=1, row=4, sticky='nsew', pady=5, padx=1)

        # ETIQUETAS
        self.__btnAddTag = ttk.Button(self.__block1, text="Agregar Etiqueta:", command=self.__agregarEtiqueta,
                                      state='disabled', width=5)
        self.__btnAddTag.grid(column=0, row=5, sticky='nsew', pady=5, padx=1)
        self.__inputTag = ttk.Combobox(self.__block1, font=('Ubuntu', '11', 'bold'),
                                       width=15, textvariable=self.__etiqueta, justify='right')
        self.__inputTag.grid(column=1, row=5, sticky='nsew', pady=5, padx=2)
        self.__inputTag.bind('<KeyRelease>', self.update)
        self.__inputTag.bind("<<ComboboxSelected>>", self.callback)
        ttk.Label(self.__block1, text='Disponibles:', padding=5, font=('Ubuntu', '11', 'bold')).grid(column=0,
                                                                                                               row=6,
                                                                                                               columnspan=1,
                                                                                                               sticky='nsew')
        self.__lblTagsRest = ttk.Label(self.__block1, text='5', font=('Ubuntu', '12', 'bold'),
                                       foreground=self.__controller.configTema['Tags'], padding=5)
        self.__lblTagsRest.grid(column=1, row=6, columnspan=1, sticky='nsew')

        self.__tagFrame = ttk.Labelframe(self.__block1, text="Tags", borderwidth=6, relief='sunken')
        self.__tagFrame.grid(column=0, row=7, columnspan=2, sticky='nsew', padx=1, pady=5)

        if self.__controller.selectID:
            if self.__eventoActual.etiquetas:
                tags = self.__eventoActual.etiquetas.split(sep=',')
                for tag in tags:
                    self.__etiqueta.set(tag)
                    self.__agregarEtiqueta()
                event_tags = EtiquetaDao.seleccionar_evento_etiquetas(id_evento=self.__id)
                for tag in event_tags:
                    self.__listaEtiquetas.append((tag.id_etiqueta, tag.nombre))

        # CALENDARIO SELECCIONABLE
        self.__calFrame = ttk.Frame(self.__mainBlock, padding=1)
        self.__ventanaCal = tkCalendar(self.__calFrame, selectmode="day", date_pattern="y-mm-dd")
        self.__ventanaCal.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.__btnSel = ttk.Button(self.__calFrame, text="Seleccionar")
        self.__btnCan = ttk.Button(self.__calFrame, text="Cerrar", command=self.__cerrarCal)
        self.__btnSel.grid(column=0, row=1, pady=5, padx=5, sticky=tk.NE)
        self.__btnCan.grid(column=1, row=1, pady=5, padx=5, sticky=tk.NW)

        # FECHA
        ttk.Label(self.__block2, font=('Ubuntu', '12', 'bold'), text="Fecha:", width=10, justify='left').grid(column=0,
                                                                                                    row=0,
                                                                                                    columnspan=1,
                                                                                                    sticky='nsew',
                                                                                                    pady=5)
        self.__inputFecha = ttk.Entry(self.__block2, font=('Ubuntu', '11', 'bold'), textvariable=self.__fecha,
                                      state='readonly')
        self.__inputFecha.config(justify='center', width=10)
        self.__inputFecha.grid(column=1, row=0, columnspan=1, sticky='nsew', pady=5)
        self.__inputFecha.bind("<ButtonPress-1>", self.__seleccionarFechaEvento)

        # HORA
        hora = ttk.Label(self.__block2, font=('Ubuntu', '12', 'bold'), width=10, text="Hora:", justify="left")
        hora.grid(column=0, row=1, columnspan=1, sticky='nsew')
        self.__inputHora = ttk.Frame(self.__block2, width=10)
        diezHoras = list(map(lambda x: '0' + str(x), range(10)))
        self.__horas = diezHoras.copy()
        self.__horas.extend(map(lambda x: str(x), range(10, 24)))
        self.__min = diezHoras
        self.__min.extend(map(lambda x: str(x), range(10, 60)))
        comboHora = ttk.Combobox(self.__inputHora, font=('Ubuntu', '11', 'bold'), textvariable=self.__hHora,
                                 values=self.__horas, width=3, state='readonly', justify='right')
        comboHora.grid(column=0, row=0, sticky='nsew')
        comboMin = ttk.Combobox(self.__inputHora, font=('Ubuntu', '11', 'bold'), textvariable=self.__mHora,
                                values=self.__min, width=3, state='readonly', justify='right')
        comboMin.grid(column=2, row=0, sticky='nsew')
        ttk.Label(self.__inputHora, text=":", font=('Arial', 14), justify='left').grid(column=1, row=0,
                                                                                       sticky='nsew', padx=2)
        self.__inputHora.grid(column=1, row=1, pady=5)

        # DURACIÓN
        ttk.Label(self.__block2,
                    font=('Ubuntu', '12', 'bold'),
                    text="Duración:",
                    width=10,
                    justify='left').grid(column=0, row=2,
                    columnspan=1,
                    sticky='nsew',
                    pady=5)
        vcmd_duration = (self.__block2.register(self.__validate_duration), '%P')
        ivcmd_duration = (self.__block2.register(self.__on_invalid_duration), '%P')
        self.__minLblFrame = ttk.LabelFrame(self.__block2, text='Minutos', width=10)
        self.__inputDura = ttk.Entry(self.__minLblFrame,
                                     validate='focus', validatecommand=vcmd_duration,
                                     invalidcommand=ivcmd_duration,
                                     width=12,
                                     font=('Ubuntu', '11', 'bold'),
                                     textvariable=self.__duracion,
                                     justify='center')
        self.__inputDura.grid(column=0, row=0, columnspan=1, sticky='nsew')
        self.label_error_duration = ttk.Label(self.__block2, foreground='red', width=10)
        self.label_error_duration.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=1)
        self.__minLblFrame.grid(column=1, row=2, sticky='nsew', pady=5)

        # AGREGAR RECORDATORIO
        self.__lblFrameRecor = ttk.LabelFrame(self.__block2, text='Recordatorio', relief='flat', width=10)
        self.__canvas = tk.Canvas(self.__lblFrameRecor, width=40, height=40,
                           highlightbackground=self.__controller.configTema['hlbgCanvas'])
        self.__canvas.grid(column=0, row=0, sticky='nsew', pady=1)
        img = (Image.open(self.__controller.configTema['imagen']))
        resized_image = img.resize((40, 40), Image.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)
        self.__canvas.create_image(2, 2, anchor=tk.NW, image=new_image)
        self.__canvas.image = new_image
        self.__recorChBx = ttk.Checkbutton(self.__lblFrameRecor, command=self.__agregarRecor,
                                           variable=self.__checkValue)
        self.__recorChBx.grid(column=1, row=0, sticky='nsew', pady=5, padx=(5, 0))
        self.__inputRecor = ttk.Labelframe(self.__block2, text="Configurar", width=10)
        self.__lblFrameRecor.grid(row=4, column=0, sticky='nsew')

        # BOTONES ACEPTAR Y CANCELAR

        btnFrame = ttk.Frame(self.__block3)
        self.__btnAceptar = ttk.Button(btnFrame, style='btnAceptar.TButton', text="Aceptar",
                                       command=self.__enviarEvento, state='disabled')
        self.__btnAceptar.grid(column=0, row=0, padx=(0, 3))
        btnCancelar = ttk.Button(btnFrame, style='btnCancelar.TButton', text="Cancelar", command=self.__limpiarCampos)
        btnCancelar.grid(column=1, row=0, padx=(3, 0))
        btnFrame.grid(column=1, row=0, pady=5, sticky='nsew')
        if self.__titulo.get() != '':
            self.__btnAceptar['state'] = 'enabled'

        self.__block1.grid(column=0, row=0, rowspan=2, sticky='nsew')
        self.__block2.grid(column=1, row=1, sticky='nsew')
        self.__block3.grid(column=0, row=2, columnspan=2, sticky='nsew')
        self.__mainBlock.grid(column=0, row=0, sticky='nsew')

    def update(self, *args):
        options = []
        typed = self.__inputTag.get()
        if typed == '':
            tags = self.__tags_in_db
        else:
            tags = EtiquetaDao.seleccionar_nombre(typed)
        self.__inputTag['values'] = list(map(lambda x: str(x.id_etiqueta)+' '+x.nombre, tags))
        self.__inputTag.event_generate('<Down>')
        self.__inputTag.after(100, self.__inputTag.focus_set)

    def callback(self, e):
        selection = self.__inputTag.selection_get().split(' ')
        self.__inputTag.set(selection[1])
        self.__selectedOptionId = int(selection[0])

    def __validate_title(self, p):
        if p != '':
            self.__show_message_title()
            input_duracion = self.__inputDura.get()
            if str.isdigit(input_duracion):
                self.__btnAceptar['state'] = 'enabled'
            return True
        else:
            return False

    def __validate_duration(self, p):
        if str.isdigit(p):
            self.__show_message_duration()
            if self.__titulo.get() != '':
                self.__btnAceptar['state'] = 'enabled'
            return True
        else:
            return False

    def __show_message_duration(self, error='', color=None):
        self.label_error_duration['text'] = error
        self.__inputDura['foreground'] = color if color else self.__controller.configTema['fgText']

    def __show_message_title(self, error='', color=None):
        self.label_error_title['text'] = error
        self.__inputTit['foreground'] = color if color else self.__controller.configTema['fgText']

    def __on_invalid_duration(self, p):
        if p == "":
            self.__show_message_duration('Este campo es obligatorio', 'red')
        else:
            self.__show_message_duration('El valor debe ser numérico', 'red')
        self.__btnAceptar['state'] = 'disabled'

    def __on_invalid_title(self):
        self.__show_message_title('Este campo es obligatorio', 'red')
        self.__btnAceptar['state'] = 'disabled'

    def actualizar(self):
        self.__cargarComponentes()

    def __agregarRecor(self):
        """Es llamado al activar el widget CheckButton del label Recordatorio, y genera un frame que contiene
        los widgets relacionados a la fecha y hora del recordatorio para ser configurados por el usuario."""
        if self.__checkValue.get() == '1':
            # FECHA
            self.__inputFechaRecor = ttk.Entry(self.__inputRecor, font=('Ubuntu', '11', 'bold'),
                                               textvariable=self.__fechaRecor, state='readonly')
            self.__inputFechaRecor.config(justify='center', width=10)
            self.__fechaRecor.set(datetime.today().strftime('%Y-%m-%d'))
            self.__inputFechaRecor.grid(column=0, row=0, columnspan=1, sticky='nsew', pady=5)
            self.__inputFechaRecor.bind("<ButtonPress-1>", self.__seleccionarFechaRecor)
            # HORA
            self.__inputHoraRecor = ttk.Frame(self.__inputRecor)
            comboRecorHora = ttk.Combobox(self.__inputHoraRecor, font=('Ubuntu', '11', 'bold'),
                                          textvariable=self.__hRecor, values=self.__horas, width=3, state='readonly',
                                          justify='right')
            comboRecorHora.set(datetime.now().strftime('%H'))
            comboRecorHora.grid(column=0, row=0, columnspan=1, sticky='nsew')
            comboRecorMin = ttk.Combobox(self.__inputHoraRecor, font=('Ubuntu', '11', 'bold'),
                                         textvariable=self.__mRecor, values=self.__min, width=3, state='readonly',
                                         justify='right')
            comboRecorMin.set(datetime.now().strftime('%M'))
            comboRecorMin.grid(column=2, row=0, columnspan=1, sticky='nsew')
            ttk.Label(self.__inputHoraRecor, text=":", font=('Arial', '14', 'bold'), justify='left').grid(column=1,
                                                                                                          row=0,
                                                                                                          columnspan=1,
                                                                                                          sticky='nsew',
                                                                                                          padx=2)
            self.__inputHoraRecor.grid(column=0, row=1, sticky='nsew', pady=0)
            self.__inputRecor.grid(column=1, row=4, sticky='nsew', pady=0)
        else:
            self.__inputRecor.destroy()
            self.__inputRecor = ttk.Labelframe(self.__block2, text="Configurar")


    def __seleccionarFechaRecor(self, event):
        """Es llamado al hacer click en el campo fecha de la interfaz, desplegando un pequeño calendario gráfico que
        permite elegir una determinada fecha para el evento."""
        self.__desplegarCalendarioSeleccionable(self.__obtenerFechaRecor)

    def __seleccionarFechaEvento(self, event):
        """Es llamado al hacer click en el campo fecha del frame Recordatorio , desplegando un pequeño calendario gráfico que
       permite elegir una determinada fecha para el recordatorio."""
        self.__desplegarCalendarioSeleccionable(self.__obtenerFechaEvento)

    def __desplegarCalendarioSeleccionable(self, tipo):
        """Genera gráficamente la interfaz de un calendario que permite explorar y seleccionar fechas."""
        self.__btnSel.config(command=tipo)
        self.__calFrame.grid(row=0, column=1, sticky='e')

    def __cerrarCal(self):
        """Destruye el frame donde se generó el calendario para selección de fechas."""
        self.__calFrame.grid_remove()

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
            if self.__checkValue.get() == '1':
                stringRecor = self.__fechaRecor.get()+' '+self.__hRecor.get()+':'+self.__mRecor.get()+':00'
            else:
                stringRecor = None
            values = {
                'id_evento': self.__id,
                'titulo': self.__titulo.get(),
                'descripcion': self.__inputDesc.get("1.0", "end-1c"),
                'id_importancia': int(self.__importancia.get().split(' ')[0]),
                'fecha_hora': self.__fecha.get()+' '+self.__hHora.get()+':'+self.__mHora.get()+':00',
                'duracion': int(self.__duracion.get()),
                'etiquetas': None,
                'recordatorio': stringRecor
            }
            evento = Evento(**values)
            old_tags = list(filter(lambda tg: tg[0] != 0, self.__listaEtiquetas))
            new_tags = list(filter(lambda tg: tg[0] == 0, self.__listaEtiquetas))
            if self.__controller.selectID:  # actualización de un evento existente
                id_evento = self.__id
                EventoDao.actualizar(evento)
                tags_on_db = sorted(list(map(lambda x: x[1], EventoEtiquetaDao.seleccionar(id_evento))))
                old_tags_to_compare = sorted(list(map(lambda x: x[0], old_tags)))
                if old_tags_to_compare != tags_on_db:  # pregunta si se eliminaron etiquetas al actualizar
                    delete_tags = list(filter(lambda tg: tg not in old_tags_to_compare, tags_on_db))
                    for tag in delete_tags:  # se eliminan las relaciones de la tabla eventos_etiquetas en la db
                        EventoEtiquetaDao.eliminar(id_evento=id_evento, id_etiqueta=tag)
                    added_tags = list(filter(lambda tg: tg not in tags_on_db, old_tags_to_compare))
                    for tag in added_tags:  # se agregam las nuevas relaciones de la tabla eventos_etiquetas en la db
                        EventoEtiquetaDao.insertar(id_evento=id_evento, id_etiqueta=tag)
            else:  # Creación de un evento nuevo
                id_evento = EventoDao.insertar(evento)
                while old_tags: # si se seleccionaron etiquetas existentes, se procede a insertarlas en la tabla intermedia eventos_etiquetas
                    EventoEtiquetaDao.insertar(id_evento=id_evento, id_etiqueta=old_tags.pop()[0])
            while new_tags:
                id_etiqueta_insertada = EtiquetaDao.insertar(Etiqueta(nombre=new_tags.pop()[1]))
                EventoEtiquetaDao.insertar(id_evento=id_evento, id_etiqueta=id_etiqueta_insertada)

            # if len(new_tags) > 0: # si se crearon nuevas etiquetas (se ejecuta tanto para actualización como nuevo evento)
            #     id_etiquetas_insertadas = list(map(lambda x: EtiquetaDao.insertar(Etiqueta(nombre=x[1])), new_tags))  # etiqueta nueva
            #     for id_tag in id_etiquetas_insertadas:
            #         EventoEtiquetaDao.insertar(id_evento=id_evento, id_etiqueta=id_tag)  # nuevas relaciones en la tabla eventos_etiquetas

            if self.__id:
                messagebox.showinfo(title="Aviso", message="Evento actualizado con éxito!")
                self.__parent.destroy()
            else:
                messagebox.showinfo(title="Aviso", message="Evento agregado con éxito!")
                self.__limpiarCampos()
            self.__controller.actualizar()

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
        if self.__controller.selectID == None:
            value = fecha+' '+hora
            if EventoDao.eixiste_fecha_hora(fecha_hora=value):
                rdo = False
                messagebox.showerror(title="Error", message="'Ya existe un evento en la misma fecha y hora.\nPor favor elija otra fecha/hora.'")
            else:
                rdo = True
        else:
            rdo = True
        return rdo

    def __limpiarCampos(self):
        """Elimina el contenido de los widgets de la interfaz que haya completado el usuario o hayan sido autocompletados
        por modificación de un evento."""
        if self.__controller.selectID:
            self.__parent.destroy()
        else:
            self.__titulo.set('')
            self.__descripcion = ''
            self.__importancia.set(self.__importancia_options[0] if self.__importancia_options else '')
            self.__fecha.set(datetime.today().strftime('%Y-%m-%d'))
            self.__hHora.set(datetime.now().strftime('%H'))
            self.__mHora.set(datetime.now().strftime('%M'))
            self.__duracion.set('30')
            self.__fechaRecor.set(datetime.today().strftime('%Y-%m-%d'))
            if self.__inputDesc != None:
                self.__inputDesc.delete("1.0", "end-1c")
            if self.__checkValue.get() == '1':
                self.__recorChBx.invoke()
            if self.__ventanaCal != None:
                self.__cerrarCal()
            if self.__tagFrame != None:
                self.__tagFrame.destroy()
                self.__lblTagsRest['text'] = '5'
                self.__tagFrame = ttk.Labelframe(self.__block1, text="Tags", borderwidth=6, relief='sunken')
                self.__tagFrame.grid(column=0, row=7, columnspan=2, sticky='nsew')
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

        def deleteTag(tag):
            for tuple in self.__listaEtiquetas:
                if tag in tuple:
                    self.__listaEtiquetas.remove(tuple)
                    break

        def modificar1(event):
            tagLabel['relief'] = 'raised'

        def modificar2(event):
            tagLabel['relief'] = 'ridge'

        def eliminar(event):
            cant = int(self.__lblTagsRest['text'])
            if cant == 0:
                self.__lblTagsRest['foreground'] = self.__controller.configTema['Tags']
            self.__lblTagsRest['text'] = str(cant + 1)
            deleteTag(tagLabel["text"])
            tagLabel.destroy()

        if self.__etiqueta.get() not in list(map(lambda x: x[1], self.__listaEtiquetas)):
            cant = int(self.__lblTagsRest['text'])
            self.__lblTagsRest['text'] = str(cant - 1)
            if cant == 1:
                self.__lblTagsRest['foreground'] = 'red'
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

    def set_theme(self):
        self.__title_label.config(background=self.__controller.configTema['bgLabelTextNewEvent'])
        self.__content_label.config(background=self.__controller.configTema['bgLabelTextNewEvent'])
        self.__inputDesc.config(background=self.__controller.configTema['bgLabelText'])
        self.__inputDesc.config(foreground=self.__controller.configTema['fgText'])
        self.__import_label.config(background=self.__controller.configTema['bgLabelTextNewEvent'])
        self.__canvas.config(highlightbackground=self.__controller.configTema['hlbgCanvas'])
        img = (Image.open(self.__controller.configTema['imagen']))
        resized_image = img.resize((40, 40), Image.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)
        self.__canvas.create_image(2, 2, anchor=tk.NW, image=new_image)
        self.__canvas.image = new_image