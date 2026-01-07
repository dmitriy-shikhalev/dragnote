"""ЗО модуля - парсить упоаэгегия их текста в модели предметной области."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from consts import NAME, OCTAVE, SIGN
from domain import Composition, Harmony, Note


coder_typevar = TypeVar("coder_typevar", Composition, Harmony, Note, NAME, OCTAVE, SIGN)


class AbstractCoder(ABC, Generic[coder_typevar]):
    @classmethod
    @abstractmethod
    def encode(cls, obj: coder_typevar) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def decode(cls, text: str) -> coder_typevar:
        raise NotImplementedError


class OctaveCoder(AbstractCoder[OCTAVE]):
    pass


class SignCoder(AbstractCoder[SIGN]):
    pass


class NameCoder(AbstractCoder[NAME]):
    pass


class NoteCoder(AbstractCoder[Note]):
    pass


class HarmonyCoder(AbstractCoder[Harmony]):
    pass


class CompositionCoder(AbstractCoder[Composition]):
    pass
