from typing import Literal


__version__ = "0.0.2"

Endianness = Literal["little", "big"]

from . import ncducolors  # noqa: E402
from .attribute import Attribute  # noqa: E402
from .config import Config  # noqa: E402
from .key import Key  # noqa: E402
from .ncducolors import NcduColors  # noqa: E402
from .sequence import Sequence  # noqa: E402
from .theme import Theme  # noqa: E402
from .color import Color  # noqa: E402

