from datetime import datetime
import json
from pathlib import Path
from enum import Enum
from APIs.camera_api import Camera
import threading
import logging

logger = logging.getLogger("Defense")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
arquivo = logging.FileHandler("defense.log", encoding="utf-8")


arquivo.setFormatter(formatter)

console = logging.StreamHandler()
console.setFormatter(formatter)

logger.addHandler(arquivo)
logger.addHandler(console)


one_stop_event = threading.Event()
one_thread = None
one_arisen = False
two_stop_event = threading.Event()
two_thread = None
two_arisen = False

CAM_PASSWD = "Ct14!#6tVq@"

class Painel(Enum):
    One = "Painel Bloco I"
    Two = "Painel Bloco II"
    Three = "Painel DED"
    Four = "Painel 4"

class Cameras(Enum):
    
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


c1 = Camera(Cameras.BlocoI.Saida, CAM_PASSWD)

# Saida(1) diminui o n do painel de vagas e saida(2) aumenta o n de vagas
c2 = Camera(Cameras.BlocoI.Entrada, CAM_PASSWD)

# Saida(1) diminui o n do painel de vagas e saida(2) aumenta o n de vagas
c3 = Camera(Cameras.BlocoII.Entrada, CAM_PASSWD)

c4 = Camera(Cameras.BlocoII.Saida, CAM_PASSWD)

# Saida(1) aumenta o n do painel
c5 = Camera(Cameras.DED.Entrada, CAM_PASSWD)

# Saida(1) diminui o n do painel
c6 = Camera(Cameras.DED.Saida, CAM_PASSWD)

class Paineis:
    @staticmethod
    def aumentar_n_paineis(painel:Painel):
        secs = .3
        try:
            match painel:
                case Painel.One:
                    c2.pulsate(2,secs)
                case Painel.Two:
                    c3.pulsate(2,secs)
                case Painel.Three:
                    c5.pulsate(1,secs)
        except:
            print("Erro na hora de aumentar n de vagas")
    @staticmethod
    def diminuir_n_paineis(painel:Painel):
        secs = .3
        try:
            match painel:
                case Painel.One:
                    c2.pulsate(1,secs)
                case Painel.Two:
                    c3.pulsate(1,secs)
                case Painel.Three:
                    c6.pulsate(1,secs)
        except:
            print("Erro na hora de diminuir n de vagas")

def mudar_vagas_painel(painel:Painel,action = 0):
    match painel:
        case Painel.One:
            Paineis.aumentar_n_paineis(Painel.One) if action == 0 else Paineis.diminuir_n_paineis(Painel.One)
        case Painel.Two:
            Paineis.aumentar_n_paineis(Painel.Two) if action == 0 else Paineis.diminuir_n_paineis(Painel.Two)
        case Painel.Three:
            Paineis.aumentar_n_paineis(Painel.Three) if action == 0 else Paineis.diminuir_n_paineis(Painel.Three)
            
"""         case Painel.Two:
            c.pulsate(1) if action == 0 else c.pulsate(2)
        case Painel.Three:
            c.pulsate(1) if action == 0 else c.pulsate(2) """


def one_rise_up():
    while not one_stop_event.is_set():
        c2.pulsate(0,1)
        c1.pulsate(0,1)

def two_rise_up():
    while not two_stop_event.is_set():
        c3.pulsate(0,1)
        c4.pulsate(0,1)

def veiculo_grande(painel: Painel, time = 20):
    global one_thread, one_arisen,two_arisen

    match painel:
        case Painel.One:
            if not one_arisen:
                logger.info(f"{datetime.now()}\tInicio do levantamento das lanças do {Painel.One}")
                one_arisen = True
                one_stop_event.clear()
                one_thread = threading.Thread(target=one_rise_up)
                one_thread.start()
                logger.info(f"{datetime.now()}\tFim do levantamento das lanças do {Painel.One}")
            else:
                one_arisen = False
                one_stop_event.set()
                if one_thread and one_thread.is_alive():
                    one_thread.join()
            
        case Painel.Two:
            if not two_arisen:
                logger.info(f"{datetime.now()}\tInicio do levantamento das lanças do {Painel.Two}")

                two_arisen = True
                two_stop_event.clear()
                two_thread = threading.Thread(target=two_rise_up)
                two_thread.start()
                logger.info(f"{datetime.now()}\tFim do levantamento das lanças do {Painel.Two}")
            else:
                two_arisen = False
                two_stop_event.set()
                if two_thread and two_thread.is_alive():
                    two_thread.join()


painel_vagas = {
    Painel.One.value: 0,
    Painel.Two.value: 0,
    Painel.Three.value: 0,
    Painel.Four.value: 0,
}

NUMBERS_FILE_NAME = "numbers.json"
LOG_NUMBERS_FILE_NAME = "LOG.txt"

def criar_arquivo_necessario():
    if not Path(NUMBERS_FILE_NAME).exists():
        criar_atualizar()

def criar_atualizar(painel_vagas = painel_vagas):
    with open(NUMBERS_FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(painel_vagas,fp=f)

def ler() -> dict:
    with open(NUMBERS_FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

painel_vagas = ler()
def aumentar_valor_arquivo(painel: Painel):
    match painel:
        case Painel.One:
            painel_vagas[Painel.One.value] = int(painel_vagas[Painel.One.value]) +1
            criar_atualizar(painel_vagas)
        case Painel.Two:
            painel_vagas[Painel.Two.value] = int(painel_vagas[Painel.Two.value]) +1
            criar_atualizar(painel_vagas)
        case Painel.Three:
            painel_vagas[Painel.Three.value] = int(painel_vagas[Painel.Three.value]) +1
            criar_atualizar(painel_vagas)

def diminuir_valor_arquivo(painel: Painel):
    match painel:
        case Painel.One:
            painel_vagas[Painel.One.value] = int(painel_vagas[Painel.One.value]) -1
            criar_atualizar(painel_vagas)
        case Painel.Two:
            painel_vagas[Painel.Two.value] = int(painel_vagas[Painel.Two.value]) -1
            criar_atualizar(painel_vagas)    
        case Painel.Three:
            painel_vagas[Painel.Three.value] = int(painel_vagas[Painel.Three.value]) -1
            criar_atualizar(painel_vagas)