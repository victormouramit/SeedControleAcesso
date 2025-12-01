import requests
import shutil
import zipfile
import os
import sys

VERSAO_ATUAL = "0.1.2"
URL_INFO = "https://raw.githubusercontent.com/victormouramit/SeedControleAcesso/refs/heads/main/update.json"
DOWNLOAD_VERSION = ""
def tem_update():
    info = requests.get(URL_INFO).json()
    ultima = info["version"]
    DOWNLOAD_VERSION = ultima
    print(ultima)
    return ultima, ultima != VERSAO_ATUAL, info["download_url"]


def aplicar_update(url):
    # baixa update.zip
    response = requests.get(url, stream=True)
    print(url)

    with open(f"{DOWNLOAD_VERSION}.zip", "wb") as f:
        shutil.copyfileobj(response.raw, f)

    # extrai tudo por cima do cliente atual
    with zipfile.ZipFile(f"{DOWNLOAD_VERSION}.zip", "r") as z:
        z.extractall(".")

    os.remove(f"{DOWNLOAD_VERSION}.zip")
    print("Atualização aplicada! Reiniciando...")
    os.execl(sys.executable, sys.executable, *sys.argv)