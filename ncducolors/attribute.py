from enum import auto, Flag
from functools import reduce
from typing import Optional, Final

from . import Endianness


_SHIFT: Final[int] = 8


class Attribute(Flag):
    STANDOUT   = 1 << 8 + _SHIFT
    UNDERLINE  = auto()
    REVERSE    = auto()
    BLINK      = auto()
    DIM        = auto()
    BOLD       = auto()
    ALTCHARSET = auto()
    INVISIBLE  = auto()
    PROTECT    = auto()
    HORIZONTAL = auto()
    LEFT       = auto()
    LOW        = auto()
    RIGHT      = auto()
    TOP        = auto()
    VERTICAL   = auto()
    NONE       = 0

    @property
    def as_string(self) -> Optional[str]:
        if self == Attribute.NONE:
            return None

        flags = {flag for flag in Attribute.__members__.values() if flag in self and flag is not Attribute.NONE}

        return " + ".join(map(lambda flag: flag.name.capitalize(), flags))

    def get_code(self, length: int = 4, byteorder: Endianness = "little", signed: bool = False) -> bytes:
        return self.value.to_bytes(length=length, byteorder=byteorder, signed=signed)

    @staticmethod
    def from_names(names: Optional[str]) -> "Attribute":
        if names is None:
            return Attribute.NONE

        return reduce(lambda a, b: a | b, map(lambda k: getattr(Attribute, k.upper(), Attribute.NONE), names.replace(' ', '').split('+')))

    @staticmethod
    def from_code(value: bytes, byteorder: Endianness = "little", signed: bool = True) -> "Attribute":
        return Attribute(int.from_bytes(value, signed=signed, byteorder=byteorder))
