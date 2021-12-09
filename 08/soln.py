segments = {
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

s_all = "abcdefg"


def solve(ten, four):

    res = 0
    for combo in four:
        if len(combo) in [2, 4, 3, 7]:
            res += 1
    return res

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