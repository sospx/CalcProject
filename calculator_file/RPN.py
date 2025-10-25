from calculator_file.logics import *
from calculator_file.operators import *
from calculator_file.class_errors import *


def status_operators(curr_el, prev_el):
    # Если новоприбывший в стек оператор строго главнее уже находящегося, то True, иначе False
    return priorities_of_operations[curr_el] < priorities_of_operations[prev_el]


def RPN(expression):
    """
    Подсчет итогового резльтата из Обратной польской нотации

    :param expression: list
    :return: result: list
    """

    brackets_stack = []
    stack = []
    result = []
    for current_element in expression:
        if stack:
            prev_element = stack[-1]
        else:
            prev_element = "@"

        if return_type(current_element) == "number":
            result.append(current_element)
        elif return_type(current_element) == "operator":
            if not stack:
                stack.append(current_element)
            else:
                flag = True
                while flag:
                    # если оператор строго главнее или обо спенень, то ничего не выталкиваем
                    if status_operators(current_element, prev_element) or (current_element == prev_element == "^"):
                        flag = False
                    else:
                        result.append(stack.pop())
                        if stack:
                            prev_element = stack[-1]
                        else:
                            flag = False
                stack.append(current_element)
        elif return_type(current_element) == "bracket":
            if current_element == "(":
                brackets_stack.append("(")
                stack.append(current_element)
            elif current_element == ")":
                if brackets_stack and brackets_stack[-1] == "(":
                    del brackets_stack[-1]
                else:
                    raise ParenthesesError("Неправильная скобочная последовательность")

                flag = True
                while flag:
                    if stack[-1] != "(":
                        result.append(stack.pop())
                    else:
                        del stack[-1]
                        if stack:
                            if stack[-1] in "~$":
                                result.append(stack.pop())
                        flag = False

    result.extend(stack[::-1])
    if brackets_stack:
        raise ParenthesesError("Неправильная скобочная последовательность")
    if is_unary(result[0]):
        raise InvalidSequenceError("Неверное расположение унарных операторов")
    return result
