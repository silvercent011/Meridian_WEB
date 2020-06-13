import requests
import json
from config import Settings

def req_level0(path):
    # Requisição sem autenticação
    url = f"{Settings().API_LINK}{path}"
    data = {
        "key": Settings().MD5_KEY,
    }
    retorno = requests.get(url, data=data)

    texto = retorno.text

    return json.loads(texto)

def req_level1(path, data = None):
    # Requisição sem autenticação
    url = f"{Settings().API_LINK}{path}"
    # data = json.dumps(data)
    retorno = requests.post(url, data)

    texto = retorno.text

    return json.loads(texto)


def req_level2(path, data):
    # Requisição sem autenticação
    url = f"{Settings().API_LINK}{path}"
    data = {
        "key": Settings().MD5_KEY,
        "dt_nascimento": data['dt_nascimento']
    }
    retorno = requests.get(url, data=data)

    texto = retorno.text

    return json.loads(texto)