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

from ..context import Context
from .task import Task
from typing import Any, Type

# vxt
from vxt.audio.audio import Audio

# tasks
from .audio.amplify import AmplifyTask
from .audio.delete_track import DeleteTrackTask
from .audio.export import ExportTask
from .audio.normalize import NormalizeTask
from .audio.play import PlayTask
from .audio.rename_track import RenameTrackTask
from .audio.split_silence import SplitSilenceTask
from .audio.split_track import SplitTrackTask
from .speech2text.speech import SpeechTask


class TaskFactory(object):
    """A task factory"""

    @staticmethod
    def make(task: Type, ctx: Context, cli_args: CliArgs) -> Task:
        """Make a Task from class name and current context"""
        if task == AmplifyTask:
            return TaskFactory.__amplify_task(ctx, cli_args.get_as_int())

    @staticmethod
    def __amplify_task(ctx: Context, dB: int) -> AmplifyTask:
        audio = TaskFactory.__get_audio(ctx)
        return AmplifyTask(audio, dB)

    @staticmethod
    def __get_audio(ctx: Context) -> Audio:
        if ctx.playlist.length > 0:
            return ctx.playlist.get(ctx.cursor)
        else:
            # If playlist is empty, edit audio source
            return ctx.source
