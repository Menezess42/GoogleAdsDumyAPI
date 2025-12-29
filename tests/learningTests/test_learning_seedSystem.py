from pprint import pprint
import pandas as pd

def mulberry32(seed):
    state = {"value": seed}

    def generate():
        state["value"] = (state["value"] + 0x6D2B79F5) & 0xFFFFFFFF
        t = state["value"]
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t = (t ^ (t + ((t ^ (t >> 7)) * (t | 61)))) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) >> 0) / 4294967296

    return generate

aux_list = [
    "cadeira",
    "lampada",
    "computador",
    "jardim",
    "montanha",
    "chocolate",
    "telefone",
    "biblioteca",
    "oceano",
    "violino",
    "janela",
    "borboleta",
    "relogio",
    "telescopio",
    "cachoeira",
    "piano",
    "nuvem",
    "labirinto",
    "estrela",
    "cathedral",
]

lista_cores = [
    "vermelho",
    "azul",
    "verde",
    "amarelo",
    "roxo",
    "laranja",
    "rosa",
    "cinza",
    "marrom",
    "turquesa",
    "carmesim",
    "índigo",
    "coral",
]

lista_animais = ["leão", "águia", "golfinho", "tigre", "panda", "lobo", "coruja"]

lista_profissoes = [
    "arquiteto",
    "médico",
    "engenheiro",
    "professor",
    "chef",
    "piloto",
    "cientista",
    "artista",
    "advogado",
    "músico",
    "astronauta",
    "fotógrafo",
    "escritor",
    "mecânico",
    "bailarino",
    "programador",
    "veterinário",
]


def simulated_API(gen):
    number = gen()
    aux_list_number = len(aux_list) * number
    lista_cores_number = len(lista_cores) * number
    lista_animais_number = len(lista_animais) * number
    lista_profissoes_number = len(lista_profissoes) * number

    aux_list_number = int(aux_list_number)
    lista_cores_number = int(lista_cores_number)
    lista_animais_number = int(lista_animais_number)
    lista_profissoes_number = int(lista_profissoes_number)

    api = {
        "list1": aux_list[aux_list_number],
        "list2": lista_cores[lista_cores_number],
        "list3": lista_animais[lista_animais_number],
        "list4": lista_profissoes[lista_profissoes_number],
    }

    return api


gen = mulberry32(42)


def test_reproducibility_of_seed_list1():
    api = simulated_API(gen)
    assert api["list1"] == "relogio"


def test_reproducibility_of_seed_list2():
    api = simulated_API(gen)
    assert api["list2"] == "laranja"


def test_reproducibility_of_seed_list3():
    api = simulated_API(gen)
    assert api["list3"] == "lobo"


def test_reproducibility_of_seed_list4():
    api = simulated_API(gen)
    assert api["list4"] == "fotógrafo"
