from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from lib.file_access import read_input_lines


class Direction(Enum):
    ALL = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Blizzard:
    location: Point
    direction: Direction


class Day24:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    @property
    def width(self):
        return len(self.raw_input[0]) - 2

    @property
    def height(self):
        return len(self.raw_input) - 2

    @property
    def start(self):
        return Point(self.raw_input[0].index("."), 0)

    @property
    def goal(self):
        return Point(self.raw_input[-1].index("."), len(self.raw_input) - 1)

    def parse_blizzards(self):
        blizzards = set()
        for y, row in enumerate(self.raw_input):
            for x, char in enumerate(row):
                location = Point(x, y)
                match char:
                    case "^":
                        blizzards.add(Blizzard(location, Direction.NORTH))
                    case ">":
                        blizzards.add(Blizzard(location, Direction.EAST))
                    case "v":
                        blizzards.add(Blizzard(location, Direction.SOUTH))
                    case "<":
                        blizzards.add(Blizzard(location, Direction.WEST))

        return blizzards

    def move_blizzard(self, blizzard):
        match blizzard.direction:
            case Direction.NORTH:
                new_x = blizzard.location.x
                new_y = blizzard.location.y - 1
            case Direction.EAST:
                new_x = blizzard.location.x + 1
                new_y = blizzard.location.y
            case Direction.SOUTH:
                new_x = blizzard.location.x
                new_y = blizzard.location.y + 1
            case Direction.WEST:
                new_x = blizzard.location.x - 1
                new_y = blizzard.location.y

        if new_x < 1:
            new_x = self.width
        elif new_x > self.width:
            new_x = 1

        if new_y < 1:
            new_y = self.height
        elif new_y > self.height:
            new_y = 1

        return Blizzard(Point(new_x, new_y), blizzard.direction)

    @cached_property
    def maps(self):
        blizzards = self.parse_blizzards()

        maps = []
        while True:
            blizzard_locations = {blizzard.location for blizzard in blizzards}

            if len(maps) > 0 and maps[0] == blizzard_locations:
                break

            maps.append(blizzard_locations)
            blizzards = list(map(self.move_blizzard, blizzards))

        return maps

    def next_locations(self, current_locations, time):
        next_locations = set()
        for loc in current_locations:
            nearby = {
                Point(loc.x, loc.y + 1),
                Point(loc.x + 1, loc.y),
                Point(loc.x - 1, loc.y),
                Point(loc.x, loc.y - 1),
                loc,
            }
            possible_locations = {
                l for l in nearby if l.x > 0 and l.y > 0 and l.x <= self.width and l.y <= self.height or l == self.goal
            }
            new_locations = possible_locations - self.maps[time % len(self.maps)]
            next_locations.update(new_locations)

        if len(next_locations) == 0:
            next_locations.add(self.start)

        return next_locations

    def part1(self):
        time = 0
        current_locations = {self.start}

        while self.goal not in current_locations:
            time += 1
            current_locations = self.next_locations(current_locations, time)

        print()
        print("Part 1")
        print(f"  Solution to part 1: {time}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day24()
puzzle.part1()
puzzle.part2()
