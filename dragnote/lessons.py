import os


def get_lessons(lessons_path: str):
    files = os.listdir(lessons_path)
    raise ZeroDivisionError(files)
