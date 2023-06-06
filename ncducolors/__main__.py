import argparse
import json
import shutil
import sys
from io import TextIOWrapper
from pathlib import Path
from typing import Optional

from . import __version__
from ncducolors.config import Config
from ncducolors.ncducolors import NcduColors


HELP_MESSAGE = """
NcduColors dumps and patches pre-2.0 Ncdu's internal themes.

Usage:
  ncducolors [--ncdu PATH] extract-default-config <FILE> [--compact]
  ncducolors [--ncdu PATH] apply-config <FILE>
  ncducolors [--ncdu PATH] revert (--offset INT | --config FILE)
  ncducolors [--ncdu PATH] dump-internal-default-config [--compact]
             [--with[out]-darkbg] [--[little|big]-endian]
  ncducolors (-h | --help)
  ncducolors --version

Actions:
  extract-default-config         Extracts Ncdu's configuration, its two/three themes,
                                 colors and attributes. Works only on non-patched binaries.
                                 (make a backup of it before proceding!)
  apply-config                   Overwrites the binary configuration file with the one
                                 provided.
  revert                         Does the same thing of apply-config, but uses
                                 NcduColors' colors and attributes. In other words,
                                 everything else than "path" and "offset" is discarded.
  dump-internal-default-config   Should be used in exceptional cases only
                                 (last-resort recovery, analysis, etc...).
                                 It uses NcduColors' (not Ncdu's) binaries.

Options:
  -h --help        Show this screen.
  --version        Show version and exit.
  --ncdu PATH      Use the provided Ncdu binary as reference for some default values
                   (default: Ncdu is automatically recognised).
  --big-endian     Force the dumping of the internal default config used by Ncdu on
                   big-endian machines (default: depends on the Ncdu binary).
  --little-endian  Like --big-endian, but for little endian binaries.
  --with-darkbg    Force the dumping of the internal default config used by Ncdu >= 1.7.
  --without-darkbg Force the dumping of the internal default config used by Ncdu < 1.7.
  --compact        Disable the JSON indentation.
  --offset INT     Use the provided offset (it's binary-dependent - be careful).

How to use this software:
1. Use 'extract-default-config' to extract your config to a JSON file.
2. Make a backup of the mentioned JSON file.
3. Use your editor of choice to edit the *values* (also: DON'T edit "offset").
4. Use 'apply-config' to apply the new configuration file.
5. Done. Launch Ncdu. Or re-start from step 3 / 'revert' using step 2's backup.

Config keys and values:
- "ncdu" is the Path to the Ncdu binary and "offset" depends on it. Don't touch them.
- "off", "dark" and (optionally) "darkbg" are the themes' names.
- "fg" and "bg" support the colors: Black, Red, Green, Yellow, Blue, Magenta, Cyan, White.
- "a" supports the attributes: Standout, Underline, Reverse, Blink, Dim, Bold, Altcharset,
  Invisible, Protect, Horizontal, Left, Low, Right, Top, Vertical (concatenate with '+').
- The value "null" means default foreground color, background color or all attributes off.
- Colors and attributes are case-insensitive.

In case something goes very wrong:
  NcduColors does some checks before applying any new configuration file.
  However, something could still go wrong if you use this tool in the wrong way.
  In case something bad happens, please reinstall Ncdu using your package manager.

For more help: see https://gitlab.com/Midblyte/NcduColors.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT.
""".strip()


class Handlers:
    COMPACT_ARGS = {"indent": None, "separators": (",", ":")}
    EXPANDED_ARGS = {"indent": 4}

    @staticmethod
    def dump_internal_default_config(ncdu: NcduColors, compact: bool, config: TextIOWrapper, darkbg: Optional[bool] = None, byteorder: Optional[str] = None):
        internal_default_config = NcduColors.dump_internal_default_config(with_darkbg=darkbg or ncdu.supports_darkbg, byteorder=byteorder or ncdu.byteorder)

        kwargs = Handlers.COMPACT_ARGS if compact else Handlers.EXPANDED_ARGS

        isatty = config.isatty()

        with config as file:
            file.write(json.dumps(internal_default_config.as_dict(), **kwargs))

        if isatty:
            print("Config dumped successfully.")

    @staticmethod
    def extract_default_config(ncdu: NcduColors, compact: bool, config: TextIOWrapper):
        extracted_default_config = ncdu.extract_default_config()

        kwargs = Handlers.COMPACT_ARGS if compact else Handlers.EXPANDED_ARGS

        isatty = config.isatty()

        with config as file:
            file.write(json.dumps(extracted_default_config.as_dict(), **kwargs))

        if isatty:
            print("Config extracted successfully.")

    @staticmethod
    def apply_config(ncdu: NcduColors, config: TextIOWrapper):
        new_config = Config.from_buffer(config)

        if ncdu.apply_config(new_config=new_config):
            print("Config applied successfully.")
        else:
            print("Config is already applied.")

    @staticmethod
    def revert(ncdu: NcduColors, config: Optional[TextIOWrapper] = None, offset: Optional[int] = None):
        internal_default_config: Config = NcduColors.dump_internal_default_config(
            ncdu=ncdu.ncdu,
            offset=offset or Config.from_buffer(config).offset,
            with_darkbg=ncdu.supports_darkbg,
            byteorder=ncdu.byteorder
        )

        if ncdu.apply_config(new_config=internal_default_config):
            print("Ncdu defaults reverted successfully.")
        else:
            print("Ncdu has already been reverted to its defaults.")


def get_parser():
    parser = argparse.ArgumentParser(prog="ncducolors", usage="%(prog)s [--ncdu PATH] <action> [...]", add_help=False)
    parser.add_argument("--help", "-h", action="store_true", default=argparse.SUPPRESS, help="Show this help message and exit")
    parser.add_argument("--ncdu", type=Path, default=shutil.which("ncdu"), help="Path of Ncdu binary")
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {__version__}")

    subparser = parser.add_subparsers(title="action")

    dump_internal_default_config = subparser.add_parser(
        name="dump-internal-default-config",
        help="Dump this software's internal config. Usually, you shouldn't rely on this config"
    )
    dump_internal_default_config.set_defaults(handler=Handlers.dump_internal_default_config)
    dump_internal_default_config.add_argument("config", type=argparse.FileType("wt"), default=sys.stdout, help="Path of config file (JSON) where to save")
    dump_internal_default_config.add_argument("--compact", action="store_true", help="Don't indent the JSON file")
    dump_internal_default_config_type = dump_internal_default_config.add_mutually_exclusive_group(required=False)
    dump_internal_default_config_type.add_argument("--with-darkbg", dest="darkbg", action="store_true")
    dump_internal_default_config_type.add_argument("--without-darkbg", dest="darkbg", action="store_false")
    dump_internal_default_config_byteorder = dump_internal_default_config.add_mutually_exclusive_group(required=False)
    dump_internal_default_config_byteorder.add_argument("--little-endian", dest="byteorder", action="store_const", const="little")
    dump_internal_default_config_byteorder.add_argument("--big-endian", dest="byteorder", action="store_const", const="big")

    extract_default_config = subparser.add_parser(name="extract-default-config", help="Extract the original binary config converted to JSON")
    extract_default_config.set_defaults(handler=Handlers.extract_default_config)
    extract_default_config.add_argument("config", type=argparse.FileType("wt"), default=sys.stdout, help="Path of config file (JSON) where to extract")
    extract_default_config.add_argument("--compact", action="store_true", help="Don't indent the JSON file")

    apply_config = subparser.add_parser(name="apply-config", help="Apply an edited config")
    apply_config.set_defaults(handler=Handlers.apply_config)
    apply_config.add_argument("config", type=argparse.FileType("rt"), help="Path of config file (JSON) to apply")

    revert = subparser.add_parser(name="revert", help="Revert Ncdu as it was before being patched")
    revert.set_defaults(handler=Handlers.revert)
    revert_args = revert.add_mutually_exclusive_group(required=True)
    revert_args.add_argument("--config", type=argparse.FileType("rt"), help="Path of config file to load the offset from")
    revert_args.add_argument("--offset", type=int, help="Offset to Ncdu binary's colors config")

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    try:
        if args.ncdu is None:
            raise ValueError("Ncdu was not found.")

        if hasattr(args, "help") or not hasattr(args, "handler"):
            return print(HELP_MESSAGE)

        if (handler := getattr(args, "handler", None)) is not None:
            ncdu = NcduColors(ncdu=args.ncdu.expanduser())

            delattr(args, "ncdu")
            delattr(args, "handler")

            handler(ncdu=ncdu, **args.__dict__)
        else:
            parser.print_help()
    except Exception as exception:
        print(f"Error: {exception}", end="\n\n")

        parser.print_usage()

        exit(1)


if __name__ == "__main__":
    main()
