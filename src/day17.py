from dataclasses import dataclass
from functools import cached_property, reduce
from lib.file_access import read_input_lines

FORMATIONS = (
    ("####",),
    (
        ".#.",
        "###",
        ".#.",
    ),
    (
        "###",
        "..#",
        "..#",
    ),
    (
        "#",
        "#",
        "#",
        "#",
    ),
    (
        "##",
        "##",
    ),
)


@dataclass
class Point:
    x: int
    y: int


class RockFormation:
    def __init__(self, formation):
        self.formation = formation

    def rock_positions(self, offset):
        for y, row in enumerate(self.formation):
            for x, symbol in enumerate(row):
                if symbol == "#":
                    yield x + offset.x, y + offset.y

    @property
    def width(self):
        return len(self.formation[0])


class Tetris:
    def __init__(self, moves):
        self.moves = moves
        self.rock = set()
        self.fallen = 0
        self.falling_rock = RockFormation(FORMATIONS[0])
        self.falling_position = Point(2, 3)

    def __str__(self):
        description = []
        for y in range(self.tower_height - 1, -1, -1):
            description.append("|")
            for x in range(7):
                symbol = "#" if (x, y) in self.rock else "."
                description[-1] += symbol
            description[-1] += "|"
        description.append("+-------+")

        return "\n".join(description)

    @property
    def tower_height(self):
        return reduce(lambda m, r: max(m, r[1]), self.rock, 0) + 1

    def move_and_drop(self):
        self._move()
        self._drop()

    def _confirm_shift(self, new_position):
        if new_position.x < 0 or new_position.x > 7 - self.falling_rock.width or new_position.y < 0:
            return False

        if any(map(lambda pos: pos in self.rock, self.falling_rock.rock_positions(new_position))):
            return False

        self.falling_position = new_position
        return True

    def _move(self):
        move_symbol = next(self.moves)
        dx = -1 if move_symbol == "<" else 1
        self._confirm_shift(Point(self.falling_position.x + dx, self.falling_position.y))

    def _drop(self):
        confirmation = self._confirm_shift(Point(self.falling_position.x, self.falling_position.y - 1))
        if not confirmation:
            self.rock.update(self.falling_rock.rock_positions(self.falling_position))
            self.fallen += 1
            self.falling_rock = RockFormation(FORMATIONS[self.fallen % len(FORMATIONS)])
            self.falling_position = Point(2, self.tower_height + 3)


class Day17:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    def moves(self):
        index = 0
        while True:
            yield self.raw_input[0][index]
            index = (index + 1) % len(self.raw_input[0])

    def part1(self):
        print()
        print("Part 1")

        tetris = Tetris(self.moves())
        while tetris.fallen < 2022:
            tetris.move_and_drop()

        print(f"  Solution to part 1: {tetris.tower_height}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day17()
puzzle.part1()
puzzle.part2()

# 3066 too low
