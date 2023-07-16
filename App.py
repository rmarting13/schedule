import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime
from Archivo import BaseDeDatos
from db_context.evento_dao import EventoDao
from views.busqueda import FiltroDeEventos
from views.mensual import VistaMensual
from views.nuevo_evento import NuevoEventoVista
from views.popup import PopUp
from views.semanal import VistaSemanal

# Configuración de los colores de la interfaz según el tema
awdark = {'bgNombreDia': '#000',
          'bgSinEventos': '#555a57',
          'bgDiaMes': '#490d56',
          'bgHoy': '#6c33e1',
          'bgNoDiaMes': '#7f5c66',
          'bgLabelText': '#242421',
          'bgLabelNormal': '#595953',
          'fgText': 'white',
          'imagen': 'Temas/bell_dark_bg.png',
          'hlbgCanvas': '#33393b',
          'Tags': '#6aff00',
          'bgLabelTextNewEvent': '#2c1559'
          }

awlight = {'bgNombreDia': '#bfc9cb',
           'bgSinEventos': 'white',
           'bgDiaMes': '#bbbbba',
           'bgHoy': '#d9d000',
           'bgNoDiaMes': '#929290',
           'bgLabelText': 'white',
           'bgLabelNormal': '#e4e4e3',
           'fgText': 'black',
           'imagen': 'Temas/bell_light_bg.png',
           'hlbgCanvas': '#e8e8e7',
           'Tags': '#2f00ff',
           'bgLabelTextNewEvent': '#889feb'
           }


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        parent.title("Calendario de Eventos")
        self.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.resizable(True, True)
        self.configTema = awdark
        self.nombreTema = tk.StringVar()
        self.__primerInicio = True
        self.selectID = None
        self.frameTemas = ttk.LabelFrame(self, text='Cambiar Tema', padding=5)
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
        self.__lblReferencia = ttk.LabelFrame(self, text='Niveles de importancia', padding=5, borderwidth=5,
                                              relief='solid')
        ttk.Label(self.__lblReferencia, text='IMPORTANTE', font='Helvetica 8 bold', padding=(15, 5, 15, 5),
                  background='#7d0c0c', foreground='white', borderwidth=5, relief='solid', width=12).grid(column=0, row=0,
                                                                                                      pady=5, padx=5)
        ttk.Label(self.__lblReferencia, text='NORMAL', font='Helvetica 8 bold', padding=(27, 5, 0, 5),
                  background=self.configTema['bgLabelNormal'], borderwidth=5, relief='solid', width=12).grid(column=0,
                                                                                                             row=1,
                                                                                                             pady=5,
                                                                                                             padx=5)
        self.__lblReferencia.grid(column=0, row=2, columnspan=1, sticky=tk.N)
        self.__rightFrame = ttk.Frame(self, padding=5, borderwidth=2, relief="groove")
        self.__cargarVistaSemanal()
        self.__rightFrame.grid(column=1, row=0, rowspan=3, padx=5, pady=5)

    def __cargarMenuLateral(self):
        """Muestra en el frame izquierdo, todos los botones corresponidentes a la interfaz del menú principal."""
        self.__menuFrame = ttk.Labelframe(self, text="Menu", padding=5, borderwidth=2, relief="groove")
        self.btnModif = ttk.Button(self.__menuFrame, text="Modificar Evento", style='Botones.TButton', width=15,
                                   command=self.__modificar, padding=5, state='disabled')
        self.btnModif.grid(column=0, row=4, padx=5, pady=5)
        self.__btnVistaSem = ttk.Button(self.__menuFrame, text="Vista Semanal", width=15,
                                        command=self.__cargarVistaSemanal, padding=5)
        self.__btnVistaSem.grid(column=0, row=0, padx=5, pady=5)
        self.__btnVistaMen = ttk.Button(self.__menuFrame, text="Vista Mensual", width=15,
                                        command=self.__cargarVistaMensual, padding=5)
        self.__btnVistaMen.grid(column=0, row=1, padx=5, pady=5)
        self.__btnNuevo = ttk.Button(self.__menuFrame, text="Nuevo Evento", command=self.__nuevoEvento, padding=5,
                                     width=15, )
        self.__btnNuevo.grid(column=0, row=2, pady=5, padx=5)
        self.__btnBuscar = ttk.Button(self.__menuFrame, text="Buscar Evento", width=15, command=self.__buscar,
                                      padding=5)
        self.__btnBuscar.grid(column=0, row=3, padx=5, pady=5)
        self.btnElim = ttk.Button(self.__menuFrame, text="Eliminar Evento", width=15, command=self.__eliminar,
                                  padding=5, state='disabled')
        self.btnElim.grid(column=0, row=5, padx=5, pady=5)
        self.__menuFrame.grid(column=0, row=0, padx=5, pady=5, sticky=tk.N)

    def __cargarVistaSemanal(self):
        """Mestra en el frame derecho, los widgets que representan una semana, incluyendo los días y la tabla
        con eventos de cada día."""
        self.__frameMen = None
        self.__frameFiltro = None
        self.__rightFrame.destroy()
        self.__rightFrame = ttk.Frame(self, padding=5, borderwidth=2, relief="groove")
        ttk.Label(self.__rightFrame, text='Vista Semanal', font=('Century Gothic', '30')).grid(column=0, row=0, pady=10)
        self.__frameSem = VistaSemanal(self.__rightFrame, self)
        self.__rightFrame.grid(column=1, row=0, rowspan=3, padx=5, pady=5)
        self.__btnVistaSem['state'] = 'disabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'enabled'
        self.btnModif['state'] = 'disabled'
        self.btnElim['state'] = 'disabled'
        self.__btnNuevo['state'] = 'enabled'

    def __cargarVistaMensual(self):
        """Mestra en el frame derecho, los widgets que representan un mes, incluyendo los días y la tabla
        con eventos de cada día."""
        self.__frameSem = None
        self.__frameFiltro = None
        self.__rightFrame.destroy()
        self.__rightFrame = ttk.Frame(self, padding=0, borderwidth=2, relief="groove")
        self.__frameMen = VistaMensual(self.__rightFrame, self)
        self.__rightFrame.grid(column=1, row=0, rowspan=3, padx=0, pady=0)
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'disabled'
        self.btnModif['state'] = 'disabled'
        self.btnElim['state'] = 'disabled'
        self.__btnNuevo['state'] = 'enabled'

    def __crearEvento(self, txt):
        """Muestra en el frame derecho, la interfaz del formulario que debe completar el usuario para crear un evento."""
        self.__rightFrame.destroy()
        self.__rightFrame = ttk.Frame(self, padding=5, borderwidth=2, relief="groove")
        ttk.Label(self.__rightFrame, text=txt, font=('Century Gothic', '30')).grid(column=0, row=0, pady=10)
        NuevoEventoVista(self.__rightFrame, self).grid()
        self.__rightFrame.grid(column=1, row=0, rowspan=3, padx=5, pady=5)
        if txt == 'Modificar Evento':
            self.__btnNuevo['state'] = 'enabled'
        else:
            self.__btnNuevo['state'] = 'disabled'
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnBuscar['state'] = 'enabled'
        self.__btnVistaMen['state'] = 'enabled'
        self.btnModif['state'] = 'disabled'
        self.btnElim['state'] = 'disabled'

    def __nuevoEvento(self):
        """Es llamado al presionar el botón Nuevo Evento, y llama al método __crearEvento pero sin
        rellenar los campos del formulario."""
        self.selectID = None
        self.__crearEvento('Nuevo Evento')

    def __buscar(self):
        """Muestra en el frame derecho, la interfaz de búsqueda y filtro."""
        self.__frameMen = None
        self.__frameSem = None
        self.__rightFrame.destroy()
        self.__rightFrame = ttk.Frame(self, padding=5, borderwidth=2, relief="groove")
        ttk.Label(self.__rightFrame, text='Búsqueda', font=('Century Gothic', '30')).grid(column=0, row=0, pady=10)
        self.__frameFiltro = FiltroDeEventos(self.__rightFrame, self)
        self.__rightFrame.grid(column=1, row=0, rowspan=3, padx=5, pady=5)
        self.__btnBuscar['state'] = 'disabled'
        self.__btnVistaMen['state'] = 'enabled'
        self.__btnVistaSem['state'] = 'enabled'
        self.__btnNuevo['state'] = 'enabled'

    def __modificar(self):
        """Es llamado al presionar el botón Modificar, y llama al método __crearEvento con los campos
        autocompletados por los datos del evento a modificar."""
        self.__crearEvento('Modificar Evento')

    def __eliminar(self):
        """Es llamado al presionar el botón Eliminar, llamando al método borrarEvento de la clase archivo
        y le pasa como parámetro el atributo __selectID, el cual contiene ID del evento seleccionado de 
        la tabla de eventos de alguna vista (Mensual, Semanal, Búsqueda), luego actualiza la vista que se 
        encuentre activa en ese momento."""
        EventoDao.eliminar(id_evento=self.selectID)
        PopUp(self).mensaje('Evento eliminado con éxito!')
        if self.__frameFiltro != None:
            self.__frameFiltro.actualizar()
        if self.__frameSem != None:
            self.__frameSem.actualizar()
        if self.__frameMen != None:
            self.__frameMen.actualizar()

    def setTheme(self):
        """Cambia la configuración del tema elegido en la interfaz. Para que los cambios
        surtan efecto se volverán a cargar los widgets y frames de la interfaz."""
        s = ttk.Style()
        if self.__primerInicio:
            s.theme_use(self.nombreTema.get())
            s.configure('lblName.TLabel', font=('Nueva Std Cond', '10', 'bold'))
            s.configure('WeekFrame.TFrame', background='#9763f8')
            s.configure('TButton', font=('Verdana', '8', 'bold'))
            s.map('btnAceptar.TButton',
                  background=[('!active', '#0047cc'), ('pressed', '#03009d'), ('active', '#3b7fff')])
            s.map('btnCancelar.TButton',
                  background=[('!active', '#d40000'), ('pressed', '#d46300'), ('active', '#ff3d45')])
            s.map('btnSigAnt.TButton',
                  background=[('!active', '#6a20a2'), ('pressed', '#4a1572'), ('active', '#a046e5')])
            self.__primerInicio = False
        else:
            opt = PopUp(self).advertencia()
            if opt == True:
                s.theme_use(self.nombreTema.get())
                if self.nombreTema.get() == 'awdark':
                    s.configure('lblName.TLabel', font=('Nueva Std Cond', '10', 'bold'))
                    s.configure('WeekFrame.TFrame', background='#9763f8')
                    s.configure('TButton', font=('Verdana', '8', 'bold'))
                    s.map('btnAceptar.TButton',
                          background=[('!active', '#0047cc'), ('pressed', '#03009d'), ('active', '#3b7fff')])
                    s.map('btnCancelar.TButton',
                          background=[('!active', '#d40000'), ('pressed', '#d46300'), ('active', '#ff3d45')])
                    s.map('btnSigAnt.TButton',
                          background=[('!active', '#6a20a2'), ('pressed', '#4a1572'), ('active', '#a046e5')])
                    self.configTema = awdark
                else:
                    s.configure('lblName.TLabel', font=('Nueva Std Cond', '10', 'bold'))
                    s.configure('TButton', font=('Verdana', '8', 'bold'))
                    s.configure('WeekFrame.TFrame', background='#185ceb')
                    s.map('btnAceptar.TButton',
                          background=[('!active', '#0ed145'), ('pressed', '#1f9d43'), ('active', '#2cfe67')])
                    s.map('btnCancelar.TButton',
                          background=[('!active', '#ff0000'), ('pressed', '#b40000'), ('active', '#ff5252')])
                    s.map('btnSigAnt.TButton',
                          background=[('!active', '#53a9f4'), ('pressed', '#0082f4'), ('active', '#88c2f5')])
                    self.configTema = awlight
                self.__rightFrame.destroy()
                self.cargarComponentes()

if __name__ == '__main__':
    root = tk.Tk()
    root.tk.call("lappend", "auto_path", "Temas")
    root.tk.call('package', 'require', 'awdark')
    root.tk.call('package', 'require', 'awlight')
    App(root).grid()
    root.mainloop()
