import json
from io import TextIOWrapper
from pathlib import Path
from typing import Optional
from shutil import which

from ncducolors.theme import Theme
from ncducolors import Endianness


class Config:
    __slots__ = "ncdu", "offset", "off", "dark", "darkbg"

    def __init__(self, ncdu: Path, offset: int, off: Theme, dark: Theme, darkbg: Optional[Theme] = None):
        self.ncdu = ncdu
        self.offset = offset
        self.off = off
        self.dark = dark
        self.darkbg = darkbg

    @staticmethod
    def from_buffer(reader: TextIOWrapper) -> "Config":
        with reader as file:
            config = Config.from_dict(json.loads(file.read()))

        return config

    @staticmethod
    def from_dict(dct: dict) -> "Config":
        if (dct_keys := set(dct.keys())) != (slots := set(Config.__slots__)) and dct_keys != slots - {"darkbg"}:
            raise TypeError("Not a serialized Config object.")

        return Config(
            ncdu=Path(dct["ncdu"]).expanduser() if dct["ncdu"] is not None else Path(which("ncdu")),
            offset=dct["offset"],
            **{k: Theme.from_dict(k, dct[k]) for k in ("off", "dark", "darkbg") if k in dct}
        )

    def as_dict(self) -> dict:
        return {
            "ncdu": str(self.ncdu) if isinstance(self.ncdu, Path) else self.ncdu,
            "offset": self.offset,
            **{k: getattr(self, k).as_dict() for k in (("off", "dark", "darkbg") if self.darkbg is not None else ("off", "dark"))}
        }

    def as_bytes(self, byteorder: Endianness = "little") -> bytes:
        if self.darkbg is None:
            themes = self.off, self.dark
        else:
            themes = self.off, self.dark, self.darkbg

        bytes_block = b""

        for str_key in Theme.KEYS:
            for theme in themes:
                bytes_block += getattr(theme, str_key).as_bytes(byteorder=byteorder)

        return bytes_block
