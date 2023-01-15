from dataclasses import dataclass
from functools import cached_property
from methodtools import lru_cache
import re
from lib.file_access import read_input_lines

DESC_REGEX = re.compile(
    (
        r"Blueprint (\d+): "
        r"Each ore robot costs (\d+) ore. "
        r"Each clay robot costs (\d+) ore. "
        r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
        r"Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
)


@dataclass(frozen=True)
class ResourceCounts:
    ore: int
    clay: int
    obsidian: int
    geode: int

    def add(self, other):
        return ResourceCounts(
            self.ore + other.ore, self.clay + other.clay, self.obsidian + other.obsidian, self.geode + other.geode
        )

    def subtract(self, other):
        return ResourceCounts(
            self.ore - other.ore, self.clay - other.clay, self.obsidian - other.obsidian, self.geode - other.geode
        )

    def greater_than(self, other):
        subtracted = self.subtract(other)
        return subtracted.ore >= 0 and subtracted.clay >= 0 and subtracted.obsidian >= 0 and subtracted.geode >= 0


ADDITIONAL_ROBOT = {
    "ore": ResourceCounts(1, 0, 0, 0),
    "clay": ResourceCounts(0, 1, 0, 0),
    "obsidian": ResourceCounts(0, 0, 1, 0),
    "geode": ResourceCounts(0, 0, 0, 1),
}


def optimistic_max_resource(time_left, current_robots, current_resource):
    return current_resource + current_robots * time_left + time_left * (time_left - 1) / 2


class Blueprint:
    def __init__(self, desc):
        match = DESC_REGEX.match(desc)
        self.id = int(match.groups()[0])
        self.robot_costs = {
            "geode": ResourceCounts(int(match.groups()[5]), 0, int(match.groups()[6]), 0),
            "obsidian": ResourceCounts(int(match.groups()[3]), int(match.groups()[4]), 0, 0),
            "clay": ResourceCounts(int(match.groups()[2]), 0, 0, 0),
            "ore": ResourceCounts(int(match.groups()[1]), 0, 0, 0),
        }

    @property
    def most_ore_robots(self):
        return max([x.ore for x in self.robot_costs.values()])

    @property
    def most_clay_robots(self):
        return max([x.clay for x in self.robot_costs.values()])

    @property
    def most_obsidian_robots(self):
        return max([x.obsidian for x in self.robot_costs.values()])

    def optimal_geodes(self, alotted_time):
        optimal = self._optimal_geodes(alotted_time, ResourceCounts(1, 0, 0, 0), ResourceCounts(0, 0, 0, 0))
        print(f"Found optimal geode count {optimal} for blueprint with ID {self.id}")

        return optimal

    @lru_cache(maxsize=None)
    def _optimal_geodes(self, time_left, robot_counts, resource_counts):
        if time_left == 0:
            return resource_counts.geode

        buildable_robots = {
            name: costs for name, costs in self.robot_costs.items() if resource_counts.greater_than(costs)
        }

        if "ore" in buildable_robots and robot_counts.ore >= self.most_ore_robots:
            del buildable_robots["ore"]

        if "clay" in buildable_robots and robot_counts.clay >= self.most_clay_robots:
            del buildable_robots["clay"]

        if "obsidian" in buildable_robots and robot_counts.obsidian >= self.most_obsidian_robots:
            del buildable_robots["obsidian"]

        new_resources = resource_counts.add(robot_counts)

        time = time_left - 1

        if "geode" in buildable_robots:
            return self._optimal_geodes(
                time,
                robot_counts.add(ADDITIONAL_ROBOT["geode"], new_resources.subtract(buildable_robots["geode"])),
                resources,
            )

        max_geodes = 0
        for name, costs in buildable_robots.items():
            robots = robot_counts.add(ADDITIONAL_ROBOT[name])
            resources = new_resources.subtract(costs)

            if optimistic_max_resource(time, robots.geode, resources.geode) > max_geodes:
                max_geodes = max(max_geodes, self._optimal_geodes(time, robots, resources))

        if optimistic_max_resource(time, robot_counts.geode, new_resources.geode) > max_geodes:
            max_geodes = max(max_geodes, self._optimal_geodes(time, robot_counts, new_resources))

        return max_geodes


class Day19:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    def generate_blueprints(self):
        return [Blueprint(desc) for desc in self.raw_input]

    def part1(self):
        quality_levels = [bp.id * bp.optimal_geodes(24) for bp in self.generate_blueprints()]

        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum(quality_levels)}")

    def part2(self):
        geodes_in_32 = [bp.optimal_geodes(32) for bp in self.generate_blueprints()[0:3]]

        print()
        print("Part 2")
        print(f"  Solution to part 2: {geodes_in_32[0] * geodes_in_32[1] * geodes_in_32[2]}")


puzzle = Day19()
puzzle.part1()
puzzle.part2()
