import chordal as cd
import funcs as f


def inicializa(grafo, path): # formato de lista de arestas!!!!!
	with open(path, "r") as f:
		line = f.readline().split()
		while line[0] == "#" :
			line = f.readline().split()

		n = int(line[0])
		m = int(line[1])
		edges = []
		for i in range(m):
			line = f.readline().split()
			edges.append(( int(line[0]), int(line[1]) ))

		grafo = cd.Graph(n, edges)
		grafo = grafo.criaGrafo(grafo)
		# print(list(grafo.edges()))
		return grafo

def main(): # aquivo do path é do estilo do teste.txt
	path = str(input("Digite o nome do arquivo: "))
	graph = None
	graph = inicializa(graph, path)
	adj_list = graph.gera_adlist()
	print(adj_list)
	print(graph.is_chordal())


main()