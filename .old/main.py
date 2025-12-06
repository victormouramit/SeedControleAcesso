SERVER_IP_ADDRESS = "192.168.15.36"
SERVER_ADDRESS = f"http://{SERVER_IP_ADDRESS}"
SYSTEM_PASSWORD = "Hmite1234@"
USER_NAME = "system"

POST_AUTH_ENDPOINT = "/brms/api/v1.0/accounts/authorize"
PUT_KEEP_ALIVE_ENDPOINT = "/brms/api/v1.0/accounts/keepalive"
POST_UPDATE_TOKEN_ENDPOINT = "/brms/api/v1.0/accounts/updateToken"
POST_DEVICES_ENDPOINT = "/admin/API/tree/devices"
GET_PARKING_LOT_LIST_ENDPOINT = "/ipms/api/v1.1/parking-lot/list"

import requests
import simplejson as json
import time
from camera import Camera

# First Auth Proccess
first_auth = {
    "userName": USER_NAME,
    "ipAddress": ""
}

# Primeira AUTH
r = requests.post(f"{SERVER_ADDRESS}{POST_AUTH_ENDPOINT}",json=first_auth)

json_r = json.loads(r.text)
realm = json_r["realm"]
random_key = json_r["randomKey"]

print(f"first auth code:{r}")

# 5 passos para assinatura
from Crypto.Hash import MD5

temp = MD5.new(bytes(SYSTEM_PASSWORD,"utf-8")).hexdigest()
temp2 = MD5.new(bytes(f"{USER_NAME}{temp}","utf-8")).hexdigest()
temp3 = MD5.new(bytes(temp2,"utf-8")).hexdigest()
temp4 = MD5.new(bytes(f"{USER_NAME}:{realm}:{temp3}","utf-8")).hexdigest()
signature = MD5.new(bytes(f"{temp4}:{random_key}","utf-8")).hexdigest()
#print(signature)

# Second Auth Proccess
second_auth= {
    "userName": USER_NAME,
    "randomKey": random_key,
    "mac": "",
    "encryptType": "MD5",
    "ipAddress": "",
    "signature": signature,
}
r = requests.post(f"{SERVER_ADDRESS}{POST_AUTH_ENDPOINT}",json=second_auth)
# Code response for second auth code
print(f"second auth code:{r}")
response_text = json.loads(r.text)
duration = response_text["duration"] # 30 seconds
token = response_text["token"]

print(response_text)
headers = {"X-Subject-Token": f"{token}"}

''' devices_request = {
    "orgCode": "",
    "deviceCodes": [],
    "categories": []
} '''

#r = requests.post(f"{SERVER_ADDRESS}{POST_DEVICES_ENDPOINT}", json=devices_request, headers=headers)


# Get list of Parking Lots
""" r = requests.get(f"{SERVER_ADDRESS}{GET_PARKING_LOT_LIST_ENDPOINT}",headers=headers)
response = json.loads(r.text)


parking_lost = response["data"]["results"]
n_parking_lots = len(parking_lost) """

# Getting the amount of places to park
""" 
def update_token():
    new_signature = MD5.new(bytes(f"{temp4}:{token}")).hexdigest()
    r = requests.post(f"{SERVER_ADDRESS}{POST_UPDATE_TOKEN_ENDPOINT}",json={"signature": new_signature}, headers=headers)
    response = json.loads(r.text)
    token = response["data"]["token"]
    
def keep_alive_token():
    r = requests.put(f"{SERVER_ADDRESS}{PUT_KEEP_ALIVE_ENDPOINT}", json={ })
    response = json.loads(r.text)
    token = response["data"]["token"]

keep_alive_counter = 0
update_token_counter = 0
while True:
    for p in parking_lost:
        idle = int(p["idleParkingSpaceCount"])
        total = int(p["totalParkingSpaceCount"])
        parking_spaces = total - idle
        parking_lot_name = p["parkingLotName"]
        if parking_spaces == 0:
            print(f"The parking lot: {parking_lot_name} is full")
    time.sleep(1)
    keep_alive_counter += 1
    update_token_counter += 1
    # waits 20 seconds for using the keep alive interface
    if keep_alive_counter == 20:
        keep_alive_token()
        keep_alive_counter = 0

    # waits 20 seconds for using the update token
    if update_token_counter == 1200:
        update_token()
        update_token_counter = 0
 """





