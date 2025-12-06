import requests
import shutil
import zipfile
import os
import sys

URL_INFO = "https://raw.githubusercontent.com/victormouramit/SeedControleAcesso/refs/heads/main/update.json"

info = requests.get(URL_INFO, stream=True).json()
# baixa update.zip
download_version = info["version"]
response = requests.get(info["download_url"],stream=True)
print(f"{download_version} sendo baixada...")
with open(f"{download_version}.zip", "wb") as f:
    shutil.copyfileobj(response.raw, f)
# extrai tudo por cima do cliente atual
with zipfile.ZipFile(f"{download_version}.zip", "r") as z:
    z.extractall(".")
os.remove(f"{download_version}.zip")
print("Atualização aplicada! Reiniciando...")
os.execl(sys.executable, sys.executable, *sys.argv)

input("Press button")