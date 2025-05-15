import math


def load_incidence_matrix_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    matrix_lines = []
    weights_line = None
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('#'):
            weights_line = lines[i+1].strip()
            break
        matrix_lines.append(line)

    incidence = [list(map(int, line.split())) for line in matrix_lines]
    weights = list(map(int, weights_line.split()))

    num_vertices = len(incidence)
    num_edges = len(incidence[0])
    adjacency = [[math.inf] * num_vertices for _ in range(num_vertices)]

    for e in range(num_edges):
        u = v = None
        for i in range(num_vertices):
            if incidence[i][e] == 1:
                u = i
            elif incidence[i][e] == -1:
                v = i
        if u is not None and v is not None:
            adjacency[u][v] = weights[e]

    for i in range(num_vertices):
        adjacency[i][i] = 0

    return adjacency
