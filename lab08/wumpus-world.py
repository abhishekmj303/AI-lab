import numpy as np
from collections import defaultdict


class Agent:
    LEFT = {'NORTH': 'WEST', 'WEST': 'SOUTH', 'SOUTH': 'EAST', 'EAST': 'NORTH'}
    RIGHT = {'NORTH': 'EAST', 'EAST': 'SOUTH', 'SOUTH': 'WEST', 'WEST': 'NORTH'}
    FORWARD = {'NORTH': (0, 1), 'EAST': (1, 0), 'SOUTH': (0, -1), 'WEST': (-1, 0)}
    TURNS = {('NORTH', 'NORTH'): [], ('NORTH', 'EAST'): ['RIGHT'], ('NORTH', 'SOUTH'): ['RIGHT', 'RIGHT'],
             ('NORTH', 'WEST'): ['LEFT'], ('EAST', 'NORTH'): ['LEFT'], ('EAST', 'EAST'): [],
             ('EAST', 'SOUTH'): ['RIGHT'], ('EAST', 'WEST'): ['RIGHT', 'RIGHT'], ('SOUTH', 'NORTH'): ['RIGHT', 'RIGHT'],
             ('SOUTH', 'EAST'): ['LEFT'], ('SOUTH', 'SOUTH'): [], ('SOUTH', 'WEST'): ['RIGHT'],
             ('WEST', 'NORTH'): ['RIGHT'], ('WEST', 'EAST'): ['RIGHT', 'RIGHT'], ('WEST', 'SOUTH'): ['LEFT'],
             ('WEST', 'WEST'): []}
    SENSES = defaultdict(str, {'P': 'B', 'W': 'S', 'G': 'G'})

    def __init__(self, world, n):
        self.world = defaultdict(str, world)
        self.n = n
        self.kb = defaultdict(set)
        self.pos = (1, 1)
        self.direction = 'EAST'
        self.arrow = 1
        self.score = 0
        self.have_gold = 0
        self.alive = 1

    def turn_left(self):
        self.score -= 1
        self.direction = Agent.LEFT[self.direction]
        print('Turned left')

    def turn_right(self):
        self.score -= 1
        self.direction = Agent.RIGHT[self.direction]
        print('Turned right')

    def move_forward(self):
        pos = np.array(self.pos)
        pos += np.array(Agent.FORWARD[self.direction])

        if pos.any() < 1 or pos.any() > 4:
            pos -= np.array(Agent.FORWARD[self.direction])
            print('Hit wall at', self.pos)
            return False

        self.score -= 1
        self.pos = tuple(pos)
        self.kb[self.pos].add('V')
        if self.world[self.pos] in ('P', 'W'):
            self.alive = 0
            self.score -= 1000
            because = 'pit' if self.world[self.pos] == 'P' else 'wumpus'
            print('Died at', self.pos, 'because of', because)
            return False
        else:
            self.kb[self.pos].add('OK')
        print('Move forward to', self.pos)
        return True

    def shoot(self):
        print('Shoot arrow')
        if self.arrow:
            self.score -= 10
            self.arrow = 0
            pos = np.array(self.pos) + np.array(Agent.FORWARD[self.direction])
            if pos.any() < 1 or pos.any() > 4:
                return
            pos = tuple(pos)
            if self.world[pos] == 'W':
                self.kb[pos].add('Sc')
                self.world.pop(pos)
                print('Killed wumpus at', pos)
            else:
                print('Missed at', pos)
        else:
            print('No arrow')

    def grab(self):
        print('Grab gold')
        if self.world[self.pos] == 'G':
            self.have_gold = 1
            self.score += 1000
            self.world.pop(self.pos)
            print('Grabbed gold at', self.pos)
        else:
            print('No gold at', self.pos)

    def sense(self):
        if self.world[self.pos] == 'G':
            self.kb[self.pos].add('G')
        all_env = set()
        for adj in self.adjacent():
            env = self.world[adj]
            all_env.add(env)
            if env and env != 'G':
                self.kb[self.pos].add(Agent.SENSES[env])
        if 'W' not in all_env:
            self.kb[self.pos].discard('S')
        return self.kb[self.pos]

    def adjacent(self, pos=None):
        pos = np.array(self.pos) if pos is None else np.array(pos)
        adj = []
        for a in Agent.FORWARD.values():
            i, j = pos + np.array(a)
            if 1 <= i <= self.n and 1 <= j <= self.n:
                adj.append((i, j))
        return adj

    def __repr__(self):
        return f'Agent({self.pos}, {self.direction})\nScore: {self.score}'


def move_to(agent, pos):
    print('Go to', pos)
    diff = tuple(np.array(pos) - np.array(agent.pos))
    direction = list(Agent.FORWARD.keys())[list(Agent.FORWARD.values()).index(diff)]
    turns = Agent.TURNS[(agent.direction, direction)]
    for turn in turns:
        if turn == 'LEFT':
            agent.turn_left()
        elif turn == 'RIGHT':
            agent.turn_right()
    agent.move_forward()


def ai_next_action(agent: Agent):
    senses = agent.sense()
    print('Current:', {agent.pos: agent.kb[agent.pos]})
    print('Action:', end=' ')
    if 'G' in senses:
        agent.grab()
        return True
    ok_visited, ok_not_visited = [], []
    for adj in agent.adjacent():
        if 'W' in agent.kb[adj]:
            agent.shoot()
            return True
        if 'OK' in agent.kb[adj] and 'V' not in agent.kb[adj]:
            ok_not_visited.append(adj)
            continue
        if 'OK' in agent.kb[adj] and 'V' in agent.kb[adj]:
            ok_visited.append(adj)
    if ok_not_visited:
        move_to(agent, ok_not_visited[0])
        return True
    if ok_visited:
        move_to(agent, ok_visited[0])
        return True
    return False


def analyze_adj(agent: Agent):
    senses = agent.sense()
    agent.kb[agent.pos].add('V')
    agent.kb[agent.pos].add('OK')
    total_ok = 0
    adjacents = agent.adjacent()
    print('Adjacents:', {adj: agent.kb[adj] for adj in adjacents})
    for adj in adjacents:
        if 'OK' not in agent.kb[adj] and 'P' not in agent.kb[adj] and 'W' not in agent.kb[adj]:
            if 'B' in senses and 'S' in senses:
                agent.kb[adj].add('P?')
                agent.kb[adj].add('W?')
            elif 'B' in senses:
                if 'W?' not in agent.kb[adj]:
                    agent.kb[adj].add('P?')
                agent.kb[adj].discard('W?')
            elif 'S' in senses:
                if 'P?' not in agent.kb[adj]:
                    agent.kb[adj].add('W?')
                agent.kb[adj].discard('P?')
            else:
                agent.kb[adj].discard('P?')
                agent.kb[adj].discard('W?')
        if 'P?' not in agent.kb[adj] and 'W?' not in agent.kb[adj]:
            agent.kb[adj].add('OK')
            total_ok += 1
    if total_ok == len(adjacents)-1:
        for adj in adjacents:
            if 'OK' not in agent.kb[adj] and 'P' not in agent.kb[adj] and 'W' not in agent.kb[adj]:
                if 'B' in senses and 'P?' in agent.kb[adj]:
                    agent.kb[adj].add('P')
                    agent.kb[adj].discard('P?')
                    break
                elif 'S' in senses and 'W?' in agent.kb[adj]:
                    agent.kb[adj].add('W')
                    agent.kb[adj].discard('W?')
                    break


def user_traverse(agent: Agent):
    print('1. Move forward')
    print('2. Turn left')
    print('3. Turn right')
    print('4. Shoot')
    print('5. Grab')
    print('6. Exit')
    action = int(input('Enter action: '))
    while agent.alive:
        if agent.pos == (1, 1) and agent.have_gold:
            print('You won!')
            break
        if action == 1:
            agent.move_forward()
            analyze_adj(agent)
        elif action == 2:
            agent.turn_left()
        elif action == 3:
            agent.turn_right()
        elif action == 4:
            agent.shoot()
        elif action == 5:
            agent.grab()
        elif action == 6:
            break


def ai_traverse(agent):
    path = []
    max_iter = 100
    while agent.alive and not agent.have_gold and max_iter > 0:
        print(agent)
        analyze_adj(agent)
        if not ai_next_action(agent):
            print('No action possible to take by AI')
            user_traverse(agent)
            return
        if agent.pos in path:
            # delete path until pos
            path = path[:path.index(agent.pos)]
        path.append(agent.pos)
        max_iter -= 1
        print()
    if not agent.alive:
        return
    if agent.have_gold:
        path.pop()
        while agent.pos != (1, 1):
            print(agent)
            print('Action:', end=' ')
            move_to(agent, path.pop())
            print()
        print(agent)
        print('AI won!')
    if max_iter == 0:
        print('Max iteration reached')
        user_traverse(agent)


def main():
    world = {
        (3, 1): 'P',
        (1, 3): 'W',
        (2, 3): 'G',
        (3, 3): 'P',
        (4, 4): 'P',
    }

    agent = Agent(world, 4)
    ai_traverse(agent)


if __name__ == '__main__':
    main()
