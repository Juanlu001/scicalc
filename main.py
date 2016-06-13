"""Scientific calculator in Python

Author: Juan Luis Cano Rodríguez <juanlu001@gmail.com>

"""
from scicalc.parse import parse


def main():
    """Main Read - Eval - Print - Loop.

    """
    while True:
        try:
            line = input("> ")
            print(parse(line))
        except SyntaxError as e:
            print(e)
        except EOFError:
            break


if __name__ == '__main__':
    main()
