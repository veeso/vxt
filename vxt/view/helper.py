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

# from PyInquirer i
from PyInquirer import prompt
from typing import List, Callable, Any, Optional, Union
from termcolor import colored

Validate = Callable[[str], Union[bool, str]]
Filter = Callable[[str], Any]


class ViewHelper(object):
    def __init__(self) -> None:
        super().__init__()

    def select(self, title: str, choices: List[str]) -> str:
        """Prompt user with a select"""
        questions = [
            {"type": "list", "name": "result", "message": title, "choices": choices},
        ]
        result = prompt(questions)["result"]
        return result

    def confirm(self, title: str) -> bool:
        """Prompt user with a confirm"""
        questions = [
            {"type": "confirm", "name": "result", "message": title},
        ]
        result = prompt(questions)["result"]
        return result

    def input(
        self,
        title: str,
        validate: Optional[Validate] = None,
        filter: Optional[Filter] = None,
    ) -> Any:
        """Ask for a value and validate"""
        questions = [
            {
                "type": "input",
                "name": "result",
                "message": title,
                "filter": filter,
                "validate": validate,
            },
        ]
        result = prompt(questions)["result"]
        return result

    def error(self, text: str) -> None:
        """Print error message"""
        print(colored(text, "red"))

    def info(self, text: str) -> None:
        """Print info message"""
        print(colored(text, "yellow"))
