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

from .context import Context
from .helper import ViewHelper
from .args import CliArgs
from .task.factory import (
    TaskFactory,
    AmplifyTask,
    DeleteTrackTask,
    ExportTask,
    NormalizeTask,
    PlayTask,
    RenameTrackTask,
    SplitSilenceTask,
    SplitTrackTask,
    SpeechTask,
)


from enum import Enum


class State(Enum):
    """Current step in view state machine"""

    # 1st step; ask user parameters to split by silence, then split audio and get speech recognition
    TRACKIFY_SOURCE = 1
    # 2nd step: show the track menu; this step is recurring
    TRACKS_LIST_MENU = 2
    # 3rd step: show track operation menu
    TRACK_TASK_MENU = 3
    AMPLIFY_TRACK = 4
    DELETE_TRACK = 5
    NORMALIZE_TRACK = 6
    PLAY_TASK = 7
    RENAME_TRACK = 8
    SPLIT_TRACK = 9
    # 4th step: export all tracks
    EXPORT_TRACKS = 10
    # last step: exit
    EXIT = 255


class View(object):
    """View class defines the class that will run all of the task required to run vxt"""

    def __init__(self, ctx: Context) -> None:
        super().__init__()
        self.__ctx = ctx
        self.__state: State = State.TRACKIFY_SOURCE
        self.__vh: ViewHelper = ViewHelper()

    def run(self) -> None:
        """Run application"""
        while not self.__state == State.EXIT:
            if self.__state == State.TRACKIFY_SOURCE:
                self.__trackify_source()
            # TODO: match

    def __trackify_source(self) -> None:
        """Run trackify source state"""
        # TODO:
        # set new state to `TRACKS_LIST_MENU`
        self.__state = State.TRACKS_LIST_MENU


"""
questions = [
    {
        "type": "input",
        "name": "result",
        "message": "porcoddue",
        "validate": lambda x : True if x == "5" else "diocannone",
        "filter": lambda x : 10
    },
]
prompt(questions)
"""