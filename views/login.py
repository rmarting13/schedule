import sys
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

from mysql.connector import Error, errorcode
from db_context.mysql_connection import Connection as Con

class Login(tk.Frame):
    def __init__(self, parent, state):
        super().__init__(parent)
        self.parent = parent
        self.state = state
        self.parent.title("Login")
        # self.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.parent.resizable(True, True)
        self.parent.geometry('340x470')
        self.parent.configure(bg='#8151cf')

        self.cargar_componentes()

    def cargar_componentes(self):
        self.frame = tk.Frame(bg='#8151cf')

        self.icon_label = tk.Frame(self.frame, background='#8151cf')
        canvas = tk.Canvas(self.icon_label, width=180, height=150, background='#8151cf',highlightbackground='#8151cf')
        canvas.grid(column=0, row=0, sticky='nsew', pady=1)
        img = Image.open('/home/rmarting13/Documents/schedule-repo/schedule/themes/calendar.png')
        resized_image = img.resize((180, 150), Image.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(2, 2, anchor=tk.NW, image=new_image)
        canvas.image = new_image

        # Creating widgets
        self.login_label = tk.Label(
            self.frame, text="Login", bg='#3a3a3b', fg="#00ffae", font=("Ubuntu", 30))
        self.username_label = tk.Label(
            self.frame, text="Usuario:", bg='#8151cf', fg="#FFFFFF", font=("Ubuntu", 12))
        self.username_entry = tk.Entry(self.frame, font=("Ubuntu", 12))
        self.password_entry = tk.Entry(self.frame, show="*", font=("Ubuntu", 12))
        self.password_label = tk.Label(
            self.frame, text="Constraseña:", bg='#8151cf', fg="#FFFFFF", font=("Ubuntu", 12))
        self.login_button = tk.Button(
            self.frame, text="Login", bg="#3243d9", fg="#FFFFFF", font=("Ubuntu", 12), command=self.login)

        # Placing widgets on the screen
        self.icon_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.login_label.grid(row=1, column=0, columnspan=2, sticky="news", pady=10)
        self.username_label.grid(row=2, column=0)
        self.username_entry.grid(row=2, column=1, pady=20)
        self.password_label.grid(row=3, column=0)
        self.password_entry.grid(row=3, column=1, pady=20)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.frame.grid()

    def login(self):
        try:
            user = self.username_entry.get()
            password = self.password_entry.get()
            Con.set_user_pass(user, password)
            authentication = Con.get_connection()
            if authentication:
                messagebox.showinfo(title="Acceso correcto", message="Usted ha iniciado sesión con éxito.")
                self.state.append(True)
                self.parent.destroy()
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Ah ocurrido un error:\n {e}.")
            sys.exit()


if __name__ == '__main__':
    root = tk.Tk()
    Login(root,[]).grid()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

