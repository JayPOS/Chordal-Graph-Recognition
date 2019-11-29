import networkx as nx
from src import funcs as f
from src.funcs import criarListaDeLista, listSubtract, isEmpty


class Graph:
    def __init__(self, n, edges):
        self.G = nx.Graph()
        self.n = n
        self.edges = edges
        self.componentes = None

    @staticmethod
    def criaGrafo(self):
        for i in range(1, self.n):
            self.G.add_node(i)

        self.G.add_edges_from(self.edges)
        if nx.is_connected(self.G) is False:
            self.componentes = [self.G.subgraph(c).copy() for c in nx.connected_components(self.G)]
        return self

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
        adjlist = criarListaDeLista(self.n)

        for aresta in self.edges:
            #print("p.aresta2 ", aresta[0], " p.aresta1 ", aresta[1])
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
                i,  #vertice
                listaAdj[i], #vizinhos
                [], #rotulos
                False, #visitado
                -1]) #largura

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

        vertex.sort(key = sortFunc)

        return vertex

    #Retorna o ciclo problematico
    #Caso contrario, retorna None
    def is_chordal(self):
        lex = self.get_lexBfs()

        L = []
        for i in range(self.n):
            L.append(set())

        for v in lex:
            if not isEmpty(v[2]):
                u = min(v[2])
                L[u] = L[u].union(set([lex[x][0] for x in v[2]]) - {lex[u][0]})
            else:
                break

        for i in range(self.n):
            if not isEmpty(L[i] - set(lex[i][1])):
                problema = list(L[i]) + lex[i][1]
                problema.append(lex[i][0])
                return False, problema
        return True

    #Retorna o ciclo problematico
    #Caso contrario, retorna None
    def is_chordal_brute(self, n):
        
        ciclos = f.identificaCiclo(self.gera_entrada(), n) # chama funcao que identifica os ciclos
        adj_list = self.gera_adlist() # gera lst de adjacencia.
        for ciclo in ciclos: # for x in ciclos
            for vertice in ciclo: # for v em x
                grau = 0 #grau = 0
                for vizinho in adj_list[vertice]: # for vizinho em N(v)
                    if vizinho in ciclo: # se vizinho em ciclo
                        grau += 1 # grau = grau + 1
                if grau >= 3: # se grau maior ou igual a 3, para e retorna true
                    break
            else: # se nao ha v com grau >= 3 no ciclo, retorna false e o ciclo.
                return False, ciclo
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
