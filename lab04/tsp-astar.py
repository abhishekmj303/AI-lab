INF = float('inf')

graph = [
    [0, 12, 10, 19, 8],
    [12, 0, 3, 7, 6],
    [10, 3, 0, 2, 20],
    [19, 7, 2, 0, 4],
    [8, 6, 20, 4, 0]
]


def enque(queue, tpl):
    path, g_n, f_n = tpl
    for i in range(len(queue)):
        if f_n >= queue[i][-1]:
            queue.insert(i, tpl)
            break
    else:
        queue.append(tpl)


def tsp_bfs(graph, start):
    n = len(graph)
    queue = [([start], 0, 0)]
    min_cost = INF
    min_path = []

    while queue:
        path, cost, heuristic = queue.pop(0)
        node = path[-1]
        if len(path) == n:
            cost += graph[node][start]
            if cost < min_cost:
                min_cost = cost
                min_path = path + [start]
        else:
            for neighbor in range(n):
                if graph[node][neighbor] and neighbor not in path:
                    g_n = cost + graph[node][neighbor]
                    h_n = remaining_mst(graph, path + [neighbor])
                    f_n = g_n + h_n
                    enque(queue, (path + [neighbor], g_n, f_n))

    return min_path, min_cost


def remaining_graph(graph, path):
    n = len(graph)
    new_graph = [[0 if i in path[1:-1] or j in path[1:-1] else graph[i][j] for i in range(n)] for j in range(n)]
    return new_graph


def remaining_mst(graph, path):
    n = len(graph)
    m = n - len(path[1:-1])
    graph = remaining_graph(graph, path)
    selected = [False for i in range(n)]
    selected[path[0]] = True

    cost = 0
    count = 0
    while count < m-1:
        minimum = INF
        a, b = 0, 0
        for i in range(n):
            if selected[i]:
                for j in range(n):
                    if not selected[j] and graph[i][j]:
                        if minimum > graph[i][j]:
                            minimum = graph[i][j]
                            a, b = i, j
        cost += graph[a][b]
        selected[b] = True
        count += 1
    return cost


soln = tsp_bfs(graph, 0)
print("TSP Route using A*: ", end="")
print(*soln[0], sep="->")
print("Cost of the Route:", soln[1])
