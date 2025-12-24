"""Зона ответственности модуля - одно уражнение.

Эксерсайз инициализируется композицией. Ран запускает. Умеет проиграть композицию, сравнить ввод с текущей частью
композиции, проиграть запомнить прогресс по композиции, упасть с овер ошибкой, дать текущие правильные гармонии, дать 
текущую гармонию, сравнить 2 гармонии, проиграть звук успеха, проиграть звук неудачи, проиграть гармонию с
длительностью.
Нужно добавить класс ИтераторКомпозиции!
"""

from dragnote.domain import Composition


class CompositionIterator:
    def __init__(self, composition: Composition):
        self.composition = composition


class Exercise:
    def __init__(self, composition: Composition):
        self.composition = composition
        self.composition_iterator = CompositionIterator(composition)

    def run(self):
        raise NotImplementedError
