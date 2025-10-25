from calculator_file.tokenization import tokenization
from calculator_file.RPN import RPN
from calculator_file.calculation import calculation
from calculator_file.class_errors import *

expression = input("""Добро пожаловать в калькулятор!😎 
Введите выражение:
""")
try:
    expression_tokens = tokenization(expression)
    if expression_tokens:
        rpn = RPN(expression_tokens)
        if rpn:
            res = calculation(rpn)
            print(f"✅Результат: {res}")

except InvalidSequenceError as e:
    print("Ошибка:", e, '\n')

except MainCalculatorError as e:
    print("Ошибка:", e, '\n')

except Exception as e:
    print("Неизвестная ошибка:", e, '\n')
