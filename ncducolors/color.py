from enum import Enum, auto
from typing import Optional

from . import Endianness


class Color(Enum):
    BLACK   = 0
    RED     = auto()
    GREEN   = auto()
    YELLOW  = auto()
    BLUE    = auto()
    MAGENTA = auto()
    CYAN    = auto()
    WHITE   = auto()
    NONE    = -1
    UNKNOWN = NONE

    @property
    def as_string(self) -> Optional[str]:
        return self.name.capitalize() if self is not Color.NONE else None

    def get_code(self, length: int = 2, byteorder: Endianness = "little", signed: bool = True) -> bytes:
        return self.value.to_bytes(length=length, byteorder=byteorder, signed=signed)

    @staticmethod
    def from_name(name: Optional[str]) -> "Color":
        return getattr(Color, name.upper(), Color.UNKNOWN) if name is not None else Color.NONE

    @staticmethod
    def from_code(value: bytes, byteorder: Endianness = "little", signed: bool = True) -> "Color":
        return Color.by_value(int.from_bytes(value, signed=signed, byteorder=byteorder))

    @classmethod
    def by_value(cls, value: int):
        for member in cls:
            if member.value == value:
                return member

        return Color.UNKNOWN
