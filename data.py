from datetime import datetime
import json
from pathlib import Path
from enum import Enum
from APIs.camera_api import Camera
import time

CAM_PASSWD = "Ct14!#6tVq@"

class Painel(Enum):
    One = "Painel 1"
    Two = "Painel 2"
    Three = "Painel 3"
    Four = "Painel 4"

class Camera(Enum):
    
    class BlocoI:
        Entrada = "192.168.40.3"
        Saida = "192.168.40.2"
    class BlocoII:
        Entrada = "192.168.40.4"
        Saida = "192.168.40.7"
    class DED:
        Entrada = "192.168.40.9"
        Saida = "192.168.40.10"
        SaidaFundo = "192.168.40.8"


c1 = Camera(Camera.BlocoI.Saida, CAM_PASSWD) #Bloco I Desce(1) vagas e Sobe(2)
c2 = Camera(Camera.BlocoI.Entrada, CAM_PASSWD) #Bloco I Desce(1) vagas e Sobe(2)
c3 = Camera(Camera.BlocoII.Entrada, CAM_PASSWD) #Bloco I Sobe vagas

class Paineis:
    @staticmethod
    def aumentar_vagas(painel:Painel):
        match painel:
            case Painel.One:
                c2.pulsate(2)
    def diminuir_vagas(painel:Painel):
        match painel:
            case Painel.One:
                c2.pulsate(1)

def mudar_vagas_painel(painel:Painel,action = 0):
    match painel:
        case Painel.One:
            Paineis.aumentar_vagas(Painel.One) if action == 0 else Paineis.diminuir_vagas(Painel.One)
            
"""         case Painel.Two:
            c.pulsate(1) if action == 0 else c.pulsate(2)
        case Painel.Three:
            c.pulsate(1) if action == 0 else c.pulsate(2) """

def veiculo_grande(painel: Painel, time = 30):
    match painel:
        case Painel.One:
            print(datetime.now())
            for _ in range(time):
                c2.pulsate(0)
                c1.pulsate(0)
            print(datetime.now())

painel_vagas = {
    Painel.One.value: 0,
    Painel.Two.value: 0,
    Painel.Three.value: 0,
    Painel.Four.value: 0,
}

FILE_NAME = "numbers.json"

def criar_arquivo_necessario():
    if not Path(FILE_NAME).exists():
        criar_atualizar()

def criar_atualizar(painel_vagas = painel_vagas):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(painel_vagas,fp=f)
    


def ler() -> dict:
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)
    