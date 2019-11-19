import networkx as nx
import funcs as f

class Graph:
    def __init__(self, n, edges):
        self.G = nx.Graph()
        self.n = n
        self.edges = edges

    @staticmethod
    def criaGrafo(self):
        for i in range(1,  self.n +1):
            self.G.add_node(i)

        self.G.add_edges_from(self.edges)
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
        adjlist = []
        x = self.gera_entrada()
        for vertice in range(1, self.n +1):
            adjlist.append([])

        for aresta in x:
            # print("p.aresta2 ", aresta[0], " p.aresta1 ", aresta[1])
            adjlist[aresta[0]-1].append(aresta[1])
            adjlist[aresta[1]-1].append(aresta[0])


        return adjlist

    def is_chordal(self):
    	ciclos = f.identificaCiclo(self.gera_entrada())
    	adj_list = self.gera_adlist()
    	for ciclo in ciclos:
    		for vertice in ciclo:
    			grau = 0
    			for vizinho in adj_list[vertice]:
    				if vizinho in ciclo:
    					grau+=1
    			if grau >= 3:
    				break
    		else:
    			print("Ciclo nao cordal = ", ciclo)
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
