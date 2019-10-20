from is_solvable import is_solvable
from n_puzzle import AStar, Greedy, Uniform


def testAstar(heuristic, size, times=10):
    print('*' * 20)
    print(f'Started test for {heuristic} with size {size}')
    for _ in range(times):
        search = AStar(size=size, heuristic=heuristic, filename=None, print_output=True)
        print(search.current_node)
        if is_solvable(puzzle=search.current_node.puzzle, size=search.size):
            try:
                search.solver()
                print()
            except SystemExit:
                print()
                continue
        else:
            raise Exception("is'n solvable")


def testGreedy(heuristic, size, times=10):
    print('*' * 20)
    print(f'Started test for {heuristic} with size {size}')
    for _ in range(times):
        search = Greedy(size=size, heuristic=heuristic, filename=None, print_output=None)
        print(search.current_node)
        if is_solvable(puzzle=search.current_node.puzzle, size=search.size):
            try:
                search.solver()
                print()
            except SystemExit:
                print()
                continue
        else:
            raise Exception("is'n solvable")


def testUniform(heuristic, size, times=10):
    print('*' * 20)
    print(f'Started test for with size {size}')
    for _ in range(times):
        search = Uniform(size=size, heuristic=heuristic, filename=None, print_output=None)
        print(search.current_node)
        if is_solvable(puzzle=search.current_node.puzzle, size=search.size):
            try:
                search.solver()
                print()
            except SystemExit:
                print()
                continue
        else:
            raise Exception("is'n solvable")


if __name__ == "__main__":
    testAstar(heuristic='manhatten', size=3, times=100)
    print("Have finished TEST recently!")
    #
    # testAstar(heuristic='manhatten', size=3, times=100)
    # print("Have finished TEST recently!")
    #
    # testAstar(heuristic='euclidian', size=3, times=100)
    # print("Have finished TEST recently!")
    #
    # testGreedy(heuristic='misplaced', size=3, times=10)
    # print("Have finished TEST recently!")
    #
    # testGreedy(heuristic='manhatten', size=3, times=100)
    # print("Have finished TEST recently!")
    #
    # testGreedy(heuristic='euclidian', size=3, times=100)
    # print("Have finished TEST recently!")
    #
    # testUniform(heuristic='euclidian', size=3, times=10)
    # print("Have finished TEST recently!")
