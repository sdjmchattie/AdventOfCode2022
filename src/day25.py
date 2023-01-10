from functools import cached_property
from lib.file_access import read_input_lines

snafu_char_to_decimal = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

decimal_to_snafu_char = {
    -2: "=",
    -1: "-",
    0: "0",
    1: "1",
    2: "2",
}


def snafu_to_decimal(value):
    def dec_part(char, power):
        return snafu_char_to_decimal[char] * 5**power

    dec_values = [dec_part(char, index) for index, char in enumerate(reversed(value))]
    return sum(dec_values)


def decimal_to_snafu(value):
    def closest_digit(remainder, power):
        differences = [remainder - x * 5**power for x in range(-2, 3)]
        abs_diffs = [abs(diff) for diff in differences]
        min_difference = min(abs_diffs)
        digit_index = abs_diffs.index(min_difference)

        return decimal_to_snafu_char[digit_index - 2], differences[digit_index]

    snafu = ""
    for power in range(25, -1, -1):
        digit, value = closest_digit(value, power)
        if digit != "0" or len(snafu) > 0:
            snafu += digit

    return snafu


class Day25:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    def part1(self):
        decimal_fuel = sum([snafu_to_decimal(snafu) for snafu in self.raw_input])

        print()
        print("Part 1")
        print(f"  Solution to part 1: {decimal_to_snafu(decimal_fuel)}")


puzzle = Day25()
puzzle.part1()
