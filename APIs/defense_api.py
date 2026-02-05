USER_NAME = "system"

POST_AUTH_ENDPOINT = "/brms/api/v1.0/accounts/authorize"
PUT_KEEP_ALIVE_ENDPOINT = "/brms/api/v1.0/accounts/keepalive"
POST_UPDATE_TOKEN_ENDPOINT = "/brms/api/v1.0/accounts/updateToken"
GET_DEVICES_ENDPOINT = "/brms/api/v1.1/definition/device-type/list"
GET_DEVICE_BY_CODE_ENDPOINT = "/brms/api/v1.1/device/"
GET_PARKING_LOT_LIST_ENDPOINT = "/ipms/api/v1.1/parking-lot/list"
TIME_TO_CHECK_PARKING_LOTS = 0

from enum import Enum
import requests
import simplejson as json
from APIs.camera_api import Camera
import time
import threading
from datetime import datetime,timedelta
from Crypto.Hash import MD5
from data import *

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
        threading.Thread(target=self.keep_alive_token).start()
        threading.Thread(target=self.update_token).start()
    def cript(self,value):
        return MD5.new(bytes(value,'utf-8')).hexdigest()
    def auth(self):
        # Primeira AUTH
        logger.info("Inicioda Auth01")
        try:
            r = requests.post(f"{self.server_address}{POST_AUTH_ENDPOINT}",json={"userName": USER_NAME, "ipAddress": ""})
        except requests.exceptions.HTTPError as e:
            logger.error(f"Falha na Auth01Request--{e}")
        ## Deve dar 401
        json_r = json.loads(r.text)
        realm = json_r["realm"]
        random_key = json_r["randomKey"]

        #print(f"first auth code:{r}")

        # 5 passos para assinatura
        temp = self.cript(self.system_passwd)
        temp2 = self.cript(f"{USER_NAME}{temp}")
        temp3 = self.cript(temp2)
        self.temp4 = self.cript(f"{USER_NAME}:{realm}:{temp3}")
        self.signature = self.cript(f"{self.temp4}:{random_key}")
       
        # Second Auth Proccess
        logger.info("Inicio da Auth02")
        try:
            r = requests.post(f"{self.server_address}{POST_AUTH_ENDPOINT}",json={
                "userName": USER_NAME,
                "randomKey": random_key,
                "mac": "",
                "encryptType": "MD5",
                "ipAddress": "",
                "signature": self.signature,
            })
        except requests.exceptions.HTTPError as e:
            logger.error(f"Falha na Auth02Request--{e}")

        # Code response for second auth code
        response_text = json.loads(r.text)
        self.token = response_text["token"]
        self.refresh_token_header()
    def refresh_token_header(self):
        self.headers = {"X-Subject-Token": f"{self.token}"}
    def update_token(self):
        tempo = datetime.now()
        while True:
            time.sleep(100)
            if datetime.now() >= tempo + timedelta(minutes=23):
                try:
                    print(f"{datetime.now()}\tPASSOU 23 MIN, ATUALIZANDO TOKEN")
                    new_signature = self.cript(f"{self.temp4}:{self.token}")
                    #new_signature = MD5.new(bytes(f"{self.temp4}:{self.token}",'utf-8')).hexdigest()
                    #print(new_signature)
                    try:
                        r = requests.post(f"{self.server_address}{POST_UPDATE_TOKEN_ENDPOINT}",json={"signature": new_signature}, headers=self.headers)
                        #print(r.text)
                    except requests.exceptions.HTTPError as e:
                        logger.error(f"Erro em TokenUpdateRequest ---- {e}")
                        continue
                    #print(f"<{r.status_code}>\t{r.content}")
                    response = json.loads(r.text)
                    #print(f"response: {response}")
                    self.token = response["data"]["token"]
                    #print(self.token)
                    self.refresh_token_header()
                    tempo = datetime.now()
                    logger.info(f"{datetime.now()}\t----Token Atualizado com sucesso-----")
                except:
                    logger.error(f"{datetime.now()}\t----Erro na atualização do Token----")
                    continue
    def keep_alive_token(self):
        tempo = datetime.now()
        while True:
            time.sleep(5)
            try:
                if datetime.now() >= tempo + timedelta(seconds=20):
                    #print(f"{datetime.now()}\t20 segundos se passaram: Token Sendo Mantido Vivo")
                    try:
                        r = requests.put(f"{self.server_address}{PUT_KEEP_ALIVE_ENDPOINT}", json={ }, headers=self.headers)
                    except requests.exceptions.HTTPError as e:
                        logger.error(f"Erro em KeepAliveTokenRequest --- {e}")
                        continue
                    response = json.loads(r.text)
                    self.token = response["data"]["token"]
                    self.refresh_token_header()
                    tempo = datetime.now()
                    #print(f"{datetime.now()}\t****Token mantido vivo com sucesso****")
            except:
                logger.error(f"Erro em KeepAliveToken")
    # Get a list of Parking Lots
    def get_parking_lots(self):
        try:
            r = requests.get(f"{self.server_address}{GET_PARKING_LOT_LIST_ENDPOINT}",headers=self.headers)
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro em GetParkingLotsRequest --- {e}")
        response = json.loads(r.text)
        parking_lots = response["data"]["results"]
        #n_parking_lots = len(parking_lots)
        return parking_lots
    def get_devices(self):
        r = requests.get(f"{self.server_address}{GET_DEVICES_ENDPOINT}",json={},headers=self.headers)
        print(r.text)
    def get_device(self, code):
        r = requests.get(f"{self.server_address}{GET_DEVICE_BY_CODE_ENDPOINT}{code}",json={},headers=self.headers)
        j = json.loads(r.text)
        return j["data"]["deviceIp"]
        #print(r.text)