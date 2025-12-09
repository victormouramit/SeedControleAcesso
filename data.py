from datetime import datetime
import json
from pathlib import Path
from enum import Enum
from APIs.camera_api import Camera
import time

CAM_PASSWD = "Ct14!#6tVq@"

class Painel(Enum):
    One = "Painel Bloco I"
    Two = "Painel Bloco II"
    Three = "Painel DED"
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
c4 = Camera(Camera.BlocoII.Saida, CAM_PASSWD) #Bloco I Sobe vagas

class Paineis:
    @staticmethod
    def aumentar_vagas(painel:Painel):
        secs = .3
        match painel:
            case Painel.One:
                c2.pulsate(2,secs)
            case Painel.Two:
                c3.pulsate(2,secs)

    @staticmethod
    def diminuir_vagas(painel:Painel):
        secs = .3
        match painel:
            case Painel.One:
                c2.pulsate(1,secs)
            case Painel.Two:
                c3.pulsate(1,secs)

def mudar_vagas_painel(painel:Painel,action = 0):
    match painel:
        case Painel.One:
            Paineis.aumentar_vagas(Painel.One) if action == 0 else Paineis.diminuir_vagas(Painel.One)
        case Painel.Two:
            Paineis.aumentar_vagas(Painel.Two) if action == 0 else Paineis.diminuir_vagas(Painel.Two)
        case Painel.Three:
            Paineis.aumentar_vagas(Painel.Three) if action == 0 else Paineis.diminuir_vagas(Painel.Three)
            
"""         case Painel.Two:
            c.pulsate(1) if action == 0 else c.pulsate(2)
        case Painel.Three:
            c.pulsate(1) if action == 0 else c.pulsate(2) """

def veiculo_grande(painel: Painel, time = 120):
    match painel:
        case Painel.One:
            print(f"{datetime.now()}\tInicio do levantamento das lanças do {Painel.One}")
            for _ in range(time):
                c2.pulsate(0,1)
                c1.pulsate(0,1)
            print(f"{datetime.now()}\tInicio do levantamento das lanças do {Painel.One}")
        case Painel.Two:
            print(f"{datetime.now()}\tInicio do levantamento das lanças do {Painel.Two}")
            for _ in range(time):
                c3.pulsate(0,1)
                c4.pulsate(0,1)
            print(f"{datetime.now()}\tInicio do levantamento das lanças do {Painel.Two}")


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
    