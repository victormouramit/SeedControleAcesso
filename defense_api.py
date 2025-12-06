USER_NAME = "system"

POST_AUTH_ENDPOINT = "/brms/api/v1.0/accounts/authorize"
PUT_KEEP_ALIVE_ENDPOINT = "/brms/api/v1.0/accounts/keepalive"
POST_UPDATE_TOKEN_ENDPOINT = "/brms/api/v1.0/accounts/updateToken"
GET_DEVICES_ENDPOINT = "/brms/api/v1.1/definition/device-type/list"
GET_DEVICE_BY_CODE_ENDPOINT = "/brms/api/v1.1/device/"
GET_PARKING_LOT_LIST_ENDPOINT = "/ipms/api/v1.1/parking-lot/list"
TIME_TO_CHECK_PARKING_LOTS = 0.5

from enum import Enum
import requests
import simplejson as json
from camera import Camera
import time
import threading
from datetime import datetime,timedelta
from Crypto.Hash import MD5


class Defense:
    def __init__(self,server_ip,system_passwd):
        self.server_ip = server_ip
        self.system_passwd = system_passwd
        self.server_address = f"http://{server_ip}"
        self.token = ""
        self.headers = {"X-Subject-Token": f"{self.token}"}
        self.temp4 = ""
        self.signature = ""
        self.auth()
        threading.Thread(target=self.keep_alive_counter).start()
        threading.Thread(target=self.update_token_counter).start()
    def auth(self):
        # Primeira AUTH
        r = requests.post(f"{self.server_address}{POST_AUTH_ENDPOINT}",json={"userName": USER_NAME, "ipAddress": ""})

        json_r = json.loads(r.text)
        realm = json_r["realm"]
        random_key = json_r["randomKey"]

        #print(f"first auth code:{r}")

        # 5 passos para assinatura
        temp = MD5.new(bytes(self.system_passwd,"utf-8")).hexdigest()
        temp2 = MD5.new(bytes(f"{USER_NAME}{temp}","utf-8")).hexdigest()
        temp3 = MD5.new(bytes(temp2,"utf-8")).hexdigest()
        self.temp4 = MD5.new(bytes(f"{USER_NAME}:{realm}:{temp3}","utf-8")).hexdigest()
        self.signature = MD5.new(bytes(f"{self.temp4}:{random_key}","utf-8")).hexdigest()
        #print(signature)

        # Second Auth Proccess
        r = requests.post(f"{self.server_address}{POST_AUTH_ENDPOINT}",json={
            "userName": USER_NAME,
            "randomKey": random_key,
            "mac": "",
            "encryptType": "MD5",
            "ipAddress": "",
            "signature": self.signature,
        })
        # Code response for second auth code
        print(f"second auth code:{r}")
        response_text = json.loads(r.text)
        self.token = response_text["token"]
        self.refresh_token_header()
    def refresh_token_header(self):
        self.headers = {"X-Subject-Token": f"{self.token}"}
    def update_token(self):
        tempo = datetime.now()
        while True:
            time.sleep(300)
            if datetime.now >= tempo + timedelta(minutes=20):
                new_signature = MD5.new(bytes(f"{self.temp4}:{self.token}")).hexdigest()
                r = requests.post(f"{self.server_address}{POST_UPDATE_TOKEN_ENDPOINT}",json={"signature": new_signature}, headers=self.headers)
                response = json.loads(r.text)
                self.token = response["data"]["token"]
                self.refresh_token_header()
                tempo = datetime.now()
                print("20 minutos se passaram: Token Atualizado")
    def keep_alive_token(self):
        tempo = datetime.now()
        while True:
            time.sleep(5)
            if datetime.now >= tempo + timedelta(seconds=20):
                print("20 segundos se passaram: Token Sendo Mantido Vivo")
                r = requests.put(f"{self.server_address}{PUT_KEEP_ALIVE_ENDPOINT}", json={ }, headers=self.headers)
                response = json.loads(r.text)
                self.token = response["data"]["token"]
                self.refresh_token_header()
                tempo = datetime.now()
    # Get a list of Parking Lots
    def get_parking_lots(self):
        r = requests.get(f"{self.server_address}{GET_PARKING_LOT_LIST_ENDPOINT}",headers=self.headers)
        response = json.loads(r.text)
        parking_lots = response["data"]["results"]
        #n_parking_lots = len(parking_lots)
        return parking_lots
    def get_devices(self):
        r = requests.get(f"{self.server_address}{GET_DEVICES_ENDPOINT}",json={},headers=self.headers)
        print(r.text)
    def get_device(self,code):
        r = requests.get(f"{self.server_address}{GET_DEVICE_BY_CODE_ENDPOINT}{code}",json={},headers=self.headers)
        j = json.loads(r.text)
        return j["data"]["deviceIp"]
        #print(r.text)

# Getting the amount of places to park

defense = Defense("172.25.76.167","Kd8SVmE009XB")
parking_lots = defense.get_parking_lots()

# Busca pelas cameras de entrada para acionar as saídas de alarme
def find_camera_ip(positions,num_alarm_out = 1):
    positions = p["positions"]
    for pos in positions:
        points = pos["points"]
        for point in points:
            # Verificar se a camera tem "entrada" no nome
            if "entrada" in point["pointName"].lower() :
                bindingChannels = point["bindingChannels"]
                for x in bindingChannels:
                    cameraIp = defense.get_device(x["deviceCode"])
                    c = Camera(cameraIp,"Ct14!#6tVq@")
                    print(f"Ativando saida de Alarme da camera com IP:{cameraIp}")
                    c.pulsate(num_alarm_out)

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
    One = "1"
    Two = "2"
    Three = "3"

# Faz a verificação inicial para ver as vagas disponíveis em cada estacionamento
for p in parking_lots:
    match p["id"]:
        case ID_Estacionamento.One.value:
            estacionamentos[Estacionamento.BLOCO_I] = int(p["idleParkingSpaceCount"])
        case ID_Estacionamento.Two.value:
            estacionamentos[Estacionamento.BLOCO_II] = int(p["idleParkingSpaceCount"])
        case ID_Estacionamento.Three.value:
            estacionamentos[Estacionamento.DED] = int(p["idleParkingSpaceCount"])


print(estacionamentos)
# Compara o Id do estacionamento para associar a camera correta
# Verifica se os valores de vagas estão diferentes do valor inicial

CAM_PASSWD = "Ct14!#6tVq@"

def mudar_no_display(dif,estacionamento: str, action = 0):
    """
        action 0 = sobe,
        action 1 = desce
    """
    match estacionamento:
        case Estacionamento.BLOCO_I:
            c = Camera("192.168.40.3", CAM_PASSWD)
            for _ in range(dif):
                c.pulsate(1) if action == 0 else c.pulsate(2)
        case Estacionamento.BLOCO_II:
            c = Camera("192.168.40.4", CAM_PASSWD)
            for _ in range(dif):
                c.pulsate(1) if action == 0 else c.pulsate(2)
        case Estacionamento.DED:
            c_sobe = Camera("192.168.40.9", CAM_PASSWD)
            c_desce = Camera("192.168.40.10", CAM_PASSWD)
            for _ in range(dif):
                c_sobe.pulsate(1) if action == 0 else c_desce(1)

def verificar_estacionamento(estacionamento: Estacionamento,vagas_atual: int):
    if estacionamentos[estacionamento] >  vagas_atual:
        dif = estacionamentos[estacionamento] - vagas_atual
        mudar_no_display(dif,estacionamento,0)
    elif estacionamentos[estacionamento] <  vagas_atual:
        dif = vagas_atual - estacionamentos[estacionamento]
        mudar_no_display(dif,estacionamento,1)

while True:
    # Checa cada estacionamento
    for p in parking_lots:
        # Número de Vagas Disponíveis do Estacionamento
        if p["idleParkingSpaceCount"] != None:
            number_parking_spaces = int(p["idleParkingSpaceCount"])
        else:
            number_parking_spaces = 0
        match p["id"]:
            # Verifica o id do estacionamento
            # Caso corresponda a algum, verifica se nesse estacionamento, o número de vagas aumentou ou diminuiu
            case ID_Estacionamento.One.value:
                verificar_estacionamento(Estacionamento.BLOCO_I,number_parking_spaces)
            case ID_Estacionamento.Two.value:
                verificar_estacionamento(Estacionamento.BLOCO_II,number_parking_spaces)
            case ID_Estacionamento.Three.value:
                verificar_estacionamento(Estacionamento.DED,number_parking_spaces)
            
    time.sleep(TIME_TO_CHECK_PARKING_LOTS)