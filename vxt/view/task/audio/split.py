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
from vxt.audio.audio import Audio
from vxt.audio.track import Track
from vxt.audio.processor import AudioProcessor
from typing import List


class SplitTask(ITask):
    """A task to split audio by silence into tracks"""

    def __init__(
        self,
        audio: Audio,
        min_silence_len: int,
        silence_threshold: int,
        keep_silence: int,
    ) -> None:
        super().__init__()
        self.__audio = audio
        self.__min_silence_len = min_silence_len
        self.__silence_threshold = silence_threshold
        self.__keep_silence = keep_silence

    def run(self) -> List[Track]:
        return AudioProcessor().split_by_silence(
            self.__audio,
            self.__min_silence_len,
            self.__silence_threshold,
            self.__keep_silence,
        )
