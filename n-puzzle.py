#! /usr/bin/python
import sys
from generator import make_goal, make_puzzle
from termcolor import colored
from copy import deepcopy
from heuristic import Heuristic
from is_solvable import is_solvable


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
        return dict(puzzle=matrix)

    def generate_final_state(self, size):
        source = make_goal(size)
        matrix = self.make_matrix(source=source, size=size)
        return dict(puzzle=matrix)

    @staticmethod
    def swap_tiles(swap_from, swap_to, node):
        node_copy = deepcopy(node)
        tmp = node_copy[swap_from[0]][swap_from[1]]
        node_copy[swap_from[0]][swap_from[1]] = node_copy[swap_to[0]][swap_to[1]]
        node_copy[swap_to[0]][swap_to[1]] = tmp

        return node_copy

    def get_coordinate_of_empty_till(self, node):
        empty_till = []
        coordinates = []
        for row in range(len(node)):
            if 0 in node[row]:
                empty_till = [row, node[row].index(0)]

        # print("BEFORE", empty_till)
        row = empty_till[0] + 1
        if self.size - row == self.size - 1:
            # print('down')
            coordinates.append((empty_till[0] + 1, empty_till[1]))
        elif self.size - row > 0:
            # print("up&down")
            coordinates.append((empty_till[0] + 1, empty_till[1]))
            coordinates.append((empty_till[0] - 1, empty_till[1]))
        elif self.size - row == 0:
            # print('up')
            coordinates.append((empty_till[0] - 1, empty_till[1]))

        element = empty_till[1] + 1
        if self.size - element == self.size - 1:
            # print('right')
            coordinates.append((empty_till[0], empty_till[1] + 1))
        elif self.size - element > 0:
            # print('left&right')
            coordinates.append((empty_till[0], empty_till[1] + 1))
            coordinates.append((empty_till[0], empty_till[1] - 1))
        elif self.size - element == 0:
            # print('left')
            coordinates.append((empty_till[0], empty_till[1] - 1))
        # print("AFTER", empty_till)
        return coordinates, empty_till

    def generate_children(self, current_node):
        """
        Generate children nodes of current node.
        Add them to open_list
        :param current_node:
        :return:
        """
        node = deepcopy(current_node['puzzle'])
        swap_coordinates, empty_till = self.get_coordinate_of_empty_till(current_node['puzzle'])
        # print(swap_coordinates, empty_till)
        for coord in swap_coordinates:
            # print(empty_till, coord)
            tmp = self.swap_tiles(swap_from=empty_till, swap_to=coord, node=node)
            self.open_list.append(dict(puzzle=tmp))
            # self.print_puzzle(dict(puzzle=tmp))

    def choose_next_node(self):
        """
        Calculate f(x) for each new generated node from open_list.
        Choose next node.
        :return: next node.
        """
        # check node with same f(x)

        for node in self.open_list:
            heuristic = Heuristic(current_node=deepcopy(node['puzzle']), final_node=deepcopy(self.final_node['puzzle']))
            h_score = heuristic.misplaced()
            print(h_score)
            node['f_score'] = self.calculate_f_score(h_score)

        self.open_list.sort(key=lambda x: x['f_score'], reverse=True)
        print(self.open_list)



    def final_state_reached(self, current_node):
        return True if current_node['puzzle'] == self.final_node['puzzle'] else False

    def check_open_list(self):
        """
        Remove explored nodes.
        """
        for node in self.closed_list:
            self.open_list.remove(node)

    def print_puzzle(self, node, color='yellow'):
        # pattern = "{:^4}" * self.size
        for i in node['puzzle']:
            print(colored(("{:^4}" * self.size).format(*i), color))
        print(colored('*' * self.size * 4, 'red'))

    def calculate_f_score(self, h_score): return len(self.closed_list) - 1 + h_score


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
        current_node = deepcopy(self.initial_node)

        while not self.final_state_reached(current_node):
            self.print_puzzle(node=current_node)
            self.generate_children(current_node=current_node)
            # print(self.open_list)
            self.closed_list.append(current_node)
            # print(self.closed_list)
            self.check_open_list()
            # print(self.open_list)

            current_node = self.choose_next_node()
            break
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
    if is_solvable(puzzle=a_search.final_node['puzzle'], size=a_search.size):
        print("Puzzle is SOLVABLE!")
        a_search.solver()
    else:
        print("Puzzle isn't SOLVABLE!")
