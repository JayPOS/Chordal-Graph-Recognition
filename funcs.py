def ta_dentro(ciclo, ciclos):
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
    if inicio == False and v == v_inicial: # se ta no inicio ele pula essa parte
        if ta_dentro(ciclo, ciclos) == False:
            # print("Ciclo " + str(ciclo))
            ciclos.append(ciclo.copy())
        return

    for aresta in lst_aberta:
        if v in aresta:
            copia = lst_aberta.copy()
            copia.remove(aresta)
            
            a,b = aresta

            if v == a and (b not in ciclo or b is v_inicial):
                ciclo.append(b)
                # print("a= " + str(a) + " b= " + str(b))
                achaCiclo(v_inicial, b, copia, False, ciclo, ciclos)
                ciclo.remove(b)
            elif v == b and (a not in ciclo or a is v_inicial):
                ciclo.append(a)
                # print("a= " + str(a) + " b= " + str(b))
                achaCiclo(v_inicial, a, copia, False, ciclo, ciclos)
                ciclo.remove(a)

def trataCiclos(ciclos):
    lst_tratada = []
    for ciclo in ciclos:
        if len(ciclo) >= 4:
            lst_tratada.append(ciclo)
    return lst_tratada


def identificaCiclo(edge_list):
    #faz a busca em largura normal e depois quando aparece um vertice vizinho marcado
    #  verifica se ele ja apareceu antes, se sim, verifica se consegue achar ciclo, senao continua a busca.
    lst_aberta = []
    ciclo =[]
    lst_ciclos = []
    fila = []

    fila.append(0)
    while len(fila) != 0:

        vertice = fila.pop(0)
        
        for aresta in edge_list:
            if aresta not in lst_aberta:
                if vertice in aresta:
                    lst_aberta.append(aresta)
                    if vertice == aresta[0]:
                        if aresta[1] in fila:
                            achaCiclo(aresta[1], aresta[1], lst_aberta, True, ciclo, lst_ciclos)
                        else:
                            fila.append(aresta[1])
                    elif vertice == aresta[1]:
                        if aresta[0] in fila:
                            achaCiclo(aresta[1], aresta[1], lst_aberta, True, ciclo, lst_ciclos)
                        else:
                            fila.append(aresta[0])
                            
    return trataCiclos(lst_ciclos)



def is_chordal(ciclos, adj_list):
    for ciclo in ciclos:
        for vertice in ciclo:
            grau = 0

            # print("opa", vertice)
            for vizinho in adj_list[vertice]:
                if vizinho in ciclo:
                    grau+=1
            
            if grau >= 3:
                break

        else:
            print("Ciclo nao cordal = ", ciclo)
            return False
    return True