#!/usr/bin/python3

from setuptools import find_packages, setup
from pathlib import Path

# The directory containing this file
ROOT = Path(__file__).parent

README = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="vxt",
    version="0.1.1",
    description="A python CLI tool to extract voice sentences from audio files with speech recognition",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Christian Visintin",
    author_email="christian.visintin1997@gmail.com",
    url="https://github.com/veeso/vxt",
    license="MIT",
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[
        "click>=8",
        "pathlib2>=2",
        "inquirer>=2.8",
        "pydub>=0.25",
        "PyInquirer>=1.0.3",
        "SpeechRecognition>=3.8",
        "termcolor>=1",
        "yaspin>=2",
    ],
    entry_points={"console_scripts": ["attila = vxt.__main__:main"]},
    packages=find_packages(exclude=("tests",)),
    keywords=["Speech recognition", "voice extract", "audio voice", "split audio"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
