import re
from lib.file_access import read_input_lines

SPLIT_REGEX = re.compile(r"[,-]")


class Day04:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def process_input(self):
        def split_values(line):
            vals = re.split(SPLIT_REGEX, line)
            range_1 = set(range(int(vals[0]), int(vals[1]) + 1))
            range_2 = set(range(int(vals[2]), int(vals[3]) + 1))

            return (range_1, range_2)

        self.ranges = list(map(split_values, self.raw_input))

    def part1(self):
        count = sum(map(lambda r: len(r[0] - r[1]) == 0 or len(r[1] - r[0]) == 0, self.ranges))

        print()
        print("Part 1")
        print(f"  Solution to part 1: {count}")

    def part2(self):
        count = sum(map(lambda r: len(r[0]) != len(r[0] - r[1]), self.ranges))

        print()
        print("Part 2")
        print(f"  Solution to part 2: {count}")


puzzle = Day04()
puzzle.part1()
puzzle.part2()
