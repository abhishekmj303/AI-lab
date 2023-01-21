from math import gcd


def fill(j):
    global jugs
    print(f"Fill J{j}")
    jugs[j] = caps[j]


def empty(j):
    global jugs
    print(f"Empty J{j}")
    jugs[j] = 0


def pour(j1, j2):
    global jugs
    print(f"Pour J{j1} to J{j2}")
    if caps[j2] - jugs[j2] < jugs[j1]:
        jugs[j1] = (jugs[j1] + jugs[j2]) - caps[j2]
        jugs[j2] = caps[j2]
    else:
        jugs[j2] += jugs[j1]
        jugs[j1] = 0


# two-jug problem
def main():
    global jugs, caps
    caps = list(map(int, input("Enter the capacity of 2 jugs: ").split()))
    goal = int(input("Enter the goal amount needed: "))

    if caps[0] > caps[1]:
        caps[0], caps[1] = caps[1], caps[0]

    if goal > caps[1] or goal % gcd(caps[0], caps[1]) != 0:
        print("No solution possible")
        return

    while goal not in jugs:
        if jugs[1] == caps[1]:
            empty(1)
        if jugs[0] == 0:
            fill(0)
        pour(0, 1)

    if jugs[0] != goal:
        empty(0)
    elif jugs[1] != goal:
        empty(1)


if __name__ == "__main__":
    jugs = [0, 0]
    caps = [0, 0]
    main()
