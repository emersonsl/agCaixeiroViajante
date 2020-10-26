import math
import numpy as np
from random import randint
from random import sample
from random import shuffle
from random import random
import matplotlib.pyplot as plt 
from matplotlib import colors
import pandas as pd

pontos = []
individuos = []
novosIndividuos = []
fitness = []
geracoes = []
qntPontos = 30
qntIndividuos = 100
qntGeracoes = 100
taxaMutacao = 0.2
taxaCrossover = 0.6

def gerarPontos():
    for i in range(qntPontos):
        x = randint(0, 300)
        y = randint(0, 300)
        pontos.append((x,y))

def plotarPontos():
    for i in range(qntPontos):
        plt.scatter(pontos[i][0], pontos[i][1], marker='o')

def plotarCaminho(individuo):
    x_c = []
    y_c = []
    for i in range(qntPontos):
        i_ponto = individuo[i]
        x_c.append(pontos[i_ponto][0])
        y_c.append(pontos[i_ponto][1])
    plt.plot(x_c,y_c, color='r')

def plotarGeracao(i_geracao):
    df = geracoes[i_geracao]
    df = df.drop(columns=['Fitness'])
    lista = df.values.tolist()
    plotarCaminho(lista[0])
    i_pontoInicial = lista[0][0]
    plt.scatter(pontos[i_pontoInicial][0], pontos[i_pontoInicial][1], color='r',marker='o')
    plt.title("Geração "+str(i_geracao), fontdict=None, loc='center', pad=None)
    plt.show()

def gerarIndividuos():
    for i in range(qntIndividuos):
        individuos.append(sample(range(0, qntPontos),qntPontos))   

def calcularDistancia(a, b):
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

def calcularFitness():
    fitness.clear()
    for i in range(qntIndividuos):
        soma = 0
        for k in range(qntPontos-1):
            pontoA = pontos[individuos[i][k]]
            pontoB = pontos[individuos[i][k+1]]
            soma+=calcularDistancia(pontoA, pontoB)
        fitness.append(soma)

def ordenarIndividuos():
    nomePontos = []
    for i in range(qntPontos): #gerando nome das colunas
        nomePontos.append("P"+str(i+1))

    df = pd.DataFrame(individuos, index=None, columns=nomePontos)
    df['Fitness'] = fitness
    df = df.sort_values(['Fitness'])
    geracoes.append(df)
    df = df.drop(columns=['Fitness'])
    individuos.clear()
    listaTemp = df.values.tolist()

    for i in range(len(listaTemp)):
        individuos.append(listaTemp[i])

def crossoverOrdem(i_pai1 , i_pai2):
    binario = bin(randint(0,((2**qntIndividuos)-1)))[2:]
    
    for i in range(qntPontos-len(binario)): #adicionando zeros a esquerda
        binario = "0"+binario

    filho = np.zeros((qntPontos,), dtype=int).tolist()
    lista = [] 
    lista_aux = []

    pai1 = individuos[i_pai1]
    pai2 = individuos[i_pai2]

    #caso seja 1 o filho recebe o valor do indice referente ao pai 1, caso zero salva na lista
    for i in range(qntPontos):
        filho[i] = pai1[i] if binario[i] == '1' else lista.append(pai1[i]) 
    
    for i in range(len(lista)): #lista com os indices dos elementos do pai 2, de acordo com lista 1
        lista_aux.append(pai2.index(lista[i])) 
    
    for i in range(qntPontos): #substituidos as posicões zeros pelos valores dos menores indices salvos na lista aux
        if(binario[i] == '0'):
            filho[i] = pai2[min(lista_aux)]
            lista_aux.remove(min(lista_aux))
    
    return filho

def mutacaoPermutacao(i_ele):
    i1 = randint(0, qntPontos-1)
    i2 = randint(0, qntPontos-1)
    ele = individuos[i_ele]
    temp = ele[i1]
    ele[i1] = ele[i2]
    ele[i2] = temp

def mutacaoSubLista(i_ele):
    i1 = randint(0, qntPontos-1)
    i2 = randint(i1, qntPontos-1)

    ele = individuos[i_ele]
    
    temp = ele[i1:i2+1]
    shuffle(temp)
    
    for i in range(len(temp)):
        ele[i+i1] = temp[i]

def elitismo():
    for i in range(int(qntIndividuos/2)):
        novosIndividuos.append(individuos[i])
    
def crossover():
    
    for i in range(int(qntIndividuos/4)):
        i1 = randint(0, len(individuos)-1)
        i2 = randint(0, len(individuos)-1)
        
        while(i1==i2): #evitando que o pai 2 seja igual ao pai 1
            i2 = randint(0, len(individuos)-1)
        
        ind1 = individuos[i1]
        ind2 = individuos[i2]
        if(random()<=taxaCrossover): #executa o crossover caso o número sorteado seja menor que a taxa 
            novosIndividuos.append(crossoverOrdem(i1,i2))
            novosIndividuos.append(crossoverOrdem(i2,i1))
        else: #adiciona os pais sorteados
            novosIndividuos.append(ind1)
            novosIndividuos.append(ind2)
        individuos.remove(ind1)
        individuos.remove(ind2)
    
    if(qntIndividuos % 4 != 0): #compensando divisões não exatas
        i = randint(0, len(individuos)-1)
        novosIndividuos.append(individuos[i])
        individuos.remove(individuos[i])

def mutacao():
    for i in range(qntIndividuos):
        if(random()<=taxaMutacao):
            mutacaoPermutacao(i)
            mutacaoSubLista(i)

def atualizarLista():
    individuos.clear()
    for i in range(qntIndividuos):
        individuos.append(novosIndividuos[i])
    
    novosIndividuos.clear()
def plotGeracao():
    plotarPontos()
    plotarCaminho(individuos[0])
    plt.show()

def ploatGeracoes():
    for i in range(0, qntGeracoes, int(qntGeracoes/5)):
        plotarGeracao(i)
        print("Geração "+str(i)+":\n")
        print(geracoes[i].head())

def executarAG():
    gerarPontos()
    gerarIndividuos()
    calcularFitness()
    ordenarIndividuos()

    for i in range(qntGeracoes-1):
        elitismo()
        crossover()
        atualizarLista()
        mutacao()
        calcularFitness()
        ordenarIndividuos()

    ploatGeracoes()
executarAG()



