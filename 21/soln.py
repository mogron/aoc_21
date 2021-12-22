def solve():
    pass


def main():
    with open("input.txt") as f:
        inp = f.read().splitlines()
    ps = [int(line.split()[-1]) - 1 for line in inp]
    scores = [0, 0]
    idx = 0
    die = 1
    rolls = 0
    while max(scores) < 1000:
        move = 3 * die + 3
        ps[idx] = (ps[idx] + move) % 10
        die += 3
        scores[idx] += ps[idx] + 1
        rolls += 3
        idx = 1 - idx
    print(rolls * scores[idx])


if __name__ == "__main__":
    main()
