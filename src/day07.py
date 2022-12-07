import re

from lib.file_access import read_input_lines

REGEX_FILE_LISTING = re.compile(r"^(\d+) ")


class Directory:
    def __init__(self, name):
        self._name = name
        self._sub_directories = []
        self._file_sizes = []

    def add_directory(self, directory):
        self._sub_directories.append(directory)

    def add_file(self, size):
        self._file_sizes.append(size)

    def get_size(self):
        size = sum(self._file_sizes)

        for dir in self._sub_directories:
            size += dir.get_size()

        return size


class Day07:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def process_input(self):
        self.all_directories = set()
        self.current_directory = []
        for line in self.raw_input:
            if line == "$ cd ..":
                self.current_directory.pop()
            elif line[:5] == "$ cd ":
                new_directory = Directory(line[5:])
                self.all_directories.add(new_directory)

                if len(self.current_directory) > 0:
                    self.current_directory[-1].add_directory(new_directory)

                self.current_directory.append(new_directory)
            elif file_match := REGEX_FILE_LISTING.match(line):
                self.current_directory[-1].add_file(int(file_match.group(1)))

    def part1(self):
        dir_sizes = map(lambda dir: dir.get_size(), self.all_directories)

        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum([x for x in dir_sizes if x <= 100000])}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: ")


puzzle = Day07()
puzzle.part1()
puzzle.part2()
