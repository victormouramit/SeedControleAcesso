import requests
import shutil
import zipfile
import os
import sys

VERSAO_ATUAL = "1.0.0"
URL_INFO = "https://raw.githubusercontent.com/victormouramit/SeedControleAcesso/refs/heads/main/update.json"
def tem_update():
    info = requests.get(URL_INFO).json()
    ultima = info["version"]
    print(ultima)
    return ultima, ultima != VERSAO_ATUAL, info["download_url"]


def aplicar_update(url):
    # baixa update.zip
    response = requests.get(url, stream=True)
    with open("update.zip", "wb") as f:
        shutil.copyfileobj(response.raw, f)

    # extrai tudo por cima do cliente atual
    with zipfile.ZipFile("update.zip", "r") as z:
        z.extractall(".")

    os.remove("update.zip")
    print("Atualização aplicada! Reiniciando...")
    os.execl(sys.executable, sys.executable, *sys.argv)

ultima, precisa, url = tem_update()

print(f"{ultima}, p: {precisa}, url:{url}")