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
from ..args import CliArgs
from .task import Task
from typing import Optional, Type

# vxt
from vxt.audio.audio import Audio

# tasks
from .audio.amplify import AmplifyTask
from .audio.delete_track import DeleteTrackTask
from .audio.export import ExportTask
from .audio.normalize import NormalizeTask
from .audio.play import PlayTask
from .audio.rename_track import RenameTracksTask
from .audio.split_silence import SplitSilenceTask
from .audio.split_track import SplitTrackTask
from .speech2text.manual import ManualSpeechTask
from .speech2text.speech import SpeechTask


class TaskFactory(object):
    """A task factory"""

    @staticmethod
    def make(task: Type[Task], ctx: Context, cli_args: CliArgs) -> Task:
        """Make a Task from class name and current context"""
        if task == AmplifyTask:
            return TaskFactory.__amplify_task(ctx, cli_args.get("dB").as_int())
        elif task == DeleteTrackTask:
            return TaskFactory.__delete_track_trask(ctx)
        elif task == ExportTask:
            return TaskFactory.__export_task(ctx, cli_args.get("format").as_str())
        elif task == NormalizeTask:
            return TaskFactory.__normalize_task(ctx)
        elif task == PlayTask:
            return TaskFactory.__play_task(ctx)
        elif task == RenameTracksTask:
            return TaskFactory.__rename_track_task(ctx)
        elif task == SplitSilenceTask:
            return TaskFactory.__split_silence_task(
                ctx,
                cli_args.get("min_silence_len").as_int(),
                cli_args.get("silence_threshold").as_int(),
                cli_args.get("keep_silence").as_int(),
            )
        elif task == SplitTrackTask:
            return TaskFactory.__split_track_task(ctx, cli_args.get("offset").as_int())
        elif task == SpeechTask:
            return TaskFactory.__speech_task(ctx)
        elif task == ManualSpeechTask:
            return TaskFactory.__manual_speech_task(
                ctx, cli_args.get("speech").as_str()
            )
        else:
            raise NotImplementedError

    @staticmethod
    def __amplify_task(ctx: Context, dB: int) -> AmplifyTask:
        return AmplifyTask(TaskFactory.__get_audio(ctx), dB)

    @staticmethod
    def __delete_track_trask(ctx: Context) -> DeleteTrackTask:
        return DeleteTrackTask(ctx.playlist, ctx.cursor)

    @staticmethod
    def __export_task(ctx: Context, format: Optional[str]) -> ExportTask:
        return ExportTask(TaskFactory.__get_audio(ctx), format, ctx.config.output_dir)

    @staticmethod
    def __normalize_task(ctx: Context) -> NormalizeTask:
        return NormalizeTask(TaskFactory.__get_audio(ctx))

    @staticmethod
    def __play_task(ctx: Context) -> NormalizeTask:
        return PlayTask(TaskFactory.__get_audio(ctx))

    @staticmethod
    def __rename_track_task(ctx: Context) -> RenameTracksTask:
        return RenameTracksTask(ctx.playlist, ctx.config.output_fmt)

    @staticmethod
    def __split_silence_task(
        ctx: Context, min_silence_len: int, silence_threshold: int, keep_silence: int
    ) -> SplitSilenceTask:
        return SplitSilenceTask(
            TaskFactory.__get_audio(ctx),
            min_silence_len,
            silence_threshold,
            keep_silence,
        )

    @staticmethod
    def __split_track_task(ctx: Context, offset: int) -> SplitTrackTask:
        return SplitTrackTask(
            ctx.playlist, ctx.cursor, offset, ctx.config.engine, ctx.config.language
        )

    @staticmethod
    def __speech_task(ctx: Context) -> SpeechTask:
        return SpeechTask(
            ctx.config.engine, TaskFactory.__get_audio(ctx), ctx.config.language
        )

    @staticmethod
    def __manual_speech_task(ctx: Context, speech: str) -> ManualSpeechTask:
        return ManualSpeechTask(TaskFactory.__get_audio(ctx), speech)

    @staticmethod
    def __get_audio(ctx: Context) -> Audio:
        if ctx.playlist.length > 0:
            return ctx.playlist.get(ctx.cursor)
        else:
            # If playlist is empty, edit audio source
            return ctx.source
