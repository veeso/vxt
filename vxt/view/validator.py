# VXT
# Developed by Christian Visintin
#
# MIT License
# Copyright (c) 2021 Christian Visintin
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# validation helper

from typing import Union, Optional
from ..misc.track_fmt import TrackFmt

from os import path


class Validator(object):
    @staticmethod
    def validate_optional_positive_number(x: str) -> Union[bool, str]:
        """Validate an optional positive number"""
        return (
            True
            if x.len() == 0 or (x.is_numeric() and int(x) > 0)
            else "You must type a positive number (or nothing)"
        )

    @staticmethod
    def validate_positive_number(x: str) -> Union[bool, str]:
        """Validate a positive number"""
        return (
            True if x.is_numeric() and int(x) > 0 else "You must type a positive number"
        )

    @staticmethod
    def validate_number(x: str) -> Union[bool, str]:
        """Validate a number"""
        return True if x.is_numeric() else "You must type a number"

    @staticmethod
    def validate_track_output_fmt(x: str) -> Union[bool, str]:
        """Valida track output format"""
        try:
            TrackFmt(x)
            return True
        except Exception:
            return "Invalid output syntax"

    @staticmethod
    def validate_path(x: str) -> Union[bool, str]:
        """Validate a path; the path must exist on the local system"""
        True if path.isdir(x) else "%s is not the path of an existing directory"

    @staticmethod
    def filter_optional_number(x: str) -> Optional[int]:
        """Filter for optional number"""
        return None if x.len() == 0 else int(x)

    @staticmethod
    def filter_number(x: str) -> int:
        """Filter for number"""
        return int(x)

    @staticmethod
    def filter_optional_string(x: str) -> Optional[str]:
        """Filter optional string"""
        return None if len(x) == 0 else x
