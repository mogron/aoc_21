from itertools import combinations
from copy import deepcopy


class Pair:
    parent = None

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @property
    def magnitude(self):
        lm = self.left if isinstance(self.left, int) else self.left.magnitude
        rm = self.right if isinstance(self.right, int) else self.right.magnitude
        return 3 * lm + 2 * rm

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        if isinstance(value, Pair):
            value.parent = self
        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        if isinstance(value, Pair):
            value.parent = self
        self._right = value

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"


def explode(a, nesting):
    if not isinstance(a, Pair):
        return False
    if nesting == 4:
        # go up until we can go to the left
        cur = a
        while cur.parent:
            if cur.parent.left != cur:
                # can go left -- go left, then go as far right as possible
                cur = cur.parent
                if not isinstance(cur.left, Pair):
                    cur.left += a.left
                    break
                cur = cur.left
                while isinstance(cur.right, Pair):
                    cur = cur.right
                cur.right += a.left
                break
            cur = cur.parent
        # go up until we can go to the right
        cur = a
        while cur.parent:
            if cur.parent.right != cur:
                # can go right -- go right, then go as far left as possible
                cur = cur.parent
                if not isinstance(cur.right, Pair):
                    cur.right += a.right
                    break
                cur = cur.right
                while isinstance(cur.left, Pair):
                    cur = cur.left
                cur.left += a.right
                break
            cur = cur.parent
        if a == a.parent.left:
            a.parent.left = 0
        else:
            a.parent.right = 0
        return True
    exploded = explode(a.left, nesting + 1)
    if exploded:
        return True
    exploded = explode(a.right, nesting + 1)
    return exploded


def calc_split(x):
    return x // 2, x - x // 2


def split(a):
    if not isinstance(a.left, Pair):
        if a.left >= 10:
            x, y = calc_split(a.left)
            a.left = Pair(x, y)
            return True
    else:
        splitted = split(a.left)
        if splitted:
            return True
    if not isinstance(a.right, Pair):
        if a.right >= 10:
            x, y = calc_split(a.right)
            a.right = Pair(x, y)
            return True
        return False
    else:
        splitted = split(a.right)
        return splitted


def reduce_step(a):
    if explode(a, 0):
        return True
    if split(a):
        return True
    return False


def reduce(a):
    while reduce_step(a):
        continue
    return a


def add(a, b):
    return Pair(a, b)


def add_and_reduce(a, b):
    x = add(a, b)
    return reduce(x)


def parse_pair(s, cur):
    cur += 1  # skip initial bracket
    if s[cur].isdigit():
        left = int(s[cur])
        cur += 1
    else:
        left, cur = parse_pair(s, cur)
    cur += 1  # skip comma
    if s[cur].isdigit():
        right = int(s[cur])
        cur += 1
    else:
        right, cur = parse_pair(s, cur)
    cur += 1  # skip final bracket
    return Pair(left, right), cur


def main():
    with open("input.txt") as f:
        inp = f.read().splitlines()
    pairs_orig = [pair for pair, _ in [parse_pair(line, 0) for line in inp]]
    pairs = deepcopy(pairs_orig)
    pair = pairs[0]
    for other_pair in pairs[1:]:
        pair = add_and_reduce(pair, other_pair)
    print(pair)
    print(pair.magnitude)

    print(
        max(
            max(
                add_and_reduce(deepcopy(pair), deepcopy(other_pair)).magnitude,
                add_and_reduce(deepcopy(other_pair), deepcopy(pair)).magnitude,
            )
            for pair, other_pair in combinations(pairs_orig, 2)
        )
    )


if __name__ == "__main__":
    main()
