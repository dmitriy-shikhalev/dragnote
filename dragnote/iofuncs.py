"""ЗО модуля - обеспечение работы функций ввода-вывода.

Чтение нот, проигрывание звуков, вывод текста на экран.
"""

from dragnote.domain import Harmony, Info


def read_input(harmony_list: list[Harmony] | None = None, first_harmony: Harmony | None = None):
    if harmony_list:
        input_str = " ".join(":".join(note.to_str() for note in harmony.notes) for harmony in harmony_list)
    elif first_harmony:
        input_str = f"First note is {first_harmony.to_str()}"
    else:
        raise ValueError("Notes list is None and first_harmony is None")
    return input(f"({input_str})> ")


def print_info(info: Info):
    print("Current is %s, common count is %s, attempts %s" % (info.current, info.common, info.attempts))
