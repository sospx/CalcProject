from calculator_file.logics import *
from calculator_file.operators import *
from calculator_file.class_errors import *


def tokenization(input_expression):
    """
    Подсчет итогового резльтата из Обратной польской нотации

    :param input_expression: str
    :return: tokens: list
    """

    pattern = r'\d*\.?\d+\s+\d*\.?\d+'
    if re.search(pattern, input_expression):
        raise TwoNumbersInARowError()

    tokens = []
    expression = ''.join(input_expression.split())
    expression = expression.replace("**", "^")
    expression = expression.replace("//", "|")
    expression = expression.replace("..", "#")

    if not expression or expression.strip() == "":
        raise EmptyExpressionError()
    for el in expression:
        if el not in "0123456789.+-*^/|%()":
            raise checking_characters(el)

    count = -1
    token = expression[0]
    prev_element = None
    for index in range(1, len(expression)):
        if count <= 0:
            count += 1
        current_element = expression[index]
        if token in "()":
            tokens.append(token)
            prev_element = token
            token = current_element
        elif token in "*/^|%":
            tokens.append(token)
            prev_element = token
            token = current_element
        elif token in "+-":
            if count == 0 or prev_element in priorities_of_operations:
                if token == "+":
                    tokens.append("$")
                    prev_element = token
                    token = current_element
                elif token == "-":
                    tokens.append("~")
                    prev_element = token
                    token = current_element
            else:
                tokens.append(token)
                prev_element = token
                token = current_element
        elif not return_equality(token, current_element):
            tokens.append(token)
            prev_element = token
            token = current_element
        else:
            if token[0] == ".":
                token = "0" + token
            token += current_element
    tokens.append(token)
    if "." in tokens:
        raise InvalidSequenceError("Неизвестная точка '.'")
    if [1 for t in tokens if t.count(".") > 1]:
        # invalid_characters()
        raise InvalidSequenceError("В дробном числе не может быть двух и более '.'")
    return tokens
