from enum import Enum
from functools import cached_property
from lib.file_access import read_input_lines

import re

DISTANCE_REGEX = re.compile(r"^\d+")
TURN_REGEX = re.compile(r"^[LR]")


class Direction(Enum):
    East = 0
    South = 1
    West = 2
    North = 3


class Journey:
    def __init__(self, map, directions):
        self._map = map
        self._directions = directions

        self.direction = Direction.East
        self.row = 1
        self.column = self._map[0].index(".") + 1

    def follow_journey(self):
        directions = self._directions

        while True:
            next_distance = DISTANCE_REGEX.match(directions)
            if next_distance is not None:
                directions = directions[len(next_distance[0]) :]
                self.move(int(next_distance[0]))

            next_turn = TURN_REGEX.match(directions)
            if next_turn is not None:
                directions = directions[len(next_turn[0]) :]
                self.turn(next_turn[0])

            if len(directions) == 0:
                break

    def move(self, distance):
        raise NotImplementedError()

    def turn(self, direction):
        if direction == "L":
            new_direction = self.direction.value - 1
            if new_direction == -1:
                new_direction = 3
        else:
            new_direction = self.direction.value + 1
            if new_direction == 4:
                new_direction = 0

        self.direction = Direction(new_direction)


class FlatJourney(Journey):
    def move(self, distance):
        for _ in range(distance):
            if self.direction == Direction.East:
                new_row = self.row
                new_column = self.column + 1
                if new_column > len(self._map[new_row - 1]):
                    new_column = min(self._map[new_row - 1].index("."), self._map[new_row - 1].index("#")) + 1
            elif self.direction == Direction.South:
                new_row = self.row + 1
                new_column = self.column
                if (
                    new_row > len(self._map)
                    or len(self._map[new_row - 1]) < new_column
                    or self._map[new_row - 1][new_column - 1] == " "
                ):
                    whole_column = list(
                        map(lambda row: row[new_column - 1] if len(row) >= new_column else " ", self._map)
                    )
                    new_row = min(whole_column.index("."), whole_column.index("#")) + 1
            elif self.direction == Direction.West:
                new_row = self.row
                new_column = self.column - 1
                if new_column < 1 or self._map[new_row - 1][new_column - 1] == " ":
                    reversed_row = list(reversed(self._map[new_row - 1]))
                    new_column = len(reversed_row) - min(reversed_row.index("."), reversed_row.index("#"))
            else:
                new_row = self.row - 1
                new_column = self.column
                if (
                    new_row < 1
                    or len(self._map[new_row - 1]) < new_column
                    or self._map[new_row - 1][new_column - 1] == " "
                ):
                    whole_column = list(
                        reversed(
                            list(map(lambda row: row[self.column - 1] if len(row) >= new_column else " ", self._map))
                        )
                    )
                    new_row = len(self._map) - min(whole_column.index("."), whole_column.index("#"))

            if self._map[new_row - 1][new_column - 1] == ".":
                self.row = new_row
                self.column = new_column


class CubeJourney(Journey):
    def move(self, distance):
        for _ in range(distance):
            if self.direction == Direction.East:
                new_row, new_column, new_direction = self.move_east()
            elif self.direction == Direction.South:
                new_row, new_column, new_direction = self.move_south()
            if self.direction == Direction.West:
                new_row, new_column, new_direction = self.move_west()
            if self.direction == Direction.North:
                new_row, new_column, new_direction = self.move_north()

            if self._map[new_row - 1][new_column - 1] == ".":
                self.row = new_row
                self.column = new_column
                self.direction = new_direction

    def move_east(self):
        if self.row >= 1 and self.row <= 50 and self.column == 150:
            return 151 - self.row, 100, Direction.West
        elif self.row >= 51 and self.row <= 100 and self.column == 100:
            return 50, 50 + self.row, Direction.North
        elif self.row >= 101 and self.row <= 150 and self.column == 100:
            return 151 - self.row, 150, Direction.West
        elif self.row >= 151 and self.row <= 200 and self.column == 50:
            return 150, self.row - 100, Direction.North
        else:
            return self.row, self.column + 1, Direction.East

    def move_south(self):
        if self.column >= 1 and self.column <= 50 and self.row == 200:
            return 1, self.column + 100, Direction.South
        elif self.column >= 51 and self.column <= 100 and self.row == 150:
            return self.column + 100, 50, Direction.West
        elif self.column >= 101 and self.column <= 150 and self.row == 50:
            return self.column - 50, 100, Direction.West
        else:
            return self.row + 1, self.column, Direction.South

    def move_west(self):
        if self.row >= 1 and self.row <= 50 and self.column == 51:
            return 151 - self.row, 1, Direction.East
        elif self.row >= 51 and self.row <= 100 and self.column == 51:
            return 101, self.row - 50, Direction.South
        elif self.row >= 101 and self.row <= 150 and self.column == 1:
            return 151 - self.row, 51, Direction.East
        elif self.row >= 151 and self.row <= 200 and self.column == 1:
            return 1, self.row - 100, Direction.South
        else:
            return self.row, self.column - 1, Direction.West

    def move_north(self):
        if self.column >= 1 and self.column <= 50 and self.row == 101:
            return self.column + 50, 51, Direction.East
        elif self.column >= 51 and self.column <= 100 and self.row == 1:
            return self.column + 100, 1, Direction.East
        elif self.column >= 101 and self.column <= 150 and self.row == 1:
            return 200, self.column - 100, Direction.North
        else:
            return self.row - 1, self.column, Direction.North


class Day22:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    @cached_property
    def map(self):
        return self.raw_input[0:-2]

    @cached_property
    def directions(self):
        return self.raw_input[-1]

    def part1(self):
        journey = FlatJourney(self.map, self.directions)
        journey.follow_journey()

        password = 1000 * journey.row + 4 * journey.column + journey.direction.value

        print()
        print("Part 1")
        print(f"  Solution to part 1: {password}")

    def part2(self):
        journey = CubeJourney(self.map, self.directions)
        journey.follow_journey()

        password = 1000 * journey.row + 4 * journey.column + journey.direction.value
        print()
        print("Part 2")
        print(f"  Solution to part 2: {password}")


puzzle = Day22()
puzzle.part1()
puzzle.part2()
