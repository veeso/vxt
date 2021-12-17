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

from .audio import Audio, AudioSegment


class AudioSource(Audio):
    """Defines a physical audio source, such as an audio file or a recording device"""

    def __init__(self, slug: str, audio: AudioSegment) -> None:
        """
        Initialize a new AudioSource.
        Slug is a string which identifies the audio source uniquely, such as a file path or a device,
        while audio is the AudioSegment containing the audio
        """
        super().__init__()
        self._audio = audio
        self._slug = slug

    @property
    def audio(self) -> AudioSegment:
        return self._audio

    @property
    def slug(self) -> str:
        return self._slug

    def set_audio(self, audio: AudioSegment) -> None:
        self._audio = audio
