import os, time
import json
from datetime import datetime

def limpar_tela():
    os.system("cls")

def aguarde(segundos):
    time.sleep(segundos)

def inicializarBancoDeDados():
    try:
        banco = open("log.dat", "r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("log.dat", "w")

def escreverDados(nome, pontos):
    banco = open("log.dat", "r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    data_br = datetime.now().strftime("%d/%m/%Y")
    hora_br = datetime.now().strftime("%H:%M:%S")
    dadosDict[nome] = (pontos, data_br, hora_br)

    banco = open("log.dat", "w")
    banco.write(json.dumps(dadosDict))
    banco.close()

def maior_pontuador():
    banco = open("log.dat", "r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    nome_maior = None
    dataJogada = None
    maior_pontos = -1

    for nome, info in dadosDict.items():
        pontos = info[0]
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            dataJogada = info[1]

    return nome_maior, maior_pontos, dataJogada
