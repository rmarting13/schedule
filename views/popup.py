import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, END, messagebox
from datetime import datetime
from calendar import Calendar
from tkcalendar import Calendar as tkCalendar
from Archivo import BaseDeDatos

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

    @staticmethod
    def error(msj):
        return messagebox.showerror(message=f'Error!\n{msj}')
