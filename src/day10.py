from lib.file_access import read_input_lines
import re

PARSING_REGEX = re.compile(r"^(\w+) (-?\d+)$")


class Day10:
    def __init__(self):
        self._raw_input = read_input_lines(__file__)

    def process_input(self):
        next_val = 1
        self.signal = []

        for line in self._raw_input:
            if line == "noop":
                self.signal.append(next_val)
            elif match := PARSING_REGEX.match(line):
                dval = int(match.group(2))
                self.signal.extend((next_val, next_val))
                next_val += dval

    def render_crt(self):
        for index, sprite_pos in enumerate(self.signal):
            row_index = index % 40
            print("⬛" if abs(sprite_pos - row_index) <= 1 else "🟧", end="")

            if row_index == 39:
                print()

    def part1(self):
        sum_of_signals = sum(((40 * i) + 20) * v for i, v in enumerate(self.signal[19::40]))

        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum_of_signals}")

    def part2(self):
        print()
        print("Part 2")
        print()
        self.render_crt()
        print()


puzzle = Day10()
puzzle.process_input()
puzzle.part1()
puzzle.part2()
