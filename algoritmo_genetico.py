import random
import os
import csv

import sys
print('INDIVÍDUOS: ' + sys.argv[1])
print('GERAÇÕES: ' + sys.argv[2])
print('CROMOSSOMOS: ' + sys.argv[3])

# gerando lista de otimizações
otimizacoes = []
with open('passes.txt', 'r') as filehandle:
    for line in filehandle:
        currentPlace = line[:-1]
        otimizacoes.append(currentPlace)

os.system("rm -f algoritmo-genetico.log")
os.system("touch algoritmo-genetico.log")

print(otimizacoes)
print('====================================================')
subset = random.sample(otimizacoes, 50)

print(subset)

individuos = int(sys.argv[1])
geracoes = int(sys.argv[2])
cromosomos = int(sys.argv[3])

tempoMelhorIndividuo = float("inf")
melhorIndividuo = ''

populacao = []
print("populacao INICIAL")
count = 0


#gerando população aleatoriamente
for individuo in range(individuos):
    # global cromosomos
    populacao.append(random.sample(otimizacoes, cromosomos))

for i in populacao:
    count += 1
    print(count)
    print(i)

def obter_tempo():
    with open('run.log') as csvfile:
        readCSV = csv.reader(csvfile, delimiter='\t')
        soma = 0
        for row in readCSV:
            if (row[3] == 'JobRuntime'):
                pass
            else:
                soma += float(row[3])
    csvfile.close()
    return soma

def medir_fitness(populacao):
    cmd = ''
    fitness = [0 for i in range(individuos)]
    indiceFit = 0
    average = []
    for individuo in populacao:
        
        ist = ''
        for i in individuo:
            ist += i + ' '
        cmd = 'OPT="' + ist + ' " ./run.sh'
        tempos = []
        for indj in range(3):
            os.system(cmd)
            tempos.append(obter_tempo())
            print(tempos[indj])

        media = sum(tempos) / len(tempos)
        print('========================================================')
        print(media)
        print('========================================================')
        fitness[indiceFit] = media
        indiceFit += 1

    return fitness

def torneio(indice_individuo1, indice_individuo2):
    print("TORNEIO")
    print(str(indice_individuo1) + " - [" + ", ".join(str(f) for f in populacao[indice_individuo1]) + "] = " + "{:.9}".format(fitness[indice_individuo1]))
    print(str(indice_individuo2) + " - [" + ", ".join(str(f) for f in populacao[indice_individuo2]) + "] = " + "{:.9}".format(fitness[indice_individuo2]))

    if abs(fitness[indice_individuo1]) < abs(fitness[indice_individuo2]):
        indice_ganhador = indice_individuo1
    else:
        indice_ganhador = indice_individuo2

    print("ganhador")
    print(str(indice_ganhador) + " - [" + ", ".join(str(f) for f in populacao[indice_ganhador]) + "] = " + "{:.9}".format(fitness[indice_ganhador]))
    print("")
    
    return indice_ganhador

def sorteioNovaOtm():
    indice = random.randint(0, len(otimizacoes) - 1)
    return otimizacoes[indice]

#Função de mutação
def mutacao(indice_individuo):
    print("MUTAÇÃO")
    print(str(indice_individuo) + " - [" + ", ".join(str(f) for f in populacao[indice_individuo]) + "]")
    indice_mutado = random.randint(0, cromosomos - 2)
    novaOtimizacao = sorteioNovaOtm()

    while populacao[indice_individuo][indice_mutado] == novaOtimizacao:
        novaOtimizacao = sorteioNovaOtm()
    
    populacao[indice_individuo][indice_mutado] = novaOtimizacao

    print(str(indice_individuo) + " - [" + ", ".join(str(f) for f in populacao[indice_individuo]) + "]")
    print("")

#Função de crossover
def crossover(indice_individuo1, indice_individuo2):
    print("crossover")
    print(str(indice_individuo1) + " - [" + ", ".join(str(f) for f in populacao[indice_individuo1]) + "]")
    print(str(indice_individuo2) + " - [" + ", ".join(str(f) for f in populacao[indice_individuo2]) + "]")
    indice_crossover = random.randint(1, cromosomos - 1)
    print("Índice de crossover " + str(indice_crossover));
    print("Descendencias")
    descendencia1 = populacao[indice_individuo1][:indice_crossover] + populacao[indice_individuo2][indice_crossover:]
    print(descendencia1)
    descendencia2 = populacao[indice_individuo2][:indice_crossover] + populacao[indice_individuo1][indice_crossover:]
    print(descendencia2)
    return descendencia1, descendencia2

def imprime_arquivo(texto):
    arquivo = open('algoritmo-genetico.log', 'r')
    conteudo = arquivo.readlines()
    conteudo.append(texto)
    conteudo.append('\n')
    conteudo.append('\n')

    arquivo = open('algoritmo-genetico.log', 'w')
    arquivo.writelines(conteudo)

    arquivo.close()

#Imprime população
def imprime_populacao(fitness):
    indesc = ''
    temp = ''

    for individuo in range(individuos):
        indesc = str(individuo) + " - [" + ", ".join(str(f) for f in populacao[individuo]) + "]"
        temp = "---> Tempo: %f seg." % fitness[individuo]
        print(indesc)
        print(temp)
        imprime_arquivo(indesc)
        imprime_arquivo(temp)

for geracao in range(geracoes):

    print("")
    print("--------- GERAÇÃO " + str(geracao) +" ---------")
    imprime_arquivo("\n")
    imprime_arquivo("=================== GERAÇÃO " + str(geracao) +" ===================")
    fitness = medir_fitness(populacao)

    indiceMelhorIndividuo = fitness.index(min(fitness))
    if fitness[indiceMelhorIndividuo] < tempoMelhorIndividuo:
        tempoMelhorIndividuo = fitness[indiceMelhorIndividuo]
        melhorIndividuo = "[" + " ".join(str(f) for f in populacao[indiceMelhorIndividuo]) + "]"

    imprime_populacao(fitness)
    nova_geracao = [0 for x in range(individuos)]


    for i in range(int(individuos / 2)):
        individuo_ganhador = torneio(i, individuos - 1 - i)
        nova_geracao[i] = populacao[individuo_ganhador]

    mutacaoes = random.randint(0, individuos / 2)
    for j in range(mutacaoes):
        mutacao(random.randint(0, mutacaoes))

    indice_filhos = int(individuos / 2)
    for k in range(0, int(individuos / 2), 2):
        nova_geracao[indice_filhos], nova_geracao[indice_filhos + 1] = crossover(k, k+1)
        indice_filhos += 2
        print("")

    populacao = nova_geracao

print("")
print("------- ÚLTIMA GERAÇÃO -------")
imprime_arquivo("\n")
imprime_arquivo("=================== ÚLTIMA GERAÇÃO ===================")
imprime_populacao(medir_fitness(populacao))
imprime_arquivo("=================== MELHOR INDIVÍDUO ===================")
imprime_arquivo(str(tempoMelhorIndividuo))
imprime_arquivo(melhorIndividuo)
