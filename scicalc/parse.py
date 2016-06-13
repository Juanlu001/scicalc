"""Parsing functions.

"""
from collections import deque

from scicalc.tokenize import (split_tokens, T_NUMBERS, T_OPERATORS, T_FUNCTIONS, T_DELIMITERS)

# Operator precedence
OP_PRECEDENCE = {
    'UNARY_MINUS': 4,
    'LOG': 4,
    'TIMES': 3,
    'DIVIDE': 3,
    'PLUS': 2,
    'MINUS': 2,
}


def parse(tokens):
    return [tok for _, tok in postfix_from_infix(split_tokens(tokens))]


def postfix_from_infix(tokens):
    """Return postfix notation (RPN) from infix (human-friendly)

    Returns
    -------
    deque
        Output queue to be evaluated

    Notes
    -----
    Based on https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    With the current generator architecture it's difficult to change
    the program to allow implicit multiplication. One idea is to
    inject a TIMES operator when some conditions are met, but it
    breaks the stream.

    """
    output_queue = deque()
    operator_stack = []
    prev = None
    for ii, token in enumerate(tokens):
        t_type = token[0]

        # First check for unary minus and replace token if necessary
        if t_type == 'MINUS' and (ii == 0 or
                                  prev[0] == 'LEFT' or
                                  prev[0] in T_OPERATORS or
                                  prev[0] in T_FUNCTIONS):
            token = ('UNARY_MINUS', '-u')

        # Go on parsing
        if t_type in T_NUMBERS:
            output_queue.append(token)
        elif t_type in T_FUNCTIONS:
            operator_stack.append(token)
        elif t_type in T_OPERATORS:
            o1 = token
            while operator_stack:
                o2 = operator_stack[-1]
                if ((o2[0] in T_FUNCTIONS and OP_PRECEDENCE[o1[0]] < OP_PRECEDENCE[o2[0]]) or
                        (o2[0] in T_OPERATORS and OP_PRECEDENCE[o1[0]] <= OP_PRECEDENCE[o2[0]])):
                    output_queue.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(o1)
        elif t_type == 'LEFT':
            operator_stack.append(token)
        elif t_type == 'RIGHT':
            while operator_stack:
                top = operator_stack.pop()
                if top[0] in ('LEFT',):
                    break
                output_queue.append(top)
            else:
                raise SyntaxError("Mismatched parentheses")

        # Save last token for next iteration
        prev = token

    # No more tokens to read
    while operator_stack:
        top = operator_stack.pop()
        if top[0] in T_DELIMITERS:
            raise SyntaxError("Mismatched parentheses")
        else:
            output_queue.append(top)

    return output_queue
