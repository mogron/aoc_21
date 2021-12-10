
d = {
    "[": "]",
    "(": ")",
    "{": "}",
    "<": ">"
}

p2 = {
    "]": 2,
    ")": 1,
    "}": 3,
    ">": 4
}

def solve2(s):
    stack = []
    for c in s:
        if c in d:
            stack.append(c)
        else:
            if not stack:
                return 0
            last = stack.pop()
            if c != d[last]:
                return 0
    score = 0
    while stack:
        last = stack.pop()
        v = d[last]
        points = p2[v]
        score *= 5
        score += points
    return score 

def main():
    with open("input.txt") as f:
        inp = f.readlines()
    scores = []
    for line in inp:
        res = solve2(line.strip())
        if res > 0:
            scores.append(res)
    scores.sort()
    print(scores[len(scores) // 2])

if __name__ == "__main__":
    main()