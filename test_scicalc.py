import pytest

from scicalc.tokenize import tokenize


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


@pytest.mark.xfail
def test_error_invalid_token_with_whitespace():
    with pytest.raises(SyntaxError) as excinfo:
        tokenize('1 + lo g 2')
    assert ('SyntaxError: Invalid charater "l"'
            in excinfo.exconly())
