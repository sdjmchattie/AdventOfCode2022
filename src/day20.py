from dataclasses import dataclass
from functools import cached_property, reduce
from lib.file_access import read_input_lines


@dataclass
class Code:
    index: int
    value: int


class Day20:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    def initial_state(self):
        return [Code(i, int(x)) for i, x in enumerate(self.raw_input)]

    def part1(self):
        size = len(self.raw_input)
        state = self.initial_state()
        for index in range(size):
            item_to_move = next(filter(lambda code: code.index == index, state))
            cur_index = state.index(item_to_move)
            new_index = cur_index + item_to_move.value % (size - 1)
            new_index = new_index % size + new_index // size

            state.remove(item_to_move)
            state.insert(new_index, item_to_move)

        zero_item = next(filter(lambda code: code.value == 0, state))
        zero_index = state.index(zero_item)
        sum_of_coordinates = reduce(lambda acc, i: acc + state[((i + 1) * 1000 + zero_index) % size].value, range(3), 0)

        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum_of_coordinates}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day20()
puzzle.part1()
puzzle.part2()
