from dataclasses import dataclass
from lib.file_access import read_input_lines
import re


REGEX_INPUT_LINE = re.compile(r"^.+x=(-?\d+), y=(-?\d+):.+x=(-?\d+), y=(-?\d+)$")


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Range:
    min: int
    max: int

    def length(self):
        return self.max - self.min + 1

    def overlaps_with(self, range):
        return self.max >= range.min and self.min <= range.max


@dataclass
class Sensor:
    location: Point
    beacon: Point

    @property
    def reach(self):
        return abs(self.location.x - self.beacon.x) + abs(self.location.y - self.beacon.y)

    def coverage_range_on_row(self, row):
        dist_from_row = abs(row - self.location.y)
        range_width = self.reach - dist_from_row

        if range_width >= 0:
            return Range(self.location.x - range_width, self.location.x + range_width)
        else:
            return None


class Day15:
    def __init__(self):
        self._raw_input = read_input_lines(__file__)

    def process_input(self):
        vals = [list(map(int, REGEX_INPUT_LINE.match(line).groups())) for line in self._raw_input]
        self._sensors = [Sensor(Point(sx, sy), Point(bx, by)) for sx, sy, bx, by in vals]

    def part1(self):
        row_ranges = filter(
            lambda v: v is not None, (sensor.coverage_range_on_row(2000000) for sensor in self._sensors)
        )

        coallesced_ranges = []
        for new_range in row_ranges:
            overlapped_ranges = [new_range]
            for range in coallesced_ranges[:]:
                if range.overlaps_with(new_range):
                    overlapped_ranges.append(range)
                    coallesced_ranges.remove(range)

            min_x = min(overlapped_ranges, key=lambda r: r.min).min
            max_x = max(overlapped_ranges, key=lambda r: r.max).max
            coallesced_ranges.append(Range(min_x, max_x))

        beacons_on_row = set((sensor.beacon for sensor in self._sensors if sensor.beacon.y == 2000000))

        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum(map(lambda r: r.length(), coallesced_ranges)) - len(beacons_on_row)}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day15()
puzzle.process_input()
puzzle.part1()
puzzle.part2()
