from calculator_file.logics import *
from calculator_file.operators import *
from calculator_file.class_errors import *


def calculation(list_expression):
    """
    Подсчет итогового резльтата из Обратной польской нотации

    :param list_expression: list
    :return: result: float
    """
    stack = []
    for element in list_expression:
        if return_type(element) == "number":
            stack.append(float(element))
        elif return_type(element) == "operator":
            if not is_unary(element):
                try:
                    try:
                        if element in "|%":
                            if "." in stack[-2] or "." in stack[-1]:
                                raise InvalidSequenceError("Ошибка счета")
                        res = operations[element](stack[-2], stack[-1])
                    except:
                        raise InvalidSequenceError("Ошибка счета")
                    stack[-1] = res
                    del stack[-2]
                except:
                    raise InvalidSequenceError("Ошибка счета")
            else:
                res = operations[element](stack[-1])
                stack[-1] = res
    if len(stack) > 1:
        raise InvalidSequenceError("Ошибка счета")
    result = stack[-1]
    return round(result, 3)
