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
        @lru_cache(maxsize=None)
        def best_relief(valves, opened, time_left):
            if time_left <= 0:
                return 0

            relief_if_1_opened = 0 if valves[0].name in opened else valves[0].flow_rate * (time_left - 1)
            relief_if_2_opened = 0 if valves[1].name in opened or valves[0] == valves[1] else valves[1].flow_rate * (time_left - 1)

            moves_1 = valves[0].adjacent + ((valves[0].name,) if relief_if_1_opened > 0 else ())
            moves_2 = valves[1].adjacent + ((valves[1].name,) if relief_if_2_opened > 0 else ())
            move_combos = ((move_1, move_2) for move_1 in moves_1 for move_2 in moves_2)

            max_relief = 0
            for new_valve_names in move_combos:
                new_relief = 0
                newly_opened_1 = ()
                if valves[0].name == new_valve_names[0]:
                    newly_opened_1 = (new_valve_names[0],)
                    new_relief += relief_if_1_opened

                newly_opened_2 = ()
                if valves[1].name == new_valve_names[1]:
                    newly_opened_2 = (new_valve_names[1],)
                    new_relief += relief_if_2_opened

                new_valves = tuple(map(lambda valve: self._valves[valve], new_valve_names))
                new_opened = tuple(sorted(opened + newly_opened_1 + newly_opened_2))

                max_relief = max(max_relief, new_relief + best_relief(new_valves, new_opened, time_left - 1))

            return max_relief

        print()
        print("Part 2")

        best = best_relief((self._valves["AA"], self._valves["AA"]), (), 26)

        print(f"  Solution to part 2: {best}")


puzzle = Day16()
puzzle.process_input()
puzzle.part1()
puzzle.part2()
