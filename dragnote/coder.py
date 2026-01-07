"""ЗО модуля - парсить упоаэгегия их текста в модели предметной области."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Composition, Duration, Harmony, Note
from dragnote.errors import CoderError

CODER_TYPE = TypeVar("CODER_TYPE", Composition, Harmony, Duration, Note, NAME, OCTAVE, SIGN)


class AbstractCoder(ABC, Generic[CODER_TYPE]):
    @classmethod
    @abstractmethod
    def encode(cls, obj: CODER_TYPE, **kwargs) -> str:
        raise NotImplementedError  # pragma: no cover

    @classmethod
    @abstractmethod
    def decode(cls, text: str, **kwargs) -> CODER_TYPE:
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
                raise CoderError(f"Unknown octave: {obj}")

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
                raise CoderError(f"Can't parse octave: {text}")


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
                raise CoderError(f"Unknown sign: {obj}")

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
                raise CoderError(f"Unknown sign: {text}")


class NameCoder(AbstractCoder[NAME]):
    @classmethod
    def encode(cls, obj: NAME) -> str:
        match obj:
            case NAME.C:
                return "C"
            case NAME.D:
                return "D"
            case NAME.E:
                return "E"
            case NAME.F:
                return "F"
            case NAME.G:
                return "G"
            case NAME.A:
                return "A"
            case NAME.H:
                return "H"
            case _:
                raise CoderError(f"Unknown name {obj}")

    @classmethod
    def decode(cls, text: str) -> NAME:
        match text.upper():
            case "C":
                return NAME.C
            case "D":
                return NAME.D
            case "E":
                return NAME.E
            case "F":
                return NAME.F
            case "G":
                return NAME.G
            case "A":
                return NAME.A
            case "H":
                return NAME.H
            case _:
                raise CoderError(f"Unknown name {text}")


class NoteCoder(AbstractCoder[Note]):
    @classmethod
    def encode(cls, obj: Note) -> str:
        return f"{NameCoder.encode(obj.name)}{SignCoder.encode(obj.sign)}{OctaveCoder.encode(obj.octave)}"

    @classmethod
    def decode(cls, text: str) -> Note:
        name = NameCoder.decode(text[0])
        octave = OctaveCoder.decode(text[-1])
        return Note(name=name, sign=SignCoder.decode(text[1:-1]), octave=octave)


class DurationCoder(AbstractCoder[Duration]):
    @classmethod
    def encode(cls, obj: Duration) -> str:
        return f"({obj.numerator}/{obj.denominator})"

    @classmethod
    def decode(cls, text: str) -> Duration:
        if text[0] != "(" or text[-1] != ")":
            raise CoderError(f"Unknown duration: {text}")
        parts = text[1:-1].split("/")
        if len(parts) != 2 or not all((part.isnumeric() for part in parts)):
            raise CoderError(f"Unknown duration: {text}")
        return Duration(numerator=int(parts[0]), denominator=int(parts[1]))


class HarmonyCoder(AbstractCoder[Harmony]):
    @classmethod
    def encode(cls, obj: Harmony, with_duration: bool) -> str:
        if with_duration:
            return ":".join(NoteCoder.encode(note) for note in obj.notes) + DurationCoder.encode(obj.duration)
        return ":".join(NoteCoder.encode(note) for note in obj.notes)

    @classmethod
    def decode(cls, text: str, with_duration: bool) -> Harmony:
        if with_duration:
            notes, duration = text.split("(")
            duration = "(" + duration
            notes_list = notes.split(":")
            return Harmony(
                notes=tuple([NoteCoder.decode(note) for note in notes_list]),
                duration=DurationCoder.decode(duration),
            )
        notes_list = text.split(":")
        return Harmony(notes=tuple([NoteCoder.decode(note) for note in notes_list]))


class CompositionCoder(AbstractCoder[Composition]):
    @classmethod
    def encode(cls, obj: Composition, with_duration: bool) -> str:
        return " ".join(HarmonyCoder.encode(harmony, with_duration=with_duration) for harmony in obj.harmonies)

    @classmethod
    def decode(cls, text: str, with_duration: bool) -> Composition:
        parts = text.split()
        return Composition(harmonies=tuple([HarmonyCoder.decode(part, with_duration=with_duration) for part in parts]))
