import pytest
from calculator_file.tokenization import tokenization
from calculator_file.RPN import RPN
from calculator_file.calculation import calculation
from calculator_file.class_errors import *


@pytest.mark.parametrize("expr,expected", [
    # Базовые арифметические операции
    ("8 - 3 * 2", 2),
    ("15 / 3 + 4", 9.0),
    ("6 * 7 - 8", 34),
    ("20 + 30 / 5", 26.0),
    ("(8 - 3) * (2 + 4)", 30),
    ("(15 + 5) / (3 + 1)", 5.0),
    ("(2 * 6) + (10 / 2)", 17.0),
    ("(12 - 4) * (3 + 2) / 5", 8.0),
    ("3 ** 4", 81),
    ("4 ** 3", 64),
    ("5 ** 2 + 3", 28),
    ("2 ** 2 ** 3", 256),
    ("+10 - 5", 5),
    ("-8 + 12", 4),
    ("-(3 * 4)", -12),
    ("+(-6 * 2)", -12),
    ("2.5 * 4", 10.0),
    ("7.5 / 2.5", 3.0),
    ("0.1 * 10 + 2", 3.0),
    ("3.2 - 1.2", 2.0),
    ("4 + 6 * 2", 16),
    ("8 / 2 + 3 * 2", 10.0),
    ("10 - 3 * 2 + 4", 8),
    ("(4 + 6) * 2 - 5", 15),
    ("0 + 15", 15),
    ("25 * 0 + 8", 8),
    ("1 * 45", 45),
    ("100 / 1 - 50", 50.0),
    ("((5 + 3) * 2) - 4", 12),
    ("(2 * (3 + 4)) / 2", 7.0),
    ("(10 - (3 * 2)) * 4", 16),
    ("((8 / 2) + (3 * 3))", 13.0),
    ("2 * 3 ** 2", 18),
    ("(2 * 3) ** 2", 36),
    ("10 / 2 ** 2", 2.5),
    ("-3 ** 2", 9),
    ("1 + 2 + 3 + 4 + 5", 15),
    ("2 * 3 * 4 / 2", 12.0),
    ("10 - 2 - 3 - 1", 4),
    ("100 / 2 / 5", 10.0),
])
def test_expressions(expr, expected):
    tokens = tokenization(expr.replace(" ", ""))
    rpn = RPN(tokens)
    res = calculation(rpn)
    assert float(res) == expected


@pytest.mark.parametrize("expr,num", [
    ("100", 100),
    ("-25", -25),
    ("+456", 456),
    ("2.718", 2.718),
    ("1", 1),
    ("-1", -1),
    ("+1", 1),
    ("0.5", 0.5),
    ("-0.5", -0.5),
    ("+0.5", 0.5),
    ("2.0", 2.0),
    ("-3.5", -3.5),
    ("+4.5", 4.5),
    ("15.", 15.0),
    (".25", 0.25),
    ("-.75", -0.75),
    ("+.125", 0.125),
    ("123456789", 123456789),
    ("-987654321", -987654321),
    ("0.001", 0.001),
    ("-0.001", -0.001),
    ("1000.5", 1000.5),
    ("-2000.75", -2000.75),
])
def test_number(expr, num):
    tokens = tokenization(expr.replace(" ", ""))
    rpn = RPN(tokens)
    res = calculation(rpn)
    assert float(res) == num


@pytest.mark.parametrize("expr", [
    "234 4",
    "34 1",
    "1 2 3",
    "5  6",
    ".5 1.5",
    "2+3 4",
    "1 2+3",
    "1. 2",
])
def test_numbers_in_a_row(expr):
    with pytest.raises(TwoNumbersInARowError):
        checking_two_numbers_in_a_row(expr)


# Тесты на ошибку деления на ноль
@pytest.mark.parametrize("expr", [
    "12 // 0",
    "(5 + 3) / 0",
    "15 / (5 - 5)",
    "20 // (4 * 0)",
    "(12 / 3) / 0",
    "50 / ((10 - 10))",
    "7 % 0",
    "(8 + 4) % (6 - 6)",
    "0 / 0",
    "0 // 0",
    "(0) / (0)",
    "-8 / 0",
    "9 / (-0)",
    "0 / 0"
])
def test_division_by_zero(expr):
    tokens = tokenization(expr.replace(" ", ""))
    rpn = RPN(tokens)
    with pytest.raises(DivisionNumByZeroError):
        calculation(rpn)


@pytest.mark.parametrize("expr", [
    "4 + 5)))))",
    "(3 + 1))",
    "(()",
    "(()(",
    "((1 + 245)",
    "(45 + 23))",
    "((15+ 22) * 31",
    "(()((())(()",
    "(())(8))) )(",
    "(1 + 3))((6 + 4)",
])
def test_brackets(expr):
    with pytest.raises((InvalidSequenceError, BracketsError)):
        checking_valid_empty_brackets(expr)


# Тесты на ошибку остатка от деления на ноль
@pytest.mark.parametrize("expr", [
    "7 % 0",
    "10 % (5 - 5)",
    "(15 + 5) % (10 - 10)",
    "100 % (50 - 25 * 2)",
    "-7 % 0",
    "(-10) % (5 - 5)",
    "(3 + 2) % (2 - 2)",
    "(8 % 4) % 0",
    "0 % 0",
    "0 % (1 - 1)",
    "10 % ((2 + 3) - 5)",
    "(2 * 5) % (10 - 10)",
    "((7 + 3) * 2) % (20 - 20)",
])
def test_division_by_zero(expr):
    tokens = tokenization(expr.replace(" ", ""))
    rpn = RPN(tokens)
    with pytest.raises(InvalidSequenceError):
        calculation(rpn)


# Тесты на ошибки целочисленных операции только для целых
@pytest.mark.parametrize("expr", [
    "10.5 // 2",
    "7.2 % 3",
    "3.0 // 1",
    "5.5 % 2",
    "-4.2 // 2",
    "-7.5 % 3",
    "0.1 // 1",
    "0.0 % 1",
    "(3.5 + 2) // 2",
    "10 // (2.5)",
    "(7 % 2.0)",
    "(8.0 // 2) + 1",
])
def test_integer_only_operations(expr):
    tokens = tokenization(expr.replace(" ", ""))
    rpn = RPN(tokens)
    with pytest.raises(InvalidSequenceError):
        calculation(rpn)


# Тесты на смешанные типы: Int и Float
@pytest.mark.parametrize("expr,expected", [
    ("3 + 4.4", 7.4),
    ("4.8 - 1.0", 3.8),
    ("4 * 3.0", 12.0),
    ("5.0 / 5", 1.0),
])
def test_int_float(expr, expected):
    tokens = tokenization(expr.replace(" ", ""))
    rpn = RPN(tokens)
    res = calculation(rpn)
    assert float(res) == expected


# Тесты на вложенные скобки и приоритет операций
@pytest.mark.parametrize("expr,expected", [
    ("(3 + 4) * (2 + 6) - 10", 46),
    ("((2 + 3) * (4 + 1)) ** 2 - 5", 620),
    ("(5 + 3) * 6 - 2 ** 4", 32),
    ("(10 - 2) * (3 + 1) / 4", 8.0),
    ("((8 / 2) + (3 * 4)) ** 2", 256),
    ("(12 + 3) * (6 - 2) + 10", 70),
    ("(20 / 4) * (3 + 2) - 15", 10.0),
    ("((5 + 3) ** 2) / (2 * 2)", 16.0),
    ("(15 - 5) * (2 + 3) / 5", 10.0),
    ("(7 + 2) * (4 - 1) ** 2", 81),
])
def test_bracket(expr, expected):
    tokens = tokenization(expr.replace(" ", ""))
    rpn = RPN(tokens)
    res = calculation(rpn)
    assert float(res) == expected


# Тесты на очень большие числа
@pytest.mark.parametrize("expr", [
    "11 ** 10910",
    "11 ** 100010",
    "22 ** 33333",
    "9999953534253423523 * 999993453453454525235",
    "11 ** 1070 + 10 ** 1045",
    "15 ** 5630 * 1234 ** 45",
    "(10 ** 100) ** 10",
    "12345252352452355456789 ** 5",
    "2 ** 1224500 * 2 ** 102252",

])
def test_numbers(expr):
    tokens = tokenization(expr.replace(" ", ""))
    rpn = RPN(tokens)
    try:
        res = calculation(rpn)
    except Exception as e:
        assert isinstance(e, MainCalculatorError)
