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

    def _exposed_faces_of_voxel(self, voxel):
        exposed_faces = 6
        for axis, value in enumerate(voxel):
            for delta in (-1, 1):
                adjacent = list(voxel)
                adjacent[axis] = value + delta
                if tuple(adjacent) in self._voxels:
                    exposed_faces -= 1

        return exposed_faces


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
        print(f"  Solution to part 2: ")


puzzle = Day18()
puzzle.part1()
puzzle.part2()
