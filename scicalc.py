"""Scientific calculator in Python

Author: Juan Luis Cano Rodríguez <juanlu001@gmail.com>

"""

def tokenize(line):
    """Tokenizes a line of input.

    """
    return list(line.replace(" ", ""))


def main():
    """Main Read - Eval - Print - Loop.

    """
    while True:
        try:
            line = input("> ")
            print(line)
        except EOFError:
            break


if __name__ == '__main__':
    main()
