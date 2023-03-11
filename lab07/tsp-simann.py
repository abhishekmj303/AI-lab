import random
import math
from matplotlib import pyplot as plt
from copy import deepcopy


class City:
    def __init__(self):
        self.x = random.randint(1, 9)
        self.y = random.randint(1, 9)

    def dist(self, other):
        x1 = (self.x - other.x)**2
        y1 = (self.y - other.y)**2
        return (x1+y1)**0.5

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Route(list):
    def __init__(self):
        super(Route, self).__init__()
        while len(self) != 15:
            c = City()
            if c not in self:
                self.append(c)

    def cost(self):
        total = 0
        for i in range(len(self)-1):
            total += self[i].dist(self[i+1])
        total += self[-1].dist(self[0])
        return total

    def next_route(self):
        route = deepcopy(self)
        c1, c2 = random.sample(range(len(self)), 2)
        route[c1], route[c2] = route[c2], route[c1]
        return route

    def plot(self, title=None):
        X = [c.x for c in self] + [self[0].x]
        y = [c.y for c in self] + [self[0].y]
        plt.plot(X, y, 'o-')
        plt.title(title)
        plt.show()


def sim_ann(route, T, T0, alpha):
    all_iter = [(route, route.cost())]

    while T > T0:
        next_route = route.next_route()
        next_cost = next_route.cost()
        dE = next_cost - route.cost()
        if dE < 0:
            route = next_route
        elif random.random() < math.exp(-dE/T):
            route = next_route
        else:
            continue
        all_iter.append((next_route, next_cost))
        T *= alpha

    return all_iter


def progress_plot(all_iter):
    all_costs = [i[1] for i in all_iter]
    plt.plot(all_costs)
    plt.title(f"Progress over {len(all_iter)} iterations")
    plt.show()


def main():
    initial_route = Route()
    initial_cost = initial_route.cost()
    print("Initial State:", initial_route, initial_cost)
    initial_route.plot(f"Initial State: {initial_cost:.2f}")

    result = sim_ann(initial_route, 10**10, 0.1, 0.97)
    final_route, final_cost = result[-1]
    print("Final State:", final_route, final_cost)
    final_route.plot(f"Final State: {final_cost:.2f}")

    progress_plot(result)


if __name__ == '__main__':
    main()
