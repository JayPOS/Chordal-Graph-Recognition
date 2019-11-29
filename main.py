from src import chordal as cd
import networkx as nx

def inicializa(grafo, path): # formato de lista de arestas!!!!!
        with open(path, "r") as f:
                line = f.readline().split()

                n = int(line[0])
                m = int(line[1])
                edges = []
                for i in range(m):
                        line = f.readline().split()
                        edges.append(( int(line[0]), int(line[1]) ))

                grafo = cd.Graph(n, edges)

                return grafo

def main(): # aquivo do path é do estilo do teste.txt
        #path = str(input("Digite o nome do arquivo: "))
        graph = None

        for i in range(1, 8, 1):
            print("TESTE %s" % i)
            graph = inicializa(graph, "./data/teste%s.txt" % i)
            print(graph.is_chordal())
            print(graph.is_chordal_brute(graph.n))


main()
