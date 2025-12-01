import requests
import simplejson as json
import re

HTTP_METHOD = "http://"
BASE_ENDPOINT = "/cgi-bin/"
IP_ADDRESS = f"{HTTP_METHOD}192.168.15.5"
GET_ALARM_STATES_ENDPOINTS = f"{BASE_ENDPOINT}alarm.cgi?action=getOutState"
GET_ALARM_OUTPUT_CHANNELS = f"{BASE_ENDPOINT}alarm.cgi?action=getOutSlots"
GET_CONFIG_ALARM_OUT = f"{BASE_ENDPOINT}configManager.cgi?action=getConfig&name=AlarmOut"
GET_SET_CONFIG_ALARM_OUT = f"{BASE_ENDPOINT}configManager.cgi?action=setConfig&AlarmOut[1].Mode=1&AlarmOut[1].Name=Beep"

r = requests.get(f"{IP_ADDRESS}{GET_ALARM_STATES_ENDPOINTS}")
print(r)
print(r.headers)
from Crypto.Hash import MD5
if r.status_code == 401:
    auth = r.headers["WWW-Authenticate"].replace('Digest ', 'Digest username="admin", ')
    auth = f'{auth},uri="/{GET_ALARM_STATES_ENDPOINTS}"'
    match = re.search(r'realm="([^"]*)"',auth)
    if match:
        realm = match.group(1)
    match = re.search(r'nonce="([^"]*)"',auth)
    if match:
        nonce = match.group(1)
    match = re.search(r'qop="([^"]*)"',auth)
    if match:
        qop = match.group(1)
    match = re.search(r'opaque="([^"]*)"',auth)
    if match:
        opaque = match.group(1)
    
    username = "admin"
    passwd = "Hmite1234@"
    method = "GET"
    uri = GET_SET_CONFIG_ALARM_OUT
    nc = "00000001"
    cnonce = "0a4f113b"
    # NÂO MUDE UMA LINHA DESSA PORRA
    A1 = MD5.new(bytes(f'{username}:{realm}:{passwd}',"utf-8")).hexdigest()
    A2 = MD5.new(bytes(f"{method}:{uri}","utf-8")).hexdigest()
    response =MD5.new(bytes(f'{A1}:{nonce}:{nc}:{cnonce}:{qop}:{A2}',"utf-8")).hexdigest()

    auth = f'Digest username="{username}",realm="{realm}",nonce="{nonce}",uri="{uri}",response="{response}",opaque="{opaque}",qop={qop},nc={nc},cnonce="{cnonce}"'
    



