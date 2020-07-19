import requests
import json
from config import Settings
from flask import session


def GetFree(path):
    # Requisição livre
    url = f"{Settings().API_LINK}{path}"
    retorno = requests.get(url)

    texto = retorno.text

    return json.loads(texto)


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


def PatchWithUserToken(path, data):
    url = f"{Settings().API_LINK}{path}"
    header = {
        "auth": session['TKN'],
    }
    retorno = requests.patch(url, headers=header, data=data)

    texto = retorno.text

    return json.loads(texto)


def DeleteWithUserToken(path):
    url = f"{Settings().API_LINK}{path}"
    header = {
        "auth": session['TKN'],
    }
    retorno = requests.delete(url, headers=header)

    texto = retorno.text

    return json.loads(texto)


def GetFromBoletimService(alunoID):
    url = f"{Settings.BOLETIM_API}{alunoID}.json"
    retorno = requests.get(url)
    texto = retorno.text
    return json.loads(texto)
