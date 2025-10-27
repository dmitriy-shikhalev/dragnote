import logging
import os

import yaml
import pydantic_yaml

from dragnote.domain import Composition
from dragnote.errors import NoFile

logger = logging.getLogger(__name__)
DIRNAME = "compositions"
LIST_FILENAME = "list.yaml"


def get_filename(num: int):
    filenames = yaml.load(open(os.path.join(DIRNAME, LIST_FILENAME)), yaml.Loader)["compositions"]
    if num >= len(filenames):
        raise NoFile(f"No composition with num {num}")
    return filenames[num]


def get_full_filename(filename: str) -> str:
    return os.path.join(DIRNAME, filename)


def parse_file(filename: str):
    return pydantic_yaml.parse_yaml_file_as(Composition, open(filename))  # type: ignore[type-var]


def parse_composition(num: int) -> Composition:
    logger.debug("Get file num %s", num)
    filename = get_filename(num)
    logger.debug("Filename: %s", filename)
    full_filename = get_full_filename(filename)
    logger.debug("Full filename: %s", full_filename)
    if not os.path.exists(full_filename):
        raise NoFile(full_filename)
    return parse_file(full_filename)
