from functools import cached_property
from lib.file_access import read_input_lines
import re

line_regex = re.compile(r"^(\w+): (.+)$")
number_regex = re.compile(r"^\d+$")
operation_regex = re.compile(r"^(\w+) (.) (\w+)$")


class Monkey:
    def __init__(self, operation):
        self._operation = operation
        self.all_monkeys = {}

    @cached_property
    def value(self):
        if (number_match := number_regex.match(self._operation)) is not None:
            return int(number_match[0])
        elif (op_match := operation_regex.match(self._operation)) is not None:
            left_val = self.all_monkeys[op_match[1]].value
            right_val = self.all_monkeys[op_match[3]].value

            if op_match[2] == "+":
                return left_val + right_val
            elif op_match[2] == "-":
                return left_val - right_val
            elif op_match[2] == "*":
                return left_val * right_val
            elif op_match[2] == "/":
                return left_val / right_val

    def check_equality_operation(self):
        op_match = operation_regex.match(self._operation)
        left_val = self.all_monkeys[op_match[1]].value
        right_val = self.all_monkeys[op_match[3]].value
        print(left_val)
        print(right_val)
        print()

        return left_val == right_val


class Day21:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    def monkeys(self):
        matches = (line_regex.match(line) for line in self.raw_input)
        monkeys = {match[1]: Monkey(match[2]) for match in matches}
        for monkey in monkeys.values():
            monkey.all_monkeys = monkeys

        return monkeys

    def part1(self):
        root_monkey = self.monkeys()["root"]

        print()
        print("Part 1")
        print(f"  Solution to part 1: {root_monkey.value}")

    def part2(self):
        humn_val = 3876027196000
        while True:
            monkeys = self.monkeys()
            monkeys["humn"]._operation = str(humn_val)
            if monkeys["root"].check_equality_operation():
                break

            humn_val += 1

        print()
        print("Part 2")
        print(f"  Solution to part 2: {humn_val}")


puzzle = Day21()
puzzle.part1()
puzzle.part2()
