from enum import Enum
import threading
from APIs.camera_api import Camera
from APIs.defense_api import Defense
from data import *

defense = Defense("172.25.76.167","Kd8SVmE009XB")
parking_lots = defense.get_parking_lots()

# Busca pelas cameras de entrada para acionar as saídas de alarme

class Estacionamento(Enum):
    BLOCO_I = "Bloco I"
    BLOCO_II = "Bloco II"
    DED = "DED"

estacionamentos = {
    Estacionamento.BLOCO_I: 0,
    Estacionamento.BLOCO_II: 0,
    Estacionamento.DED: 0,
}

class ID_Estacionamento(Enum):
    One = "2"
    Two = "1"
    Three = "3"

# Faz a verificação inicial para ver as vagas disponíveis em cada estacionamento
for p in parking_lots:
    if p["idleParkingSpaceCount"] != None:
        number_parking_spaces = int(p["idleParkingSpaceCount"])
    else:
        number_parking_spaces = 0
    match p["id"]:
        case ID_Estacionamento.One.value:
            estacionamentos[Estacionamento.BLOCO_I] = number_parking_spaces
        case ID_Estacionamento.Two.value:
            estacionamentos[Estacionamento.BLOCO_II] = number_parking_spaces
        case ID_Estacionamento.Three.value:
            estacionamentos[Estacionamento.DED] = number_parking_spaces


print(estacionamentos)
# Compara o Id do estacionamento para associar a camera correta
# Verifica se os valores de vagas estão diferentes do valor inicial

CAM_PASSWD = "Ct14!#6tVq@"

def mudar_no_display(dif,estacionamento: str, action = 0):
    """
        action 0 = sobe,
        action 1 = desce
    """
    print(f"Valor mudado no display, action:{action},estacionamento:{estacionamento},")
    match estacionamento:
        case Estacionamento.BLOCO_I:
            c = Camera(Camera.BlocoI.Entrada, CAM_PASSWD)
            for _ in range(dif):
                c.pulsate(1) if action == 0 else c.pulsate(2)
        case Estacionamento.BLOCO_II:
            c = Camera(Camera.BlocoII.Entrada, CAM_PASSWD)
            for _ in range(dif):
                c.pulsate(1) if action == 0 else c.pulsate(2)
        case Estacionamento.DED:
            c_sobe = Camera(Camera.DED.Entrada, CAM_PASSWD)
            c_desce = Camera(Camera.DED.Saida, CAM_PASSWD)
            for _ in range(dif):
                c_sobe.pulsate(1) if action == 0 else c_desce(1)

def verificar_estacionamento(estacionamento: Estacionamento,vagas_atual: int):
    #print(f"vagas em mem:{estacionamentos[estacionamento]} - {vagas_atual}")
    if estacionamentos[estacionamento] >  vagas_atual:
        dif = estacionamentos[estacionamento] - vagas_atual
        mudar_no_display(dif,estacionamento,0)
        estacionamentos[estacionamento] = vagas_atual
    elif estacionamentos[estacionamento] <  vagas_atual:
        dif = vagas_atual - estacionamentos[estacionamento]
        mudar_no_display(dif,estacionamento,1)
        estacionamentos[estacionamento] = vagas_atual




# Analisa todos os estacionamentos em busca de alguma mudança no valor contando o número de vagas
def analisar_estacionamentos():
    #print("analisando estacionamentos")    
    while True:
        # Checa cada estacionamento
        for p in defense.get_parking_lots():
            # Número de Vagas Disponíveis do Estacionamento
            if p["idleParkingSpaceCount"] != None:
                number_parking_spaces = int(p["idleParkingSpaceCount"])
            else:
                number_parking_spaces = 0
            match p["id"]:
                # Verifica o id do estacionamento
                # Caso corresponda a algum, verifica se nesse estacionamento, o número de vagas aumentou ou diminuiu
                case ID_Estacionamento.One.value:
                    #print(number_parking_spaces)
                    verificar_estacionamento(Estacionamento.BLOCO_I,number_parking_spaces)
                case ID_Estacionamento.Two.value:
                    verificar_estacionamento(Estacionamento.BLOCO_II,number_parking_spaces)
                case ID_Estacionamento.Three.value:
                    verificar_estacionamento(Estacionamento.DED,number_parking_spaces)
        #time.sleep(TIME_TO_CHECK_PARKING_LOTS)

t = threading.Thread(target=analisar_estacionamentos)
t.start()
t.join()
print("fim de curso")
