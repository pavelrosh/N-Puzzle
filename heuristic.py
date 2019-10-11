from numpy import array, where
from math import sqrt


class Heuristic:
    def __init__(self, current_node, final_node):
        self.current_node = current_node
        self.final_node = final_node
        self.size = len(current_node.puzzle)

    def misplaced(self):
        current = [y for x in self.current_node.puzzle for y in x]
        final = [y for x in self.final_node.puzzle for y in x]
        h_score = 0
        i = 0
        while i < len(current):
            if current[i] != final[i] and current[i] != 0:
                h_score += 1
            i += 1

        return h_score

    @staticmethod
    def get_coordinates(puzzle, item):
        arr = array(puzzle)
        return int(where(arr == item)[0]), int(where(arr == item)[1])

    def manhatten(self):
        h_score = 0

        for x in range(self.size):
            for y in range(self.size):
                x_goal, y_goal = self.get_coordinates(puzzle=self.final_node.puzzle, item=self.current_node.puzzle[x][y])
                dx, dy = abs(x_goal - x), abs(y_goal - y)
                h_score += dx + dy

        return h_score

    def euclidean(self):
        h = 0
        for x in range(self.size):
            for y in range(self.size):
                x_goal, y_goal = self.get_coordinates(puzzle=self.final_node.puzzle, item=self.current_node.puzzle[x][y])
                dx, dy = abs(x_goal - x), abs(y_goal - y)
                h += sqrt(dx * dx + dy * dy)

        return h

    # def euclidean_squared(self):
    #     from math import sqrt
    #     h = 0
    #     for x in range(self.size):
    #         for y in range(self.size):
    #             x_goal, y_goal = self.get_coordinates(puzzle=self.final_node.puzzle, item=self.current_node.puzzle[x][y])
    #             dx, dy = abs(x_goal - x), abs(y_goal - y)
    #             h += (dx * dx + dy * dy)
    #     return h
