import numpy as np


def astar(weights, profit, capacity):
    n = len(weights)
    open_list = [((), 0, 0)]

    for i in range(n):
        knap, w, p = open_list.pop(0)
        f_n1, f_n2 = -1, -1

        # include 'i'th element
        if w+weights[i] <= capacity:
            knap_incl = (knap + (i,), w+weights[i], p+profit[i])
            h_n1 = heuristic(weights[i+1:], profit[i+1:], capacity-knap_incl[1])
            f_n1 = p+profit[i] + h_n1

        # not include 'i'th element
        knap_notincl = (knap, w, p)
        h_n2 = heuristic(weights[i+1:], profit[i+1:], capacity-knap_notincl[1])
        f_n2 = p + h_n2

        if f_n1 == -1:
            open_list.append(knap_notincl)
        else:
            if f_n1 <= f_n2:
                open_list.append(knap_notincl)
            else:
                open_list.append(knap_incl)

    return open_list.pop(0)


def heuristic(weights, profit, capacity):
    if len(weights) == 0:
        return 0

    p_by_w = np.array(profit) / np.array(weights)
    greedy_order = np.argsort(p_by_w)[::-1]

    w, p = 0, 0
    for i in greedy_order:
        if weights[i] + w <= capacity:
            w += weights[i]
            p += profit[i]
        else:
            break

    return p


weights = [10, 300, 1, 200, 100]
profit = [1000, 4000, 5000, 5000, 2000]
capacity = 400

max_knap, w, p = astar(weights, profit, capacity)
print("Knapsack contains:", *max_knap)
print("Weight of knapsack:", w)
print("Profit of knapsack:", p)
