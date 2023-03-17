import numpy as np


class Block:
    def __init__(self, env):
        self.pit = 0
        self.wumpus = 0
        self.gold = 0
        self.breeze = 0
        self.stench = 0
        self.visited = 0
        self.ok = 0
        if env == 'PIT':
            self.pit = 1
        elif env == 'WUMPUS':
            self.wumpus = 1
        elif env == 'GOLD':
            self.gold = 1

    def __str__(self):
        env, state = "", ""
        if self.pit: env += "P"
        if self.wumpus: env += "W"
        if self.gold: env += "G"
        if self.breeze: env += "B"
        if self.stench: env += "S"

        state = "V" if self.visited else " "
        ok_str = {0: "  ", 1: " ✓", -1: "?P", -2: "?W", -3: "??"}
        state += ok_str[self.ok]

        return f"{env.center(3)}\n{state}"


class WumpusWorld(tuple):
    def __new__(cls, world):
        return super().__new__(cls, world)

    def __init__(self, world):
        self[0][0].visited = 1
        self[0][0].ok = 1
        n = len(world)
        for i in range(n):
            for j in range(n):
                if self[i][j].pit:
                    if 0 <= i-1 and not self[i-1][j].pit and not self[i-1][j].wumpus:
                        self[i - 1][j].breeze = 1
                    if 0 <= j-1 and not self[i][j-1].pit and not self[i][j-1].wumpus:
                        self[i][j - 1].breeze = 1
                    if i+1 < n and not self[i+1][j].pit and not self[i+1][j].wumpus:
                        self[i + 1][j].breeze = 1
                    if j+1 < n and not self[i][j+1].pit and not self[i][j+1].wumpus:
                        self[i][j + 1].breeze = 1
                if self[i][j].wumpus:
                    if 0 <= i-1 and not self[i-1][j].pit and not self[i-1][j].wumpus:
                        self[i - 1][j].stench = 1
                    if 0 <= j-1 and not self[i][j-1].pit and not self[i][j-1].wumpus:
                        self[i][j - 1].stench = 1
                    if i+1 < n and not self[i+1][j].pit and not self[i+1][j].wumpus:
                        self[i + 1][j].stench = 1
                    if j+1 < n and not self[i][j+1].pit and not self[i][j+1].wumpus:
                        self[i][j + 1].stench = 1

        def get(self, pos):
            return self[pos[0]][pos[1]]


class Agent:
    LEFT = {'NORTH': 'WEST', 'WEST': 'SOUTH', 'SOUTH': 'EAST', 'EAST': 'NORTH'}
    RIGHT = {'NORTH': 'EAST', 'EAST': 'SOUTH', 'SOUTH': 'WEST', 'WEST': 'NORTH'}
    FORWARD = {'NORTH': (1, 0), 'EAST': (0, 1), 'SOUTH': (-1, 0), 'WEST': (0, -1)}

    def __init__(self, world):
        self.world = world
        self.n = len(world)
        self.position = np.array((0, 0))
        self.direction = 'EAST'
        self.arrow = 1
        self.score = 0
        self.have_gold = 0
        self.wumpus_dead = 0
        self.dead = 0

    def turn_left(self):
        self.direction = Agent.LEFT[self.direction]

    def turn_right(self):
        self.direction = Agent.RIGHT[self.direction]

    def move_forward(self):
        self.position += np.array(Agent.FORWARD[self.direction])

        if self.position.any() < 0 or self.position.any() >= 4:
            self.position -= np.array(Agent.FORWARD[self.direction])
            return False

        self.score -= 1
        i, j = self.position
        self.world[i][j].visited = 1
        if self.world[i][j].pit or self.world[i][j].wumpus:
            self.dead = 1
            self.score -= 1000
            return False
        else:
            self.world[i][j].ok = 1

        return True

    def shoot(self):
        if self.arrow:
            self.score -= 10
            self.arrow = 0
            i, j = self.position + np.array(Agent.FORWARD[self.direction])
            if self.world[i][j].wumpus:
                self.wumpus_dead = 1
                self.world[i][j].wumpus = 0
                for a in Agent.FORWARD.values():
                    i, j = self.position + np.array(a)
                    if 0 <= i < self.n and 0 <= j < self.n:
                        self.world[i][j].stench = 0
                return True
            return False
        else:
            return False

    def grab(self):
        i, j = self.position
        if self.world[i][j].gold:
            self.have_gold = 1
            self.score += 1000
            return True
        return False

    def sense(self):
        i, j = self.position
        return self.world[i][j]

    def adjacent(self):
        adj = []
        for a in Agent.FORWARD.values():
            i, j = self.position + np.array(a)
            if 0 <= i < self.n and 0 <= j < self.n:
                adj.append(np.array((i, j)))
        return adj

    def analyse_adj(self):
        block = self.sense()
        adj = self.adjacent()
        var = 0
        if block.breeze and block.stench:
            var = -3
        elif block.breeze:
            var = -1
        elif block.stench:
            var = -2
        for a in adj:
            i, j = a
            if not self.world[i][j].ok:
                self.world[i][j].ok = var

    def __repr__(self):
        end = '\033[0m'
        underline = '\033[4m'
        world_str = ""
        for i in range(self.n-1, -1, -1):
            world_str += "+-----" * 4 + "+\n"
            world_str += "|"
            for j in range(self.n):
                env = str(self.world[i][j]).split("\n")[0]
                if tuple(self.position) == (i, j):
                    env = f"{underline}{env}{end}"
                world_str += f" {env} |"
            world_str += "\n|"
            for j in range(self.n):
                state = str(self.world[i][j]).split("\n")[1]
                if tuple(self.position) == (i, j):
                    state = f"{underline}{state}{end}"
                world_str += f" {state} |"
            world_str += "\n"
        world_str += "+-----" * 4 + "+\n"
        return world_str


world = [
    [Block('NONE'), Block('NONE'), Block('PIT'), Block('NONE')],
    [Block('NONE'), Block('NONE'), Block('NONE'), Block('NONE')],
    [Block('WUMPUS'), Block('GOLD'), Block('PIT'), Block('NONE')],
    [Block('NONE'), Block('NONE'), Block('NONE'), Block('PIT')]
]

agent = Agent(WumpusWorld(world))
print(agent)

agent.move_forward()
print(agent)

agent.move_forward()
print(agent)
