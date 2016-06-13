"""Evaluation functions.

"""
from itertools import product
from math import log

from scicalc.tokenize import (split_tokens, T_NUMBERS, T_VARIABLES, T_OPERATORS, T_FUNCTIONS)
from scicalc.parse import postfix_from_infix


# Operator operations
OP_OPERATIONS = {
    'PLUS': lambda x, y: float(x) + float(y),
    'MINUS': lambda x, y: float(x) - float(y),
    'TIMES': lambda x, y: float(x) * float(y),
    'DIVIDE': lambda x, y: float(x) / float(y),
    'LOG': lambda x: log(float(x)),  # For consistency
    'UNARY_MINUS': lambda x: -float(x),
}


def evaluate(line):
    tokenized = list(split_tokens(line))
    types, values = zip(*tokenized)
    if "x" in values or "=" in values:
        # It might be an equation
        if "x" not in values:
            raise SyntaxError("There must be a variable x in the equation")
        elif "=" not in values:
            raise SyntaxError("Variables not supported in expressions")
        elif values.count("=") > 1:
            raise SyntaxError("Malformed equation, too many equal = signs")
        elif "/" in values:
            raise SyntaxError("Divisions are not supported in equations")
        elif "log" in values:
            raise SyntaxError("Logarithms are not supported in equations")
        else:
            # TODO: Check if equation is linear
            return "x = %s" % _solve_equation(tokenized)
    else:
        # It's a simple expression
        return _evaluate_expression(tokenized)


def _evaluate_postfix(tokens):
    # TODO: Properly evaluate
    # https://en.wikipedia.org/wiki/Reverse_Polish_notation

    evaluation_stack = []
    while tokens:
        t_type, value = tokens.popleft()
        if t_type in T_NUMBERS:
            evaluation_stack.append(value)
        else:
            if t_type in T_OPERATORS:
                # Two arguments
                val2 = evaluation_stack.pop()
                val1 = evaluation_stack.pop()
                args = (val1, val2)
            elif t_type in T_FUNCTIONS:
                # One argument
                args = (evaluation_stack.pop(),)
            else:
                raise RuntimeError("Internal error")

            # Put operation result onto the stack
            op = OP_OPERATIONS[t_type]
            evaluation_stack.append(op(*args))

    if len(evaluation_stack) == 1:
        return evaluation_stack[0]
    else:
        raise SyntaxError("Too many values")


def _evaluate_expression(tokens):
    return _evaluate_postfix(postfix_from_infix(tokens))


def _equation_quantities(lhs, rhs):
    for member, value in product([lhs, rhs], ['0', '1']):
        rep_token = ('INTEGER', value)
        yield float(_evaluate_expression(_replace_variable(member, rep_token)))


def _solve_equation(tokens):
    # This already assumes preconditions
    # TODO: Share method
    # http://stackoverflow.com/q/29482158/554319
    # http://mathforum.org/library/drmath/view/62929.html
    lhs, rhs = _split_by_index(tokens, tokens.index(('EQUALS', "=")))
    lhs0, lhs1, rhs0, rhs1 = _equation_quantities(lhs, rhs)
    return (rhs0 - lhs0) / (rhs0 - lhs0 + lhs1 - rhs1)


def _split_by_index(seq, index):
    return seq[:index], seq[index + 1:]


def _replace_variable(tokens, rep_token):
    return [rep_token if tok[0] in T_VARIABLES else tok for tok in tokens]
