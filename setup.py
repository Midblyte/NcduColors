#!/usr/bin/env python3
import re
from pathlib import Path

from setuptools import setup


with open("README.md", "r") as readme:
    long_description = readme.read()


# Get the version from ncducolors/__init__.py without actually importing the package
__version__ = eval(re.search(r'__version__.+(".+")$', (Path(__file__).with_name("ncducolors") / "__init__.py").read_text(), re.M).group(1))


setup(
    name="NcduColors",
    version=__version__,
    description="Ncdu themes patcher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Midblyte/NcduColors",
    author="Midblyte",
    author_email="ncducolors@midblyte.anonaddy.me",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities"
    ],
    keywords="ncdu themes",
    project_urls={
        "Source": "https://github.com/Midblyte/NcduColors",
        "Documentation": "https://github.com/Midblyte/NcduColors#how-to-use",
        "Tracker": "https://github.com/Midblyte/NcduColors/issues",
    },
    python_requires=">=3.8",
    packages=["ncducolors"],
    zip_safe=False,
    entry_points={"console_scripts": ["ncducolors = ncducolors.__main__:main"]}
)
