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

from vxt.audio.track import Track
from ..task import Task as ITask
from vxt.audio.playlist import Playlist
from vxt.audio.file_audio_source import FileAudioSource
from vxt.speech2text.engine import Speech2TextEngine

from pydub import AudioSegment
from tempfile import NamedTemporaryFile


class SplitTrackTask(ITask):
    """A task to split a certain track from playlist audio"""

    def __init__(
        self,
        playlist: Playlist,
        index: int,
        offset: int,
        engine: Speech2TextEngine,
        language: str,
    ) -> None:
        super().__init__()
        self.__playlist = playlist
        self.__index = index
        self.__offset = offset
        self.__engine = engine
        self.__language = language

    def run(self) -> Playlist:
        # get track
        track = self.__playlist.get(self.__index)
        # split into two
        chunk = track.audio[: self.__offset]
        pre_track = Track(self.__clone_audio(chunk), track.index, None)
        chunk = track.audio[self.__offset :]
        post_track = Track(self.__clone_audio(chunk), pre_track.index + 1, None)
        # get speech for "pre"
        pre_track.speech = self.__engine.get_speech(pre_track, self.__language)
        # get speech for "post"
        post_track.speech = self.__engine.get_speech(post_track, self.__language)
        # replace at index
        self.__playlist.replace(pre_track, self.__index)
        # add post to playlist
        self.__playlist.insert(post_track, self.__index + 1)
        return self.__playlist

    def __clone_audio(self, audio: AudioSegment) -> AudioSegment:
        temp = NamedTemporaryFile("wb+")
        audio.export(temp.name, "wav")
        cloned = FileAudioSource(temp.name)
        return cloned.audio
