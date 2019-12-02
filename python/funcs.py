def create_list_of_list(i):
    a = []

    for i in range(i):
        a.append([])

    return a


def is_empty(lst):
    if len(lst) == 0:
        return True
    return False


def list_subtract(a, b):  # Nickolas?
    return [item for item in a if item not in b]


def is_inside(cycle, cycles):  # verifica se o ciclo passado por parametro ja esta na lista de ciclos
    for x in cycles:
        if len(x) == len(cycle):
            aux = cycle.copy()
            aux.sort()
            aux2 = x
            aux2.sort()

            if aux2 == aux:
                return True
        else:
            return False
    return False


def find_cycle(initial_vertex, v, lst_aberta, start, cycle, cycles):
    if start is False and v == initial_vertex:  # se chegou no vertice inicial e nao eh o inicio.
        if not is_inside(cycle, cycles):  # se o ciclo achado nao ta na lista de ciclos
            # print("Ciclo " + str(ciclo))
            cycles.append(cycle.copy())  # adiciona o ciclo na lst
        return  # retorna

    for edge in lst_aberta:  # for aresta em lista_aberta
        if v in edge:  # for v em aresta
            copied = lst_aberta.copy()  # cria copia de lst_aberta
            copied.remove(edge)  # remove a aresta atual da copia da lista

            a, b = edge  # atribui os vertices da aresta a 2 variaveis a e b

            if v == a and (
                    b not in cycle or b is initial_vertex):  # se v eh igual ao prim. elem. da aresta e o segundo nao ta no ciclo ou eh o vert inicial
                cycle.append(b)  # adiciona o segundo elem. em ciclo
                # print("a= " + str(a) + " b= " + str(b))
                find_cycle(initial_vertex, b, copied, False, cycle,
                           cycles)  # chama achaCiclo com o segundo elem. como v inicial.
                cycle.remove(b)  # remove o segundo elem. do ciclo
            elif v == b and (
                    a not in cycle or a is initial_vertex):  # senao se v e o segundo elem da aresta e o primeiro nao ta no ciclo ou eh o vert inicial.
                cycle.append(a)  # adiciona o prim elem. no ciclo
                # print("a= " + str(a) + " b= " + str(b))
                find_cycle(initial_vertex, a, copied, False, cycle, cycles)  # chama achaCiclo com o prim elem como v inicial.
                cycle.remove(a)  # remove o primeiro elem do ciclo


def treat_cycles(cycles):  # Retira os ciclos de tamanho maior ou igual a 4 da lista de ciclos.
    treated_list = []
    for cycle in cycles:  # for x em ciclos
        # print(ciclo)
        if len(cycle) >= 4:  # se tamanho de x e maior ou igual a 4
            treated_list.append(cycle)  # adiciona o ciclo achado.
    return treated_list  # retorna lst_tratada.


def identify_cycle(edge_list, n):
    # faz a busca em largura normal e depois quando aparece um vertice vizinho marcado
    #  verifica se ele ja apareceu antes, se sim, verifica se consegue achar ciclo no Acha ciclo, senao continua a busca.
    lst_aberta = []
    cycle = []
    cycle_list = []
    queue = []
    visited = []
    for i in range(n):
        visited.append(0)

    queue.append(0)  # comeca pelo 0, adiciona ele na fila.
    while len(queue) != 0:

        vertex = queue.pop(0)  # coloca 0 no vertice atual
        visited[0] = 1
        # e tira o 0 da fila
        for edge in edge_list:  # for arestas na lista de arestas
            if edge not in lst_aberta:  # se aresta nao ta em lst_aberta
                if vertex in edge:  # se vertice esta em aresta
                    lst_aberta.append(edge)  # adiciona aresta em lst_aberta

                    if vertex == edge[0]:  # se vertice e o primeiro elem. da aresta.
                        if edge[1] in queue:  # se o segundo vertice da aresta ta na fila.
                            find_cycle(edge[1], edge[1], lst_aberta, True, cycle,
                                       cycle_list)  # chama achaCiclo com o segundo vert da aresta como v_inicial e atual.
                        else:
                            queue.append(edge[1])  # senao adciona o vertice na fila
                            visited[edge[1]] = 1
                    elif vertex == edge[1]:  # senao se vertice e o segundo elem. da aresta.
                        if edge[0] in queue:  # se o primeiro elem. da aresta ests na fila.
                            find_cycle(edge[0], edge[0], lst_aberta, True, cycle,
                                       cycle_list)  # chama achaCiclo com o prim vertice como v_inicial e atual
                        else:
                            queue.append(edge[0])  # senao adiciona o prim. elemento na fila
                            visited[edge[0]] = 1
        if len(queue) == 0:
            for x in range(n):
                if visited[x] == 0:
                    queue.append(x)
                    visited[x] = 1

    return treat_cycles(cycle_list)  # retorna os ciclos tratados. (ler trataCiclos(ciclos))
