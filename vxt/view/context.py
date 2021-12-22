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

from .config import Config
from vxt.audio.audio_source import AudioSource
from vxt.audio.playlist import Playlist


class Context(object):
    """Application context"""

    def __init__(self, config: Config, source: AudioSource) -> None:
        super().__init__()
        # Init context
        self.__config: Config = config
        self.__source: AudioSource = source
        # runtime params
        self.__playlist: Playlist = Playlist([])
        self.__track_cursor: int = 0

    @property
    def config(self) -> Config:
        return self.__config

    @property
    def source(self) -> AudioSource:
        return self.__source

    # -- runtime props

    @property
    def playlist(self) -> Playlist:
        return self.__playlist

    @playlist.setter
    def playlist(self, p: Playlist):
        self.__playlist = p

    @property
    def cursor(self) -> int:
        return self.__track_cursor

    def cursor_up(self):
        """Move track cursor up"""
        if self.cursor + 1 < self.playlist.length:
            self.__track_cursor += 1

    def cursor_down(self):
        """Move track cursor down"""
        if self.cursor > 0:
            self.__track_cursor -= 1
