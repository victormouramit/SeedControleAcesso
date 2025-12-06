from tkinter import *
from tkinter import ttk
from data import *
#import requests
#import shutil
#from defense_api import *

VERSAO_ATUAL = "0.1.4"

""" URL_INFO = "https://raw.githubusercontent.com/victormouramit/SeedControleAcesso/refs/heads/main/update.json"
URL_UPDATER_EXE = "https://github.com/victormouramit/SeedControleAcesso/raw/refs/heads/main/updates/updater.exe"

def tem_update():
    info = requests.get(URL_INFO).json()
    ultima = info["version"]
    print(ultima)
    return ultima, ultima != VERSAO_ATUAL, info["download_url"]

def aplicar_update():
    # Baixa updater.exe
    r = requests.get(URL_UPDATER_EXE, stream=True)
    with open(f"updater.exe", "wb") as f:
        shutil.copyfileobj(r.raw, f)
    subprocess.Popen(["updater.exe"])
 """

#d = Defense("172.25.76.167","Kd8SVmE009XB")
root = Tk()
root.title("CONTROLE")
frm = ttk.Frame(root,padding=10)
frm.grid()

criar_arquivo_necessario()
vagas_guardadas = ler()

def mudar_painel_gui(Painel:Painel,entry_value: StringVar,action = 0):
    # Atualiza GUI
    valor = int(entry_value.get())
    
    novo_valor = valor+1 if action == 0 else valor-1

    entry_value.set(novo_valor)
      # Atualiza no arquivo
    vagas_guardadas[Painel.value] = novo_valor
    criar_atualizar(vagas_guardadas)

def un_block():
    print(c.get_state)
    state = NORMAL if str(c.get_state) == DISABLED else DISABLED
    c.configure(state=state)
    c2.configure(state=state)

""" ultima, precisa, url = tem_update()
v_var = StringVar()
if precisa:
    print(f"Nova versão {ultima} disponível! 🍰✨")
    v_var.set(f"Nova versão disponível.")
    ttk.Button(frm,text="Baixar",command=lambda: aplicar_update()).grid(column=0,row=3)
else:
    print("Você já está na última versão 💖✨") """


ttk.Button(frm,text="Bloquear/Desbloquear",command=un_block).grid(column=0,row=0)
#ttk.Label(frm,text=f"v{VERSAO_ATUAL}",foreground="green").grid(column=0,row=1)

""" v = ttk.Label(frm,text="",textvariable=v_var)
v.grid(column=0,row=2) """


class Painel_Widget(ttk.Frame):
    def __init__(self, parent, label, variable = Painel, state = DISABLED):
        ttk.Frame.__init__(self,parent)
        ttk.Label(self,text=label).grid(column=0,row=0)
        self.get_state = state
        painel_value = StringVar(value=vagas_guardadas[variable.value])
        self.painel_entry = ttk.Entry(self)
        self.painel_entry.config(state=state,textvariable=painel_value)
        self.painel_entry.grid(column=1,row=0)

        self.painel_subir_btn = ttk.Button(self,text="Subir",command= lambda: mudar_painel_gui(variable,painel_value,0))
        self.painel_subir_btn.config(state=state)
        self.painel_subir_btn.grid(column=0,row=5)
        
        self.painel_descer_btn = ttk.Button(self,text="Descer",command= lambda: mudar_painel_gui(variable,painel_value,1))
        self.painel_descer_btn.config(state=state)
        self.painel_descer_btn.grid(column=1,row=5)
    def configure(self,state = DISABLED):
        self.get_state = state
        self.painel_descer_btn.configure(state=state)
        self.painel_subir_btn.configure(state=state)
        self.painel_entry.configure(state=state)

c = Painel_Widget(frm, "Painel 1",Painel.One)
c.grid(column=1,row=0)
c2 = Painel_Widget(frm, "Painel 2",Painel.Two)
c2.grid(column=1,row=1)
c2 = Painel_Widget(frm, "Painel 3",Painel.Two)
c2.grid(column=2,row=0)
c2 = Painel_Widget(frm, "Painel 4",Painel.Two)
c2.grid(column=2,row=1)

# Painel 01
""" ttk.Label(frm,text="Painel 1:").grid(column=1,row=0)
painel_1_value = StringVar(value=vagas_guardadas[Painel.One.value])

painel_1_entry = ttk.Entry(frm)
painel_1_entry.config(state=DISABLED,textvariable=painel_1_value)
painel_1_entry.grid(column=2,row=0)

painel_1_subir_btn = ttk.Button(frm,text="Subir",command=lambda: mudar_painel_gui(Painel.One,painel_1_value,0))
painel_1_subir_btn.config(state=DISABLED)
painel_1_subir_btn.grid(column=1,row=1)
painel_1_descer_btn = ttk.Button(frm,text="Descer",command=lambda: mudar_painel_gui(Painel.One,painel_1_value,1))
painel_1_descer_btn.config(state=DISABLED)
painel_1_descer_btn.grid(column=2,row=1)
# FimDoPainel

# Painel 02
ttk.Label(frm,text="Painel 2:").grid(column=1,row=2)
painel_2_value = StringVar(value=vagas_guardadas[Painel.Two.value])

painel_2_entry = ttk.Entry(frm)
painel_2_entry.config(state=DISABLED,textvariable=painel_2_value)
painel_2_entry.grid(column=2,row=2)

painel_2_subir_btn = ttk.Button(frm,text="Subir",command=lambda: mudar_painel_gui(Painel.Two,painel_2_value,0))
painel_2_subir_btn.config(state=DISABLED)
painel_2_subir_btn.grid(column=1,row=3)
painel_2_descer_btn = ttk.Button(frm,text="Descer",command=lambda: mudar_painel_gui(Painel.Two,painel_2_value,1))
painel_2_descer_btn.config(state=DISABLED)
painel_2_descer_btn.grid(column=2,row=3)
# FimDoPainel

# Painel 03
ttk.Label(frm,text="Painel 3:").grid(column=3,row=0)
painel_3_value = StringVar(value=vagas_guardadas[Painel.Three.value])

painel_3_entry = ttk.Entry(frm)
painel_3_entry.config(state=DISABLED,textvariable=painel_3_value)
painel_3_entry.grid(column=4,row=0)

painel_3_subir_btn = ttk.Button(frm,text="Subir",command=lambda: mudar_painel_gui(Painel.Three,painel_3_value,0))
painel_3_subir_btn.config(state=DISABLED)
painel_3_subir_btn.grid(column=3,row=1)
painel_3_descer_btn = ttk.Button(frm,text="Descer",command=lambda: mudar_painel_gui(Painel.Three,painel_3_value,1))
painel_3_descer_btn.config(state=DISABLED)
painel_3_descer_btn.grid(column=4,row=1)
# FimDoPainel

# Painel 04
ttk.Label(frm,text="Painel 4:").grid(column=3,row=2)
painel_4_value = StringVar(value=vagas_guardadas[Painel.Four.value])

painel_4_entry = ttk.Entry(frm)
painel_4_entry.config(state=DISABLED,textvariable=painel_4_value)
painel_4_entry.grid(column=4,row=2)

painel_4_subir_btn = ttk.Button(frm,text="Subir",command=lambda: mudar_painel_gui(Painel.Four,painel_4_value,0))
painel_4_subir_btn.grid(column=3,row=3)
painel_4_subir_btn.config(state=DISABLED)
painel_4_descer_btn = ttk.Button(frm,text="Descer",command=lambda: mudar_painel_gui(Painel.Four,painel_4_value,1))
painel_4_descer_btn.config(state=DISABLED)
painel_4_descer_btn.grid(column=4,row=3)
# FimDoPainel
 """

root.mainloop()
