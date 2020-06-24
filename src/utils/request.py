import requests
import json
from config import Settings
from flask import session


def GetWithKey(path):
    # Requisição com autenticação
    url = f"{Settings().API_LINK}{path}"
    data = {
        "key": Settings().MD5_KEY,
    }
    retorno = requests.get(url, data=data)

    texto = retorno.text

    return json.loads(texto)


def PostWithoutAuth(path, data=None):
    # Requisição sem autenticação
    url = f"{Settings().API_LINK}{path}"
    # data = json.dumps(data)
    retorno = requests.post(url, data)

    texto = retorno.text

    return json.loads(texto)


def GetWithoutAuth(path, data):
    # Requisição sem autenticação
    url = f"{Settings().API_LINK}{path}"
    query = {
        "key": Settings().MD5_KEY,
    }
    query.update(data)
    retorno = requests.get(url, data=query)

    texto = retorno.text

    return json.loads(texto)


def GetWithUserToken(path):
    url = f"{Settings().API_LINK}{path}"
    header = {
        "auth": session['TKN'],
    }
    retorno = requests.get(url, headers=header)

    texto = retorno.text

    return json.loads(texto)

def PostWithUserToken(path, data):
    url = f"{Settings().API_LINK}{path}"
    header = {
        "auth": session['TKN'],
    }
    retorno = requests.post(url, headers=header, data=data)

    texto = retorno.text

    return json.loads(texto)
