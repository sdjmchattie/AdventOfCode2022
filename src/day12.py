from dataclasses import dataclass
from lib.file_access import read_input_lines
from copy import deepcopy


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class GridDijkstra:
    def __init__(self, grid, neighbour_predicate, start, end_func):
        self._grid = grid
        self._neighbour_predicate = neighbour_predicate
        self._start = start
        self._end_func = end_func

        self._max_x = len(self._grid[0]) - 1
        self._max_y = len(self._grid) - 1

    def run(self):
        unvisited = set()
        distance = {}
        get_neighbours = self._neighbour_func()

        unreachable = self._max_x * self._max_y + 1
        for x in range(self._max_x + 1):
            for y in range(self._max_y + 1):
                point = Point(x, y)
                unvisited.add(point)
                distance[point] = unreachable
        distance[self._start] = 0

        current = self._start
        while not self._end_func(current):
            neighbours = get_neighbours(current)
            unvisited_neighbours = filter(lambda point: point in unvisited, neighbours)

            for neighbour in unvisited_neighbours:
                new_distance = distance[current] + 1
                distance[neighbour] = min(distance[neighbour], new_distance)

            unvisited.remove(current)
            current = min(unvisited, key=lambda point: distance[point])

        return distance[current]

    def _neighbour_func(self):
        max_x = self._max_x
        max_y = self._max_y

        def neighbours(at_point):
            return set(
                filter(
                    lambda neighbour_point: self._neighbour_predicate(neighbour_point, at_point),
                    filter(
                        lambda point: point.x >= 0 and point.x <= max_x and point.y >= 0 and point.y <= max_y,
                        (
                            Point(at_point.x - 1, at_point.y),
                            Point(at_point.x + 1, at_point.y),
                            Point(at_point.x, at_point.y - 1),
                            Point(at_point.x, at_point.y + 1),
                        ),
                    ),
                )
            )

        return neighbours


class Day12:
    def __init__(self):
        self._raw_input = read_input_lines(__file__)

    def process_input(self):
        grid = []
        for y, line in enumerate(self._raw_input):
            grid.append([])
            for x, position in enumerate(line):
                if position == "S":
                    self._s_position = Point(x, y)
                    position = "a"

                if position == "E":
                    self._e_position = Point(x, y)
                    position = "z"

                grid[y].append(ord(position) - ord("a"))

        self._grid = grid

    def part1(self):
        djikstra = GridDijkstra(
            self._grid,
            lambda neighbour, source: self._grid[neighbour.y][neighbour.x] - self._grid[source.y][source.x] <= 1,
            self._s_position,
            lambda point: point == self._e_position,
        )
        path_length = djikstra.run()

        print()
        print("Part 1")
        print(f"  Solution to part 1: {path_length}")

    def part2(self):
        djikstra = GridDijkstra(
            self._grid,
            lambda neighbour, source: self._grid[source.y][source.x] - self._grid[neighbour.y][neighbour.x] <= 1,
            self._e_position,
            lambda point: self._grid[point.y][point.x] == 0,
        )
        path_length = djikstra.run()

        print()
        print("Part 2")
        print(f"  Solution to part 2: {path_length}")


puzzle = Day12()
puzzle.process_input()
puzzle.part1()
puzzle.part2()
