from views import controller, login
import tkinter as tk

try:
    root = tk.Tk()
    state = []
    login.Login(root, state).grid()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    if state:
        root = tk.Tk()
        root.tk.call("lappend", "auto_path", "themes")
        root.tk.call('package', 'require', 'awdark')
        root.tk.call('package', 'require', 'awlight')
        controller.App(root).grid()
        root.eval('tk::PlaceWindow . center')
        root.mainloop()
except Exception as err:
    print(err)
