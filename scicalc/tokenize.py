"""Tokenization functions.

"""
import re

TOKENS = [
    ('FLOAT', r'\d+\.\d+'),
    ('INTEGER', r'\d+'),
    ('MINUS', r'\-'),
    ('PLUS', r'\+'),
    ('TIMES', r'\*'),
    ('DIVIDE', '/'),
    ('OPEN', r'\('),
    ('CLOSE', r'\)'),
    ('LOG', 'log'),
    ('VARIABLE', 'x'),
    ('EQUALS', '='),
]


def tokenize(line):
    """Tokenizes a line of input.

    """
    return [token for token, _ in split_tokens(line.replace(" ", ""))]


def split_tokens(line):
    span = slice(0, None)
    while True:
        line = line[span]
        if line:
            for t_type, pattern in TOKENS:
                match = re.match(pattern, line)
                if match:
                    span = slice(match.end(), None)
                    yield match.group(), t_type
                    break
        else:
            break
