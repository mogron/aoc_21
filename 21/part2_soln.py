from itertools import product

# state in a single universe is:
# (p1_score, p2_score, p1_pos, p2_pos, p_idx)
# So the multiverse can be represented as a five-dimensional array of size 21 x 21 x 10 x 10 x 2,
# mapping each possible state to its frequency.
# A state update iterates over the current state and generates the successor frequencies,
# until all games are finished.


def make_state():
    state = [
        [
            [[[0 for _ in range(2)] for _ in range(10)] for _ in range(10)]
            for _ in range(21)
        ]
        for _ in range(21)
    ]
    return state


def tick(state):
    state_next = make_state()
    updated = False
    p1_wins = 0
    p2_wins = 0
    for p1_score, g_p1_score in enumerate(state):
        for p2_score, g_p2_score in enumerate(g_p1_score):
            for p1_pos, g_p1_pos in enumerate(g_p2_score):
                for p2_pos, g_p2_pos in enumerate(g_p1_pos):
                    for idx, freq in enumerate(g_p2_pos):
                        if freq == 0:
                            continue
                        updated = True
                        for r1, r2, r3 in product([1, 2, 3], [1, 2, 3], [1, 2, 3]):
                            roll = r1 + r2 + r3
                            if idx == 0:
                                p1_pos_next = (p1_pos + roll) % 10
                                p1_score_next = p1_score + p1_pos_next + 1
                                if p1_score_next >= 21:
                                    p1_wins += freq
                                else:
                                    state_next[p1_score_next][p2_score][p1_pos_next][
                                        p2_pos
                                    ][1 - idx] += freq
                            if idx == 1:
                                p2_pos_next = (p2_pos + roll) % 10
                                p2_score_next = p2_score + p2_pos_next + 1
                                if p2_score_next >= 21:
                                    p2_wins += freq
                                else:
                                    state_next[p1_score][p2_score_next][p1_pos][
                                        p2_pos_next
                                    ][1 - idx] += freq
    return state_next, p1_wins, p2_wins, updated


def main():
    with open("input.txt") as f:
        inp = f.read().splitlines()
    ps = [int(line.split()[-1]) - 1 for line in inp]
    state = make_state()

    state[0][0][ps[0]][ps[1]][0] = 1
    p1_wins_total = 0
    p2_wins_total = 0
    updated = True
    while updated:
        state, p1_wins, p2_wins, updated = tick(state)
        p1_wins_total += p1_wins
        p2_wins_total += p2_wins
    print(max(p1_wins_total, p2_wins_total))


if __name__ == "__main__":
    main()
