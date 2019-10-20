from config import PATH_TO_MAPS


def clean_file(filename):
    try:
        source = [line.split('#', 1)[0].split() for line in open(file=PATH_TO_MAPS + filename, mode='r')]
        source = [line for line in source if len(line) > 0]
        return source
    except FileNotFoundError:
        print("File not found!")
        exit()


def parse(filename):
    cleaned = clean_file(filename)
    puzzle = []
    if 0 < len(cleaned[0][0]) < 3 and cleaned[0][0].isdigit():
        size = int(cleaned[0][0])
        cleaned.pop(0)
        for row in cleaned:
            if len(row) == size:
                try:
                    puzzle.append([int(i) for i in row])
                except ValueError:
                    print("Invalid input")
                    exit()
            else:
                print("Invalid input")
                exit()
        return puzzle
    else:
        print("Invalid input")
        exit()


if __name__ == "__main__":
    print(parse(filename='not_valid_file'))
