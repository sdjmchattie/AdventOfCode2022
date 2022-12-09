from lib.file_access import read_input_lines
import re

REGEX_INSTRUCTION = re.compile(r"^([LDUR]) (\d+)$")

DIR_LEFT = "L"
DIR_RIGHT = "R"
DIR_UP = "U"
DIR_DOWN = "D"


class RopeSimulator:
    def __init__(self):
        self._head_x = 0
        self._head_y = 0

        self._tail_x = 0
        self._tail_y = 0

        self._tail_visited_locations = set()

    def move(self, direction):
        if direction == DIR_RIGHT:
            self._head_x += 1
        elif direction == DIR_LEFT:
            self._head_x -= 1
        elif direction == DIR_UP:
            self._head_y += 1
        elif direction == DIR_DOWN:
            self._head_y -= 1

        self._move_tail()

    def number_of_tail_locations(self):
        return len(self._tail_visited_locations)

    def _move_tail(self):
        if abs(self._head_x - self._tail_x) > 2 or abs(self._head_y - self._tail_y) > 2:
            raise Exception(
                f"Something odd has happened.  Head is at ({self._head_x}, {self._head_y}) "
                f"and tail is at ({self._tail_x}, {self._tail_y})."
            )

        if self._head_x - self._tail_x == 2:
            self._tail_x += 1
            self._tail_y = self._head_y
        elif self._tail_x - self._head_x == 2:
            self._tail_x -= 1
            self._tail_y = self._head_y
        elif self._head_y - self._tail_y == 2:
            self._tail_y += 1
            self._tail_x = self._head_x
        elif self._tail_y - self._head_y == 2:
            self._tail_y -= 1
            self._tail_x = self._head_x

        self._tail_visited_locations.add((self._tail_x, self._tail_y))


class Day09:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self._simulator = RopeSimulator()

    def process_input(self):
        for line in self.raw_input:
            match = REGEX_INSTRUCTION.match(line)
            direction, distance = match.groups()
            for _ in range(int(distance)):
                self._simulator.move(direction)

    def part1(self):
        print()
        print("Part 1")
        print(f"  Solution to part 1: {self._simulator.number_of_tail_locations()}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day09()
puzzle.process_input()
puzzle.part1()
puzzle.part2()
