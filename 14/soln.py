from collections import Counter, defaultdict


def solve(s, rules, iterations):
    pair_counts = defaultdict(lambda: 0, Counter(zip(s, s[1:])))
    letter_counts = defaultdict(lambda: 0, Counter(s))
    for _ in range(iterations):
        for pair, cnt in list(pair_counts.items()):
            if pair in rules:
                a, b = pair
                middle = rules[pair]
                pair_counts[(a, middle)] += cnt
                pair_counts[(middle, b)] += cnt
                pair_counts[pair] -= cnt
                letter_counts[middle] += cnt
    print(max(letter_counts.values()) - min(letter_counts.values()))


def main():
    with open("input.txt") as f:
        s, _, *inp = f.read().splitlines()
    rules = {}
    for rule in inp:
        a, b = rule.split(" -> ")
        a1, a2 = a
        rules[(a1, a2)] = b
    solve(s, rules, 10)
    solve(s, rules, 40)


if __name__ == "__main__":
    main()
