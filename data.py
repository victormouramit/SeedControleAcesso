import json
from pathlib import Path
from enum import Enum

class Painel(Enum):
    One = "Painel 1"
    Two = "Painel 2"
    Three = "Painel 3"
    Four = "Painel 4"

painel_vagas = {
    Painel.One.value: 0,
    Painel.Two.value: 0,
    Painel.Three.value: 0,
    Painel.Four.value: 0,
}

FILE_NAME = "numbers.json"

def criar_arquivo_necessario():
    if not Path(FILE_NAME).exists():
        criar_atualizar()

def criar_atualizar(painel_vagas = painel_vagas):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(painel_vagas,fp=f)


def ler() -> dict:
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)
    