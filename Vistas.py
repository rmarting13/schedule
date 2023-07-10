import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, END, messagebox
from datetime import datetime
from calendar import Calendar 
from tkcalendar import Calendar as tkCalendar
from Archivo import BaseDeDatos

class Calendario(Calendar):
    """Clase que representa un calendario."""
    def __init__(self):
        super().__init__(firstweekday=6)
        self.__strMesLargo = ('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
        self.__strMesCorto = ('Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic')
        self.__strDiaLargo = ('Lúnes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo')
        self.__strDiaCorto = ('Lu','Ma','Mi','Ju','Vi','Sa','Do')

    def nombreDelMes(self, mes, tipo=0):
        """Retorna un string indicando el nombre del Mes de acuerdo al número ingresado por parámetro. El parámetro tipo
        indica si el nombre es formato largo o formato corto."""
        if tipo == 0:
            cad = self.__strMesCorto[mes-1]
        else:
            cad = self.__strMesLargo[mes-1]
        return cad
    
    def nombreDelDia(self, dia, tipo=0):
        """Retorna un string indicando el nombre del Día de la semana, de acuerdo al número ingresado por parámetro.
        El parámetro tipo indica si el nombre es formato largo o formato corto."""
        if tipo == 0:
            cad = self.__strDiaCorto[dia-1]
        else:
            cad = self.__strDiaLargo[dia-1]
        return cad
    
    def matrizMensual(self, anio, mes):
        """Retorna una matriz con los días del mes y año pasados por parámetro. Cada fila de la matriz
        representa una semana, cuyos días son valores enteros y los días fuera del mes se representan con un 0."""
        return self.monthdatescalendar(anio, mes)

    def listaDeSemanas(self, anio, mes):
        """"Retorna una lista cuyos elementos son listas de valores del tipo datetime.date(), las cuales
        representan cada semana del mes. La primer y ultima lista puede contener los ultimos días del mes
        anterior y/o los primeros días posterior que se incluyen en la primer y ultima semana respectivamente."""
        iterableDias = list(self.itermonthdates(anio,mes))
        listaSemanas = []
        ini = 0; fin = 7
        for i in range(6): 
            if len(iterableDias[ini:fin]) != 0:
                listaSemanas.append(iterableDias[ini:fin])
                ini += 7; fin += 7
        return listaSemanas

class PopUp(ttk.Frame):
    """Clase que representa una ventana emergente con un cuadro de diálogo."""
    def __init__(self, parent):
        super().__init__(parent)
        self.seleccion = None

    @staticmethod
    def mensaje(msj):
        """Muestra un mensaje recibido por parámetro en el cuadro de diálogo del widget."""
        messagebox.showinfo(message=msj)

    @staticmethod
    def advertencia():
        return messagebox.askyesno(message='Esta acción reiniciará la aplicación.\n¿Desea continuar?')

class VistaEvento(ttk.Frame):
    """Clase que representa gráficamente los datos de un evento."""

    def __init__(self,parent,datos,gui):
        super().__init__(parent, padding=(20))
        self.__parent = parent
        self.__parent.title('Evento')
        self.__gui = gui
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)
        self.__datos = datos
        self.cargarComponentes()

    def cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a cada campo de los datos de un evento."""
        ttk.Label(self,text='TITULO:',style='lblName.TLabel',padding=5,borderwidth=2,relief='raised').grid(column=0,row=0,padx=5,pady=5,sticky=tk.W)
        self.__lblTitulo = ttk.Label(self,text=self.__datos['TITULO'],font=('Ubuntu','12','bold'),padding=5,background=self.__gui.configTema['bgLabelText'])
        self.__lblTitulo.grid(column=1,row=0,padx=5,pady=5,sticky=tk.W)
        ttk.Label(self,text='DESCRIPCION:',style='lblName.TLabel',padding=5,borderwidth=2,relief='raised').grid(column=0,row=1,padx=5,pady=5,sticky=tk.W)
        self.__lblDesc = tk.Text(self,font=('Ubuntu','10'),width=60,height=10,background=self.__gui.configTema['bgLabelText'],foreground=self.__gui.configTema['fgText'])
        self.__lblDesc.insert(tk.INSERT,self.__datos['DESCRIPCION'])
        self.__lblDesc['state'] = 'disabled'
        self.__lblDesc.grid(column=0,row=2,columnspan=4,padx=5,pady=5,sticky=tk.W)
        ttk.Label(self,text='FECHA Y HORA:',style='lblName.TLabel',padding=5,borderwidth=2,relief='raised').grid(column=2,row=0,padx=5,pady=5,sticky=tk.W)
        self.__lblFecha = ttk.Label(self,text=self.__datos['FECHA']+' - '+self.__datos['HORA'],font=('Ubuntu','11','bold'),padding=5,background=self.__gui.configTema['bgLabelText'])
        self.__lblFecha.grid(column=3,row=0,padx=5,pady=5,sticky=tk.W)
        ttk.Label(self,text='DURACION:',style='lblName.TLabel',padding=5,borderwidth=2,relief='raised').grid(column=0,row=3,padx=5,pady=5,sticky=tk.W)
        self.__lblDura = ttk.Label(self,text=self.__datos['DURACION'],font=('Ubuntu','11','bold'),padding=5,background=self.__gui.configTema['bgLabelText'])
        self.__lblDura.grid(column=1,row=3,padx=5,pady=5,sticky=tk.W)
        ttk.Label(self,text='IMPORTANCIA:',style='lblName.TLabel',padding=5,borderwidth=2,relief='raised').grid(column=2,row=3,padx=5,pady=5,sticky=tk.W)
        self.__lblImpor = ttk.Label(self,text=self.__datos['IMPORTANCIA'],font=('Ubuntu','11','bold'),padding=5,background=self.__gui.configTema['bgLabelText'])
        self.__lblImpor.grid(column=3,row=3,padx=5,pady=5,sticky=tk.W)
        ttk.Label(self,text='ETIQUETAS: ',style='lblName.TLabel',padding=5,borderwidth=2,relief='raised').grid(column=0,row=4,padx=5,pady=5,sticky=tk.W)
        self.__lblTag = ttk.Label(self,text=self.__datos['ETIQUETA'],font=('Ubuntu','11','bold'),padding=5,background=self.__gui.configTema['bgLabelText'])
        self.__lblTag.grid(column=1,row=4,columnspan=4,padx=5,pady=5,sticky=tk.W)
        canvas = tk.Canvas(self, width= 40, height= 40,borderwidth=0,highlightbackground=self.__gui.configTema['hlbgCanvas'])
        canvas.grid(column=0,row=5,columnspan=1,sticky=(tk.E),pady=5)
        img = (Image.open(self.__gui.configTema['imagen']))
        resized_image = img.resize((40,40), Image.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(2,2,anchor=tk.NW, image=new_image)
        canvas.image = new_image
        self.__lblRecor = ttk.Label(self,text=self.__datos['RECORDATORIO'],style='lblName.TLabel',padding=5,background=self.__gui.configTema['bgLabelText'])
        self.__lblRecor.grid(column=1,row=5,padx=5,pady=5)

class VistaSemanal(ttk.Frame):
    """Clase que representa gráficamente los días de una semana y sus eventos"""
    def __init__(self, parent, gui):
        super().__init__(parent, padding=(5))
        self.__gui = gui
        self.grid(column=0,row=1,sticky=(tk.N, tk.S, tk.E, tk.W))
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
        ttk.Button(self,style='btnSigAnt.TButton',text="Anterior",command=self.__retroceder).grid(column=0,row=0,pady=5,padx=5)
        ttk.Button(self,style='btnSigAnt.TButton',text="Siguiente",command=self.__avanzar).grid(column=2,row=0,pady=5,padx=5)
        self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)
        
        for week in self.__semanas:
            if self.__fechaActualDT.date() in week:
                self.__semanaActual = self.__semanas.index(week)
                break

        self.__lblMes = ttk.Label(self,text=self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual),font=('Century Gothic','12','bold'),padding=5)
        self.__lblMes.grid(column=1,row=0,columnspan=1,pady=5)
        self.actualizar()

    def actualizar(self):
        """Vuelve a cargar los widgets de los días de la semana y sus tablas con eventos actualizada desde el archivo .csv"""
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0,row=1,columnspan=3,pady=5)

    def __mostrarSemana(self,semana):
        """Genera y retorna un frame que contiene cada uno de los widgets que representan los días de la semana,
        incluyendo sus respectivas tablas con eventos."""
        self.__listaTablas = []
        fechasConEventos = self.__db.mapearFechas()
        weekFrame = ttk.Frame(self,style='WeekFrame.TFrame',padding=5)
        for col, dia in enumerate(semana):
            eventFrame = ttk.Frame(weekFrame,borderwidth=2,relief="solid")
            lblDia = ttk.Label(eventFrame,width=14,text=self.__cal.nombreDelDia(col,1)+'  '+dia.strftime('%d/%m'),font='Helvetica 12 bold',padding=5,background=self.__gui.configTema['bgNombreDia'])
            lblDia.grid(column=0,row=0,pady=5,padx=0)
            if col == 0:
                lblDia['foreground'] = 'red'
            if col == 6:
                lblDia['foreground'] = 'blue'
            if dia == self.__fechaActualDT.date():
                lblDia['background'] = self.__gui.configTema['bgHoy']
            eventFrame.grid(column=col,row=1,pady=0,padx=2)
            self.__frameEventos = ttk.Frame(eventFrame)
            diaFormat = dia.strftime('%d/%m/%Y')
            if diaFormat in map(lambda x: x[1],fechasConEventos):
                eventosDelDia = self.__db.leerDatosFiltrados({'FECHA':diaFormat})
                self.__crearTablaTreeView(self.__frameEventos,eventosDelDia)
            else:
                ttk.Label(self.__frameEventos,text='SIN EVENTOS',font='Helvetica 12',padding=(15,75,15,75),background=self.__gui.configTema['bgSinEventos']).grid()
            self.__frameEventos.grid(column=0,row=1,pady=5,padx=0)
        return weekFrame

    def __crearTablaTreeView(self,frame,datos):
        """Crea una tabla tk.TreeView en la que se muestran cada uno de los eventos correspondientes."""
        tablaTreeView = ttk.Treeview(frame,columns=('id','ev'),show="headings",selectmode="extended",height=7,padding=5)
        tablaTreeView["displaycolumns"] = ('ev')
        tablaTreeView.column('ev',width=120,anchor=tk.W)
        tablaTreeView.heading('ev',text="Eventos",anchor=tk.CENTER)
        tablaTreeView.grid(column=0,row=0)
        tablaTreeView.bind("<ButtonPress-1>", self.__onClickCell)
        tablaTreeView.bind("<Double-Button-1>", self.__doubleOnClickCell)
        for row in datos:
            cad = row['HORA']+'  '+row['TITULO']
            valores = (row['ID'],cad)
            tablaTreeView.insert('',tk.END,tags=row['IMPORTANCIA'],values=valores)
        tablaTreeView.tag_configure(tagname='Importante',font='Helvetica 8 bold',background='red',foreground='white')
        self.__listaTablas.append(tablaTreeView)

    def __onClickCell(self,event):
        """Define el comportamiento ciertos widgets al hacer un click seleccionando un evento de la tabla."""
        tabla = list(filter(lambda x: x.focus()!='',self.__listaTablas))
        if len(tabla)!=0 and tabla[0] != None:
            self.__gui.btnElim['state'] = 'enabled'
            self.__gui.btnModif['state'] = 'enabled'
            item = tabla[0].item(tabla[0].focus(),'values')
            self.__gui.selectID = item[0]
            tabla[0].selection_remove(tabla[0].selection()[0])
            tabla[0].focus("")
        else:
            self.__gui.btnModif['state'] = 'disabled'
            self.__gui.btnElim['state'] = 'disabled'
    
    def __doubleOnClickCell(self,event):
        """Define el comportamiento ciertos widgets al hacer doble click sobre un evento de la tabla."""
        tabla = list(filter(lambda x: x.focus()!='',self.__listaTablas))
        if len(tabla)!=0 and tabla != None:
            item = tabla[0].item(tabla[0].focus(),'values')
            id = item[0]
            evento = self.__db.filtrarPorID(id)
            ventana = tk.Toplevel(self)
            VistaEvento(ventana,evento,self.__gui)
            ventana.grid()
            tabla[0].selection_remove(tabla[0].selection()[0])
            tabla[0].focus("")

    def __retroceder(self):
        """Permite generar gráficamente los widgets la semana anterior."""
        self.__frameWeek.destroy()
        if self.__semanaActual-1 < 0:
            if self.__mesActual-1 < 1:
                self.__anioActual -= 1
                self.__mesActual = 12
            else:
                self.__mesActual -= 1
            self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)
            self.__semanaActual = len(self.__semanas)-2
        else:
            self.__semanaActual -= 1
        self.__lblMes['text'] = self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual)
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0,row=1,columnspan=3,pady=5)
        
    def __avanzar(self):
        """Permite generar gráficamente los widgets la semana siguiente."""
        self.__frameWeek.destroy()
        if self.__semanaActual+1 >= len(self.__semanas)-1:
            if self.__mesActual+1 > 12:
                self.__anioActual += 1
                self.__mesActual = 1
            else:
                self.__mesActual += 1
            self.__lblMes['text'] = self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual)
            self.__semanas = self.__cal.listaDeSemanas(self.__anioActual, self.__mesActual)
            self.__semanaActual = 0
        else:
            self.__semanaActual += 1
        self.__frameWeek = self.__mostrarSemana(self.__semanas[self.__semanaActual])
        self.__frameWeek.grid(column=0,row=1,columnspan=3,pady=5)

class VistaMensual(ttk.Frame):
    """Clase que representa gráficamente los días de un mes completo y sus eventos"""
    def __init__(self, parent, gui):
        super().__init__(parent, padding=(0))
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)
        self.__gui = gui
        self.__fechaActualDT = datetime.today()
        self.__anioActual = int(self.__fechaActualDT.strftime('%Y'))
        self.__mesActual = int(self.__fechaActualDT.strftime('%m'))
        self.__db = BaseDeDatos('EventosDB.csv')
        self.__cal = Calendario()
        self.__mes = self.__cal.matrizMensual(self.__anioActual,self.__mesActual)
        self.__cargarComponentes()

    def __cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a la interfaz de la vista mensual."""
        ttk.Button(self,style='btnSigAnt.TButton',text="Anterior",command=self.__anterior).grid(column=0,row=0,pady=5,padx=(5,0),)
        ttk.Button(self,style='btnSigAnt.TButton',text="Siguiente",command=self.__siguiente).grid(column=2,row=0,pady=5,padx=(0,5))
        self.__lblNombreMes = ttk.Label(self,text=self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual),font=('Century Gothic','12','bold'),padding=5,borderwidth=2,relief="sunken")
        self.__lblNombreMes.grid(column=1,row=0,columnspan=1,padx=0,pady=5)
        self.__mesFrame = ttk.Frame(self,padding=5)
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0,row=1,columnspan=3,pady=0,padx=0)

    def actualizar(self):
        """Vuelve a cargar los widgets de los días del mes y sus tablas con eventos actualizadas desde el archivo .csv"""
        self.__mesFrame = ttk.Frame(self,padding=5)
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0,row=1,columnspan=3,pady=0,padx=0)

    def __mostrarMes(self,frame, mes):
        """Genera y retorna un frame que contiene cada uno de los widgets que representan los días del mes, incluyendo
        sus respectivas tablas con eventos."""
        self.__listaTablas = []
        fechasConEventos = self.__db.mapearFechas()
        monthFrame = ttk.Frame(frame,style='WeekFrame.TFrame',padding=5)
        self.labels = []
        dias = []
        for m in range(7):
            labelDay = ttk.Label(monthFrame,width=9,text=self.__cal.nombreDelDia(m,1),font='Helvetica 12 bold',padding=(18,0,5,0),background=self.__gui.configTema['bgNombreDia'],borderwidth=2,relief='solid')
            if labelDay['text'] == 'Domingo':
                labelDay['foreground'] = 'red'
            if labelDay['text'] == 'Sábado':
                labelDay['foreground'] = 'blue'
            labelDay.grid(column=m,row=0,padx=2,pady=2)
            dias.append(labelDay)
        self.labels.append(dias)
        if len(self.__mes) == 6:
            pad = (21,18,21,18)
            height = 2
        else:
            pad = (21,28,21,28)
            height = 3
        for week in self.__mes:
            labels_row = []
            for c, date in enumerate(week):
                frameDay = ttk.Frame(monthFrame,borderwidth=2,relief='solid')
                label = ttk.Label(frameDay,width=10,text=str(date.day),font='Helvetica 12 bold',padding=(5,0,5,0),background=self.__gui.configTema['bgDiaMes'])
                label.grid(padx=2,pady=2)
                diaFormat = date.strftime('%d/%m/%Y')
                if diaFormat in map(lambda x: x[1],fechasConEventos):
                    eventosDelDia = self.__db.leerDatosFiltrados({'FECHA':diaFormat})
                    self.__crearTablaTreeView(frameDay,eventosDelDia,height)
                else:
                    ttk.Label(frameDay,text='SIN EVENTOS',font='Helvetica 8',width=10,padding=pad,background=self.__gui.configTema['bgSinEventos']).grid()
                frameDay.grid(row=self.__mes.index(week)+1, column=c,padx=2,pady=2)
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
    
    def __crearTablaTreeView(self,frame,datos,altura):
        """Crea una tabla tk.TreeView en la que se muestran cada uno de los eventos correspondientes."""
        tablaTreeView = ttk.Treeview(frame,columns=('id','ev'),show='',selectmode="extended",height=altura,padding=5)
        tablaTreeView["displaycolumns"] = ('ev')
        tablaTreeView.column('ev',width=95,anchor=tk.W)
        tablaTreeView.heading('ev',text="Eventos",anchor=tk.CENTER)
        tablaTreeView.grid(column=0,row=1)
        tablaTreeView.bind("<ButtonPress-1>", self.__onClickCell)
        tablaTreeView.bind("<Double-Button-1>", self.__doubleOnClickCell)
        for row in datos:
            valores = (row['ID'],row['TITULO'])
            tablaTreeView.insert('',tk.END,tags=row['IMPORTANCIA'],values=valores)
        tablaTreeView.tag_configure(tagname='Importante',font='Helvetica 8 bold',background='red',foreground='white')
        self.__listaTablas.append(tablaTreeView)
    
    def __onClickCell(self,event):
        """Define el comportamiento ciertos widgets al hacer un click seleccionando un evento de la tabla."""
        tabla = list(filter(lambda x: x.focus()!='',self.__listaTablas))
        if len(tabla)!=0 and tabla[0] != None:
            self.__gui.btnElim['state'] = 'enabled'
            self.__gui.btnModif['state'] = 'enabled'
            item = tabla[0].item(tabla[0].focus(),'values')
            self.__gui.selectID = item[0]
            tabla[0].selection_remove(tabla[0].selection()[0])
            tabla[0].focus("")
        else:
             self.__gui.btnModif['state'] = 'disabled'
             self.__gui.btnElim['state'] = 'disabled'
    
    def __doubleOnClickCell(self,event):
        """Define el comportamiento ciertos widgets al hacer doble click sobre un evento de la tabla."""
        tabla = list(filter(lambda x: x.focus()!='',self.__listaTablas))
        if len(tabla)!=0 and tabla != None:
            item = tabla[0].item(tabla[0].focus(),'values')
            id = item[0]
            evento = self.__db.filtrarPorID(id)
            ventana = tk.Toplevel(self)
            VistaEvento(ventana,evento,self.__gui)
            ventana.grid()
            tabla[0].selection_remove(tabla[0].selection()[0])
            tabla[0].focus("")

    def __anterior(self):
        """Permite generar gráficamente los widgets del mes anterior."""
        self.__mesFrame.destroy()
        if self.__mesActual-1 < 1:
            self.__anioActual -= 1
            self.__mesActual = 12
        else:
            self.__mesActual -= 1
        self.__mes = self.__cal.matrizMensual(self.__anioActual,self.__mesActual)
        self.__lblNombreMes['text'] = self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual)
        self.__mesFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0,row=1,columnspan=3,pady=5,padx=5)
    
    def __siguiente(self):
        """Permite generar gráficamente los widgets del mes siguiente."""
        self.__mesFrame.destroy()
        if self.__mesActual+1 > 12:
            self.__anioActual += 1
            self.__mesActual = 1
        else:
            self.__mesActual += 1
        self.__mes = self.__cal.matrizMensual(self.__anioActual,self.__mesActual)
        self.__lblNombreMes['text'] = self.__cal.nombreDelMes(self.__mesActual,1)+' - '+str(self.__anioActual)
        self.__mesFrame = ttk.Frame(self,padding=5,borderwidth=2, relief="groove")
        self.__mostrarMes(self.__mesFrame, self.__mesActual).grid()
        self.__mesFrame.grid(column=0,row=1,columnspan=3,pady=5,padx=5)
       
class FiltroDeEventos(ttk.Frame):
    """Clase que representa gráficamente la interfaz de búsqueda y filtro de eventos."""
    def __init__(self,parent,gui):
        super().__init__(parent, padding=(5))
        self.grid(column=0,row=1,sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)
        self.__parent = gui
        self.__inputTitulo = tk.StringVar()
        self.__inputEtiqueta = tk.StringVar()
        self.__checkValueTitulo = tk.StringVar()
        self.__checkValueEtiqueta = tk.StringVar()
        self.__db = BaseDeDatos('EventosDB.csv')
        self.__cargarComponentes()
        
    def __cargarComponentes(self):
        """Muestra en un frame, los widgets correspondientes a la interfaz de la vista de búsqueda."""
        ttk.Checkbutton(self,text="Filtrar por Título:",padding=5,command=self.__filtrarPorTitulo,variable=self.__checkValueTitulo).grid(column=0,row=0,columnspan=1,sticky=tk.W)
        ttk.Checkbutton(self,text="Filtrar por Etiquetas:",padding=5,command=self.__filtrarPorEtiqueta,variable=self.__checkValueEtiqueta).grid(column=0,row=1,columnspan=1,sticky=tk.W)
        self.__inputTit = ttk.Entry(self,font=('Ubuntu','11'),width=30,textvariable=self.__inputTitulo,state='disabled')
        self.__inputTit.grid(column=1,row=0,columnspan=1,padx=5,pady=5,sticky=tk.W)
        self.__inputTag = ttk.Entry(self,font=('Ubuntu','11'),width=30,textvariable=self.__inputEtiqueta,state='disabled')
        self.__inputTag.grid(column=1,row=1,columnspan=1,padx=5,pady=5,sticky=tk.W)
        self.__btnBuscar = ttk.Button(self,text='Buscar',command=self.__buscar,state='disabled')
        self.__btnBuscar.grid(column=0,row=2,columnspan=3,pady=5,padx=5)
        self.__frameResultados = ttk.Labelframe(self,text='Resultados',padding=5,borderwidth=2,relief='sunken')
        
        columnas = ('id','ti','fe','ho','im')
        self.__tablaTreeView = ttk.Treeview(self.__frameResultados,columns=columnas,show='headings',selectmode="extended",displaycolumns=('ti','fe','ho','im'))
        
        self.__tablaTreeView.column('id',width=30,anchor=tk.CENTER)
        self.__tablaTreeView.column('ti',width=200,anchor=tk.CENTER)
        self.__tablaTreeView.column('fe',width=70,anchor=tk.CENTER)
        self.__tablaTreeView.column('ho',width=50,anchor=tk.CENTER)
        self.__tablaTreeView.column('im',width=80,anchor=tk.CENTER)

        self.__tablaTreeView.heading("id",text="Id",anchor=tk.CENTER)
        self.__tablaTreeView.heading("fe",text="Fecha",anchor=tk.CENTER)
        self.__tablaTreeView.heading("ho",text="Hora",anchor=tk.CENTER)
        self.__tablaTreeView.heading("ti",text="Título",anchor=tk.CENTER)
        self.__tablaTreeView.heading("im",text="Importancia",anchor=tk.CENTER)
        
        self.__sclBar = ttk.Scrollbar(self.__frameResultados,orient=tk.VERTICAL,command=self.__tablaTreeView.yview)
        self.__sclBar.grid(column=1,row=0,sticky=tk.NS)
        self.__tablaTreeView.configure(yscroll=self.__sclBar.set)
        self.__tablaTreeView.grid(column=0,row=0)
        self.__frameResultados.grid(column=0,row=3,columnspan=3)
        self.__tablaTreeView.bind("<ButtonPress-1>", self.__onClickCell)
        self.__tablaTreeView.bind("<Double-Button-1>", self.__doubleOnClickCell)
        self.__insertarElementos(self.__db.leerArchivoCompleto())

    def actualizar(self):
        """Vuelve a cargar la tabla con eventos actualizada desde el archivo .csv"""
        self.__buscar()

    def __onClickCell(self, event):
        """Define el comportamiento ciertos widgets al hacer un click seleccionando un evento de la tabla."""
        if self.__tablaTreeView.focus() != "":
            self.__parent.btnElim['state'] = 'enabled'
            self.__parent.btnModif['state'] = 'enabled'
            self.__parent.selectID = self.__tablaTreeView.item(self.__tablaTreeView.focus(),'values')[0]
        else:
            self.__parent.btnModif['state'] = 'disabled'
            self.__parent.btnElim['state'] = 'disabled'
    
    def __doubleOnClickCell(self,event):
        """Define el comportamiento ciertos widgets al hacer doble click sobre un evento de la tabla."""
        id = self.__tablaTreeView.item(self.__tablaTreeView.focus(),'values')[0]
        evento = self.__db.filtrarPorID(id)
        ventana = tk.Toplevel(self)
        VistaEvento(ventana,evento,self.__parent)
        ventana.grid()

    def __insertarElementos(self, datos):
        """Inserta en una talba tk.TreeView los eventos recibidos por parámetro."""
        for row in datos:
            valores = list(row.values())
            valores.pop(4)
            self.__tablaTreeView.insert('',tk.END,tags=valores[4],values=valores[:5])
            self.__tablaTreeView.tag_configure(tagname='Importante', font='Helvetica 8 bold',background='red',foreground='white')

    def __buscar(self):
        """Es llamado al presionar el botón Buscar en la interfaz gráfica, obteniendo los datos
        de los campos de filtro de la interfaz y enviándolos a la clase BaseDeDatos para que filtre dichos datos
        en el archivo csv. Una vez obtenido los eventos filtrados, los inserta en la tabla de eventos."""
        self.__tablaTreeView.delete(*self.__tablaTreeView.get_children())
        filtro = {}
        if self.__checkValueTitulo.get() not in ['0','']:
            filtro.update({'TITULO':self.__inputTitulo.get()})
        if self.__checkValueEtiqueta.get() not in ['0','']:
            filtro.update({'ETIQUETA':self.__inputEtiqueta.get()})
        if len(filtro.keys()) != 0:
            self.__listaFiltrada = self.__db.leerDatosFiltrados(filtro)
            self.__insertarElementos(self.__listaFiltrada)
        else:
            self.__insertarElementos(self.__db.leerArchivoCompleto())

    def __filtrarPorTitulo(self):
        """Es llamado al activar o desactivar el widget CheckButton del label "Filtrar por Título" en la interfa gráfica,
        y define el comportamiento de los widgets relacionados, habilitando/deshabilitando campos y botones."""
        if self.__checkValueTitulo.get() == '1':
            self.__inputTit['state'] = 'enabled'
            self.__btnBuscar['state'] = 'enabled'
        else:
            self.__inputTit.delete(0,END)
            self.__inputTit['state'] = 'disabled'
        self.__habilitarBtnBuscar()

    def __filtrarPorEtiqueta(self):
        """Es llamado al activar o desactivar el widget CheckButton del label "Filtrar por Etiqueta" en la interfa gráfica,
        y define el comportamiento de los widgets relacionados, habilitando/deshabilitando campos y botones."""
        if self.__checkValueEtiqueta.get() == '1':
            self.__inputTag['state'] = 'enabled'
        else:
            self.__inputTag.delete(0,END)
            self.__inputTag['state'] = 'disabled'
        self.__habilitarBtnBuscar()

    def __habilitarBtnBuscar(self):
        """Habilita o deshabilita el botón 'Buscar' de acuerdo a si al menos uno de los campos de filtrado está
        habilitado o no"""
        if  self.__inputTit['state'] == 'enabled' or self.__inputTag['state'] == 'enabled':
            self.__btnBuscar['state'] = 'enabled'
        else:
            self.__btnBuscar['state'] = 'disabled'

class NuevoEventoVista(ttk.Frame):
    """Clase que representa gráficamente la interfaz de creación/modificación de un evento de calendario."""
    def __init__(self, parent, gui):
        super().__init__(parent,padding=(20))
        self.__guiParent = gui
        self.grid(column=0,row=1,sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)
        self.__db = BaseDeDatos('EventosDB.csv')
        self.__ventanaCal = None
        self.__tamTag = 0
        self.__rowTag = 0
        self.__columnTag = -1
        self.__listaEtiquetas = []
        self.__id = ''
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
        if self.__guiParent.selectID != None:
            existente = self.__db.filtrarPorID(self.__guiParent.selectID)
            self.__id = existente['ID']
            self.__titulo.set(existente['TITULO'])
            self.__descripcion = existente['DESCRIPCION']
            self.__importancia.set(existente['IMPORTANCIA'])
            self.__fecha.set(existente['FECHA'])
            self.__duracion.set(existente['DURACION'])
            self.__hHora.set(existente['HORA'][:2])
            self.__mHora.set(existente['HORA'][3:])
        else:
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
        self.__block1 = ttk.Frame(self.__mainBlock,padding=10)
        self.__block1.grid_columnconfigure(0, weight=1)
        self.__block2 = ttk.Frame(self.__mainBlock,padding=10)
        self.__block2.grid_columnconfigure(0, weight=1)

        #TITULO
        ttk.Label(self.__block1,font=('Ubuntu','12','bold'),text="Título: ",justify='left',width=6).grid(column=0,row=0,columnspan=1,sticky=(tk.W),pady=5)
        self.__inputTit = ttk.Entry(self.__block1,font=('Ubuntu Medium','12','bold'),width=35,textvariable=self.__titulo,justify='right')
        self.__inputTit.grid(column=1,row=0,columnspan=1,sticky=(tk.W),pady=5)
        
        #DESCRIPCIÓN
        ttk.Label(self.__block1,font=('Ubuntu','12','bold'),text="Descripción:",justify='left').grid(column=0,row=1,columnspan=3,sticky=(tk.W),pady=5)
        self.__inputDesc = tk.Text(self.__block1,font=('Ubuntu','11'),height=10, width=60,background=self.__guiParent.configTema['bgLabelText'],foreground=self.__guiParent.configTema['fgText'])
        self.__inputDesc.insert('1.0',self.__descripcion)
        self.__inputDesc.grid(column=0,row=2,columnspan=2,sticky=(tk.E),pady=5)
        
        #IMPORTANCIA
        ttk.Label(self.__block1,font=('Ubuntu','12','bold'),text="Importancia:",justify='left').grid(column=0,row=4,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputImp = ttk.Combobox(self.__block1,textvariable=self.__importancia,font=('Ubuntu','11','bold'),values=['Importante','Normal'],justify='center')
        self.__inputImp.set(self.__importancia.get())
        self.__inputImp.config(state='readonly',width=12)
        self.__inputImp.grid(column=1,row=4,columnspan=1,sticky=(tk.E),pady=5)
        
        #ETIQUETAS
        self.__tagFrame = ttk.Labelframe(self.__block1,text="Tags",borderwidth=6,relief='sunken')
        self.__tagFrame.grid(column=0,row=7,columnspan=2)
        self.__btnAddTag = ttk.Button(self.__block1,text="Agregar Etiqueta:",command=self.__agregarEtiqueta,state='disabled')
        self.__btnAddTag.grid(column=0,row=5,columnspan=1,sticky=(tk.W),pady=5)
        ttk.Label(self.__block1,text='Etiquetas Disponibles:',padding=5,font=('Ubuntu','11','bold')).grid(column=0,row=6,columnspan=1,sticky=tk.W)
        self.__lblTagsRest = ttk.Label(self.__block1,text='5',font=('Ubuntu','12','bold'),foreground=self.__guiParent.configTema['Tags'],padding=5)
        self.__lblTagsRest.grid(column=1,row=6,columnspan=1,sticky=tk.W)
        self.__inputTag = ttk.Entry(self.__block1,font=('Ubuntu','11'),width=35,textvariable=self.__etiqueta,justify='right')        
        self.__inputTag.grid(column=1,row=5,columnspan=1,sticky=(tk.E),pady=5)
        if self.__guiParent.selectID != None:
            tags = self.__db.filtrarPorID(self.__guiParent.selectID)['ETIQUETA'].split(sep=', ')
            for tag in tags:
                self.__etiqueta.set(tag)
                self.__agregarEtiqueta()
        
        #FECHA
        ttk.Label(self.__block2,font=('Ubuntu','12','bold'),text="Fecha:",justify='left').grid(column=0,row=0,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputFecha = ttk.Entry(self.__block2,font=('Ubuntu','11','bold'),textvariable=self.__fecha,state='readonly')
        self.__inputFecha.config(justify='center',width=15)
        self.__inputFecha.grid(column=1,row=0,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputFecha.bind("<ButtonPress-1>", self.__seleccionarFechaEvento)

        #HORA
        hora=ttk.Label(self.__block2,font=('Ubuntu','12','bold'),text="Hora:",justify="left")
        hora.grid(column=0,row=1,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputHora = ttk.Labelframe(self.__block2)
        diezHoras = list(map(lambda x:'0'+str(x),range(10)))
        self.__horas = diezHoras.copy()
        self.__horas.extend(map(lambda x:str(x),range(10,24)))
        self.__min = diezHoras
        self.__min.extend(map(lambda x:str(x),range(10,60)))
        comboHora = ttk.Combobox(self.__inputHora,font=('Ubuntu','11','bold'), textvariable=self.__hHora,values=self.__horas,width=3,state='readonly',justify='right')
        comboHora.grid(column=0,row=0,columnspan=1,sticky=(tk.N))
        comboMin = ttk.Combobox(self.__inputHora,font=('Ubuntu','11','bold'), textvariable=self.__mHora,values=self.__min,width=3,state='readonly',justify='right')
        comboMin.grid(column=2,row=0,columnspan=1,sticky=(tk.N))
        self.__inputHora.grid(column=1,row=1,sticky=(tk.E),pady=0)
        ttk.Label(self.__inputHora,text=":",font=('Arial',14),justify='left').grid(column=1,row=0,columnspan=1,sticky=(tk.N),padx=2)

        #DURACIÓN
        ttk.Label(self.__block2,font=('Ubuntu','12','bold'),text="Duración:",justify='left').grid(column=0,row=2,columnspan=1,sticky=(tk.E),pady=5)
        self.__inputDura = ttk.Combobox(self.__block2,font=('Ubuntu','11','bold'),textvariable=self.__duracion,values=['1 hora','3 horas','6 horas','8 horas','12 horas','Todo el día'],justify='center')
        self.__inputDura.config(state='readonly',width=12)
        self.__inputDura.grid(column=1,row=2,columnspan=1,sticky=(tk.E),pady=5)

        #AGREGAR RECORDATORIO
        canvas= tk.Canvas(self.__block2, width= 40, height= 40,highlightbackground=self.__guiParent.configTema['hlbgCanvas'])
        canvas.grid(column=0,row=3,columnspan=1,sticky=(tk.E),pady=5)
        img= (Image.open(self.__guiParent.configTema['imagen']))
        resized_image= img.resize((40,40), Image.LANCZOS)
        new_image= ImageTk.PhotoImage(resized_image)
        canvas.create_image(2,2, anchor=tk.NW, image=new_image)
        canvas.image = new_image
        self.__recorChBx = ttk.Checkbutton(self.__block2,text="Recordatorio",command=self.__agregarRecor,variable=self.__checkValue)
        self.__recorChBx.grid(column=1,row=3,columnspan=1,sticky=(tk.W),pady=5,padx=(5,0))
        self.__inputRecor = ttk.Labelframe(self.__block2, text="Configurar recordatorio")

        #BOTONES ACEPTAR Y CANCELAR
        btnFrame = ttk.Labelframe(self.__block2)
        btnFrame.grid(column=1,row=5,pady=5,columnspan=2,sticky=tk.E,)
        self.__btnAceptar = ttk.Button(btnFrame,style='btnAceptar.TButton',text="Aceptar",command=self.__enviarEvento, state='disabled')
        self.__btnAceptar.grid(column=0,row=0,padx=(0,3))
        btnCancelar = ttk.Button(btnFrame,style='btnCancelar.TButton',text="Cancelar",command=self.__limpiarCampos)
        btnCancelar.grid(column=1,row=0,padx=(3,0))
        self.__titulo.trace("w", lambda name, index, mode: self.__activarBtnAceptar())
        if self.__titulo.get() != '':
            self.__btnAceptar['state'] = 'enabled'

        self.__block1.grid(column=0,row=0,rowspan=2)
        separator = ttk.Separator(self, orient='vertical',)
        separator.grid(column=1,row=0,rowspan=2, padx=5,sticky=tk.EW)
        self.__block2.grid(column=2,row=0,rowspan=2)
        self.__mainBlock.grid(column=0,row=0)
    
    def actualizar(self):
        self.__cargarComponentes()

    def __agregarRecor(self):
        """Es llamado al activar el widget CheckButton del label Recordatorio, y genera un frame que contiene
        los widgets relacionados a la fecha y hora del recordatorio para ser configurados por el usuario."""
        if self.__checkValue.get() == '1':
            #FECHA
            ttk.Label(self.__inputRecor,font=('Ubuntu','12','bold'),text="Fecha:",justify='left').grid(column=0,row=0,columnspan=1,sticky=(tk.E),pady=5,padx=(0,5))
            self.__inputFechaRecor = ttk.Entry(self.__inputRecor,font=('Ubuntu','11','bold'),textvariable=self.__fechaRecor,state='readonly')
            self.__inputFechaRecor.config(justify='center',width=15)
            self.__inputFechaRecor.grid(column=1,row=0,columnspan=1,sticky=(tk.W),pady=5)
            self.__inputFechaRecor.bind("<ButtonPress-1>", self.__seleccionarFechaRecor)
            #HORA
            ttk.Label(self.__inputRecor,font=('Ubuntu','12','bold'),text="Hora:",justify="left").grid(column=0,row=1,columnspan=1,sticky=(tk.E),pady=5,padx=(0,5))
            self.__inputHoraRecor = ttk.Labelframe(self.__inputRecor)
            comboRecorHora = ttk.Combobox(self.__inputHoraRecor,font=('Ubuntu','11','bold'), textvariable=self.__hRecor,values=self.__horas,width=3,state='readonly',justify='right')
            comboRecorHora.set(datetime.now().strftime('%H'))
            comboRecorHora.grid(column=0,row=0,columnspan=1,sticky=(tk.N))
            comboRecorMin = ttk.Combobox(self.__inputHoraRecor,font=('Ubuntu','11','bold'),textvariable=self.__mRecor,values=self.__min,width=3,state='readonly',justify='right')
            comboRecorMin.set(datetime.now().strftime('%M'))
            comboRecorMin.grid(column=2,row=0,columnspan=1,sticky=(tk.N))
            ttk.Label(self.__inputHoraRecor,text=":",font=('Arial','14','bold'),justify='left').grid(column=1,row=0,columnspan=1,sticky=(tk.N),padx=2)
            self.__inputHoraRecor.grid(column=1,row=1,sticky=(tk.E),pady=0)
            self.__inputRecor.grid(column=1,row=4,sticky=(tk.E),pady=0)
        else:
            #self.__cerrarCal()
            self.__inputRecor.destroy()
            self.__inputRecor = ttk.Labelframe(self.__block2, text="Configurar recordatorio")
 
    def __seleccionarFechaRecor(self,event):
       """Es llamado al hacer click en el campo fecha de la interfaz, desplegando un pequeño calendario gráfico que
       permite elegir una determinada fecha para el evento."""
       if self.__ventanaCal == None:
           self.__desplegarCalendarioSeleccionable(self.__obtenerFechaRecor)

    def __seleccionarFechaEvento(self,event):
        """Es llamado al hacer click en el campo fecha del frame Recordatorio , desplegando un pequeño calendario gráfico que
       permite elegir una determinada fecha para el recordatorio."""
        if self.__ventanaCal == None:
            self.__desplegarCalendarioSeleccionable(self.__obtenerFechaEvento)
    
    def __desplegarCalendarioSeleccionable(self,tipo):
        """Genera gráficamente la interfaz de un calendario que permite explorar y seleccionar fechas."""
        self.__ventanaCal = tkCalendar(self.__mainBlock, selectmode="day", date_pattern="dd/mm/y")
        self.__ventanaCal.grid(column=3,row=0,columnspan=2,padx=5,pady=5,sticky=tk.S)
        self.__btnSel = ttk.Button(self.__mainBlock, text="Seleccionar", command=tipo)
        self.__btnSel.grid(column=3,row=1,pady=5,padx=5,sticky=tk.NE)
        self.__btnCan = ttk.Button(self.__mainBlock, text="Cerrar", command=self.__cerrarCal)
        self.__btnCan.grid(column=4,row=1,pady=5,padx=5,sticky=tk.NW)
    
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
        self.__inputFechaRecor.delete(0,tk.END)
        self.__inputFechaRecor.insert(0, self.__ventanaCal.get_date())
        self.__inputFechaRecor['state'] = 'readonly'
        self.__cerrarCal()
       
    def __obtenerFechaEvento(self):
        """Es llamado al presionar el botón "Seleccionar" del frame del calendario de selección de fechas, obteniendo
        del mismo la fecha seleccionada e insertándola en el widget del campo fecha del frame Evento."""
        self.__inputFecha['state'] = 'normal'
        self.__inputFecha.delete(0,END)
        self.__inputFecha.insert(0, self.__ventanaCal.get_date())
        self.__inputFecha['state'] = 'readonly'
        self.__cerrarCal()    
    
    def __enviarEvento(self):
        """Recoge y almacena en un diccionario todos los strings obenidos de los widgets de la interfaz, enviándolo
        a un objeto de la clase BaseDeDatos para grabar los datos del evento o modificar uno existente."""
        fecha = self.__fecha.get(); hora = self.__hHora.get()+':'+self.__mHora.get()
        if self.__validarFechaYHora(fecha,hora):
            tags = ", ".join(self.__listaEtiquetas)
            if self.__checkValue.get() == '1':
                stringRecor = self.__fechaRecor.get()+' - '+self.__hRecor.get()+':'+self.__mRecor.get()
            else:
                stringRecor = 'No'
            datos = {
                    'ID': self.__id,
                     'TITULO':self.__titulo.get(),
                    'DESCRIPCION':self.__inputDesc.get("1.0","end-1c"),
                    'IMPORTANCIA':self.__importancia.get(),
                    'FECHA':self.__fecha.get(),
                    'HORA':self.__hHora.get()+':'+self.__mHora.get(),
                    'DURACION':self.__duracion.get(),
                    'ETIQUETA': tags,
                    'RECORDATORIO': stringRecor
                    }
            self.__db.grabarDato(datos)
            PopUp(self).mensaje('Evento agregado con éxito!')
            self.__limpiarCampos()

    def __activarBtnAceptar(self):
        """Habilita o deshabilita el estado del botón "Aceptar", de acuerdo al seguimiento de la traza del campo del
        widget correspondiente al Título del evento. De esta manera, mientras el usuario no ingrese al menos un caracter
        en el campo de Título entonces el botón no se habilitará."""
        if self.__titulo.get() == '':
            self.__btnAceptar['state']='disabled'
        else:
            self.__btnAceptar['state']='enabled'

    def __validarFechaYHora(self,fecha,hora):
        """Determina si la fecha seleccionada del evento seleccionada por el usuario, coincide o nó con algún evento ya existente.
        En caso de ser cierto, ejecuta una ventana emergente con un cuadro de diálogo indicandole al usuario la situación."""
        if self.__guiParent.selectID == None:
            rdo = (fecha,hora) not in self.__db.mapearFechasYHoras()
            if not rdo:
                PopUp(self).mensaje('Ya existe un evento en la misma fecha y hora.\nPor favor elija otra fecha/hora.')
        else:
            rdo = True
        return rdo

    def __limpiarCampos(self):
        """Elimina el contenido de los widgets de la interfaz que haya completado el usuario o hayan sido autocompletados
        por modificación de un evento."""
        self.__titulo.set('')
        self.__descripcion = ''
        self.__importancia.set('')
        self.__fecha.set(datetime.today().strftime('%d/%m/%Y'))
        self.__hHora.set(datetime.now().strftime('%H'))
        self.__mHora.set(datetime.now().strftime('%M'))
        self.__duracion.set('1 hora')
        self.__importancia.set('Normal')
        self.__fechaRecor.set(datetime.today().strftime('%d/%m/%Y'))
        if self.__inputDesc != None:
            self.__inputDesc.delete("1.0","end-1c")
        if self.__checkValue.get() == '1':
            self.__recorChBx.invoke()
        if self.__ventanaCal != None:
            self.__cerrarCal()
        if self.__tagFrame != None:
            self.__tagFrame.destroy()
            self.__tagFrame = ttk.Labelframe(self.__block1,text="Tags",borderwidth=6,relief='sunken')
            self.__tagFrame.grid(column=0,row=6,columnspan=2)
        self.__listaEtiquetas.clear()
        
    def __activarBtnEtiqueta(self):
        """Habilita o deshabilita el estado del botón Agregar Etiqueta, de acuerdo al seguimiento de la traza
        del campo de entrada de etiquetas. El botón no se habilitará a menos que el usuario ingrese un caracter en el campo."""
        if self.__etiqueta.get() == '' or len(self.__tagFrame.winfo_children()) >= 5:
            self.__btnAddTag['state']='disabled'
        else:
            self.__btnAddTag['state']='enabled'

    def __agregarEtiqueta(self):
        """Es llamado al presionar el botón "Agregar Etiqueta", recogiendo el string del campo de entrada de etiqueta
        agregándolo a una lista de etiquetas del evento y a su vez mostrando gráficamente en la interfaz, las etiquetas agregadas."""
        deleteTag = lambda tag: self.__listaEtiquetas.remove(tag)
        cant = int(self.__lblTagsRest['text'])
        self.__lblTagsRest['text'] = str(cant-1)
        if cant == 1:
            self.__lblTagsRest['foreground'] = 'red'
        def modificar1(event):
            tagLabel['relief']='raised'
        def modificar2(event):
            tagLabel['relief']='ridge'
        def eliminar(event):
            cant = int(self.__lblTagsRest['text'])
            if cant == 0:
                self.__lblTagsRest['foreground'] = self.__guiParent.configTema['Tags']
            self.__lblTagsRest['text'] = str(cant+1)
            deleteTag(tagLabel["text"])
            tagLabel.destroy()
        if self.__etiqueta.get() not in self.__listaEtiquetas:
            self.__listaEtiquetas.append(self.__etiqueta.get())
            tagLabel = ttk.Label(self.__tagFrame,font=('Ubuntu','10','bold'),text=self.__etiqueta.get(),relief='ridge',padding=5)
            tagLabel.bind("<Enter>",modificar1)
            tagLabel.bind("<Leave>",modificar2)
            tagLabel.bind("<ButtonPress-1>",eliminar)
            if self.__tamTag+tagLabel.winfo_reqwidth() < 270:
                self.__columnTag += 1
                self.__tamTag += tagLabel.winfo_reqwidth()
            else:
                self.__tamTag = 0
                self.__columnTag = 0
                self.__rowTag += 1
            tagLabel.grid(column=self.__columnTag,row=self.__rowTag,pady=5,padx=5)
            if len(self.__tagFrame.winfo_children()) >= 5:    #Deshabilita el botón si se llegó al máximo de 5 etiquetas
                self.__btnAddTag.state(['disabled'])
        self.__inputTag.delete(0,END)