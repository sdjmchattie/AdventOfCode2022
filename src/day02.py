from lib.file_access import read_input_lines

PART1_SCORE_MAP = {
    "A X": [1, 3],
    "A Y": [2, 6],
    "A Z": [3, 0],
    "B X": [1, 0],
    "B Y": [2, 3],
    "B Z": [3, 6],
    "C X": [1, 6],
    "C Y": [2, 0],
    "C Z": [3, 3],
}

PART2_SCORE_MAP = {
    "A X": [3, 0],
    "A Y": [1, 3],
    "A Z": [2, 6],
    "B X": [1, 0],
    "B Y": [2, 3],
    "B Z": [3, 6],
    "C X": [2, 0],
    "C Y": [3, 3],
    "C Z": [1, 6],
}


class Day02:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def process_input(self):
        self.part1_scores = list(map(lambda play: sum(PART1_SCORE_MAP[play]), self.raw_input))
        self.part2_scores = list(map(lambda play: sum(PART2_SCORE_MAP[play]), self.raw_input))

    def part1(self):
        print()
        print("Part 1")
        print(f"  Solution to part 1: {sum(self.part1_scores)}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: {sum(self.part2_scores)}")


puzzle = Day02()
puzzle.part1()
puzzle.part2()
