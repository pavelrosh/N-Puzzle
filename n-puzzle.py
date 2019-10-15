#! /usr/bin/python
from generator import make_goal, make_puzzle, Node
from termcolor import colored
from copy import deepcopy
from heuristic import Heuristic
from is_solvable import is_solvable
from time import time
import argparse
from parse_input_file import parse


class NPuzzleSearch:
    def __init__(self, size, heuristic, filename, print_output):
        self.open_list = []
        self.closed_list = []
        self.size = size
        self.nodes_in_open_list = len(self.open_list)
        self.number_of_nodes = 0
        self.final_node = self.generate_final_state(size=size)
        self.current_node = self.generate_initial_state(size=size, filename=filename)
        # self.current_node = Node(puzzle=[[3, 2, 6], [7, 0, 8], [1, 5, 4]])  # 0.3
        # self.current_node = Node(puzzle=[[0, 2, 3], [1, 4, 5], [8, 7, 6]])  # speed of light
        # self.current_node = Node(puzzle=[[4, 8, 3], [2, 0, 5], [6, 1, 7]])  # isn't solvable
        # self.current_node = Node(puzzle=[[7, 1, 2], [8, 0, 4], [5, 6, 3]])  # weird behavior, too long calculations
        # self.current_node = Node(puzzle=[[2,13,4,3], [14,8,10,9], [12,0,1,5], [15,6,7,11]])  # 4x4 solvable,
                                                                                             # 9.2 - manhatten,
                                                                                             # 7.2 - euclidian
        # print(self.current_node)
        self.open_list = [self.current_node]

        self.max_g = 0
        self.max_nodes_in_same_time = 1
        self.solution_history = [deepcopy(self.current_node)]
        self.heuristic = heuristic
        self.print_output = print_output
        self.start_time = time()

    @staticmethod
    def make_matrix(source, size):
        matrix = []
        i = 0
        while i < len(source):
            matrix.append(source[i:i + size])
            i += size

        return matrix

    def generate_initial_state(self, filename, size):
        if not filename:
            source = make_puzzle(size, solvable=True, iterations=10000)
            matrix = self.make_matrix(source=source, size=size)
        else:
            matrix = parse(filename)
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

        row = empty_till[0] + 1
        if self.size - row == self.size - 1:
            coordinates.append((empty_till[0] + 1, empty_till[1]))
        elif self.size - row > 0:
            coordinates.append((empty_till[0] + 1, empty_till[1]))
            coordinates.append((empty_till[0] - 1, empty_till[1]))
        elif self.size - row == 0:
            coordinates.append((empty_till[0] - 1, empty_till[1]))

        element = empty_till[1] + 1
        if self.size - element == self.size - 1:
            coordinates.append((empty_till[0], empty_till[1] + 1))
        elif self.size - element > 0:
            coordinates.append((empty_till[0], empty_till[1] + 1))
            coordinates.append((empty_till[0], empty_till[1] - 1))
        elif self.size - element == 0:
            coordinates.append((empty_till[0], empty_till[1] - 1))
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

        for coord in swap_coordinates:
            tmp = self.swap_tiles(swap_from=empty_till, swap_to=coord, node=node)
            tmp.g = node.g + 1
            self.open_list.append(tmp)
            self.nodes_in_open_list += 1

        self.max_nodes_in_same_time = (len(self.open_list) if len(self.open_list) > self.max_nodes_in_same_time
                                       else self.max_nodes_in_same_time)

    def get_f_score(self, h_score, node): pass

    def choose_next_node(self):
        """
        Calculate f(x) for each new generated node from open_list.
        Choose next node.
        :return: next node.
        """

        for node in self.open_list:
            heuristic = Heuristic(current_node=deepcopy(node), final_node=deepcopy(self.final_node),
                                  heuristic=self.heuristic)
            h_score = heuristic.calculate()
            node.h = h_score
            # print(h_score)
            node.f = self.get_f_score(h_score, node)
            # print(node.f, h_score)

        # sort list of node by f-score, from higher to lower.
        list_of_equal_nodes = deepcopy(self.open_list)
        list_of_equal_nodes.sort(key=lambda x: x.f)

        if len(list_of_equal_nodes) > 1 and list_of_equal_nodes[0].f == list_of_equal_nodes[1].f:
            return [node for node in list_of_equal_nodes if node.f == list_of_equal_nodes[0].f]
        else:
            self.solution_history.append(deepcopy(list_of_equal_nodes[0]))
            return list_of_equal_nodes[0]

    def is_goal(self, current_node):
        return True if type(current_node) is not list and current_node == self.final_node else False

    def check_open_list(self):
        """
        Remove explored nodes.
        """
        for node in self.closed_list:
            if node in self.open_list:
                self.open_list.remove(node)

        # TODO some bug occurred below, probably need to check.
        self.max_g = max([node.g for node in self.open_list])
        for node in self.open_list:
            if node.g < self.max_g:
                self.open_list.remove(node)

    def print_puzzle(self, node, color='yellow'):
        # print(f"f-score: {node.f}\tg-score: {node.g}")
        # print(colored('*' * self.size * 4, 'red'))
        for i in node.puzzle:
            print(colored(("{:^4}" * self.size).format(*i), color))
        print(colored('*' * self.size * 4, 'red'))

    def print_metrics(self):
        print(f"Calculation time: {round(time() - self.start_time, 1)} second(s)")
        print(f"Number of moves: {len(self.closed_list)}")
        print(len(self.solution_history))
        print(f"Nodes appeared in open list(Complexity in time): {self.nodes_in_open_list}")
        print(f"Maximum number of nodes in same time(Complexity in size): {self.max_nodes_in_same_time}")
        if self.print_output:
            print(f"Solution history:")
            for i in self.solution_history:
                self.print_puzzle(i)

    def solver(self):
        while not self.is_goal(self.current_node):
            if type(self.current_node) is list:
                """
                Check if there more than one child nodes with equal h-score.
                """
                list_of_equal_nodes = deepcopy(self.current_node)
                for node in list_of_equal_nodes:
                    if self.is_goal(node):
                        self.solution_history.append(node)
                        print("SUCCESS")
                        self.print_metrics()
                        exit()
                    else:
                        self.generate_children(current_node=node)
                        self.closed_list.append(node)
                        self.check_open_list()
                self.current_node = self.choose_next_node()
            else:
                self.generate_children(current_node=self.current_node)
                self.closed_list.append(self.current_node)
                self.check_open_list()
                self.current_node = self.choose_next_node()
        else:
            print("FINAL STATE REACHED!")
            self.print_metrics()


class AStar(NPuzzleSearch):
    def __init__(self, size, heuristic, filename, print_output):
        super().__init__(size, heuristic, filename, print_output)
        print(f'Algorithm: {self.__class__.__name__}')
        print(f'Heuristic: {heuristic}')

    def get_f_score(self, h_score, node): return node.g + h_score


class Greedy(NPuzzleSearch):
    def __init__(self, size, heuristic, filename, print_output):
        super().__init__(size, heuristic, filename, print_output)
        print(f'Algorithm: {self.__class__.__name__}')
        print(f'Heuristic: {heuristic}')

    def get_f_score(self, h_score, node): return h_score


class Uniform(NPuzzleSearch):
    def __init__(self, size, heuristic, filename, print_output):
        super().__init__(size, heuristic, filename, print_output)
        print(f'Algorithm: {self.__class__.__name__}')

    def get_f_score(self, h_score, node): return node.g


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("size", type=int, help="Size of the puzzle's side. Must be >3.", default=3)
    parser.add_argument("--heuristic", type=str, help="Choose your heuristic function(mispaced, manhatten, euclidian)"
                        , default='manhatten')
    parser.add_argument('-g', "--generator", action='store_true')
    parser.add_argument('-f', '--file', type=str)
    parser.add_argument('-a', '--algorithm', default='a', help="Choose between a, greedy, uniform")
    parser.add_argument('-p', '--print', action='store_true')
    args = parser.parse_args()

    if args.size > 2:
        if not args.generator:
            if args.file:
                filename = args.file
            else:
                filename = None
        else:
            filename = None
        print_output = args.print
        if args.algorithm == 'a':
            algorithm = AStar(size=args.size, heuristic=args.heuristic, filename=filename, print_output=print_output)
        elif args.algorithm == 'greedy':
            algorithm = Greedy(size=args.size, heuristic=args.heuristic, filename=filename, print_output=print_output)
        elif args.algorithm == 'uniform':
            algorithm = Uniform(size=args.size, heuristic=args.heuristic, filename=filename, print_output=print_output)
        else:
            print("Wrong algorithm name!")
            exit()

        if is_solvable(puzzle=algorithm.current_node.puzzle, size=algorithm.size):
            print("Puzzle is SOLVABLE!")
            try:
                algorithm.solver()
            except KeyboardInterrupt:
                print("Aborted manually")
        else:
            print("Puzzle isn't SOLVABLE!")
    else:
        print("wring size of puzzle!")
