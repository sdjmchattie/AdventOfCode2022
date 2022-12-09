from dataclasses import dataclass
from lib.file_access import read_input_lines
import re

REGEX_INSTRUCTION = re.compile(r"^([LDUR]) (\d+)$")

DIR_LEFT = "L"
DIR_RIGHT = "R"
DIR_UP = "U"
DIR_DOWN = "D"


@dataclass
class Knot:
    x: int
    y: int


class RopeSimulator:
    def __init__(self, knots):
        self._knots = [Knot(0, 0) for _ in range(knots)]
        self._tail_visited_locations = set()

    def move(self, direction):
        dx, dy = 0, 0

        if direction == DIR_RIGHT:
            dx = 1
        elif direction == DIR_LEFT:
            dx = -1
        elif direction == DIR_UP:
            dy = 1
        elif direction == DIR_DOWN:
            dy = -1

        self._knots[0].x += dx
        self._knots[0].y += dy

        for i in range(1, len(self._knots)):
            self._move_knot(i)

        tail = self._knots[-1]
        self._tail_visited_locations.add((tail.x, tail.y))

    def number_of_tail_locations(self):
        return len(self._tail_visited_locations)

    def _move_knot(self, index):
        def movement(value):
            return min(max(value, -1), 1)

        previous = self._knots[index - 1]
        current = self._knots[index]

        if abs(previous.x - current.x) == 2 or abs(previous.y - current.y) == 2:
            current.x += movement(previous.x - current.x)
            current.y += movement(previous.y - current.y)


class Day09:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)

    def run_steps(self, simulator):
        for line in self.raw_input:
            match = REGEX_INSTRUCTION.match(line)
            direction, distance = match.groups()
            for _ in range(int(distance)):
                simulator.move(direction)

    def part1(self):
        simulator = RopeSimulator(2)
        self.run_steps(simulator)

        print()
        print("Part 1")
        print(f"  Solution to part 1: {simulator.number_of_tail_locations()}")

    def part2(self):
        simulator = RopeSimulator(10)
        self.run_steps(simulator)

        print()
        print("Part 2")
        print(f"  Solution to part 2: {simulator.number_of_tail_locations()}")


puzzle = Day09()
puzzle.part1()
puzzle.part2()
