from vxt.audio.file_audio_source import FileAudioSource
from vxt.audio.processor import AudioProcessor

import os.path
from tempfile import NamedTemporaryFile


def test_split_by_silence():
    audio = FileAudioSource(os.path.join("assets", "audio", "benson.wav"))
    processor = AudioProcessor()
    assert 13 == len(processor.split_by_silence(audio, 500, -29, 500))


def test_amplify():
    audio = FileAudioSource(os.path.join("assets", "audio", "benson.wav"))
    processor = AudioProcessor()
    processor.amplify(audio, 4)


def test_normalize():
    audio = FileAudioSource(os.path.join("assets", "audio", "benson.wav"))
    processor = AudioProcessor()
    processor.normalize(audio)


def test_export():
    temp = NamedTemporaryFile("wb+")
    audio = FileAudioSource(os.path.join("assets", "audio", "benson.wav"))
    processor = AudioProcessor()
    processor.export(audio, temp.name, "wav")
