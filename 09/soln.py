def main():
    grid = []
    with open("input.txt") as f:
        inp = f.readlines()
    for line in inp:  
      grid += [list(map(int, line.strip()))]
    total = 0
    for y, row in enumerate(grid):
      for x, center in enumerate(row):
        if y > 0:
          if grid[y-1][x] <= center:
            continue
        if y < len(grid) - 1:
          if grid[y+1][x] <= center:
            continue
        if x < len(row) - 1:
          if grid[y][x+1] <= center:
            continue
        if x > 0:
          if grid[y][x-1] <= center:
            continue
        total += center + 1
    print(total)


if __name__ == "__main__":
    main()