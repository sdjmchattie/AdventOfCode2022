import re
from lib.file_access import read_input_lines

SPLIT_REGEX = re.compile(r"[,-]")


class Day04:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def process_input(self):
        def split_values(line):
            split_vals = re.split(SPLIT_REGEX, line)
            return list(map(lambda v: int(v), split_vals))

        self.ranges = list(map(split_values, self.raw_input))

    def part1(self):
        def ranges_fully_overlap(ranges):
            return (
                ranges[0] == ranges[2]
                or ranges[1] == ranges[3]
                or (ranges[0] > ranges[2] and ranges[1] <= ranges[3])
                or (ranges[0] < ranges[2] and ranges[1] >= ranges[3])
            )

        subset_count = sum(map(ranges_fully_overlap, self.ranges))

        print()
        print("Part 1")
        print(f"  Solution to part 1: {subset_count}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day04()
puzzle.part1()
puzzle.part2()
