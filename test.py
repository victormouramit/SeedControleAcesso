import logging

logger = logging.getLogger("Defense")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
arquivo = logging.FileHandler("defense.log", encoding="utf-8")


arquivo.setFormatter(formatter)

console = logging.StreamHandler()
console.setFormatter(formatter)

logger.addHandler(arquivo)
logger.addHandler(console)

l = "Zebra"

logger.info(f"{l}")