from lib.file_access import read_input_lines


class Day06:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def process_input(self):
        self.signal = self.raw_input[0]

    def first_unique_marker(self, marker_size):
        marker = marker_size
        while len(set(self.signal[marker - marker_size : marker])) != marker_size:
            marker += 1

        return marker

    def part1(self):
        print()
        print("Part 1")
        print(f"  Solution to part 1: {self.first_unique_marker(4)}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: {self.first_unique_marker(14)}")


puzzle = Day06()
puzzle.part1()
puzzle.part2()
