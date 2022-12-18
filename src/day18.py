from functools import cached_property
from lib.file_access import read_input_lines
import re

REGEX_INPUT_LINE = re.compile(r"^(\d+),(\d+),(\d+)$")


class Model3D:
    def __init__(self, voxels):
        self._voxels = voxels

    @cached_property
    def exposed_surface_area(self):
        return sum(map(lambda voxel: self._exposed_faces_of_voxel(voxel), self._voxels))

    @cached_property
    def exterior_surface_area(self):
        return self._surface_area_by_flood_fill()

    def _exposed_faces_of_voxel(self, voxel):
        exposed_faces = 6
        for axis, value in enumerate(voxel):
            for delta in (-1, 1):
                adjacent = list(voxel)
                adjacent[axis] = value + delta
                if tuple(adjacent) in self._voxels:
                    exposed_faces -= 1

        return exposed_faces

    def _surface_area_by_flood_fill(self):
        surface_area = 0
        to_visit = {(-1, -1, -1)}
        visited = set()

        while len(to_visit) > 0:
            visiting = to_visit.pop()
            visited.add(visiting)

            # Get all 6 adjacent voxels
            adjacent = []
            for axis, value in enumerate(visiting):
                for delta in (-1, 1):
                    new_adjacent = list(visiting)
                    new_adjacent[axis] = value + delta
                    adjacent.append(tuple(new_adjacent))

            # Remove out of bounds voxels
            adjacent = set(
                filter(
                    lambda a: a[0] >= -1 and a[1] >= -1 and a[2] >= -1 and a[0] <= 20 and a[1] <= 20 and a[2] <= 20,
                    adjacent,
                )
            )

            model_adjacent = self._voxels.intersection(adjacent)
            surface_area += len(model_adjacent)
            to_visit.update(adjacent.difference(visited).difference(model_adjacent))

        return surface_area


class Day18:
    @cached_property
    def raw_input(self):
        return read_input_lines(__file__)

    @cached_property
    def voxels(self):
        return set(map(lambda line: tuple(map(int, REGEX_INPUT_LINE.match(line).groups())), self.raw_input))

    def part1(self):
        print()
        print("Part 1")

        model = Model3D(self.voxels)

        print(f"  Solution to part 1: {model.exposed_surface_area}")

    def part2(self):
        print()
        print("Part 2")

        model = Model3D(self.voxels)

        print(f"  Solution to part 2: {model.exterior_surface_area}")


puzzle = Day18()
puzzle.part1()
puzzle.part2()
