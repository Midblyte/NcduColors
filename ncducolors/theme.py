from ncducolors.key import Key


class Theme:
    KEYS = (
        "default",
        "box_title",
        "hd",
        "sel",
        "num",
        "num_hd",
        "num_sel",
        "key",
        "key_hd",
        "dir",
        "dir_sel",
        "flag",
        "flag_sel",
        "graph",
        "graph_sel"
    )

    __slots__ = (
        "name",
        *KEYS
    )

    def __init__(self, name: str):
        self.name: str = name

        for key in Theme.KEYS:
            setattr(self, key, ...)

    @staticmethod
    def from_dict(name: str, dct: dict) -> "Theme":
        theme = Theme(name=name)

        for key, value in dct.items():
            if (key := key.lower()) not in Theme.KEYS:
                raise ValueError(f"Key {key!r} is not a valid key for Ncdu themes.")

            setattr(theme, key, Key.from_dict(dct[key]))

        return theme

    def as_dict(self):
        return {
            k: getattr(self, k).as_dict() for k in self.KEYS
        }
