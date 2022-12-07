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
        all_directories = set()
        current_directory = []
        for line in self.raw_input:
            if line == "$ cd ..":
                current_directory.pop()
            elif line[:5] == "$ cd ":
                new_directory = Directory(line[5:])
                all_directories.add(new_directory)

                if len(current_directory) > 0:
                    current_directory[-1].add_directory(new_directory)

                current_directory.append(new_directory)
            elif file_match := REGEX_FILE_LISTING.match(line):
                current_directory[-1].add_file(int(file_match.group(1)))

        self.dir_sizes = list(map(lambda dir: dir.get_size(), all_directories))

    def part1(self):

        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum([x for x in self.dir_sizes if x <= 100000])}")

    def part2(self):
        total_space = max(self.dir_sizes)
        free_space = 70000000 - total_space
        needed_space = 30000000 - free_space
        chosen_directory_size = min([x for x in self.dir_sizes if x >= needed_space])

        print()
        print("Part 2")
        print(f"  Solution to part 2: {chosen_directory_size}")


puzzle = Day07()
puzzle.part1()
puzzle.part2()
