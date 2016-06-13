"""Tokenization functions.

"""
import re

TOKENS = [
    ('WHITESPACE', r'\s+'),
    ('FLOAT', r'\d+\.\d+'),
    ('INTEGER', r'\d+'),
    ('MINUS', r'\-'),
    ('PLUS', r'\+'),
    ('TIMES', r'\*'),
    ('DIVIDE', '/'),
    ('LEFT', r'\('),
    ('RIGHT', r'\)'),
    ('LOG', 'log'),
    ('VARIABLE', 'x'),
    ('EQUALS', '='),
]

T_DELIMITERS = ('LEFT', 'RIGHT')
T_NUMBERS = ('FLOAT', 'INTEGER')
T_VARIABLES = ('VARIABLE',)
T_OPERATORS = ('MINUS', 'PLUS', 'TIMES', 'DIVIDE')
T_FUNCTIONS = ('LOG',)

T_IGNORE = 'WHITESPACE'


def tokenize(line):
    """Tokenizes a line of input.

    """
    return [token for _, token in split_tokens(line)]


def split_tokens(line):
    index = 0
    while True:
        # Cut line
        line = line[index:]
        if line:
            for t_type, pattern in TOKENS:
                match = re.match(pattern, line)
                if match:
                    # Shift string, yield token, repeat
                    index = match.end()
                    if t_type != T_IGNORE:
                        yield t_type, match.group()
                    break
            else:
                # No proper token was found
                raise SyntaxError('Invalid character "%s"'
                                  % line[0])
        else:
            break
