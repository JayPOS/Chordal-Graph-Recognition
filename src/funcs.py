def criarListaDeLista(i):
    a = []

    for i in range(i):
        a.append([])

    return a

def isEmpty(lst):
    if len(lst) == 0:
        return True
    return False

def listSubtract(a, b): # Nickolas?
    return [item for item in a if item not in b]

def ta_dentro(ciclo, ciclos): # verifica se o ciclo passado por parametro ja está na lista de ciclos
    for x in ciclos:
        if len(x) == len(ciclo):
            aux = ciclo.copy()
            aux.sort()
            aux2 = x
            aux2.sort()
            
            if aux2 == aux:
                return True
        else:
            return False
    return False

def achaCiclo(v_inicial, v, lst_aberta, inicio, ciclo, ciclos):
    if inicio == False and v == v_inicial: # se chegou no vertice inicial e nao eh o inicio.
        if ta_dentro(ciclo, ciclos) == False: # se o ciclo achado nao ta na lista de ciclos
            # print("Ciclo " + str(ciclo))
            ciclos.append(ciclo.copy()) # adiciona o ciclo na lst
        return # retorna

    for aresta in lst_aberta: # for aresta em lista_aberta
        if v in aresta: # for v em aresta
            copia = lst_aberta.copy() #cria copia de lst_aberta
            copia.remove(aresta) #remove a aresta atual da copia da lista
            
            a,b = aresta # atribui os vertices da aresta a 2 variaveis a e b


            if v == a and (b not in ciclo or b is v_inicial): # se v eh igual ao prim. elem. da aresta e o segundo nao ta no ciclo ou eh o vert inicial
                ciclo.append(b) #adiciona o segundo elem. em ciclo
                # print("a= " + str(a) + " b= " + str(b))
                achaCiclo(v_inicial, b, copia, False, ciclo, ciclos) # chama achaCiclo com o segundo elem. como v inicial.
                ciclo.remove(b) # remove o segundo elem. do ciclo
            elif v == b and (a not in ciclo or a is v_inicial): # senao se v e o segundo elem da aresta e o primeiro nao ta no ciclo ou eh o vert inicial.
                ciclo.append(a) # adiciona o prim elem. no ciclo
                # print("a= " + str(a) + " b= " + str(b))
                achaCiclo(v_inicial, a, copia, False, ciclo, ciclos) # chama achaCiclo com o prim elem como v inicial.
                ciclo.remove(a) # remove o primeiro elem do ciclo

def trataCiclos(ciclos): # Retira os ciclos de tamanho maior ou igual a 4 da lista de ciclos.
    lst_tratada = []
    for ciclo in ciclos: # for x em ciclos
        #print(ciclo)
        if len(ciclo) >= 4: # se tamanho de x é maior ou igual a 4
            lst_tratada.append(ciclo) # adiciona o ciclo achado.
    return lst_tratada # retorna lst_tratada.


def identificaCiclo(edge_list, n):
    # faz a busca em largura normal e depois quando aparece um vertice vizinho marcado
    #  verifica se ele ja apareceu antes, se sim, verifica se consegue achar ciclo no Acha ciclo, senao continua a busca.
    lst_aberta = []
    ciclo =[]
    lst_ciclos = []
    fila = []
    visitados = []
    for i in range(n):
        visitados.append(0)

    fila.append(0) # comeca pelo 0, adiciona ele na fila.
    while len(fila) != 0:

        vertice = fila.pop(0) # coloca 0 no vertice atual
        visitados[0] = 1
                            # e tira o 0 da fila
        for aresta in edge_list: # for arestas na lista de arestas
            if aresta not in lst_aberta: # se aresta nao ta em lst_aberta
                if vertice in aresta: # se vertice esta em aresta
                    lst_aberta.append(aresta) # adiciona aresta em lst_aberta

                    
                    if vertice == aresta[0]: # se vertice é o primeiro elem. da aresta.
                        if aresta[1] in fila: # se o segundo vertice da aresta ta na fila.
                            achaCiclo(aresta[1], aresta[1], lst_aberta, True, ciclo, lst_ciclos) #chama achaCiclo com o segundo vert da aresta como v_inicial e atual.
                        else: 
                            fila.append(aresta[1]) #senao adciona o vertice na fila
                            visitados[aresta[1]] = 1
                    elif vertice == aresta[1]: # senao se vertice é o segundo elem. da aresta.
                        if aresta[0] in fila: # se o primeiro elem. da aresta está na fila. 
                            achaCiclo(aresta[0], aresta[0], lst_aberta, True, ciclo, lst_ciclos) # chama achaCiclo com o prim vertice como v_inicial e atual
                        else:
                            fila.append(aresta[0]) #senao adiciona o prim. elemento na fila
                            visitados[aresta[0]] = 1
        if len(fila) == 0:
            for x in range(n):
                if visitados[x] == 0:
                    fila.append(x)
                    visitados[x] = 1
                            
    return trataCiclos(lst_ciclos) # retorna os ciclos tratados. (ler trataCiclos(ciclos))

