from lib.file_access import read_input_lines


class Day03:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def priority(item):
        priority = ord(item) - 38
        if priority > 52:
            priority -= 58

        return priority

    def find_dup_item(backpack):
        half = int(len(backpack) / 2)
        comp_1 = backpack[:half]
        comp_2 = backpack[-half:]

        return [item for item in comp_1 if item in comp_2][0]

    def process_input(self):
        self.priorities = list(map(lambda backpack: Day03.priority(Day03.find_dup_item(backpack)), self.raw_input))

    def part1(self):
        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum(self.priorities)}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day03()
puzzle.part1()
puzzle.part2()
