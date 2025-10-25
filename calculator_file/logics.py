def return_type(element):
    """
    Подсчет итогового резльтата из Обратной польской нотации

    :param element: str
    :return: type_element: str
    """

    if element.replace(".", "").isdigit() or element == ".":
        return "number"
    if element in "+-*/^|%~$":
        return "operator"
    elif element in "~$":
        return "unary_operator"
    elif element in "()":
        return "bracket"


def is_unary(operator):
    """
    Подсчет итогового резльтата из Обратной польской нотации

    :param operator: str
    :return: is_unary: bool
    """

    if operator in ["~", "$"]:
        return True
    return False


def return_equality(prev_el, curr_el):
    """
    Подсчет итогового резльтата из Обратной польской нотации

    :param prev_el, curr_el: str
    :return: return_equality: bool
    """

    list_elements = [prev_el, curr_el]
    types_elements = [None, None]
    for ind in range(2):
        types_elements[ind] = return_type(list_elements[ind])
    if types_elements[0] == types_elements[1]:
        return True
    return False
