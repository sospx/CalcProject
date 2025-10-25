priorities_of_operations = {
    "~": -1,
    "$": -1,
    "^": 0,
    "*": 1,
    "/": 1,
    "|": 1,
    "%": 1,
    "+": 2,
    "-": 2,
    "(": 3
}


operations = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "|": lambda x, y: x // y,
    "%": lambda x, y: x % y,
    "^": lambda x, y: x ** y,
    "~": lambda x: -x,
    "$": lambda x: x
}
