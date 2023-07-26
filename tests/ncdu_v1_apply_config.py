import json
import os
import shutil
import sys
import unittest
import urllib.request
from pathlib import Path
from subprocess import run

from config import Config
from ncducolors import NcduColors


# Extracted from https://dev.yorhel.nl/ncdu/changes with query selector "li strong"
VERSIONS = (
    "1.14.2",
    "1.15",
    "1.15.1",
    "1.16",
    "1.17",
    "1.18",
    "1.18.1",

    # These versions do not support theming:
    # 0.1 0.2 0.3 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 1.10 1.11 1.12

    # We can safely skip these versions as they are obsolete and harder to compile; also, gcc-9 or older seems to be required:
    # 1.13 1.14 1.14.1
)


class NcduV1(unittest.TestCase):
    FILES = Path(__file__).parent / "files"
    ARCHIVES = FILES / "archives"
    SOURCES = FILES / "sources"

    def setUp(self):
        self.init_dirs()

        for version in VERSIONS:
            self.download_and_extract_version(version=version)

    def download_and_extract_version(self, version: str):
        destination = self.SOURCES / f"ncdu_{version}"

        if not destination.exists():
            path, http_message = urllib.request.urlretrieve(
                f"https://code.blicky.net/yorhel/ncdu/archive/v{version}.tar.gz",
                self.ARCHIVES / f"ncdu_{version}.tar.gz"
            )

            shutil.unpack_archive(path, destination, "gztar")

    def init_dirs(self):
        self.FILES.mkdir(exist_ok=True)
        self.ARCHIVES.mkdir(exist_ok=True)
        self.SOURCES.mkdir(exist_ok=True)

    @unittest.skipUnless(sys.platform == "linux", "requires Linux")
    def test_compile(self):
        for version in VERSIONS:
            with self.subTest(version=version):
                self.compile_version(version=version)

    def compile_version(self, version: str):
        root = self.SOURCES / f"ncdu_{version}" / "ncdu"
        os.chdir(root)

        if not (root / "ncdu").exists() and not (root / "src" / "ncdu").exists():
            autoreconf = run(["autoreconf", "-i", "-f"], capture_output=True)
            autoreconf.check_returncode()

            autoupdate = run(["autoupdate"], capture_output=True)
            autoupdate.check_returncode()

            configure = run(["./configure"], capture_output=True)
            configure.check_returncode()

            make = run(["make"], capture_output=True)
            make.check_returncode()

        if not (executable := root / "ncdu").exists() and not (executable := root / "src" / "ncdu").exists():
            self.fail("Executable doesn't seem to exist")

        ncdu_version = run([executable.absolute(), "-v"], capture_output=True)
        ncdu_version.check_returncode()

        self.assertEqual(ncdu_version.stdout.decode("utf-8").strip(), f"ncdu {version}")

    @unittest.skipUnless(sys.platform == "linux", "requires Linux")
    def test_patch(self):
        for version in VERSIONS:
            with self.subTest(version=version):
                self.patch_version(version=version)

    def patch_version(self, version: str):
        root = self.SOURCES / f"ncdu_{version}" / "ncdu"
        os.chdir(root)

        if not (executable := root / "ncdu").exists() and not (executable := root / "src" / "ncdu").exists():
            self.fail(f"Ncdu {version} doesn't exist")

        ncdu = NcduColors(ncdu=executable)

        ncdu.apply_config(
            Config.from_dict(
                json.loads(
                    (Path(__file__).parent.with_name("assets") / "examples" / "ncdu_yellow.json").read_text()
                )
            )
        )

        ncdu_version = run([executable, "--version"], capture_output=True).stdout.decode("utf-8").strip()

        self.assertEqual(
            ncdu_version,
            f"ncdu {version}",
            f"Ncdu version mismatch after patching ({ncdu_version!r} != {f'ncdu {version}'!r})"
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.FILES)
