"""ЗО модуля - обеспечение работы функций ввода-вывода.

Чтение нот, проигрывание звуков, вывод текста на экран.
"""

from dragnote.coder import CompositionCoder
from dragnote.domain import Info


def read_input(greeting: str):
    return input(f"({greeting})> ")


def read_notes(greeting: str):
    string = read_input(greeting)
    return CompositionCoder.decode(string)


def print_info(info: Info):
    print("Current is %s, common count is %s, attempts %s" % (info.current, info.common, info.attempts))
