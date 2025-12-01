from tkinter import *
from tkinter import ttk

root = Tk()
root.title("CONTROLE")
frm = ttk.Frame(root,padding=10)
frm.grid()

def subir():
    valor = int(painel_1_value.get())
    painel_1_value.set(valor+1)
    print(painel_1_value.get())
    #root.update_idletasks()
def descer():
    valor = int(painel_1_value.get())
    painel_1_value.set(valor-1)
    print(painel_1_value.get())
    #root.update_idletasks()
def un_block():
    print(str(painel_1_entry["state"])==DISABLED)  
    state = NORMAL if str(painel_1_entry["state"]) == DISABLED else DISABLED
    painel_1_entry.config(state=state)
    painel_2_entry.config(state=state)
    painel_3_entry.config(state=state)
    painel_4_entry.config(state=state)

ttk.Button(frm,text="Bloquear/Desbloquear",command=un_block).grid(column=0,row=0)

# Painel 01
ttk.Label(frm,text="Painel 1:").grid(column=1,row=0)
painel_1_value = StringVar(value="0")

painel_1_entry = ttk.Entry(frm)
painel_1_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_1_entry.grid(column=2,row=0)

ttk.Button(frm,text="Subir",command=subir).grid(column=1,row=1)
ttk.Button(frm,text="Descer",command=descer).grid(column=2,row=1)
# FimDoPainel

# Painel 02
ttk.Label(frm,text="Painel 2:").grid(column=1,row=2)
painel_2_value = StringVar(value="0")

painel_2_entry = ttk.Entry(frm)
painel_2_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_2_entry.grid(column=2,row=2)

ttk.Button(frm,text="Subir",command=subir).grid(column=1,row=3)
ttk.Button(frm,text="Descer",command=descer).grid(column=2,row=3)
# FimDoPainel

# Painel 03
ttk.Label(frm,text="Painel 3:").grid(column=3,row=0)
painel_3_value = StringVar(value="0")

painel_3_entry = ttk.Entry(frm)
painel_3_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_3_entry.grid(column=4,row=0)

ttk.Button(frm,text="Subir",command=subir).grid(column=3,row=1)
ttk.Button(frm,text="Descer",command=descer).grid(column=4,row=1)
# FimDoPainel

# Painel 04
ttk.Label(frm,text="Painel 4:").grid(column=3,row=2)
painel_4_value = StringVar(value="0")

painel_4_entry = ttk.Entry(frm)
painel_4_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_4_entry.grid(column=4,row=2)

ttk.Button(frm,text="Subir",command=subir).grid(column=3,row=3)
ttk.Button(frm,text="Descer",command=descer).grid(column=4,row=3)
# FimDoPainel

root.mainloop()
