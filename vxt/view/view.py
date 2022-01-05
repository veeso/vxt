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

from ..audio.playlist import Playlist
from .args import CliArgs
from .context import Context
from .helper import ViewHelper
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
from .validator import Validator


from enum import Enum
from typing import Optional
from yaspin import yaspin


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
        self.__vh.info("Preparing configuration to split audio by silence…")
        # ask for parameters
        user_input: Optional[int] = self.__vh.input(
            "Enter minimum silence (default 500ms): ",
            Validator.validate_optional_positive_number,
            Validator.filter_optional_positive_number,
        )
        if user_input:
            self.__ctx.config.min_silence_len = user_input
        user_input = self.__vh.input(
            "Enter silence threshold (default -16dB): ",
            Validator.validate_optional_positive_number,
            Validator.filter_optional_positive_number,
        )
        if user_input:
            self.__ctx.config.silence_threshold = user_input
        user_input = self.__vh.input(
            "Enter the amount of silence to keep at the end of each track (default 0): ",
            Validator.validate_optional_positive_number,
            Validator.filter_optional_positive_number,
        )
        if user_input:
            self.__ctx.config.keep_silence = user_input
        # let's make cli args for task
        args = CliArgs(
            ["min_silence_len", "silence_threshold", "keep_silence"],
            [
                self.__ctx.config.min_silence_len,
                self.__ctx.config.silence_threshold,
                self.__ctx.config.keep_silence,
            ],
        )
        task = TaskFactory.make(SplitSilenceTask, self.__ctx, args)
        with yaspin(text="Splitting audio into tracks…") as spinner:
            try:
                self.__ctx.playlist = Playlist(task.run())
                spinner.ok("✔️")
            except Exception as e:
                spinner.fail("❌")
                self.__vh.error("failed to split audio source: %s" % e)
                self.__state = State.EXIT
                return
        # get speech for tracks
        for i in range(0, self.__ctx.playlist.length):
            with yaspin(
                text="Getting speech for tracks (%d/%d)"
                % (i + 1, self.__ctx.playlist.length)
            ) as spinner:
                task = SpeechTask(
                    self.__ctx.config.engine,
                    self.__ctx.playlist.get(i),
                    self.__ctx.config.language,
                )
                # Try to get speech for track
                try:
                    self.__ctx.playlist.replace(task.run(), i)
                except Exception as e:
                    spinner.fail("❌")
                    self.__vh.error("failed to split audio source: %s" % e)
                    self.__state = State.EXIT
                    return
                spinner.ok("✔️")
        # set new state to `TRACKS_LIST_MENU`
        self.__state = State.TRACKS_LIST_MENU
