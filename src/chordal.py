import networkx as nx
from src import funcs as f
from src.funcs import criarListaDeLista, isEmpty


class Graph:
    def __init__(self, n, edges, naoSepararComps = None):
        self.G = nx.Graph()
        self.n = n
        self.edges = edges
        self.componentes = []

        if naoSepararComps is None or naoSepararComps is False:
            #Cria os componentes para o networkx
            for i in range(n):
                self.G.add_node(i)

            self.G.add_edges_from(self.edges)
            componentes = [self.G.subgraph(c).copy() for c in nx.connected_components(self.G)]
            for comp in componentes:
                minNode = min(comp.nodes())
                self.componentes.append([minNode, Graph(comp.number_of_nodes(), [[e[0] - minNode, e[1] - minNode] for e in comp.edges()], True)])


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
        vertex = [] #lista de conjunto de vertices
        listaAdj = self.gera_adlist() #retorna a lista de adjacencia do grafo

        #constantes para identificar mais facilmente o acesso no vetor
        VERTEX = 0
        VIZINHOS = 1
        ROTULO = 2
        VISITADO = 3
        LARGURA = 4

        for i in range(self.n): #para cada vertice, faca
            vertex.append([ #adicione as informacoes basicas a seguir na lista
                i,  #vertice
                listaAdj[i], #vizinhos
                [], #rotulos
                False, #visitado
                -1]) #largura

        def maxVertex(): #retorna o vertice nao visitado de maior valor lexicografico
            maior = 0 #comeca pelo inicio da lista
            
            for i in range(self.n): #para cada vertice, faca
                if not vertex[i][VISITADO]: #se o vertice v nao esta visitado, faca
                    if len(vertex[i][ROTULO]) > len(vertex[maior][ROTULO]): #se o rotulo do vertice v e maior que o maior anterior, faca
                        maior = i #maior = v

            return maior #retorne o maior vertice nao visitado de acordo com o valor lexicografico

        def select(i): #seleciona e marca o maior vertice
            v = maxVertex() #pega o vertice de maior valor lexicografico nao visitado
            vertex[v][VISITADO] = True #visita o vertice
            vertex[v][LARGURA] = i #atribui seu valor

            return v #retorna o vertice escolhido

        def update(v, i): #atualiza os rotulos dos vizinhos do vertice selecionado
            for j in range(len(listaAdj[v])): #para todo vertice vizinho de v, faca
                if not vertex[listaAdj[v][j]][VISITADO]: #se nao esta visitado, faca
                    vertex[listaAdj[v][j]][ROTULO].append(i) #adicione o numero do vertice v no rotulo dos vizinhos

        for i in reversed(range(self.n)): #para cada vertice, percorrendo do final para o inicio, faca
            v = select(i) #selecione o vertice v
            update(v, i) #atualize seus vizinhos

        def sortFunc(x): #funcao que retorna a chave para ordenacao dos vertices por sua largura
            return x[LARGURA] #retorna a largura do vertice

        vertex.sort(key = sortFunc) #ordena os vertices por sua largura

        return vertex #retorna a lista de vertices com seus vizinhos, rotulos, se foi visitado e sua largura.

    #Retorna o ciclo problematico
    #Caso contrario, retorna None
    def is_chordal(self):
        def elimPerfeita(grafo, correcao = None): #subfuncao que verifica se um grafo possui eliminacao perfeita
            lex = grafo.get_lexBfs() #retorna a lista de vertices ordenados pelo lexbfs, com rotulos.

            L = []  #lista para verificar a eliminacao perfeita
            for i in range(grafo.n): #para cada vertice, faca
                L.append(set()) #adicione um conjunto vazio na lista

            for v in lex: #para cada vertice na sequencia dos vertices da busca lexicografica, faca
                if not isEmpty(v[2]): #caso o rotulo de v nao esteja vazio, faca
                    u = min(v[2]) #seleciona o vertice u com menor valor de largura
                    L[u] = L[u].union(set([lex[x][0] for x in v[2]]) - {lex[u][0]}) #adiciona na lista do vertice u, o conjunto de vertices a serem verificados
                else: #se rotulos vazios
                    break #saia do loop

            for i in range(grafo.n): #para todo vertice, faca
                if not isEmpty(L[i] - set(lex[i][1])): #se a lista do vertice, menos seus adjacentes nao for vazia, faca
                    problema = list(L[i]) + lex[i][1] #adicione os vertices problematicos
                    problema.append(lex[i][0])
                    if correcao is not None: #caso o numero dos vertices esteja errada, faca (isto ocorre, pois os vertices estao identificados separademente por componentes cordais)
                        return False, [vertice+correcao for vertice in problema] #retorne falso, e o conjunto de vertices que formam o ciclo problema
                    else: #se nao precisar corrigir a componente, faca
                        return False, problema #retorne falso, e o conjunto de vertices que formam o ciclo problema
            return True #caso contrario, retorne verdadeiro

        for componente in self.componentes: #para cada componente do grafo, faca
            elim = elimPerfeita(componente[1], componente[0]) #verifique se ha uma eliminacao perfeita
            if elim is not True: #se nao houver para a componente, entao
                return elim #retorne o problema

        return True #caso todas as componentes possuam elim perfeita, o grafo e cordal
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
