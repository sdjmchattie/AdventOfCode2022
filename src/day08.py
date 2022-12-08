from lib.file_access import read_input_lines

HEIGHT = "height"
NORTH = "north"
SOUTH = "south"
EAST = "east"
WEST = "west"


class Day08:
    def __init__(self):
        self.raw_input = read_input_lines(__file__)
        self.process_input()

    def process_input(self):
        self.forest = []

        numeric_input = list(map(lambda row: list(map(int, row)), self.raw_input))

        for y in range(0, len(numeric_input)):
            row = numeric_input[y]
            for x in range(0, len(row)):
                self.forest.append(
                    {
                        HEIGHT: row[x],
                        NORTH: list(reversed(list(map(lambda r: r[x], numeric_input[:y])))),
                        SOUTH: list(map(lambda r: r[x], numeric_input[y + 1 :])),
                        EAST: row[x + 1 :],
                        WEST: list(reversed(row[:x])),
                    }
                )

    def visible_tree_count(self):
        def tree_is_visible(tree):
            return (
                len(tree[NORTH]) == 0
                or len(tree[SOUTH]) == 0
                or len(tree[EAST]) == 0
                or len(tree[WEST]) == 0
                or max(tree[NORTH]) < tree[HEIGHT]
                or max(tree[SOUTH]) < tree[HEIGHT]
                or max(tree[EAST]) < tree[HEIGHT]
                or max(tree[WEST]) < tree[HEIGHT]
            )

        return len([tree for tree in self.forest if tree_is_visible(tree)])

    def max_scenic_score(self):
        def visible_range(trees, max_height):
            return next((i + 1 for i, e in enumerate(trees) if e >= max_height), len(trees))

        def scenic_score(tree):
            north_range = visible_range(tree[NORTH], tree[HEIGHT])
            south_range = visible_range(tree[SOUTH], tree[HEIGHT])
            east_range = visible_range(tree[EAST], tree[HEIGHT])
            west_range = visible_range(tree[WEST], tree[HEIGHT])

            return north_range * south_range * east_range * west_range

        return max(map(scenic_score, self.forest))

    def part1(self):
        print()
        print("Part 1")
        print(f"  Solution to part 1: {self.visible_tree_count()}")

    def part2(self):
        print()
        print("Part 2")
        print(f"  Solution to part 2: {self.max_scenic_score()}")


puzzle = Day08()
puzzle.part1()
puzzle.part2()
