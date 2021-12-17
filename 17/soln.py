import re


def main():
    with open("input.txt") as f:
        inp = f.readlines()[0]

    search = re.search("x=(.*)\.\.(.*), y=(.*)\.\.(.*)", inp)
    x_min = int(search.group(1))
    x_max = int(search.group(2))
    y_min = int(search.group(3))
    y_max = int(search.group(4))

    y_pos_max = 0
    total = 0
    for initial_y_vel in range(y_min - 1, -y_min + 1):
        for initial_x_vel in range(1, x_max + 1):
            x = 0
            y = 0
            y_pos_max_traj = 0
            x_vel = initial_x_vel
            y_vel = initial_y_vel
            while y >= y_min:
                x += x_vel
                y += y_vel
                y_pos_max_traj = max(y_pos_max_traj, y)
                y_vel -= 1
                x_vel = max(0, x_vel - 1)
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    total += 1
                    y_pos_max = max(y_pos_max, y_pos_max_traj)
                    break
    print(y_pos_max)
    print(total)


if __name__ == "__main__":
    main()
