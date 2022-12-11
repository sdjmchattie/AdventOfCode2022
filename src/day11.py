from functools import reduce
from math import floor
from decimal import Decimal
from lib.file_access import read_input_lines


class Monkey:
    def __init__(self, items, op_func, test_divisor, common_divisor):
        self._items = items
        self._op_func = op_func
        self._test_divisor = test_divisor
        self._common_divisor = common_divisor
        self.true_monkey = None
        self.false_monkey = None
        self.inspection_count = 0

    def inspect_items(self, should_relieve_worry):
        for item in self._items:
            self.inspection_count += 1
            item = self._op_func(item)

            if should_relieve_worry:
                item = floor(item / 3)

            item = item % self._common_divisor

            if item % self._test_divisor == 0:
                self.true_monkey.receive_item(item)
            else:
                self.false_monkey.receive_item(item)

        self._items = []

    def receive_item(self, item):
        self._items.append(item)


class Day11:
    def __init__(self):
        self._raw_input = read_input_lines(__file__)

    def part1(self):
        self._process_input()
        for _ in range(20):
            for monkey in self._monkeys:
                monkey.inspect_items(True)

        monkey_activity = [monkey.inspection_count for monkey in self._monkeys]
        monkey_activity.sort()
        monkey_business = monkey_activity[-1] * monkey_activity[-2]

        print()
        print("Part 1")
        print(f"  Solution to part 1: {monkey_business}")

    def part2(self):
        self._process_input()
        for _ in range(10000):
            for monkey in self._monkeys:
                monkey.inspect_items(False)

        monkey_activity = [monkey.inspection_count for monkey in self._monkeys]
        monkey_activity.sort()
        monkey_business = monkey_activity[-1] * monkey_activity[-2]

        print()
        print("Part 2")
        print(f"  Solution to part 2: {monkey_business}")

    def _process_input(self):
        test_divisors = (19, 3, 13, 7, 5, 11, 17, 2)
        common_divisor = reduce(lambda a, v: a * v, test_divisors)

        self._monkeys = [
            Monkey([85, 77, 77], lambda old: old * 7, test_divisors[0], common_divisor),
            Monkey([80, 99], lambda old: old * 11, test_divisors[1], common_divisor),
            Monkey([74, 60, 74, 63, 86, 92, 80], lambda old: old + 8, test_divisors[2], common_divisor),
            Monkey([71, 58, 93, 65, 80, 68, 54, 71], lambda old: old + 7, test_divisors[3], common_divisor),
            Monkey([97, 56, 79, 65, 58], lambda old: old + 5, test_divisors[4], common_divisor),
            Monkey([77], lambda old: old + 4, test_divisors[5], common_divisor),
            Monkey([99, 90, 84, 50], lambda old: old * old, test_divisors[6], common_divisor),
            Monkey([50, 66, 61, 92, 64, 78], lambda old: old + 3, test_divisors[7], common_divisor),
        ]

        self._monkeys[0].true_monkey = self._monkeys[6]
        self._monkeys[0].false_monkey = self._monkeys[7]
        self._monkeys[1].true_monkey = self._monkeys[3]
        self._monkeys[1].false_monkey = self._monkeys[5]
        self._monkeys[2].true_monkey = self._monkeys[0]
        self._monkeys[2].false_monkey = self._monkeys[6]
        self._monkeys[3].true_monkey = self._monkeys[2]
        self._monkeys[3].false_monkey = self._monkeys[4]
        self._monkeys[4].true_monkey = self._monkeys[2]
        self._monkeys[4].false_monkey = self._monkeys[0]
        self._monkeys[5].true_monkey = self._monkeys[4]
        self._monkeys[5].false_monkey = self._monkeys[3]
        self._monkeys[6].true_monkey = self._monkeys[7]
        self._monkeys[6].false_monkey = self._monkeys[1]
        self._monkeys[7].true_monkey = self._monkeys[5]
        self._monkeys[7].false_monkey = self._monkeys[1]


puzzle = Day11()
puzzle.part1()
puzzle.part2()
