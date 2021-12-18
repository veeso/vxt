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

from pydub.audio_segment import AudioSegment
from pydub.effects import normalize
from .audio import Audio
from .error import AudioError
from .track import Track
from pydub.silence import split_on_silence
from typing import List, Optional


class AudioProcessor(object):
    """
    Audio processor provides method to manipulate and work with audio
    """

    def __init__(self) -> None:
        super().__init__()

    def split_by_silence(
        self,
        audio: Audio,
        min_silence_len: int,
        silence_threshold: int,
        keep_silence: int,
    ) -> List[Track]:
        """
        Split incoming audio by silence. Produces a list of `Track`.
        Raises an `AudioError` in case of error
        """
        try:
            chunks: List[AudioSegment] = split_on_silence(
                audio,
                min_silence_len=min_silence_len,
                silence_thresh=silence_threshold,
                keep_silence=keep_silence,
            )
            return list(map(lambda x: Track(x), chunks))
        except Exception as e:
            raise AudioError("Failed to split audio: %s" % e)

    def amplify(self, audio: Audio, dB: int) -> Audio:
        """Amplify audio by `dB`"""
        new_audio: AudioSegment = audio.audio + dB
        audio.set_audio(new_audio)
        return audio

    def normalize(self, audio: Audio) -> Audio:
        """Normalize audio"""
        new_audio: AudioSegment = normalize(audio.audio)
        audio.set_audio(new_audio)
        return audio

    def export(self, audio: Audio, path: str, format: Optional[str] = None) -> None:
        """
        Export audio to path. Format is deducted by the path, if not provided
        Raises `AudioError` on failure
        """
        try:
            audio.audio.export(path, format)
        except Exception as e:
            raise AudioError("Failed to export audio to %s: %s" % (path, e))
