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
        """
        :param tile1: [0, 1]
        :param tile2: [0, 2]
        :param source: puzzle
        :return:
        """
        tmp = source[tile1[0]][tile1[1]]
        source[tile1[0]][tile1[1]] = source[tile2[0]][tile2[1]]
        source[tile2[0]][tile2[1]] = tmp


    def get_coordinate_of_empty_till(self, node):
        empty_till = []
        coordinates = []
        for row in range(len(node)):
            if 0 in node[row]:
                 empty_till = [row, node[row].index(0)]

        if empty_till:
            if empty_till[0]

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
        node = current_node['puzzle'].copy()
        empty_till_coordinate = self.get_coordinate_of_empty_till(current_node['puzzle'])
        print(empty_till_coordinate)
        # self.swap_tiles(empty_till_coordinate, )
        exit()
        # tmp = self.swap_tiles()

    def choose_next_node(self):
        """
        Calculate f(x) for each new generated node from open_list.
        Choose next node.
        :return: next node.
        """
        return

    def final_state_reached(self, current_node):
        return True if current_node['puzzle'] == self.final_node['puzzle'] else False

    def check_open_list(self):
        """
        Remove explored nodes.
        """
        print(self.open_list)

    def print_puzzle(self, node):
        # pattern = "{:^4}" * self.size
        for i in node['puzzle']:
            print(("{:^4}" * self.size).format(*i))
        print('')


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
        # self.print_puzzle(self.initial_node)
        # self.print_puzzle(self.final_node)
        current_node = self.initial_node.copy()

        # self.print_puzzle(current_node)
        while not self.final_state_reached(current_node):
            self.print_puzzle(node=current_node)
            self.generate_children(current_node=current_node)
            # self.closed_list.append(current_node)
            # self.check_open_list()
            # current_node = self.choose_next_node()
        # else:
        #     print("FINAL STATE REACHED!")

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
    a_search.solver()
