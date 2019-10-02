#! /usr/bin/python
import sys
from generator import make_goal, make_puzzle


class NPuzzleSearch:
    @staticmethod
    def make_matrix(source, size):
        matrix = []
        i = 0
        while i < len(source):
            matrix.append(source[i:i + size])
            i += size

        return matrix

    def generate_initial_state(self, size):
        source = make_puzzle(size, solvable=True, iterations=10000)
        matrix = self.make_matrix(source=source, size=size)
        return dict(puzzle=matrix, f_score=0)

    def generate_final_state(self, size):
        source = make_goal(size)
        matrix = self.make_matrix(source=source, size=size)
        return dict(puzzle=matrix, f_score=0)

    @staticmethod
    def swap_tiles(tile1, tile2, source):
        tmp = source[tile1[0]][tile1[1]]
        source[tile1[0]][tile1[1]] = source[tile2[0]][tile2[1]]
        source[tile2[0]][tile2[1]] = tmp

    @staticmethod
    def f_score(heuristic):
        pass

    @staticmethod
    def is_solvable(source):
        return True

    def generate_children(self, current_node):
        """
        Generate children nodes of current node.
        Add them to open_list
        :param current_node:
        :return:
        """
        pass

    def choose_next_node(self):
        """
        Calculate f(x) for each new generated node from open_list.
        Choose next node.
        :return: next node.
        """
        return

    @staticmethod
    def final_state_reached():
        return False

    def check_open_list(self):
        """
        Remove explored nodes.
        """
        print(self.open_list)


class ASearch(NPuzzleSearch):
    def __init__(self, size):
        """
        Format of node: {"puzzle": [[1,2,3],[1,2,3],[1,2,3]], "f_score": 8}
        """
        self.size = size
        self.initial_node = self.generate_initial_state(size=size)
        self.final_node = self.generate_final_state(size=size)
        self.open_list = [self.initial_node]
        self.closed_list = []

    def solver(self):
        current_node = dict(puzzle=self.initial_node, f_score=0)
        print(current_node)
        while self.final_state_reached():
            self.generate_children(current_node=current_node)
            self.closed_list.append(current_node)
            self.check_open_list()
            current_node = self.choose_next_node()
        else:
            print("FINAL STATE REACHED!")

    # def main(self):
    #     # check if solvable
    #     initial = self.generate_initial_state(size=self.size)
    #     if self.is_solvable(self.final):
    #         for i in initial:
    #             pattern = "{:^4}" * self.size
    #             print(pattern.format(*i))
    #         print('')
    #         for i in self.final:
    #             pattern = "{:^4}" * self.size
    #             print(pattern.format(*i))
    #     else:
    #         print("UNSOLVABLE")
    def __del__(self):
        print("Good By")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            assert int(sys.argv[-1]) > 2
        except:
            print("Size of puzzle must be more than 3")
            exit(1)
    else:
        print("Wrong number of parameters!")
        exit(1)

    a_search = ASearch(size=int(sys.argv[-1]))
    # a_search.()
