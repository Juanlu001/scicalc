import pytest

from scicalc.tokenize import tokenize
from scicalc.parse import parse
from scicalc.evaluate import evaluate


# Tokenization tests

def test_tokenize_single_int():
    assert tokenize("1") == tokenize("   1 ") == ["1"]


def test_tokenize_single_float():
    assert tokenize("1.0") == tokenize("   1.0  ") == ["1.0"]


def test_tokenize_unary():
    assert tokenize("-1") == tokenize("  -   1") == ["-", "1"]


def test_tokenize_binary_simple_operations():
    assert tokenize("1+2") == tokenize("1 +    2") == ["1", "+", "2"]
    assert tokenize("1-2") == tokenize("  1 - 2") == ["1", "-", "2"]
    assert tokenize("1*2") == tokenize("1   * 2  ") == ["1", "*", "2"]
    assert tokenize("1/2") == tokenize("1   / 2") == ["1", "/", "2"]


def test_tokenize_log():
    assert tokenize("log(2.0)") == tokenize("  log ( 2.0  )") == ["log", "(", "2.0", ")"]


def test_tokenize_parentheses():
    assert tokenize("1*(2+3)") == tokenize("  1 * (2 + 3  )") == ["1", "*", "(", "2", "+", "3", ")"]


def test_linear_equation():
    assert tokenize("2*x=1") == tokenize("  2 * x = 1") == ["2", "*", "x", "=", "1"]


def test_error_on_invalid_character():
    with pytest.raises(SyntaxError) as excinfo:
        tokenize('1 + yxz')
    assert ('SyntaxError: Invalid character "y"'
            in excinfo.exconly())


def test_error_invalid_token_with_whitespace():
    with pytest.raises(SyntaxError) as excinfo:
        tokenize('1 + lo g 2')
    assert ('SyntaxError: Invalid character "l"'
            in excinfo.exconly())


# Parsing tests

def test_parse_simple_sum():
    assert parse('1 + 1') == ['1', '1', '+']


def test_complex_expression():
    assert parse('3 + 4 * 2 / ( 1 - 5 )') == ['3', '4', '2', '*', '1', '5', '-', '/', '+']


def test_parse_function():
    assert parse('log 2') == parse('log(2)') == ['2', 'log']


# Evaluation tests
# Note: Checking floating point math results to machine precision on purpose

def test_evaluate_simple_sum():
    assert evaluate('1 + 2') == 3.0


def test_evaluate_complex_expression():
    assert evaluate('3 + 4 * 2 / ( 1 - 5 )') == 1.0


def test_evaluate_with_function():
    assert evaluate('log 2') == evaluate('log(2)') == 0.69314718055994530942


def test_log_precedence():
    assert evaluate('log(1 + 1)') == evaluate('log(2)') == 0.69314718055994530942
    assert evaluate('log 1 + 1') == 1.0


def test_evaluate_negative_number():
    assert evaluate('-1') == -1.0


# Equations tests

def test_solve_trivial_equation():
    assert evaluate('x = 1') == 'x = 1.0'


def test_assert_simple_equation():
    assert evaluate('2 * x = 1') == 'x = 0.5'
