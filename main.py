"""Scientific calculator in Python

Author: Juan Luis Cano Rodríguez <juanlu001@gmail.com>

"""
from scicalc.evaluate import evaluate


def main():
    """Main Read - Eval - Print - Loop.

    """
    while True:
        try:
            line = input("> ")
            print(evaluate(line))
        except (SyntaxError, ValueError) as e:
            print(e)
        except EOFError:
            break


if __name__ == '__main__':
    main()
