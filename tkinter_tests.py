from tkinter import *
from tkinter import ttk

root = Tk()

class Painel_Widget(ttk.Frame):
    def __init__(self, parent, label):
        ttk.Frame.__init__(self,parent)
        ttk.Label(self,text=label).grid(column=0,row=0)

        painel_entry = ttk.Entry(self)
        painel_entry.config(state=DISABLED)
        painel_entry.grid(column=1,row=4)

        painel_subir_btn = ttk.Button(self,text="Subir")
        painel_subir_btn.config(state=DISABLED)
        painel_subir_btn.grid(column=0,row=5)
        painel_descer_btn = ttk.Button(self,text="Descer")
        painel_descer_btn.config(state=DISABLED)
        painel_descer_btn.grid(column=1,row=5)


c = Painel_Widget(root)

root.mainloop()