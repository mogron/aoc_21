def get_neighbours(grid, row_idx, col_idx):
    height = len(grid)
    width = len(grid[0]) if height else 0
    row_min = max(0, row_idx - 1)
    row_max = min(width - 1, row_idx + 1)
    col_min = max(0, col_idx - 1)
    col_max = min(height - 1, col_idx + 1)
    for ri in range(row_min, row_max + 1):
        for ci in range(col_min, col_max + 1):
            if ri == row_idx and ci == col_idx:
                continue
            yield ri, ci


def print_grid(grid):
    print("-" * len(grid[0]))
    print(*["".join(map(str, row)) for row in grid], sep="\n")


def step(grid):
    n_flashed = 0
    # increment energy
    for ri, row in enumerate(grid):
        for ci, _ in enumerate(row):
            grid[ri][ci] += 1
    # flash
    flashed = True
    flashers = set()
    while flashed:
        flashed = False
        for ri, row in enumerate(grid):
            for ci, _ in enumerate(row):
                if grid[ri][ci] > 9 and (ri, ci) not in flashers:
                    flashed = True
                    n_flashed += 1
                    flashers.add((ri, ci))
                    for nri, nci in get_neighbours(grid, ri, ci):
                        grid[nri][nci] += 1
    all_flashed = True
    for ri, row in enumerate(grid):
        for ci, _ in enumerate(row):
            if grid[ri][ci] > 9:
                grid[ri][ci] = 0
            else:
                all_flashed = False
    return n_flashed, all_flashed


def solve(grid, n_steps):
    n_flashed = 0
    n_step = 0
    while True:
        n_step += 1
        n_flashed_step, all_flashed = step(grid)
        n_flashed += n_flashed_step
        if all_flashed:
            print(f"All flashed in step {n_step}")
            break
        if n_step == n_steps:
            print(n_flashed)


def main():
    with open("input.txt") as f:
        inp = f.readlines()
    grid = [list(map(int, row.strip())) for row in inp]
    n_steps = 100
    solve(grid, n_steps)


if __name__ == "__main__":
    main()
