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

from typing import List, Any


class Argument(object):
    """A single command line argument"""

    def __init__(self, arg: Any) -> None:
        super().__init__()
        self._value = arg

    def as_str(self) -> str:
        return str(self._value)

    def as_int(self) -> int:
        return int(self._value)

    def as_float(self) -> float:
        return float(self._value)


class FallbackArgument(Argument):
    def __init__(self, arg: Any) -> None:
        super().__init__(arg)

    def as_str(self) -> str:
        return self._value

    def as_int(self) -> Any:
        return self._value

    def as_float(self) -> float:
        return self._value


class CliArgs(object):
    """Command line arguments"""

    def __init__(self, keys: List[str], values: List[Any]) -> None:
        super().__init__()
        self.__args = {keys[i]: Argument(values[i]) for i in range(len(keys))}

    def get(self, key: str) -> Argument:
        """Get value with provided key"""
        value = self.__args.get(key)
        if value:
            return value
        else:
            raise KeyError(key)

    def get_or(self, key: str, default: Any) -> Argument:
        """Get value with provided key; if the value doesn't exist,
        will return an argument that will
        return the default value when tried to be accessed"""
        value = self.__args.get(key)
        if value:
            return value
        else:
            return FallbackArgument(default)
