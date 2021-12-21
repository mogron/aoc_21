from copy import deepcopy


def transform_pixel(img_in, img_out, x, y, key):
    s = (
        img_in[y - 1][x - 1 : x + 2]
        + img_in[y][x - 1 : x + 2]
        + img_in[y + 1][x - 1 : x + 2]
    )
    val = int("".join(s), 2)
    if val >= 512:
        print("hi")
        print(s)
        print(val)
        print(key[val])
    out = key[val]
    img_out[y][x] = out


def transform_img(img_in, key, iterations):
    img_out = deepcopy(img_in)
    for iteration in range(iterations):
        for y in range(1, len(img_in) - 1):
            for x in range(1, len(img_in[y]) - 1):
                transform_pixel(img_in, img_out, x, y, key)
        reset_border(img_out)
        img_in, img_out = img_out, img_in
    return img_in


def pad(img, xpad, ypad):
    w = len(img[0])
    wpad = w + xpad * 2
    res = [["0"] * wpad for _ in range(ypad)]
    res += [["0"] * xpad + row + ["0"] * xpad for row in img]
    res += [["0"] * wpad for _ in range(ypad)]
    return res


def reset_border(img):
    val = img[1][1]
    n = len(img[0])
    for row in img:
        row[0] = val
        row[1] = val
        row[n - 1] = val
        row[n - 2] = val
    img[0] = [val] * n
    img[1] = [val] * n
    img[len(img) - 1] = [val] * n
    img[len(img) - 2] = [val] * n


def print_img(img):
    print(*["".join(row) for row in img], sep="\n")


def main():
    with open("input.txt") as f:
        key, _, *img = f.read().splitlines()
    key = key.replace(".", "0").replace("#", "1")
    img = [list(row.replace(".", "0").replace("#", "1")) for row in img]
    img = list(map(list, img))
    img = pad(img, 100, 100)
    res = transform_img(img, key, 50)
    res = [row[2 : len(row) - 2] for row in res[2 : len(res) - 2]]
    print_img(res)
    lit_pixels = sum(row.count("1") for row in res)
    print(lit_pixels)


if __name__ == "__main__":
    main()
