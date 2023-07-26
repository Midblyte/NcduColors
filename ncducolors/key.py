from functools import cache

from ncducolors.attribute import Attribute
from ncducolors.color import Color
from ncducolors import Endianness


class Key:
    __slots__ = "fg", "bg", "a"

    def __init__(self, fg: Color, bg: Color, a: Attribute):
        self.fg = fg
        self.bg = bg
        self.a = a

    @staticmethod
    @cache
    def get_format(byteorder: Endianness = "little") -> str:
        return f"{'<' if byteorder == 'little' else '>'}hhI"

    @staticmethod
    def from_dict(dct: dict) -> "Key":
        if set(Key.__slots__) != set(dct.keys()):
            raise ValueError(f"Key object must have keys 'fg', 'bg' and 'a'.")

        fg = Color.from_name(dct["fg"])
        bg = Color.from_name(dct["bg"])
        a = Attribute.from_names(dct["a"])

        key = Key(fg=fg, bg=bg, a=a)

        return key

    def as_dict(self):
        return {
            "fg": self.fg.as_string,
            "bg": self.bg.as_string,
            "a": self.a.as_string
        }

    def as_bytes(self, byteorder: Endianness = "little", **kwargs) -> bytes:
        return b''.join(map(lambda f: f.get_code(byteorder=byteorder, **kwargs), (self.fg, self.bg, self.a)))
