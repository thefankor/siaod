import math


def load_graph_from_file(file_path):
    graph = []
    with open(file_path, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            graph.append(row)

    n = len(graph)
    for i in range(n):
        for j in range(n):
            if i != j and graph[i][j] == 0:
                graph[i][j] = math.inf

    return graph