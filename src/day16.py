import re
from dataclasses import dataclass
from functools import cached_property, lru_cache
from typing import Tuple

from lib.file_access import read_input_lines

REGEX_INPUT_LINE = re.compile(r"^Valve ([A-Z]+).+flow rate=(\d+).+to valves? (.+)$")


@dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    adjacent: Tuple[str]


class Day16:
    @cached_property
    def valves(self):
        input_vals = (REGEX_INPUT_LINE.match(line).groups() for line in read_input_lines(__file__))
        return {
            name: Valve(name, int(flow_rate), tuple(map(lambda adj: adj.strip(), adjacent.split(","))))
            for name, flow_rate, adjacent in input_vals
        }

    @cached_property
    def flowable_valves(self):
        return tuple(valve.name for valve in self.valves.values() if valve.flow_rate > 0)

    @lru_cache(maxsize=None)
    def distance_between(self, start, end, visited=()):
        if end == start:
            return 0

        shortest = 10000
        for adjacent in self.valves[start].adjacent:
            if adjacent in visited:
                continue

            shortest = min(shortest, 1 + self.distance_between(adjacent, end, tuple(sorted(visited + (adjacent,)))))

        return shortest

    def all_paths_from(self, start, time, visited=set()):
        """
        Gives all possible paths from a starting point, until time is up,
        opening valves at each point along the path."""
        if time <= 2:
            yield (start,)

        for next_valve in self.flowable_valves:
            if next_valve in visited or next_valve == start:
                continue

            distance = self.distance_between(start, next_valve)
            time_left_after_opening_valve = time - distance - 1
            if time_left_after_opening_valve >= 1:
                for path in self.all_paths_from(next_valve, time_left_after_opening_valve, visited.union({start})):
                    yield (start,) + path

    def relief_from_path(self, path, time):
        relief = 0
        for prev, next in zip(path[:-1], path[1:]):
            time -= self.distance_between(prev, next) + 1
            relief += self.valves[next].flow_rate * time

        return relief

    def part1(self):
        print()
        print("Part 1")

        best = max(self.relief_from_path(path, 30) for path in self.all_paths_from("AA", 30))

        print(f"  Solution to part 1: {best}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day16()
puzzle.part1()
puzzle.part2()
