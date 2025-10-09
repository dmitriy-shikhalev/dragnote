import os

import pydantic_yaml

from dragnote.domain import Composition

DIRNAME = "compositions"


def parse_file(filename: str):
    return pydantic_yaml.parse_yaml_file_as(Composition, open(filename))  # type: ignore[type-var]


def get_compositions():
    for filename in os.listdir(DIRNAME):
        yield parse_file(
            os.path.join(
                DIRNAME,
                filename,
            )
        )


def parse_composition(composition_name: str):
    for composition in get_compositions():
        if composition.name == composition_name:
            return composition
    raise ValueError(composition_name)
