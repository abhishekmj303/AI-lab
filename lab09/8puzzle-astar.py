import numpy as np


def no_of_misplaced(current: tuple, final: tuple):
    current, final = np.array(current), np.array(final)
    count = 0
    for i in range(1, len(final) ** 2):
        if np.where(current == i) != np.where(final == i):
            count += 1
    return count


def dist_to_final(current: tuple, final: tuple):
    current, final = np.array(current), np.array(final)
    dist = 0
    for i in range(len(final)):
        for j in range(len(final)):
            if final[i, j] != 0:
                cur_x, cur_y = np.where(current == final[i, j])
                diff = [cur_x[0] - i, cur_y[0] - j]
                dist += sum(np.abs(diff))
    return dist


def generate_neighbors(current: tuple):
    current = np.array(current)
    empty = np.array(np.where(current == 0)).flatten()
    next_add = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    locations = [empty + np.array(a) for a in next_add]
    neighbors = []
    for loc in locations:
        if np.any(loc < 0) or np.any(loc >= len(current)):
            continue
        current_copy = np.copy(current)
        current_copy[empty[0], empty[1]] = current_copy[loc[0], loc[1]]
        current_copy[loc[0], loc[1]] = 0
        neighbors.append(tuple(map(tuple, current_copy)))
    return neighbors


def print_puzzle(puzzle: tuple):
    for row in puzzle:
        row = ' '.join(map(str, row)).replace('0', ' ')
        print(row)
    print()


def print_path(parent: dict, current: tuple):
    if current in parent:
        print_path(parent, parent[current])
    print_puzzle(current)


def priority_enqueue(open_list: list, node: tuple):
    for i in range(len(open_list)):
        if node[1] < open_list[i][1]:
            open_list.insert(i, node)
            return
    open_list.append(node)


def astar(initial: tuple, final: tuple, heuristic):
    open_list, closed_list = [], []
    parent = {}
    open_list.append((initial, 0 + heuristic(initial, final), 0))

    max_iter = 0
    while open_list and max_iter < 1000:
        current, f_n, g_n = open_list.pop(0)
        closed_list.append(current)

        if current == final:
            return parent, f_n

        neighbors = generate_neighbors(current)
        g_n += 1

        for neighbor in neighbors:
            in_open = 1 if neighbor in [o[0] for o in open_list] else 0
            in_closed = 1 if neighbor in closed_list else 0
            if not in_closed:
                f_n = g_n + heuristic(neighbor, final)
                if not in_open:
                    priority_enqueue(open_list, (neighbor, f_n, g_n))
                    parent[neighbor] = current
                else:
                    index = [o[0] for o in open_list].index(neighbor)
                    if f_n < open_list[index][1]:
                        open_list[index] = (neighbor, f_n, g_n)
                        parent[neighbor] = current
        max_iter += 1
    if max_iter >= 1000:
        raise StopIteration('maximum iteration exceeded')


def main(hueristic, text):
    initial = (
        (2, 8, 3),
        (1, 6, 4),
        (7, 0, 5)
    )

    final = (
        (1, 2, 3),
        (8, 0, 4),
        (7, 6, 5)
    )

    print(f'Heuristic used: {text}')
    parent_dict, moves = astar(initial, final, hueristic)
    print('Steps: ')
    print_path(parent_dict, final)
    print('No. of moves: ', moves)


if __name__ == '__main__':
    main(no_of_misplaced, 'Number of misplaced tiles')
    print()
    main(dist_to_final, 'Sum of the tile distances from goal')
