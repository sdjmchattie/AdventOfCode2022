from lib.file_access import read_input_lines


class Day13:
    def __init__(self):
        self._raw_input = read_input_lines(__file__)

    def process_input(self):
        pairs = ((eval(self._raw_input[i]), eval(self._raw_input[i+1])) for i in range(0, len(self._raw_input), 3))
        indices = (index + 1 if Day13._compare(pair[0], pair[1]) == -1 else 0 for index, pair in enumerate(pairs))
        self._pairs_in_order = sum(indices)

    def part1(self):
        print()
        print("Part 1")
        print(f"  Solution to part 1: {self._pairs_in_order}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")

    @staticmethod
    def _compare(left, right):
        if type(left) == int and type(right) == int:
            if left < right:
                return -1
            elif left > right:
                return 1
            else:
                return 0
        elif type(left) == list and type(right) == int:
            return Day13._compare(left, [right])
        elif type(left) == int and type(right) == list:
            return Day13._compare([left], right)

        # left and right are both lists, have either run out of items?
        if len(left) == 0 and len(right) == 0:
            return 0
        elif len(left) == 0:
            return -1
        elif len(right) == 0:
            return 1

        first_items_compare = Day13._compare(left[0], right[0])
        return Day13._compare(left[1:], right[1:]) if first_items_compare == 0 else first_items_compare


puzzle = Day13()
puzzle.process_input()
puzzle.part1()
puzzle.part2()
