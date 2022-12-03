from functools import reduce
import string
from lib.file_access import read_input_lines


class Day03:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)

    def priority(item):
        priority = ord(item) - 38
        if priority > 52:
            priority -= 58

        return priority

    def find_dup_item(backpack):
        half = len(backpack) // 2
        comp_1 = backpack[:half]
        comp_2 = backpack[half:]

        return [item for item in comp_1 if item in comp_2][0]

    def find_badge_item(backpacks):
        def find_common(common, backpack):
            return [item for item in common if item in backpack]

        return reduce(find_common, backpacks, string.ascii_letters)[0]

    def part1(self):
        priorities = list(
            map(
                lambda backpack: Day03.priority(Day03.find_dup_item(backpack)),
                self.raw_input,
            )
        )

        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum(priorities)}")

    def part2(self):
        group_badge_priorities = map(
            lambda idx: Day03.priority(Day03.find_badge_item(self.raw_input[idx : idx + 3])),
            range(0, len(self.raw_input), 3),
        )

        print()
        print("Part 2")
        print(f"  Solution to part 2: {sum(group_badge_priorities)}")


puzzle = Day03()
puzzle.part1()
puzzle.part2()
