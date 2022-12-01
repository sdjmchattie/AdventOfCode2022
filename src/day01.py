from lib.file_access import read_input_lines


class Day01:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def process_input(self):
        inventories = [[]]
        for item in self.raw_input:
            try:
                inventories[-1].append(int(item))
            except ValueError:
                inventories.append([])

        self.elves = list(reversed(sorted(map(lambda elf: sum(elf), inventories))))

    def part1(self):
        print()
        print("Part 1")
        print(f"  Solution to part 1: {self.elves[0]}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: {sum(self.elves[0:3])}")


puzzle = Day01()
puzzle.part1()
puzzle.part2()
