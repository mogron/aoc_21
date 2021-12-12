from collections import defaultdict

Node = str
Graph = defaultdict[Node, list[Node]]


def is_small_cave(node: Node):
    return node.upper() != node


def get_num_paths(
    g: Graph, start: Node, end: Node, blocked: frozenset[Node], double_budget: int,
) -> int:
    if start == end:
        return 1
    candidates = g[start]
    num_paths = 0
    if is_small_cave(start):
        blocked_next = frozenset([x for x in blocked] + [start])
    else:
        blocked_next = blocked
    for candidate in candidates:
        if candidate in blocked:
            if double_budget > 0 and candidate != "start":
                num_paths += get_num_paths(
                    g, candidate, end, blocked_next, double_budget - 1
                )
        else:
            num_paths += get_num_paths(g, candidate, end, blocked_next, double_budget)
    return num_paths


def main():
    with open("input.txt") as f:
        inp = f.readlines()
    g: Graph = defaultdict(list)
    for line in inp:
        a, b = line.strip().split("-")
        g[a].append(b)
        g[b].append(a)
    num_paths = get_num_paths(g, "start", "end", frozenset(), double_budget=0)
    print("Num paths without double visit: ", num_paths)
    num_paths = get_num_paths(g, "start", "end", frozenset(), double_budget=1)
    print("Num paths with double visit: ", num_paths)


if __name__ == "__main__":
    main()
