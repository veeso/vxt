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

from .track import Track
from typing import Iterator, List


class Playlist(object):
    """Playlist represents a list of tracks"""

    def __init__(self, tracks: List[Track]) -> None:
        super().__init__()
        self.__tracks = tracks

    @property
    def length(self) -> int:
        """Get length of playlist"""
        return len(self.__tracks)

    def get(self, index: int) -> Track:
        """Get tracks at `i`"""
        return self.__tracks[index]

    def iter(self) -> Iterator[Track]:
        """Iter tracks"""
        return iter(self.__tracks)

    def remove(self, index: int) -> None:
        """Remove track at provided index."""
        # split list
        pre = self.__tracks[:index]
        post = self.__tracks[index + 1 :]
        # sub 1 to all tracks index
        for i, t in enumerate(post):
            t.index = t.index - 1
            post[i] = t
        self.__tracks = pre + post

    def insert(self, track: Track, index: int) -> None:
        """
        Insert `track` into playlist at the provided `index`.
        If index is less than zero or bigger than the length, the track is just pushed to the end of the list
        """
        track.index = index
        print(list(map(lambda x: x.slug, self.__tracks)))
        if index < 0 or index >= self.length:
            self.__tracks.append(track)
        else:
            pre = self.__tracks[:index]
            pre.append(track)
            post = self.__tracks[index:]
            # add 1 to all tracks index
            for i, t in enumerate(post):
                t.index = t.index + 1
                post[i] = t
            self.__tracks = pre + post

    def replace(self, track: Track, index: int) -> None:
        """Replace current track at `index` with provided `track`"""
        self.__tracks[index] = track
        self.__tracks[index].index = index

    def rename_track(self, name: str, index: int) -> None:
        """Rename track at `index` with `name`"""
        self.__tracks[index].set_name(name)
