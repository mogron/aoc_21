from itertools import permutations

segments_raw = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg"
}

segments = {k: set(v) for k, v in segments_raw.items()}

s_all = "abcdefg"


def solve(ten, four):
    """Brute force"""
    for x in permutations(s_all):
        map = {k: v for k, v in zip(s_all, x)}
        table = str.maketrans(map)
        t_ten = [set(s.translate(table)) for s in ten]
        if all(s in segments.values() for s in t_ten):
            print("found!")
            break
    else:
        exit(1)
    t_four = [set(s.translate(table)) for s in four]
    print(t_four)
    res = ""
    for combo in t_four:
        for k, v in segments.items():
            if v == combo:
                res += str(k)
                break
    print(res)
    return int(res)





def main():
    with open("input.txt") as f:
        inp = f.readlines()
    total = 0
    for line in inp:
        s_ten, s_four = line.split("|")
        ten = s_ten.split()
        four = s_four.split()
        result = solve(ten, four)
        total += result
    print(total)


if __name__ == "__main__":
    main()