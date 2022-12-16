import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple

from lib.file_access import read_input_lines

REGEX_INPUT_LINE = re.compile(r'^Valve ([A-Z]+).+flow rate=(\d+).+to valves? (.+)$')

@dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    adjacent: Tuple[str]

class Day16:
    def __init__(self):
        self._raw_input = read_input_lines(__file__)

    def process_input(self):
        input_vals = (REGEX_INPUT_LINE.match(line).groups() for line in self._raw_input)
        self._valves = {
            name: Valve(name, int(flow_rate), tuple(map(lambda adj: adj.strip(), adjacent.split(','))))
            for name, flow_rate, adjacent in input_vals
        }

    def part1(self):
        @lru_cache(maxsize=None)
        def best_relief(valve, opened, time_left):
            if time_left <= 0:
                return 0

            max_relief = 0
            opened_plus_this_valve = tuple(sorted(opened + (valve.name,)))
            relief_if_opened = 0 if valve.name in opened else valve.flow_rate * (time_left - 1)

            for adjacent in valve.adjacent:
                # Test the path where we open this valve
                if relief_if_opened != 0: # but only if it provides any relief
                    max_relief = max(
                        max_relief,
                        relief_if_opened + best_relief(self._valves[adjacent], opened_plus_this_valve, time_left - 2)
                    )

                # Test the path where we just move on without opening this valve
                max_relief = max(max_relief, best_relief(self._valves[adjacent], opened, time_left - 1))

            return max_relief

        print()
        print("Part 1")

        best = best_relief(self._valves["AA"], (), 30)

        print(f"  Solution to part 1: {best}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day16()
puzzle.process_input()
puzzle.part1()
puzzle.part2()
