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

from abc import ABCMeta, abstractmethod
from pydub import AudioSegment


class Audio(object):
    """Audio interface provides method which must be implemented by different Audio types"""

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def audio(self) -> AudioSegment:
        """Return audio segment"""
        raise NotImplementedError

    @property
    @abstractmethod
    def slug(self) -> str:
        """Return the slug which identify the audio"""
        raise NotImplementedError

    @abstractmethod
    def set_audio(self, audio: AudioSegment) -> None:
        """Set the audio segment for audio entity"""
        raise NotImplementedError
