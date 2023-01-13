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


class Elf:
    location: Point
    proposed: Point

    def __init__(self, location):
        self.location = location

    def neighbours(self, direction):
        match direction:
            case Direction.ALL:
                return {
                    Point(x, y)
                    for x in range(self.location.x - 1, self.location.x + 2)
                    for y in range(self.location.y - 1, self.location.y + 2)
                    if self.location.x != x or self.location.y != y
                }
            case Direction.NORTH:
                return {Point(x, self.location.y - 1) for x in range(self.location.x - 1, self.location.x + 2)}
            case Direction.SOUTH:
                return {Point(x, self.location.y + 1) for x in range(self.location.x - 1, self.location.x + 2)}
            case Direction.EAST:
                return {Point(self.location.x + 1, y) for y in range(self.location.y - 1, self.location.y + 2)}
            case Direction.WEST:
                return {Point(self.location.x - 1, y) for y in range(self.location.y - 1, self.location.y + 2)}

    def location_in_direction(self, direction):
        match direction:
            case Direction.NORTH:
                return Point(self.location.x, self.location.y - 1)
            case Direction.SOUTH:
                return Point(self.location.x, self.location.y + 1)
            case Direction.EAST:
                return Point(self.location.x + 1, self.location.y)
            case Direction.WEST:
                return Point(self.location.x - 1, self.location.y)

    def make_proposal(self, occupied_locations, proposal_order):
        self.proposed = None

        if len(self.neighbours(Direction.ALL) - occupied_locations) < 8:
            for direction in proposal_order:
                if len(self.neighbours(direction) - occupied_locations) == 3:
                    self.proposed = self.location_in_direction(direction)
                    break

    def review_proposal(self, all_proposals):
        if len([proposal for proposal in all_proposals if proposal == self.proposed]) > 1:
            self.proposed = None

    def apply_proposal(self):
        if self.proposed is not None:
            self.location = self.proposed


class Day23:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    def prepare(self):
        self.elves = [
            Elf(Point(x, y)) for y, row in enumerate(self.raw_input) for x, loc in enumerate(row) if loc == "#"
        ]
        self.proposal_order = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]

    def execute_round(self):
        elf_locations = {elf.location for elf in self.elves}
        for elf in self.elves:
            elf.make_proposal(elf_locations, self.proposal_order)

        all_proposals = [elf.proposed for elf in self.elves if elf.proposed is not None]
        for elf in self.elves:
            elf.review_proposal(all_proposals)
            elf.apply_proposal()

        self.proposal_order.append(self.proposal_order.pop(0))

    def count_sparsity(self):
        xs = [elf.location.x for elf in self.elves]
        ys = [elf.location.y for elf in self.elves]

        width = max(xs) - min(xs) + 1
        height = max(ys) - min(ys) + 1

        return width * height - len(self.elves)

    def part1(self):
        self.prepare()

        for _ in range(10):
            self.execute_round()

        print()
        print("Part 1")
        print(f"  Solution to part 1: {self.count_sparsity()}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day23()
puzzle.part1()
puzzle.part2()
