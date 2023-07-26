from typing import Literal


__version__ = "0.0.1"

Endianness = Literal["little", "big"]

from . import ncducolors  # noqa: E402
from .ncducolors import NcduColors  # noqa: E402
