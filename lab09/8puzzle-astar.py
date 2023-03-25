import numpy as np

initial = np.array([
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]
])

final = np.array([
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
])

print(initial)
print(final)


def no_of_misplaced(current, final):
    count = 0
    for i in range(1, len(final) ** 2):
        if np.where(current == i) != np.where(final == i):
            count += 1
    print(count)
    return count


def dist_to_final(current, final):
    dist = 0
    for i in range(len(final)):
        for j in range(len(final)):
            if final[i, j] != 0:
                cur_x, cur_y = np.where(current == final[i, j])
                diff = [cur_x[0] - i, cur_y[0] - j]
                dist += sum(np.abs(diff))
    print(dist)
    return dist


def generate_neighbors(current):
    empty = np.array(np.where(current == 0)).flatten()
    next_add = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    locations = [empty + np.array(a) for a in next_add]
    neighbors = []
    print(len(current))
    for loc in locations:
        if 0 <= loc[0] < len(current) and 0 <= loc[1] < len(current):
            current_copy = np.copy(current)
            print(loc)
            current_copy[empty[0], empty[1]] = current_copy[loc[0], loc[1]]
            current_copy[loc[0], loc[1]] = 0
            neighbors.append(current_copy)
    return neighbors


def print_path(parent, current):
    if current.tobytes() in parent:
        print_path(parent, parent[current.tobytes()])
    current = np.frombuffer(current.tobytes(), dtype=np.int8).reshape(3, 3)
    print(current)


def priority_enqueue(open_list, node):
    for i in range(len(open_list)):
        if node[1] < open_list[i][1]:
            open_list.insert(i, node)
            return
    open_list.append(node)


def astar(initial, final, heuristic):
    n = len(final)
    open_list, closed_list = [], []
    parent = {}
    open_list.append((initial, 0 + heuristic(initial, final), 0))

    while open_list:
        current, f_n, g_n = open_list.pop()
        closed_list.append(current)
        if np.array_equal(current, final):
            return parent
        neighbors = generate_neighbors(current)
        for neighbor in neighbors:
            in_open = 1 if np.isin(neighbor, [o[0] for o in open_list]).all() else 0
            in_closed = 1 if np.isin(neighbor, [c[0] for c in closed_list]).all() else 0
            if not in_closed:
                g_n += 1
                f_n = g_n + heuristic(neighbor, final)
                if not in_open:
                    priority_enqueue(open_list, (neighbor, f_n, g_n))
                    parent[neighbor.tobytes()] = current
                else:
                    index = open_list.index(neighbor)
                    if f_n < open_list[index][1]:
                        open_list[index] = (neighbor, f_n, g_n)
                        parent[neighbor.tobytes()] = current


no_of_misplaced(initial, final)
dist_to_final(initial, final)
parent_path = astar(initial, final, no_of_misplaced)
print_path(parent_path, final)
