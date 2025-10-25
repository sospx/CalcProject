import re


class MainCalculatorError(Exception):
    pass


class InvalidSequenceError(MainCalculatorError):
    def __init__(self, ret_text):
        super().__init__(ret_text)


class SymbolInvalidError(MainCalculatorError):
    def __init__(self, symbol):
        super().__init__(f"Символ недопустимый: '{symbol}'!")


class BracketsError(MainCalculatorError):
    def __init__(self, ret_text):
        super().__init__(ret_text)


class EmptyExpressionError(MainCalculatorError):
    def __init__(self):
        super().__init__("Пустое выражение")


class TwoNumbersInARowError(MainCalculatorError):
    def __init__(self):
        super().__init__("Между числами нет оператора")


class DivisionNumByZeroError(MainCalculatorError):
    def __init__(self):
        super().__init__("Нельзя делить на ноль")


def checking_two_numbers_in_a_row(exp):
    token_pat = r'\d*\.\d+|\d+|[()+\-*/%]'
    tokens = re.findall(token_pat, exp)
    was_num_chek = 0
    for token in tokens:
        try:
            float(token)
            is_number = 1
        except ValueError:
            is_number = 0
        if is_number:
            if was_num_chek:
                raise TwoNumbersInARowError()
            was_num_chek = 1
        else:
            was_num_chek = 0


def checking_characters(exp):
    chars = set("+-*/%()0123456789. ")
    for ch in exp:
        if ch not in chars:
            raise SymbolInvalidError(ch)


def checking_valid_empty_brackets(exp):
    if exp.count("(") != exp.count(")"):
        raise BracketsError("Несбалансированные скобки")
    if "()" in exp or ")(" in exp:
        raise BracketsError("Неверные скобки")
