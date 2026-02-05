from enum import Enum
import threading
from APIs.camera_api import Camera
from APIs.defense_api import Defense
from data import *

logger.info("Estabelecendo conexão com Defense")
defense = Defense("172.25.76.167","Kd8SVmE009XB")
logger.info("Conexão estabelecida com o Defense")
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

logger.info("Lendo valores Iniciais...")

#criar_arquivo_necessario()
# Faz a verificação inicial para ver as vagas disponíveis em cada estacionamento no defense
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
            
logger.info("Valores Iniciais Lidos")

CAM_PASSWD = "Ct14!#6tVq@"

# Aumenta ou diminui os números no Painel
def mudar_no_display(dif,estacionamento: Estacionamento, action = 0):
    """
        action 0 = sobe,
        action 1 = desce
    """
    old_value = estacionamentos[estacionamento]
    new_value = 0

    if action == 0:
        new_value = old_value + int(dif)
        display_change = "aumentado"
    else:
        new_value = old_value - int(dif)
        display_change = "diminuido"

    logger.info(f"{datetime.now()}\tValor {display_change} no display, de {old_value} para {new_value}, estacionamento:{estacionamento}")
    match estacionamento:
        case Estacionamento.BLOCO_I:
            for _ in range(dif):
                try:
                    if action == 0:
                        mudar_vagas_painel(Painel.One,0)
                        #aumentar_valor_arquivo(Painel.One)
                    else:
                        mudar_vagas_painel(Painel.One,1)
                        #diminuir_valor_arquivo(Painel.One)
                except:
                    logger.error("Erro no looping para adicionar vagas no estacionamento do BLOCO 1")
                    break
        case Estacionamento.BLOCO_II:
            for _ in range(dif):
                try:
                    if action == 0:
                        mudar_vagas_painel(Painel.Two,0)
                        #aumentar_valor_arquivo(Painel.Two)
                    else:
                        mudar_vagas_painel(Painel.Two,1)
                        #diminuir_valor_arquivo(Painel.Two)
                except:
                    logger.error("Erro no looping para adicionar vagas no estacionamento do BLOCO 2")
                    break
        case Estacionamento.DED:
            for _ in range(dif):
                try:
                    if action == 0:
                        mudar_vagas_painel(Painel.Three,0)
                        #aumentar_valor_arquivo(Painel.Three)
                    else:
                        mudar_vagas_painel(Painel.Three,1)
                        #diminuir_valor_arquivo(Painel.Three)
                except:
                    logger.error("Erro no looping para adicionar vagas no estacionamento do DED")
                    break

# Compara os valores para ver se o numero de vagas do estacionamento mudou
def verificar_estacionamento(estacionamento: Estacionamento,vagas_atual: int):
    # Executado, caso o numero de vagas tenha diminuido, ou seja, alguém tenha entrado
    if estacionamentos[estacionamento] >  vagas_atual:
        dif = estacionamentos[estacionamento] - vagas_atual
        mudar_no_display(dif,estacionamento,1)
        estacionamentos[estacionamento] = vagas_atual
    # Executado, caso o numero de vagas tenha aumentado, ou seja, alguém tenha saido
    elif estacionamentos[estacionamento] <  vagas_atual:
        dif = vagas_atual - estacionamentos[estacionamento]
        mudar_no_display(dif,estacionamento,0)
        estacionamentos[estacionamento] = vagas_atual

# Analisa todos os estacionamentos em busca de alguma mudança no valor contando o número de vagas
def analisar_estacionamentos():
    while True:
        # Checa cada estacionamento
        for p in defense.get_parking_lots():
            # Número de Vagas Disponíveis do Estacionamento
            if p["idleParkingSpaceCount"] != None:
                number_parking_spaces = int(p["idleParkingSpaceCount"])
            else:
                number_parking_spaces = 0
            
            try:
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
            except:
                logger.info("Falhou na analise de estacionamentos")
                continue

t = threading.Thread(target=analisar_estacionamentos)
t.start()
t.join()
print("fim de curso")
