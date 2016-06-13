"""Parsing functions.

"""
from collections import deque

from scicalc.tokenize import (split_tokens, T_NUMBERS, T_OPERATORS, T_FUNCTIONS, T_DELIMITERS)

# Operator precedence
OP_PRECEDENCE = {
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

    """
    # http://wcipeg.com/wiki/Shunting_yard_algorithm
    # http://www.oxfordmathcenter.com/drupal7/node/628
    # https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm
    # Extend with implicit multiplication
    # https://github.com/bmars/shunting-yard/commit/d34997c

    output_queue = deque()
    operator_stack = []
    for token in tokens:
        t_type = token[0]
        if t_type in T_NUMBERS:
            output_queue.append(token)
        elif t_type in T_FUNCTIONS:
            operator_stack.append(token)
        elif t_type in T_OPERATORS:
            o1 = token
            while operator_stack:
                # All supported operators are left-associative, see
                # https://en.wikipedia.org/wiki/Shunting-yard_algorithm#Detailed_example
                o2 = operator_stack[-1]
                if o2[0] in T_OPERATORS and OP_PRECEDENCE[o1[0]] <= OP_PRECEDENCE[o2[0]]:
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

    # No more tokens to read
    while operator_stack:
        top = operator_stack.pop()
        if top[0] in T_DELIMITERS:
            raise SyntaxError("Mismatched parentheses")
        else:
            output_queue.append(top)

    return output_queue
