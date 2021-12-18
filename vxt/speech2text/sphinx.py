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

from ..audio import Audio
from ..audio.processor import AudioProcessor
from .engine import Speech2TextEngine
from .error import Speech2TextError
from io import BytesIO
import speech_recognition as sr
from typing import Optional


class GoogleSpeech2TextEngine(Speech2TextEngine):
    """A speech2text engine which uses the Google API"""

    def __init__(
        self, keyword_entries: Optional[str], grammar_file: Optional[str]
    ) -> None:
        super().__init__()
        self.__engine = sr.Recognizer()
        self.__audio_proc = AudioProcessor()
        self.__keyword_entries = keyword_entries
        self.__grammar_file = grammar_file

    def get_speech(self, audio: Audio, language: str) -> Optional[str]:
        try:
            audio_data = BytesIO()
            audio.audio.export(audio_data, "wav")
            sr_audio = sr.AudioFile(audio_data)
            with sr_audio as source:
                audio_source = self.__engine.record(source)
                return self.__engine.recognize_sphinx(
                    audio_source, language, self.__keyword_entries, self.__grammar_file
                )
        except Exception as e:
            raise Speech2TextError("Speech recognition error: %s" % e)
