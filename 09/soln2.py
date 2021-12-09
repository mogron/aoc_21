def fill_basin(grid, basin, y, x):
  q = [(y, x)]
  size = 0
  while q:
    y, x = q.pop()
    if grid[y][x] >= 9:
      continue
    if basin[y][x] != -1:
      continue
    size += 1
    basin[y][x] = 1
    if y > 0:
      q.append((y-1, x))
    if y < len(grid) - 1:
      q.append((y+1, x))
    if x < len(grid[y]) - 1:
      q.append((y, x+1))
    if x > 0:
      q.append((y, x-1))
  return size

def main():
    grid = []
    basin = []
    with open("input.txt") as f:
        inp = f.readlines()
    for line in inp:  
      row = list(map(int, line.strip()))
      grid += [row]
      basin += [[-1] * len(row)]
    sizes = []
    for y, row in enumerate(grid):
      for x, center in enumerate(row):
        if center == 9:
          continue
        if basin[y][x] > -1:
          continue
        size = fill_basin(grid, basin, y, x)
        sizes.append(size)
    sizes.sort()
    print(sizes[-3:])
    a, b, c = sizes[-3:]
    print(a*b*c)


if __name__ == "__main__":
    main()