def move(start, end):
    global towers, steps

    disk = towers[start].pop()
    towers[end].append(disk)
    steps += 1
    print(f"Move D{disk} from T{start + 1} to T{end + 1}")


def toh_rec(n, start, end, inter):
    if n == 1:
        move(start, end)
        return
    toh_rec(n - 1, start, inter, end)
    move(start, end)
    toh_rec(n - 1, inter, end, start)


def toh_nonrec(n, start, end, inter):
    global towers
    stack = [(n, start, end, inter)]
    # non-recursive approach using stack
    while stack:
        n, start, end, inter = stack.pop()
        if n == 1:
            move(start, end)
            continue
        stack.append((n - 1, inter, end, start))
        stack.append((1, start, end, inter))
        stack.append((n - 1, start, inter, end))


def main(toh):
    global towers, steps
    towers = [[i for i in range(n, 0, -1)], [], []]
    steps = 0
    toh(n, 0, 2, 1)
    print(f"{steps} steps")


if __name__ == "__main__":
    n = int(input("Enter the number of disks: "))
    towers = []
    steps = 0

    print("\nRecursive approach:")
    main(toh_rec)

    print(f"\nNon-Recursive approach:")
    main(toh_nonrec)
