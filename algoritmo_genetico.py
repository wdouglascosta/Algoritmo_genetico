import random

individuos = 20
cromosomos = 9
geracoes = 3

#Creando un arreglo de 10 x 10
populacao = [[0 for x in range(cromosomos)] for x in range(individuos)]

print("populacao INICIAL")

#gerando população aleatoriamente
for individuo in range(individuos):
    for cromosomo in range(cromosomos):
        populacao[individuo][cromosomo] = random.randint(0, 1)


#Função para medir fitness
def medir_fitness(populacao): 
    fitness = [0 for i in range(individuos)]
    valores = ["Signo", 2 ** 5, 2 ** 4, 2 ** 3, 2 ** 2, 2 ** 1, 2 ** 0, 2 ** -1, 2 ** -2]
    print("")
    print("VALORES PARA REMOVER FITNESS")
    print(valores)

    for individuo in range(individuos):
        for cromosomo in range(1, cromosomos):
            fitness[individuo] += populacao[individuo][cromosomo] * valores[cromosomo]
        #Alterando o signo de acordo com o valor
        if populacao[individuo][0] == 1:
            fitness[individuo] *= -1

    #Imprimindo valores de fitness
    print("")
    print("fitness")
    for individuo in range(individuos):
        print(str(individuo) + " - [" + ", ".join(str(f) for f in populacao[individuo]) + "] = " + "{:.9}".format(fitness[individuo]))
    
    total_fitness = 0
    for x in range(individuos):
        total_fitness += abs(fitness[x])
    print("TOTAL fitness " + str(total_fitness))
    print("")
    return fitness


#Função para realizar torneio
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


#Função de mutação
def mutacao(indice_individuo):
    print("MUTAÇÃO")
    print(str(indice_individuo) + " - [" + ", ".join(str(f) for f in populacao[indice_individuo]) + "]")
    indice_mutado = random.randint(0, cromosomos - 1)
    
    if populacao[indice_individuo][indice_mutado] == 0:
        populacao[indice_individuo][indice_mutado] = 1
    else:
        populacao[indice_individuo][indice_mutado] = 0

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


#Imprime população
def imprime_populacao():
    for individuo in range(individuos):
        print(str(individuo) + " - [" + ", ".join(str(f) for f in populacao[individuo]) + "]")


for geracao in range(geracoes):
    print("")
    print("--------- GERAÇÃO " + str(geracao) +" ---------")
    imprime_populacao()
    nova_geracao = [0 for x in range(individuos)]
    
    fitness = medir_fitness(populacao)

    for i in range(individuos / 2):
        individuo_ganhador = torneio(i, individuos - 1 -i)
        nova_geracao[i] = populacao[individuo_ganhador]

    mutacaoes = random.randint(0, individuos / 2)
    for j in range(mutacaoes):
        mutacao(random.randint(0, mutacaoes))

    indice_filhos = individuos / 2
    for k in range(0, individuos / 2, 2):
        nova_geracao[indice_filhos], nova_geracao[indice_filhos + 1] = crossover(k, k+1)
        indice_filhos += 2
        print("")

    populacao = nova_geracao

print("")
print("------- ÚLTIMA GERAÇÃO -------")
imprime_populacao()
medir_fitness(populacao)
