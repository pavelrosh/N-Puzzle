def get_inversions(tiles, size):
    """
    Return number of inversions.
    """
    count = 0
    for i in range(size ** 2 - 1):
        for j in range(i, size ** 2):
            if tiles[i] and tiles[j] and tiles[i] > tiles[j]:
                count += 1
    return count


def if_odd(inversions):
    print(f"INVERSIONS: {inversions}")
    return True if inversions % 2 != 0 else False


def get_blank_row(puzzle, size):
    """
    Return row with 0-element.
    """
    for i, row in reversed(list(enumerate(puzzle))):
        if 0 in row:
            return size - i


def if_even(size, inversions, puzzle):
    """
    Checking for case of even amount of inversions.
    """
    blank_row = get_blank_row(puzzle, size)
    if (blank_row % 2 == 0 and inversions % 2 != 0) or (blank_row % 2 != 0 and inversions % 2 == 0):
        return True
    else:
        return False


def is_solvable(puzzle, size):
    """
    Check if puzzle is solvable.
    """
    tiles = [element for row in puzzle for element in row]
    inversions = get_inversions(tiles, size)
    return if_even(size, inversions, puzzle) if size % 2 == 0 else if_odd(inversions)
