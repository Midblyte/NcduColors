import mmap
import struct
from functools import cache
from pathlib import Path
from subprocess import run
from typing import Optional, Final

from . import Endianness
from .sequence import Sequence
from .attribute import Attribute
from .color import Color
from .config import Config
from .key import Key
from .theme import Theme


class NcduColors:
    def __init__(self, ncdu: Path):
        self.ncdu: Path = ncdu.absolute()

        self.version: tuple[int] = self._load_version()
        self.supports_darkbg = self.version >= (1, 17)

        self.binary: bytearray = bytearray(self.ncdu.read_bytes())

        # See https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
        if self.binary[5] == 1:
            self.byteorder: Endianness = "little"
        elif self.binary[5] == 2:
            # self.byteorder: Endianness = "big"
            raise NotImplementedError("Big endian ELF files are not supported yet.")
        else:
            raise ValueError("Malformed ELF file.")

    @cache
    def _load_version(self) -> tuple[int]:
        command = run([self.ncdu, "--version"], capture_output=True)

        command.check_returncode()

        ncdu_literally, raw_version = command.stdout.decode("utf-8").split(maxsplit=1)

        if ncdu_literally != "ncdu":
            raise ValueError(f"Executable {str(self.ncdu.absolute())!r} was not recognised as Ncdu.")

        version = tuple(map(int, raw_version.rsplit('-')[0].split('.')))

        if version >= (2, 0):
            raise ValueError(f"Version 2.0+ ({raw_version}) is not supported yet.")

        return version

    @staticmethod
    def binary_to_themes(*, binary: bytearray, offset: int, supports_darkbg: bool, byteorder: Endianness) -> tuple[Theme]:
        if supports_darkbg:
            themes: tuple[Theme] = Theme("off"), Theme("dark"), Theme("darkbg")
        else:
            themes: tuple[Theme] = Theme("off"), Theme("dark")

        key_format: Final[str] = Key.get_format(byteorder=byteorder)

        expected_length: int = struct.calcsize(key_format)

        full_binary_segment: bytearray = binary[offset: offset + expected_length * len(Theme.KEYS) * len(themes)]

        for i, key_str in enumerate(Theme.KEYS):
            for j, theme in enumerate(themes):
                index = (len(themes) * i + j) * expected_length

                binary_segment: bytearray = full_binary_segment[index : index + expected_length]

                assert len(binary_segment) == expected_length

                fg_raw, bg_raw, a_raw = struct.unpack(key_format, binary_segment)

                key = Key(
                    fg=Color.by_value(fg_raw),
                    bg=Color.by_value(bg_raw),
                    a=Attribute(a_raw)
                )

                setattr(theme, key_str, key)

        return themes

    def load_config(self, offset: int) -> Config:
        themes: tuple[Theme] = NcduColors.binary_to_themes(
            binary=self.binary,
            offset=offset,
            supports_darkbg=self.supports_darkbg,
            byteorder=self.byteorder
        )

        return Config(ncdu=self.ncdu, offset=offset, **{theme.name: theme for theme in themes})

    def extract_default_config(self) -> Config:
        if self.byteorder == "little":  # todo: big endian sequences
            offset = self.binary.find(Sequence.DEFAULT_LE_WITH_DARKBG if self.supports_darkbg else Sequence.DEFAULT_LE_WITHOUT_DARKBG)
        else:  # todo: big endian sequences
            raise NotImplementedError("Big endian ELF files are not supported yet.")

        if offset == -1:
            raise ValueError("Default config pattern not found in the binary file.\n"
                             "You can only to do a 'apply-config' (on the default config) or 'revert'.")

        default_config: Config = self.load_config(offset=offset)

        return default_config

    @staticmethod
    def dump_internal_default_config(*, ncdu: Optional["Path"] = None, offset: Optional[int] = None, with_darkbg: bool,
                                     byteorder: Endianness = "little") -> Config:
        if byteorder == "little":
            binary = Sequence.DEFAULT_LE_WITH_DARKBG if with_darkbg else Sequence.DEFAULT_LE_WITHOUT_DARKBG
        else:  # todo: big endian sequences
            raise NotImplementedError("Big endian ELF files are not supported yet.")

        themes = NcduColors.binary_to_themes(binary=binary, offset=0, supports_darkbg=with_darkbg, byteorder=byteorder)

        return Config(
            ncdu=ncdu,
            offset=offset,
            **{theme.name: theme for theme in themes}
        )

    def apply_config(self, new_config: Config) -> bool:
        offset: int = new_config.offset

        current_config: Config = self.load_config(offset=offset)

        if current_config.as_dict() == new_config.as_dict():
            return False

        with open(self.ncdu, "r+b") as edit:
            new_bytes = new_config.as_bytes()

            self.binary[offset: offset + len(new_bytes)] = new_bytes

            with mmap.mmap(edit.fileno(), 0) as mem:
                mem.seek(offset)
                mem.write(new_bytes)

        return True
