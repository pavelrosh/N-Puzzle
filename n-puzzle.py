#! /usr/bin/python
import sys
from generator import make_goal, make_puzzle, Node
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
        return Node(puzzle=matrix)

    def generate_final_state(self, size):
        source = make_goal(size)
        matrix = self.make_matrix(source=source, size=size)
        return Node(puzzle=matrix)

    @staticmethod
    def swap_tiles(swap_from, swap_to, node):
        node_copy = deepcopy(node)
        tmp = node_copy.puzzle[swap_from[0]][swap_from[1]]
        node_copy.puzzle[swap_from[0]][swap_from[1]] = node_copy.puzzle[swap_to[0]][swap_to[1]]
        node_copy.puzzle[swap_to[0]][swap_to[1]] = tmp

        return node_copy

    def get_coordinate_of_empty_till(self, node):
        empty_till = []
        coordinates = []
        for row in range(len(node.puzzle)):
            if 0 in node.puzzle[row]:
                empty_till = [row, node.puzzle[row].index(0)]

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
        node = deepcopy(current_node)
        swap_coordinates, empty_till = self.get_coordinate_of_empty_till(current_node)
        # print(swap_coordinates, empty_till)
        for coord in swap_coordinates:
            # print(empty_till, coord)
            tmp = self.swap_tiles(swap_from=empty_till, swap_to=coord, node=node)
            print(tmp)
            tmp.g = node.g + 1
            self.open_list.append(tmp)

    def choose_next_node(self):
        """
        Calculate f(x) for each new generated node from open_list.
        Choose next node.
        :return: next node.
        """

        for node in self.open_list:
            heuristic = Heuristic(current_node=deepcopy(node), final_node=deepcopy(self.final_node))
            h_score = heuristic.misplaced()
            node.h = h_score
            node.f = node.g + h_score

        # sort list of node by f-score, from higher to lower.
        self.open_list.sort(key=lambda x: x.f)
        print(self.open_list)
        # if there maximum f-score return node, else return list of nodes with highest f-score.
        if self.open_list[0].f == self.open_list[1].f:
            list_of_equal_nodes = [node for node in self.open_list if node.f == self.open_list[0].f]
            print(f"LIST: {list_of_equal_nodes}")
            return list_of_equal_nodes
        else:
            print("NE LIST")
            return self.open_list[0]

    def is_goal(self, current_node):
        # if type(current_node) is not list:
        return True if type(current_node) is not list and current_node == self.final_node else False

    def check_open_list(self):
        """
        Remove explored nodes.
        """
        for node in self.closed_list:
            if node in self.open_list:
                self.open_list.remove(node)

    def print_puzzle(self, node, color='yellow'):
        print(colored('*' * self.size * 4, 'red'))
        for i in node.puzzle:
            print(colored(("{:^4}" * self.size).format(*i), color))
        print(colored('*' * self.size * 4, 'red'))


class ASearch(NPuzzleSearch):
    def __init__(self, size):
        """
        Format of node: {"puzzle": [[1,2,3],[1,2,3],[1,2,3]], "f_score": 8}
        """
        self.size = size
        self.final_node = self.generate_final_state(size=size)
        self.open_list = []
        self.closed_list = []
        # self.current_node = self.generate_initial_state(size=self.size)
        self.current_node = Node(puzzle=[[0, 2, 3], [1,4,5], [8,7,6]])
        self.open_list = [self.current_node]

    def solver(self):
        while not self.is_goal(self.current_node):
            if type(self.current_node) is list:
                print("MANY CHILD WITH EQUAL f-score")
                """
                Check if there more than one child nodes with equal h-score.
                """
                list_of_equal_nodes = deepcopy(self.current_node)
                for node in list_of_equal_nodes:
                    if self.is_goal(node):
                        print("SUCCESS")
                        exit()
                    else:
                        # print(f"LEN of nodes list: {list_of_equal_nodes}")
                        self.print_puzzle(node=node)
                        self.generate_children(current_node=node)
                        # print("OPEN LIST", self.open_list)
                        self.closed_list.append(node)
                        # print("CLOSED LIST", self.closed_list)
                        self.check_open_list()
                        # print("OPEN LIST AFTER REMOVING", self.open_list)
                self.current_node = self.choose_next_node()
                print(self.current_node)
            else:
                print("SINGLE CHILD")
                self.print_puzzle(node=self.current_node)
                self.generate_children(current_node=self.current_node)
                # print(f"OPEN LIST: {self.open_list}")
                self.closed_list.append(self.current_node)
                # print(f"CLOSED_LIST: {self.closed_list}")
                self.check_open_list()
                # print("OPEN LIST", self.open_list)
                # print(self.open_list)
                self.current_node = self.choose_next_node()
        else:
            print("FINAL STATE REACHED!")

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
    # init_puzzle = a_search.generate_initial_state(size=a_search.size)
    # if is_solvable(puzzle=init_puzzle.puzzle, size=a_search.size):
    #     print("Puzzle is SOLVABLE!")
    a_search.solver()
    # else:
    #     print("Puzzle isn't SOLVABLE!")
