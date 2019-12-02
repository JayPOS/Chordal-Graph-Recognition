import networkx as nx
import funcs as f
from funcs import create_list_of_list, is_empty


class Graph:
    def __init__(self, n, edges, naoSepararComps=None):
        self.G = nx.Graph()
        self.n = n
        self.edges = edges
        self.componentes = []

        if naoSepararComps is None or naoSepararComps is False:
            # Cria os componentes para o networkx
            for i in range(n):
                self.G.add_node(i)

            self.G.add_edges_from(self.edges)
            componentes = [self.G.subgraph(c).copy() for c in nx.connected_components(self.G)]
            for comp in componentes:
                minNode = min(comp.nodes())
                self.componentes.append([minNode, Graph(comp.number_of_nodes(),
                                                        [[e[0] - minNode, e[1] - minNode] for e in comp.edges()],
                                                        True)])

    def criaArq(self):
        with open("teste.txt", "w+") as f:
            string = str(str(self.G.number_of_nodes()) + " " + str(self.G.number_of_edges()))
            f.write(string + "\n")
            x = self.G.edges()
            for i in list(x):
                f.write(str(i[0]) + " " + str(i[1]) + "\n")
            return self

    def leArq(self, nome_arq):
        with open(nome_arq, "r") as f:
            line = f.readline().split()
            self.G.add_nodes_from(range(1, int(line[0])))
            for i in range(int(line[1])):
                line = f.readline().split()
                self.G.add_edge(int(line[0]), int(line[1]))
            return self

    def leEdgeList(self, path):
        self.G = nx.read_edgelist(path, nodetype=int)

    def leAdjList(self, path):
        self.G = nx.read_adjlist(path, nodetype=int)

    def escreveEdgeList(self, path):
        nx.write_edgelist(self.G, path)

    def escreveAdjList(self, path):
        nx.write_adjlist(self.G, path)

    def gera_entrada(self):
        return list(self.G.edges())

    def gera_adlist(self):
        adjlist = create_list_of_list(self.n)

        for aresta in self.edges:
            adjlist[aresta[0]].append(aresta[1])
            adjlist[aresta[1]].append(aresta[0])

        return adjlist

    def is_connected(self):
        def recursiveDfs(adjLst, vis, i):
            vis[i] = True
            for j in adjLst[i]:
                if not vis[j]:
                    recursiveDfs(adjLst, vis, j)

        listaAdj = self.gera_adlist()
        vis = [False] * self.n
        recursiveDfs(listaAdj, vis, 0)

        for v in vis:
            if not v:
                return False
        return True

    def get_lexBfs(self):
        vertex = []
        listaAdj = self.gera_adlist()

        VERTEX = 0
        VIZINHOS = 1
        ROTULO = 2
        VISITADO = 3
        LARGURA = 4

        for i in range(self.n):
            vertex.append([
                i,  # vertice
                listaAdj[i],  # vizinhos
                [],  # rotulos
                False,  # visitado
                -1])  # largura

        def maxVertex():
            maior = 0

            for i in range(self.n):
                if not vertex[i][VISITADO]:
                    if len(vertex[i][ROTULO]) > len(vertex[maior][ROTULO]):
                        maior = i

            return maior

        def select(i):
            v = maxVertex()
            vertex[v][VISITADO] = True
            vertex[v][LARGURA] = i

            return v

        def update(v, i):
            for j in range(len(listaAdj[v])):
                if not vertex[listaAdj[v][j]][VISITADO]:
                    vertex[listaAdj[v][j]][ROTULO].append(i)

        for i in reversed(range(self.n)):
            v = select(i)
            update(v, i)

        def sortFunc(x):
            return x[LARGURA]

        vertex.sort(key=sortFunc)

        return vertex

    # Retorna o ciclo problematico
    # Caso contrario, retorna None
    def is_chordal(self):
        def elimPerfeita(grafo, correcao=None):
            lex = grafo.get_lexBfs()

            L = []
            for i in range(grafo.n):
                L.append(set())

            for v in lex:
                if not is_empty(v[2]):
                    u = min(v[2])
                    L[u] = L[u].union(set([lex[x][0] for x in v[2]]) - {lex[u][0]})
                else:
                    break

            for i in range(grafo.n):
                if not is_empty(L[i] - set(lex[i][1])):
                    problema = list(L[i]) + lex[i][1]
                    problema.append(lex[i][0])
                    if correcao is not None:
                        return False, [vertice + correcao for vertice in problema]
                    else:
                        return False, problema
            return True

        for componente in self.componentes:
            elim = elimPerfeita(componente[1], componente[0])
            if elim is not True:
                return elim

        return True

    # Retorna o ciclo problematico
    # Caso contrario, retorna None
    def is_chordal_brute(self, n):
        ciclos = f.identify_cycle(self.gera_entrada(), n)  # chama funcao que identifica os ciclos
        adj_list = self.gera_adlist()  # gera lst de adjacencia.
        for ciclo in ciclos:  # for x in ciclos
            for vertice in ciclo:  # for v em x
                grau = 0  # grau = 0
                for vizinho in adj_list[vertice]:  # for vizinho em N(v)
                    if vizinho in ciclo:  # se vizinho em ciclo
                        grau += 1  # grau = grau + 1
                if grau >= 3:  # se grau maior ou igual a 3, para e retorna true
                    break
            else:  # se nao ha v com grau >= 3 no ciclo, retorna false e o ciclo.
                print(ciclo)
                return False, ciclo
        return True

    def is_interval_graph(self):
        return self.is_chordal() is True and self.is_at_free()

    def is_interval_graph_brute(self, n):
        return self.is_chordal_brute(n) is True and self.is_at_free()

    def is_at_free(self):
        countRotulos = 0
        comp_rotuladas = []

        adj = self.gera_adlist()

        def bfs(seen, adj, v, idRotulos, rotulo):

            queue = [v]
            seen[v] = True
            idRotulos[v] = rotulo

            while len(queue):

                v = queue.pop(0)

                for w in adj[v]:

                    if not seen[w]:
                        idRotulos[w] = rotulo
                        seen[w] = True
                        queue.append(w)

        for v in range(self.n):

            rotulos = [0] * self.n

            seen = [False] * self.n

            for w in adj[v]:
                seen[w] = True

            seen[v] = True

            for w in range(self.n):

                if not seen[w]:
                    countRotulos += 1
                    bfs(seen, adj, w, rotulos, countRotulos)

            comp_rotuladas.append(rotulos)

        for k in range(self.n):
            for j in range(k + 1, self.n):
                for i in range(j + 1, self.n):
                    if comp_rotuladas[k][j] and comp_rotuladas[k][j] == comp_rotuladas[k][i] and comp_rotuladas[i][
                        k] and comp_rotuladas[i][k] == comp_rotuladas[i][j] and comp_rotuladas[j][k] and \
                            comp_rotuladas[j][k] == comp_rotuladas[j][i]:
                        return False

        return True

# edges = [(1,2), (1, 3), (3, 4), (4, 2), (0, 1)]
# print(f.identificaCiclo(edges))

# # print("aaa " + str(edges[0][1]))
# g = Graph(5, edges)
# Graph.criaGrafo(g)
# g = Graph.criaArq(g)

# x = g.gera_entrada()
# adj = g.gera_adlist()

# print(f.is_chordal(f.identificaCiclo(g.gera_entrada()), adj))
