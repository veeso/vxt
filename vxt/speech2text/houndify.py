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

from ..audio.audio import Audio
from .engine import Speech2TextEngine
from io import BytesIO
import speech_recognition as sr
from typing import Optional


class HoundifySpeech2TextEngine(Speech2TextEngine):
    """A speech2text engine which uses the Houndify speech2text"""

    def __init__(self, client_id: str, client_key: str) -> None:
        super().__init__()
        self.__engine = sr.Recognizer()
        self.__client_id = client_id
        self.__client_key = client_key

    def get_speech(self, audio: Audio, language: str) -> Optional[str]:
        try:
            audio_data = BytesIO()
            audio.audio.export(audio_data, "wav")
            sr_audio = sr.AudioFile(audio_data)
            with sr_audio as source:
                audio_source = self.__engine.record(source)
                return self.__engine.recognize_houndify(
                    audio_source, self.__client_id, self.__client_key, show_all=False
                )
        except Exception:
            return None
