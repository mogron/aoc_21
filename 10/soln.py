
d = {
    "[": "]",
    "(": ")",
    "{": "}",
    "<": ">"
}

p = {
    "]": 57,
    ")": 3,
    "}": 1197,
    ">": 25137
}

def solve(s):
    stack = []
    for c in s:
        if c in d:
            stack.append(c)
        else:
            if not stack:
                return p[c]
            last = stack.pop()
            if c != d[last]:
                return p[c]
    return 0      

def main():
    with open("input.txt") as f:
        inp = f.readlines()
    total = 0
    for line in inp:
        total += solve(line.strip())
    print(total)



if __name__ == "__main__":
    main()