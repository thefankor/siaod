import math

from load_incidence_matrix import load_incidence_matrix_from_file
from load_matrix import load_graph_from_file


def dijkstra(graph, start, end):
    n = len(graph)
    distances = [math.inf] * n
    visited = [False] * n
    distances[start] = 0

    for _ in range(n):
        min_distance = math.inf
        u = -1
        for i in range(n):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                u = i

        if u == -1:
            break

        if u == end:
            break

        visited[u] = True

        for v in range(n):
            if graph[u][v] != math.inf and not visited[v]:
                new_distance = distances[u] + graph[u][v]
                if new_distance < distances[v]:
                    distances[v] = new_distance

    return distances[end] if distances[end] != math.inf else None



def bellman_ford(graph, source):
    n = len(graph)
    distance = [math.inf] * n
    distance[source] = 0

    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if graph[u][v] != math.inf:
                    if distance[u] + graph[u][v] < distance[v]:
                        distance[v] = distance[u] + graph[u][v]

    for u in range(n):
        for v in range(n):
            if graph[u][v] != math.inf:
                if distance[u] + graph[u][v] < distance[v]:
                    raise ValueError("Граф содержит отрицательный цикл!")

    return distance


def dijkstra_with_path(graph, start, end):
    n = len(graph)
    distances = [math.inf] * n
    previous = [None] * n
    visited = [False] * n
    distances[start] = 0

    for _ in range(n):
        min_distance = math.inf
        u = -1
        for i in range(n):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                u = i
        if u == -1:
            break
        visited[u] = True
        for v in range(n):
            if graph[u][v] != math.inf and not visited[v]:
                new_distance = distances[u] + graph[u][v]
                if new_distance < distances[v]:
                    distances[v] = new_distance
                    previous[v] = u

    path = []
    if distances[end] != math.inf:
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        return distances[end], path
    else:
        return None, []

def johnson(graph, start, end):
    n = len(graph)
    new_graph = [row + [math.inf] for row in graph]
    new_graph.append([0] * n + [0])
    h = bellman_ford(new_graph, n)

    reweighted_graph = [[math.inf] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if graph[u][v] != math.inf:
                reweighted_graph[u][v] = graph[u][v] + h[u] - h[v]

    distance, path = dijkstra_with_path(reweighted_graph, start, end)
    if distance is None:
        return None, []
    true_distance = distance + h[end] - h[start]
    return true_distance, path


if __name__ == '__main__':
    # matrix = load_graph_from_file('files/1.txt')
    matrix = load_incidence_matrix_from_file('files/incidence_matrix.txt')
    print(johnson(matrix, 0, 4))
