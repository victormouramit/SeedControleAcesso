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
    mudar_vagas_painel(Painel,action)

def un_block():
    print(c.get_state)
    state = NORMAL if str(c.get_state) == DISABLED else DISABLED
    c.configure(state=state)
    c2.configure(state=state)
    c3.configure(state=state)
    c4.configure(state=state)
    

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
    def __init__(self, parent, label, variable = Painel, state = DISABLED, huge = False):
        ttk.Frame.__init__(self,parent)
        ttk.Label(self,text=label).grid(column=0,row=0)
        self.get_state = state
        self.painel_value = StringVar(value=vagas_guardadas[variable.value])
        self.painel_entry = ttk.Entry(self)
        self.painel_entry.config(state=state,textvariable=self.painel_value)
        self.painel_entry.grid(column=1,row=0)

        self.painel_subir_btn = ttk.Button(self,text="Subir",command= lambda: mudar_painel_gui(variable,self.painel_value,0))
        self.painel_subir_btn.config(state=state)
        self.painel_subir_btn.grid(column=0,row=5)
        
        self.painel_descer_btn = ttk.Button(self,text="Descer",command= lambda: mudar_painel_gui(variable,self.painel_value,1))
        self.painel_descer_btn.config(state=state)
        self.painel_descer_btn.grid(column=1,row=5)

        self.times_value = StringVar()
        self.painel_huge_btn = ttk.Button(self,text="LEVANTAR CANCELAS", command=lambda: veiculo_grande(variable))
        if huge == False:
            self.painel_huge_btn.configure(state=DISABLED)
        self.painel_huge_btn.grid(column=0,row=6, columnspan=2)
    def configure(self,state = DISABLED):
        self.get_state = state
        self.painel_descer_btn.configure(state=state)
        self.painel_subir_btn.configure(state=state)
        self.painel_entry.configure(state=state)

c = Painel_Widget(frm, Painel.One.value,Painel.One,huge=True)
c.grid(column=1,row=0)
c2 = Painel_Widget(frm, Painel.Two.value,Painel.Two,huge=True)
c2.grid(column=1,row=1)
c3 = Painel_Widget(frm, Painel.Three.value,Painel.Three)
c3.grid(column=2,row=0)
c4 = Painel_Widget(frm, Painel.Four.value,Painel.Four)
c4.grid(column=2,row=1)

def atualizar():
    vagas_guardadas = ler()
    print(f"{datetime.now()}\t Atualizando Interface")
    c.painel_value.set(vagas_guardadas[Painel.One.value])
    c2.painel_value.set(vagas_guardadas[Painel.Two.value])
    c3.painel_value.set(vagas_guardadas[Painel.Three.value])
    c4.painel_value.set(vagas_guardadas[Painel.Four.value])
    root.after(2000,atualizar) # 2s
    print(f"{datetime.now()}\t Fim da Atualização")

atualizar()
root.mainloop()
