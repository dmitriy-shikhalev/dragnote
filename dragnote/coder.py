"""ЗО модуля - парсить упоаэгегия их текста в модели предметной области."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Composition, Harmony, Note


coder_typevar = TypeVar("coder_typevar", Composition, Harmony, Note, NAME, OCTAVE, SIGN)


class AbstractCoder(ABC, Generic[coder_typevar]):
    @classmethod
    @abstractmethod
    def encode(cls, obj: coder_typevar) -> str:
        raise NotImplementedError  # pragma: no cover

    @classmethod
    @abstractmethod
    def decode(cls, text: str) -> coder_typevar:
        raise NotImplementedError  # pragma: no cover


class OctaveCoder(AbstractCoder[OCTAVE]):
    @classmethod
    def encode(cls, obj: OCTAVE) -> str:
        match obj:
            case OCTAVE.SMALL:
                return "0"
            case OCTAVE.FIRST:
                return "1"
            case OCTAVE.SECOND:
                return "2"
            case _:
                raise ValueError(f"Unknown octave: {obj}")

    @classmethod
    def decode(cls, text: str) -> OCTAVE:
        match text:
            case "0":
                return OCTAVE.SMALL
            case "1":
                return OCTAVE.FIRST
            case "2":
                return OCTAVE.SECOND
            case _:
                raise ValueError(f"Can't parse octave: {text}")


class SignCoder(AbstractCoder[SIGN]):
    @classmethod
    def encode(cls, obj: SIGN) -> str:
        match obj:
            case SIGN.DOUBLE_FLAT:
                return "bb"
            case SIGN.FLAT:
                return "b"
            case SIGN.NATURAL:
                return ""
            case SIGN.SHARP:
                return "#"
            case SIGN.DOUBLE_SHARP:
                return "##"
            case _:
                raise ValueError(f"Unknown sign: {obj}")

    @classmethod
    def decode(cls, text: str) -> SIGN:
        match text.lower():
            case "bb":
                return SIGN.DOUBLE_FLAT
            case "b":
                return SIGN.FLAT
            case "":
                return SIGN.NATURAL
            case "#":
                return SIGN.SHARP
            case "##":
                return SIGN.DOUBLE_SHARP
            case _:
                raise ValueError(f"Unknown sign: {text}")


class NameCoder(AbstractCoder[NAME]):
    pass


class NoteCoder(AbstractCoder[Note]):
    pass


class HarmonyCoder(AbstractCoder[Harmony]):
    pass


class CompositionCoder(AbstractCoder[Composition]):
    pass
