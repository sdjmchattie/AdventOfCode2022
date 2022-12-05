import re
from copy import deepcopy

from lib.file_access import read_input_lines

INITIAL_STACKS = [
    ["H", "C", "R"],
    ["B", "J", "H", "L", "S", "F"],
    ["R", "M", "D", "H", "J", "T", "Q"],
    ["S", "G", "R", "H", "Z", "B", "J"],
    ["R", "P", "F", "Z", "T", "D", "C", "B"],
    ["T", "H", "C", "G"],
    ["S", "N", "V", "Z", "B", "P", "W", "L"],
    ["R", "J", "Q", "G", "C"],
    ["L", "D", "T", "R", "H", "P", "F", "S"],
]

INSTRUCTION_REGEX = re.compile(r"move (\d+) from (\d+) to (\d+)")


class Day05:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def process_input(self):
        input_split_index = self.raw_input.index("")

        stacks = self.raw_input[: input_split_index - 1]  # Drop column numbering
        self.parse_stacks(stacks)

        moves = self.raw_input[input_split_index + 1 :]
        self.instructions = list(map(lambda line: list(map(int, INSTRUCTION_REGEX.match(line).groups())), moves))

    def part1(self):
        stacks = self.execute_part1()
        password = map(lambda stack: stack[-1], stacks)

        print()
        print("Part 1")
        print(f"  Solution to part 1: {''.join(password)}")

    def part2(self):
        stacks = self.execute_part2()
        password = map(lambda stack: stack[-1], stacks)

        print()
        print("Part 2")
        print(f"  Solution to part 2: {''.join(password)}")

    def parse_stacks(self, raw_input):
        raw_input.reverse()
        stacks = list(map(list, raw_input[0][1::4]))
        for row in raw_input[1:]:
            for index, box in enumerate(row[1::4]):
                stacks[index].append(box)

        stacks = list(map(lambda stack: [x for x in stack if x != " "], stacks))

        self.initial_stacks = stacks

    def execute_part1(self):
        stacks = deepcopy(self.initial_stacks)

        for instruction in self.instructions:
            boxes_to_move = instruction[0]
            from_stack = stacks[instruction[1] - 1]
            to_stack = stacks[instruction[2] - 1]

            moved = list(map(lambda _: from_stack.pop(), range(boxes_to_move)))
            to_stack.extend(moved)

        return stacks

    def execute_part2(self):
        stacks = deepcopy(self.initial_stacks)

        for instruction in self.instructions:
            boxes_to_move = instruction[0]
            from_stack = stacks[instruction[1] - 1]
            to_stack = stacks[instruction[2] - 1]

            moved = list(map(lambda _: from_stack.pop(), range(boxes_to_move)))
            to_stack.extend(reversed(moved))

        return stacks


puzzle = Day05()
puzzle.part1()
puzzle.part2()
