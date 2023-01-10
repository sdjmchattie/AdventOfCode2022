from functools import cached_property
from lib.file_access import read_input_lines


class Day19:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    def part1(self):
        print()
        print("Part 1")
        print(f"  Solution to part 1: ")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day19()
puzzle.part1()
puzzle.part2()
