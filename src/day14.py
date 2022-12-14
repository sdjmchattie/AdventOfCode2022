from lib.file_access import read_input_lines
import re

REGEX_COORDS = re.compile(r"(\d+),(\d+)")


class SandSimulator:
    def __init__(self):
        self._occupied = set()
        self._max_y = 0
        self._sand_count = 0

    @property
    def sand_count(self):
        return self._sand_count

    def add_material(self, x, y):
        self._occupied.add((x, y))
        self._max_y = max(self._max_y, y)

    def add_floor(self):
        floor_y = self._max_y + 2
        for x in range(500 - floor_y - 2, 500 + floor_y + 3):
            self.add_material(x, floor_y)

    def fill_with_sand(self):
        finished = False
        while not finished:
            sand_pos = (500, 0)
            while (new_pos := self._space_to_fall(sand_pos)) is not None:
                sand_pos = new_pos

                if new_pos[1] > self._max_y:
                    finished = True
                    break

            if not finished:
                self.add_material(*sand_pos)
                self._sand_count += 1

            if sand_pos == (500, 0):
                break

    def _space_to_fall(self, pos):
        below = (pos[0], pos[1] + 1)
        if not below in self._occupied:
            return below

        diag_left = (pos[0] - 1, pos[1] + 1)
        if not diag_left in self._occupied:
            return diag_left

        diag_right = (pos[0] + 1, pos[1] + 1)
        if not diag_right in self._occupied:
            return diag_right

        return None


class Day14:
    def __init__(self):
        self._raw_input = read_input_lines(__file__)

    def part1(self):
        print()
        print("Part 1")

        simulator = self._prepare_simulator()
        simulator.fill_with_sand()

        print(f"  Solution to part 1: {simulator.sand_count}")

    def part2(self):
        print()
        print("Part 2")

        simulator = self._prepare_simulator()
        simulator.add_floor()
        simulator.fill_with_sand()

        print(f"  Solution to part 2: {simulator.sand_count}")

    def _prepare_simulator(self):
        sand_simulator = SandSimulator()
        for line in self._raw_input:
            coord_matches = REGEX_COORDS.findall(line)
            for i in range(len(coord_matches) - 1):
                sx, sy = map(int, coord_matches[i])
                ex, ey = map(int, coord_matches[i + 1])
                for x in range(min(sx, ex), max(sx, ex) + 1):
                    for y in range(min(sy, ey), max(sy, ey) + 1):
                        sand_simulator.add_material(x, y)

        return sand_simulator


puzzle = Day14()
puzzle.part1()
puzzle.part2()
