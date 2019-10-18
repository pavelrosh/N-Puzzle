from n_puzzle import AStar, Greedy, Uniform
from is_solvable import is_solvable


def test(heuristic, size, times=10):
    print('*' * 20)
    print(f'Started test for {heuristic} with size {size}')
    for _ in range(times):
        search = AStar(size=size, heuristic=heuristic, filename=None, print_output=None)
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
    test(heuristic='misplaced', size=3, times=100)
    print("Have finished TEST recently!")

    test(heuristic='manhatten', size=3, times=100)
    print("Have finished TEST recently!")

    test(heuristic='euclidian', size=3, times=100)
    print("Have finished TEST recently!")