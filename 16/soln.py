class Parser:
    def __init__(self):
        self.version_sum = 0

    def parse_version(self, s, cur):
        return int(s[cur : cur + 3], 2), cur + 3

    def parse_type_id(self, s, cur):
        return int(s[cur : cur + 3], 2), cur + 3

    def parse_length_id(self, s, cur):
        return int(s[cur], 2), cur + 1

    def parse_group(self, s, cur):
        is_last = s[cur] == "0"
        return is_last, s[cur + 1 : cur + 5], cur + 5

    def parse_literal(self, s, cur):
        groups = []
        is_last = False
        while not is_last:
            is_last, g, cur = self.parse_group(s, cur)
            groups.append(g)
        val = int("".join(groups), 2)
        return val, cur

    def parse_packets_0(self, s, cur):
        bit_length = int(s[cur : cur + 15], 2)
        cur += 15
        orig_cur = cur
        vals = []
        while cur - orig_cur < bit_length:
            val, cur = self.parse_header(s, cur)
            vals.append(val)
            if all(c == "0" for c in s[cur : orig_cur + bit_length]):
                cur = orig_cur + bit_length
        return vals, cur

    def parse_packets_1(self, s, cur):
        num_packets = int(s[cur : cur + 11], 2)
        cur += 11
        vals = []
        for _ in range(num_packets):
            val, cur = self.parse_header(s, cur)
            vals.append(val)
        return vals, cur

    def parse_operator(self, s, cur, type_id):
        length_id, cur = self.parse_length_id(s, cur)
        if length_id == 0:
            vals, cur = self.parse_packets_0(s, cur)
        elif length_id == 1:
            vals, cur = self.parse_packets_1(s, cur)
        if type_id == 0:
            val = sum(vals)
        elif type_id == 1:
            val = 1
            for other_val in vals:
                val *= other_val
        elif type_id == 2:
            val = min(vals)
        elif type_id == 3:
            val = max(vals)
        elif type_id == 5:
            val = int(vals[0] > vals[1])
        elif type_id == 6:
            val = int(vals[0] < vals[1])
        elif type_id == 7:
            val = int(vals[0] == vals[1])
        return val, cur

    def parse_header(self, s, cur):
        version, cur = self.parse_version(s, cur)
        self.version_sum += version
        type_id, cur = self.parse_type_id(s, cur)
        if type_id == 4:
            val, cur = self.parse_literal(s, cur)
        else:
            val, cur = self.parse_operator(s, cur, type_id)
        return val, cur


def pp(s, cur):
    print(s)
    print(" " * cur + "^")


def main():
    with open("input.txt") as f:
        inp = f.readlines()
    parser = Parser()
    for line in inp:
        s = "".join([bin(int(c, 16))[2:].rjust(4, "0") for c in line])
        print(parser.parse_header(s, 0)[0])
    print(parser.version_sum)


if __name__ == "__main__":
    main()
