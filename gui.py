from tkinter import *
from tkinter import ttk
from updater import *


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
    painel_1_subir_btn.config(state=state)
    painel_1_descer_btn.config(state=state)
    painel_2_entry.config(state=state)
    painel_2_subir_btn.config(state=state)
    painel_2_descer_btn.config(state=state)
    painel_3_entry.config(state=state)
    painel_3_subir_btn.config(state=state)
    painel_3_descer_btn.config(state=state)
    painel_4_entry.config(state=state)
    painel_4_subir_btn.config(state=state)
    painel_4_descer_btn.config(state=state)

ultima, precisa, url = tem_update()
v_var = StringVar()
if precisa:
    print(f"Nova versão {ultima} disponível! 🍰✨")
    v_var.set(f"Nova versão disponível.")
    ttk.Button(frm,text="Baixar",command=lambda: aplicar_update(url)).grid(column=0,row=3)
else:
    print("Você já está na última versão 💖✨")


ttk.Button(frm,text="Bloquear/Desbloquear",command=un_block).grid(column=0,row=0)
ttk.Label(frm,text=f"v{VERSAO_ATUAL}",foreground="green").grid(column=0,row=1)

v = ttk.Label(frm,text="",textvariable=v_var)
v.grid(column=0,row=2)

# Painel 01
ttk.Label(frm,text="Painel 1:").grid(column=1,row=0)
painel_1_value = StringVar(value="0")

painel_1_entry = ttk.Entry(frm)
painel_1_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_1_entry.grid(column=2,row=0)

painel_1_subir_btn = ttk.Button(frm,text="Subir",command=subir)
painel_1_subir_btn.config(state=DISABLED)
painel_1_subir_btn.grid(column=1,row=1)
painel_1_descer_btn = ttk.Button(frm,text="Descer",command=descer)
painel_1_descer_btn.config(state=DISABLED)
painel_1_descer_btn.grid(column=2,row=1)
# FimDoPainel

# Painel 02
ttk.Label(frm,text="Painel 2:").grid(column=1,row=2)
painel_2_value = StringVar(value="0")

painel_2_entry = ttk.Entry(frm)
painel_2_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_2_entry.grid(column=2,row=2)

painel_2_subir_btn = ttk.Button(frm,text="Subir",command=subir)
painel_2_subir_btn.config(state=DISABLED)
painel_2_subir_btn.grid(column=1,row=3)
painel_2_descer_btn = ttk.Button(frm,text="Descer",command=descer)
painel_2_descer_btn.config(state=DISABLED)
painel_2_descer_btn.grid(column=2,row=3)
# FimDoPainel

# Painel 03
ttk.Label(frm,text="Painel 3:").grid(column=3,row=0)
painel_3_value = StringVar(value="0")

painel_3_entry = ttk.Entry(frm)
painel_3_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_3_entry.grid(column=4,row=0)

painel_3_subir_btn = ttk.Button(frm,text="Subir",command=subir)
painel_3_subir_btn.config(state=DISABLED)
painel_3_subir_btn.grid(column=3,row=1)
painel_3_descer_btn = ttk.Button(frm,text="Descer",command=descer)
painel_3_descer_btn.config(state=DISABLED)
painel_3_descer_btn.grid(column=4,row=1)
# FimDoPainel

# Painel 04
ttk.Label(frm,text="Painel 4:").grid(column=3,row=2)
painel_4_value = StringVar(value="0")

painel_4_entry = ttk.Entry(frm)
painel_4_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_4_entry.grid(column=4,row=2)

painel_4_subir_btn = ttk.Button(frm,text="Subir",command=subir)
painel_4_subir_btn.grid(column=3,row=3)
painel_4_subir_btn.config(state=DISABLED)
painel_4_descer_btn = ttk.Button(frm,text="Descer",command=descer)
painel_4_descer_btn.config(state=DISABLED)
painel_4_descer_btn.grid(column=4,row=3)
# FimDoPainel

root.mainloop()
