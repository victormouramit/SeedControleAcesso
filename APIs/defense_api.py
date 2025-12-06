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
    def auth(self):
        # Primeira AUTH
        r = requests.post(f"{self.server_address}{POST_AUTH_ENDPOINT}",json={"userName": USER_NAME, "ipAddress": ""})
        print(f"First Auth:{r}") ## Deve dar 401
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
            if datetime.now() >= tempo + timedelta(seconds=20):
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
    def get_device(self, code):
        r = requests.get(f"{self.server_address}{GET_DEVICE_BY_CODE_ENDPOINT}{code}",json={},headers=self.headers)
        j = json.loads(r.text)
        return j["data"]["deviceIp"]
        #print(r.text)

