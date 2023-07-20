import tkinter as tk
from tkinter import ttk, messagebox
from db_context.evento_dao import EventoDao
from views.busqueda import FiltroDeEventos
from views.mensual import VistaMensual
from views.nuevo_evento import NuevoEventoVista
from views.semanal import VistaSemanal
from themes import config


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        parent.title("Calendario de Eventos")
        self.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.resizable(False, False)
        self.configTema = config.awdark
        self.parent = parent
        self.parent.configure(bg=self.configTema['mainBg'])
        self.nombreTema = tk.StringVar()
        self.selectID = None
        self.frameTemas = ttk.LabelFrame(self, text='Temas', padding=5)
        radBtn = ttk.Radiobutton(self.frameTemas, text="Oscuro", value="awdark", padding=5, variable=self.nombreTema,
                                 command=self.setTheme)
        radBtn.grid(column=0, row=0)
        radBtn.invoke()
        self.cargarComponentes()
        self.columnconfigure([0,1], weight=1)
        self.rowconfigure([0,1,2], weight=1)

    def cargarComponentes(self):
        """Muestra en la app los widgets del menú lateral y de la vista semanal
        la cual es la vista predeterminada al ejecutar la aplicación."""
        self.__cargarMenuLateral()
        ttk.Radiobutton(self.frameTemas, text="Claro", value="awlight", padding=5, variable=self.nombreTema,
                        command=self.setTheme).grid(column=0, row=1)
        self.frameTemas.grid(column=0, row=1, pady=5)
        self.__lblReferencia = ttk.LabelFrame(self, text='Referencias', padding=2, borderwidth=5,
                                              relief='solid')
        ttk.Label(self.__lblReferencia, text='IMPORTANTE', font='Helvetica 8 bold',
                  background='#7d0c0c', foreground='white', borderwidth=5, relief='solid', width=12).grid(column=0, row=0,
                                                                                                      pady=2, padx=2)
        self.__lbl_normal = ttk.Label(self.__lblReferencia, text='NORMAL', font='Helvetica 8 bold',
                  background=self.configTema['bgLabelNormal'], borderwidth=5, relief='solid', width=12)
        self.__lbl_normal.grid(column=0, row=1, pady=2, padx=2)
        self.__lblReferencia.grid(column=0, row=2, columnspan=1, sticky=tk.N)

        #VISTA SEMANAL
        self.__view_frame = ttk.Frame(self, padding=0, borderwidth=2, relief="groove")
        self.__title_label = ttk.Label(self.__view_frame, text='Vista Semanal', font=('Century Gothic', '30'))
        self.__title_label.grid(column=0, row=0, pady=10)
        self.__week_widget = VistaSemanal(self.__view_frame, self)
        self.__week_widget.grid(column=0, row=1)
        self.__view_frame.grid(column=1, row=0, rowspan=3, padx=5, pady=5)

        # VISTA MENSUAL
        self.__month_widget = VistaMensual(self.__view_frame, self)

        #NUEVO EVENTO
        self.__new_event_widget = NuevoEventoVista(self.__view_frame, controller=self)

        #ACTUALIZAR EVENTO
        self.__update_widget = None

        #BUSCAR EVENTO
        self.__search_widget = FiltroDeEventos(self.__view_frame, self)

    def __cargarMenuLateral(self):
        """Muestra en el frame izquierdo, todos los botones corresponidentes a la interfaz del menú principal."""
        self.__menuFrame = ttk.Labelframe(self, text="Menu", padding=5, borderwidth=2, relief="groove")
        self.btnModif = ttk.Button(self.__menuFrame, text="Modificar", style='Botones.TButton', width=10,
                                   command=self.__modificar, padding=4, state='disabled')
        self.btnModif.grid(column=0, row=4, padx=2, pady=2)
        self.__btnVistaSem = ttk.Button(self.__menuFrame, text="Semana", width=10,
                                        command=self.__cargarVistaSemanal, padding=3)
        self.__btnVistaSem.grid(column=0, row=0, padx=2, pady=2)
        self.__btnVistaMen = ttk.Button(self.__menuFrame, text="Mes", width=10,
                                        command=self.__cargarVistaMensual, padding=3)
        self.__btnVistaMen.grid(column=0, row=1, padx=2, pady=2)
        self.__btnNuevo = ttk.Button(self.__menuFrame, text="Nuevo", command=self.__nuevoEvento, padding=3,
                                     width=10, )
        self.__btnNuevo.grid(column=0, row=2, pady=2, padx=2)
        self.__btnBuscar = ttk.Button(self.__menuFrame, text="Filtrar", width=10, command=self.__buscar,
                                      padding=3)
        self.__btnBuscar.grid(column=0, row=3, padx=2, pady=2)
        self.btnElim = ttk.Button(self.__menuFrame, text="Eliminar", width=10, command=self.__eliminar,
                                  padding=3, state='disabled')
        self.btnElim.grid(column=0, row=5, padx=2, pady=2)
        self.__menuFrame.grid(column=0, row=0, padx=2, pady=2, sticky=tk.N)

    def __cargarVistaSemanal(self):
        """Mestra en el frame derecho, los widgets que representan una semana, incluyendo los días y la tabla
        con eventos de cada día."""
        self.__month_widget.grid_remove()
        self.__new_event_widget.grid_remove()
        self.__search_widget.grid_remove()
        self.__title_label.config(text='Vista Semanal')
        self.__week_widget.grid(column=0, row=1)
        self.__btnVistaSem['state'] = 'disabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'enabled'
        self.btnModif['state'] = 'disabled'
        self.btnElim['state'] = 'disabled'
        self.__btnNuevo['state'] = 'enabled'

    def __cargarVistaMensual(self):
        """Mestra en el frame derecho, los widgets que representan un mes, incluyendo los días y la tabla
        con eventos de cada día."""
        self.__new_event_widget.grid_remove()
        self.__search_widget.grid_remove()
        self.__week_widget.grid_remove()
        self.__title_label.grid_remove()
        self.__view_frame.config(padding=5)
        self.__month_widget.grid(column=0, row=0, sticky='nsew')
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'disabled'
        self.btnModif['state'] = 'disabled'
        self.btnElim['state'] = 'disabled'
        self.__btnNuevo['state'] = 'enabled'

    def __nuevoEvento(self):
        """Muestra en el frame derecho, la interfaz del formulario que debe completar el usuario para crear un evento."""
        self.selectID = None
        self.__search_widget.grid_remove()
        self.__week_widget.grid_remove()
        self.__month_widget.grid_remove()
        self.__title_label.config(text='Nuevo Evento')
        self.__title_label.grid()
        self.__new_event_widget.grid(column=0, row=1)
        self.__btnNuevo['state'] = 'disabled'
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'enabled'
        self.btnModif['state'] = 'disabled'
        self.btnElim['state'] = 'disabled'


    def __buscar(self):
        """Muestra en el frame derecho, la interfaz de búsqueda y filtro."""
        self.__week_widget.grid_remove()
        self.__month_widget.grid_remove()
        self.__new_event_widget.grid_remove()
        self.__title_label.config(text='Búsqueda')
        self.__title_label.grid()
        self.__search_widget.grid(column=0, row=1)
        self.__btnBuscar['state'] = 'disabled'
        self.__btnVistaMen['state'] = 'enabled'
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnNuevo['state'] = 'enabled'

    def __modificar(self):
        """Es llamado al presionar el botón Modificar, y llama al método __crearEvento con los campos
        autocompletados por los datos del evento a modificar."""
        self.__btnNuevo['state'] = 'enabled'
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'enabled'
        self.btnModif['state'] = 'disabled'
        self.btnElim['state'] = 'disabled'
        ventana = tk.Toplevel(self, bg=self.configTema['mainBg'])
        ttk.Label(ventana, text='Cargando datos...', background=self.configTema['mainBg'],
                  font='Ubuntu 12 bold',
                  foreground=self.configTema['fgText']).grid(row=0, column=0, sticky='nsew', padx=100, pady=100)
        ventana.title("Actualizar Evento")
        ventana.grid()
        NuevoEventoVista(ventana, controller=self)



    def __eliminar(self):
        """Es llamado al presionar el botón Eliminar, llamando al método borrarEvento de la clase archivo
        y le pasa como parámetro el atributo __selectID, el cual contiene ID del evento seleccionado de 
        la tabla de eventos de alguna vista (Mensual, Semanal, Búsqueda), luego actualiza la vista que se 
        encuentre activa en ese momento."""
        EventoDao.eliminar(id_evento=self.selectID)
        messagebox.showinfo(title='Aviso', message='Evento eliminado con éxito!')
        self.actualizar()

    def actualizar(self):
        self.__week_widget.actualizar()
        self.__month_widget.actualizar()
        self.__search_widget.actualizar()

    def setTheme(self):
        """Cambia la configuración del tema elegido en la interfaz. Para que los cambios
        surtan efecto se volverán a cargar los widgets y frames de la interfaz."""
        s = ttk.Style()
        s.theme_use(self.nombreTema.get())
        if self.nombreTema.get() == 'awdark':
            s.configure('lblName.TLabel', font=('Nueva Std Cond', '10', 'bold'))
            s.configure('WeekFrame.TFrame', background='#960000')
            s.configure('DayFrame.TFrame', background='#58278c')
            s.configure('NoDayFrame.TFrame', background='#424242')
            s.configure('TButton', font=('Verdana', '8', 'bold'))
            s.map('btnAceptar.TButton',
                  background=[('!active', '#0047cc'), ('pressed', '#03009d'), ('active', '#3b7fff')])
            s.map('btnCancelar.TButton',
                  background=[('!active', '#d40000'), ('pressed', '#d46300'), ('active', '#ff3d45')])
            s.map('btnSigAnt.TButton',
                  background=[('!active', '#6a20a2'), ('pressed', '#4a1572'), ('active', '#a046e5')])
            self.configTema = config.awdark
            self.parent.configure(bg=self.configTema['mainBg'])
        else:
            s.configure('lblName.TLabel', font=('Nueva Std Cond', '10', 'bold'))
            s.configure('TButton', font=('Verdana', '8', 'bold'))
            s.configure('WeekFrame.TFrame', background='#185ceb')
            s.configure('DayFrame.TFrame', background=config.awlight['bgDiaMes'])
            s.configure('NoDayFrame.TFrame', background=config.awlight['bgNoDiaMes'])
            s.map('btnAceptar.TButton',
                  background=[('!active', '#0ed145'), ('pressed', '#1f9d43'), ('active', '#2cfe67')])
            s.map('btnCancelar.TButton',
                  background=[('!active', '#ff0000'), ('pressed', '#b40000'), ('active', '#ff5252')])
            s.map('btnSigAnt.TButton',
                  background=[('!active', '#53a9f4'), ('pressed', '#0082f4'), ('active', '#88c2f5')])
            self.configTema = config.awlight
            self.parent.configure(bg=self.configTema['mainBg'])
        #self.__lbl_normal.config(background=self.configTema['bgLabelNormal'])
        self.__week_widget.set_theme()
        self.__month_widget.set_theme()
        self.__new_event_widget.set_theme()


if __name__ == '__main__':
    root = tk.Tk()
    root.tk.call("lappend", "auto_path", "themes")
    root.tk.call('package', 'require', 'awdark')
    root.tk.call('package', 'require', 'awlight')
    App(root).grid()
    root.mainloop()
