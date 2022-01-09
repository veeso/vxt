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

from ..task import Task as ITask
from vxt.audio.track import Track
from vxt.audio.playlist import Playlist
from vxt.speech2text.engine import Speech2TextEngine
from vxt.view.helper import ViewHelper

from threading import Thread
from time import sleep
from typing import Dict, List, Optional
from yaspin import yaspin, Spinner

import traceback


class SpeechTask(ITask):
    """A task to get speech for the entire playlist"""

    def __init__(
        self, engine: Speech2TextEngine, playlist: Playlist, language: str
    ) -> None:
        super().__init__()
        self.__engine = engine
        self.__playlist = playlist
        self.__language = language

    def run(self) -> Playlist:
        try:
            return SpeechWorkerDispatcher(
                self.__engine, self.__playlist, self.__language, 16
            ).run()
        except Exception as e:
            traceback.print_exception(Exception, e, tb=None)


class SpeechWorkerDispatcher(object):
    """A dispatcher for speech worker"""

    def __init__(
        self,
        engine: Speech2TextEngine,
        playlist: Playlist,
        language: str,
        max_workers: int,
    ) -> None:
        super().__init__()
        self.__engine = engine
        self.__playlist = playlist
        self.__language = language
        self.__max_workers = max_workers
        self.__workers: List[Thread] = []
        self.__speech_dict: Dict[int, str] = {}
        self.__last_worker_started: int = -1

    def run(self) -> Playlist:
        """Run workers"""
        with yaspin(text="Getting audio speech for the playlist…") as spinner:
            while len(self.__speech_dict) < self.__playlist.length:
                for i in range(0, self.__max_workers):
                    self.__check_worker(i, spinner)
                sleep(0.1)
            spinner.ok("✔️")
        # make playlist
        for (key, value) in self.__speech_dict.items():
            self.__playlist.set_track_speech(value, key)
        return self.__playlist

    def __check_worker(self, index: int, spinner: Spinner) -> None:
        """
        Check worker at `index` status;
        if doesn't exist or has terminated, start a new one, if necessary
        """
        try:
            worker = self.__workers[index]
            # if thread has terminated, delete worker
            if not worker.is_alive():
                worker.join()
                self.__start_new_worker(index, spinner)
        except IndexError:
            # start a new worker
            self.__start_new_worker(index, spinner)

    def __start_new_worker(self, index: int, spinner: Spinner) -> None:
        """Start a new worker and put it in the list at `index`"""
        next_track = self.__next_track()
        if next_track is not None:
            self.__last_worker_started = next_track.index
            worker = Thread(
                target=SpeechWorker(
                    next_track, self.__engine, self.__language, self.__speech_dict
                ).run()
            )
            worker.start()
            self.__workers.insert(
                index,
                worker,
            )
            spinner.text = "Getting audio speech for the playlist (%d/%d)…" % (
                self.__last_worker_started,
                self.__playlist.length,
            )

    def __next_track(self) -> Optional[Track]:
        """Get the next track to work on in the worker"""
        return (
            None
            if self.__last_worker_started + 1 >= self.__playlist.length
            else self.__playlist.get(self.__last_worker_started + 1)
        )


class SpeechWorker(object):
    """A worker to get speech for a track"""

    def __init__(
        self,
        track: Track,
        engine: Speech2TextEngine,
        language: str,
        speech_dict: Dict[int, str],
    ) -> None:
        super().__init__()
        self.__track = track
        self.__engine = engine
        self.__language = language
        self.__speech_dict = speech_dict

    def run(self) -> None:
        try:
            speech = self.__engine.get_speech(self.__track, self.__language)
        except Exception as e:
            ViewHelper().error(
                "Failed to get speech for track %d: %s" % (self.__track.index, e)
            )
            speech = None
        self.__speech_dict[self.__track.index] = "" if speech is None else speech
