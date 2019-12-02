import chordal as cd
import networkx as nx
import sys

path = sys.argv[1]
graph_type = sys.argv[2]


def inicializa(grafo):  # formato de lista de arestas!!!!!
    with open(path, "r") as f:
        line = f.readline().split()

        n = int(line[0])
        m = int(line[1])
        edges = []
        for i in range(m):
            line = f.readline().split()
            edges.append((int(line[0]), int(line[1])))

        grafo = cd.Graph(n, edges)

        return grafo


# aquivo do path e do estilo do teste.txt
# path = str(input("Digite o nome do arquivo: "))

print("akdanwldnal")

graph = None
graph = inicializa(graph)

if graph_type == "1":
    print(graph.is_chordal())
else:
    print(graph.is_interval_graph())
