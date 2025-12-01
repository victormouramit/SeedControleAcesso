import requests
import shutil
import zipfile
import os
import sys

VERSAO_ATUAL = "0.1.3"
URL_INFO = "https://raw.githubusercontent.com/victormouramit/SeedControleAcesso/refs/heads/main/update.json"
def tem_update():
    info = requests.get(URL_INFO).json()
    ultima = info["version"]
    print(ultima)
    return ultima, ultima != VERSAO_ATUAL, info["download_url"]


def aplicar_update(url,download_version):
    # baixa update.zip
    response = requests.get(url, stream=True)
    print(url)

    with open(f"{download_version}.zip", "wb") as f:
        shutil.copyfileobj(response.raw, f)

    # extrai tudo por cima do cliente atual
    with zipfile.ZipFile(f"{download_version}.zip", "r") as z:
        z.extractall(".")

    os.remove(f"{download_version}.zip")
    print("Atualização aplicada! Reiniciando...")
    os.execl(sys.executable, sys.executable, *sys.argv)