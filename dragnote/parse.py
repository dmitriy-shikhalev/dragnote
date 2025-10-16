import os

import pydantic_yaml

from dragnote.domain import Composition

DIRNAME = "compositions"


def get_full_filename(filename: str) -> str:
    return os.path.join(DIRNAME, filename)


def parse_file(filename: str):
    return pydantic_yaml.parse_yaml_file_as(Composition, open(get_full_filename(filename)))  # type: ignore[type-var]


def parse_composition(num: int) -> Composition:
    return parse_file(f"{num}.yaml")
