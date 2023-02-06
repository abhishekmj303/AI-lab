def tsp_dfs(graph, start):
    n = len(graph)
    stack = [(start, [start], 0)]
    min_cost = float("inf")
    min_path = []

    while stack:
        node, path, cost = stack.pop()
        if len(path) == n:
            cost += graph[node][start]
            if cost < min_cost:
                min_cost = cost
                min_path = path + [start]
        else:
            for neighbor in range(n):
                if graph[node][neighbor] and neighbor not in path:
                    stack.append((neighbor, path + [neighbor], cost + graph[node][neighbor]))

    return min_path, min_cost


def tsp_bfs(graph, start):
    n = len(graph)
    queue = [(start, [start], 0)]
    min_cost = float("inf")
    min_path = []

    while queue:
        node, path, cost = queue.pop(0)
        if len(path) == n:
            cost += graph[node][start]
            if cost < min_cost:
                min_cost = cost
                min_path = path + [start]
        else:
            for neighbor in range(n):
                if graph[node][neighbor] and neighbor not in path:
                    queue.append((neighbor, path + [neighbor], cost + graph[node][neighbor]))

    return min_path, min_cost


def tsp_ids(graph, start):
    n = len(graph)
    min_cost = float("inf")
    min_path = []

    for depth in range(n):
        stack = [(start, [start], 0, depth)]
        while stack:
            node, path, cost, current_depth = stack.pop()
            if len(path) == n:
                cost += graph[node][start]
                if cost < min_cost:
                    min_cost = cost
                    min_path = path + [start]
            elif current_depth > 0:
                for neighbor in range(n):
                    if graph[node][neighbor] and neighbor not in path:
                        stack.append((neighbor, path + [neighbor], cost + graph[node][neighbor], current_depth - 1))

    return min_path, min_cost


graph = [
    [0, 12, 10, 19, 8],
    [12, 0, 3, 7, 6],
    [10, 3, 0, 2, 20],
    [19, 7, 2, 0, 4],
    [8, 6, 20, 4, 0]
]

print("Using DFS:", tsp_dfs(graph, 0))
print("Using BFS:", tsp_bfs(graph, 0))
print("Using IDS:", tsp_ids(graph, 0))
