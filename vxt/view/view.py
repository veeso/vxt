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
    RenameTracksTask,
    SplitSilenceTask,
    SplitTrackTask,
    ManualSpeechTask,
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
    TRACKS_LIST_MENU = 10
    PROMPT_EXIT = 11
    # 3rd step: show track operation menu
    TRACK_TASK_MENU = 20
    AMPLIFY_TRACK = 21
    DELETE_TRACK = 22
    NORMALIZE_TRACK = 23
    PLAY_TRACK = 24
    SET_TRACK_SPEECH = 25
    SPLIT_TRACK = 26
    GET_TRACK_SPEECH = 27
    # 4th step: export all tracks
    EXPORT_TRACKS = 30
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
            elif self.__state == State.TRACKS_LIST_MENU:
                self.__show_track_list_menu()
            elif self.__state == State.PROMPT_EXIT:
                self.__prompt_exit()
            elif self.__state == State.TRACK_TASK_MENU:
                self.__show_track_task_menu()
            elif self.__state == State.AMPLIFY_TRACK:
                self.__amplify_track()
            elif self.__state == State.GET_TRACK_SPEECH:
                self.__get_track_speech()
            elif self.__state == State.PLAY_TRACK:
                self.__play_track()
            elif self.__state == State.DELETE_TRACK:
                self.__delete_track()
            elif self.__state == State.NORMALIZE_TRACK:
                self.__normalize_track()
            elif self.__state == State.SET_TRACK_SPEECH:
                self.__set_track_speech()
            elif self.__state == State.SPLIT_TRACK:
                self.__split_track()
            elif self.__state == State.EXPORT_TRACKS:
                self.__export_tracks()
            else:
                raise NotImplementedError(self.__state)

    def __get_track_view_name(self) -> str:
        return "[%d] %.32s" % (
            self.__ctx.cursor,
            self.__ctx.playlist.get(self.__ctx.cursor).speech,
        )

    def __trackify_source(self) -> None:
        """Run trackify source state"""
        self.__vh.info("Preparing configuration to split audio by silence…")
        # ask for parameters
        user_input: Optional[int] = self.__vh.input(
            "Enter minimum silence (default 500ms): ",
            Validator.validate_optional_positive_number,
            Validator.filter_optional_number,
        )
        if user_input:
            self.__ctx.config.min_silence_len = user_input
        user_input = self.__vh.input(
            "Enter silence threshold (default -16dB): ",
            Validator.validate_optional_positive_number,
            Validator.filter_optional_number,
        )
        if user_input:
            self.__ctx.config.silence_threshold = user_input
        user_input = self.__vh.input(
            "Enter the amount of silence to keep at the end of each track (default 0): ",
            Validator.validate_optional_positive_number,
            Validator.filter_optional_number,
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
                    self.__vh.error("failed to get speech for track: %s" % e)
                    self.__state = State.EXIT
                    return
                spinner.ok("✔️")
        # set new state to `TRACKS_LIST_MENU`
        self.__state = State.TRACKS_LIST_MENU

    def __show_track_list_menu(self) -> None:
        """Show track list menu"""
        choices = ["export tracks", "exit VXT", "--------------------------------"]
        # make track list
        choices.extend(
            list(
                map(
                    lambda x: "%d: %.32s" % (x[0] + 1, x[1].speech),
                    enumerate(self.__ctx.playlist.iter()),
                )
            )
        )
        choice = self.__vh.select("Select the track to operate on", choices)
        index = choices.index(choice)
        if index == 0:
            self.__state = State.EXPORT_TRACKS
        elif index == 1:
            self.__state = State.PROMPT_EXIT
        elif index >= 3:
            # get track by index
            self.__ctx.cursor = index - 2  # NOTE: remove first 2 elements
            self.__state = State.TRACK_TASK_MENU

    def __prompt_exit(self) -> None:
        """Prompt user fo exit"""
        if self.__vh.confirm("Do you want to quit VXT? "):
            self.__state = State.EXIT
        else:
            self.__state = State.TRACKS_LIST_MENU

    def __show_track_task_menu(self) -> None:
        """Show track task menu"""
        choices = [
            "play audio",
            "get speech",
            "amplify audio",
            "delete track",
            "normalize audio",
            "set speech manually",
            "split track into two",
            "----------------------",
            "go back to the track list",
        ]
        choice = self.__vh.select(
            "What you want to do on track '%s'?" % self.__get_track_view_name(), choices
        )
        if choice == "play audio":
            self.__state = State.PLAY_TRACK
        elif choice == "get speech":
            self.__state = State.GET_TRACK_SPEECH
        elif choice == "amplify audio":
            self.__state = State.AMPLIFY_TRACK
        elif choice == "delete track":
            self.__state = State.DELETE_TRACK
        elif choice == "normalize audio":
            self.__state = State.NORMALIZE_TRACK
        elif choice == "split track into two":
            self.__state = State.SPLIT_TRACK
        elif choice == "set speech manually":
            self.__state = State.SET_TRACK_SPEECH
        elif choice == "go back to the track list":
            self.__state = State.TRACKS_LIST_MENU

    def __play_track(self) -> None:
        """Play current track"""
        task = TaskFactory.make(PlayTask, self.__ctx, CliArgs([], []))
        try:
            task.run()
        except Exception as e:
            self.__vh.error("Could not play track: %s" % e)
        self.__state = State.TRACK_TASK_MENU

    def __amplify_track(self) -> None:
        """Prompt user for options to amplify current track"""
        dB = self.__vh.input(
            "Amplification (dB): ", Validator.validate_number, Validator.filter_number
        )
        task = TaskFactory.make(AmplifyTask, self.__ctx, CliArgs(["dB"], [dB]))
        try:
            self.__ctx.playlist.replace(task.run(), self.__ctx.cursor)
            self.__vh.info("Track amplified by %d dB" % dB)
        except Exception as e:
            self.__vh.error("Failed to amplify track: %s" % e)
        self.__state = State.TRACK_TASK_MENU

    def __delete_track(self) -> None:
        """Prompt user wheter he wants to delete the selected track; in case of affermative answer, delete track"""
        if self.__vh.confirm("Are you sure you want to delete this track? "):
            task = TaskFactory.make(DeleteTrackTask, self.__ctx, CliArgs([], []))
            self.__ctx.playlist = task.run()
            self.__vh.info("Track deleted!")
            self.__state = State.TRACKS_LIST_MENU
        else:
            self.__state = State.TRACK_TASK_MENU

    def __normalize_track(self) -> None:
        """Normalize track audio"""
        task = TaskFactory.make(NormalizeTask, self.__ctx, CliArgs([], []))
        try:
            self.__ctx.playlist.replace(task.run(), self.__ctx.cursor)
            self.__vh.info("Normalized track audio")
        except Exception as e:
            self.__vh.error("Failed to normalize audio: %s" % e)
        self.__state = State.TRACK_TASK_MENU

    def __get_track_speech(self) -> None:
        """Get track speech"""
        self.__vh.info(self.__ctx.playlist.get(self.__ctx.cursor).speech)
        self.__state = State.TRACK_TASK_MENU

    def __set_track_speech(self) -> None:
        """Set track speech"""
        speech = self.__vh.input("Type track speech: ")
        task = TaskFactory.make(
            ManualSpeechTask, self.__ctx, CliArgs(["speech"], [speech])
        )
        self.__ctx.playlist.replace(task.run(), self.__ctx.cursor)
        self.__vh.info("Speech updated")
        self.__state = State.TRACK_TASK_MENU

    def __split_track(self) -> None:
        """Split track"""
        offset = self.__vh.input(
            "Type the offset where to cut the track (ms): ",
            Validator.validate_positive_number,
            Validator.filter_number,
        )
        task = TaskFactory.make(
            SplitTrackTask, self.__ctx, CliArgs(["offset"], [offset])
        )
        with yaspin(text="Splitting track…") as spinner:
            try:
                self.__ctx.playlist = task.run()
                spinner.ok("✔️")
            except Exception as e:
                spinner.fail("❌")
                self.__vh.error("failed to split track: %s" % e)
        self.__state = State.TRACK_TASK_MENU

    def __export_tracks(self) -> None:
        """Export tracks"""
        # prompt for output format
        self.__vh.info("To export tracks, you need to provide an output format:")
        self.__vh.info(
            "The syntax use parameters which must be preceeded by `%`, everything in between will be kept the same."
        )
        self.__vh.info("The following parameters are supported:")
        self.__vh.info("")
        self.__vh.info("- %%: print percentage symbol")
        self.__vh.info("- %d: current day")
        self.__vh.info("- %H: current hours")
        self.__vh.info("- %I: current timestamp ISO8601 syntax")
        self.__vh.info("- %M: current minutes")
        self.__vh.info("- %m: current month")
        self.__vh.info("- %S: current seconds")
        self.__vh.info("- %s: track speech")
        self.__vh.info("- %s.NUMBER track speech cut at length (e.g. `%s.24`)")
        self.__vh.info("- %t: track number in track list (from 1 to n)")
        self.__vh.info("- %y: current year with 2 digits")
        self.__vh.info("- %Y: current year with 4 digits")
        # get fmt
        fmt = self.__vh.input(
            "Output format (default: %s): " % self.__ctx.config.output_fmt,
            Validator.validate_track_output_fmt,
            Validator.filter_optional_string,
        )
        if fmt:
            self.__ctx.config.output_fmt = fmt
        # output dir
        if not self.__ctx.config.output_dir:
            self.__ctx.config.output_dir = self.__vh.input(
                "Output directory: ", Validator.validate_path
            )
        # rename tracks
        task = TaskFactory.make(RenameTracksTask, self.__ctx, CliArgs([], []))
        try:
            self.__ctx.playlist = task.run()
        except Exception as e:
            self.__vh.error("Failed to rename tracks: %s" % e)
            return
        # format
        audio_format = self.__vh.input(
            "Which audio format should be used when exporting the trcaks? "
        )
        # export tracks
        for i in range(0, self.__ctx.playlist.length):
            self.__ctx.cursor = i
            track = self.__ctx.playlist.get(i)
            with yaspin(
                text="Exporting track %d to %s/%s…"
                % (i + 1, self.__ctx.config.output_dir, track.slug)
            ) as spinner:
                try:
                    task = TaskFactory.make(
                        ExportTask, self.__ctx, CliArgs(["format"], [audio_format])
                    )
                    spinner.ok("✔️")
                except Exception as e:
                    spinner.fail("❌")
                    self.__vh.error("failed to export track: %s" % e)
                    return
        # return exit
        self.__vh.info("All tracks have been exported to %s" % self.__ctx.config.output_dir)
        # ask whether to quit
        self.__state = State.PROMPT_EXIT
