from vxt.audio.file_audio_source import FileAudioSource
from vxt.audio.track import Track

import os.path

TEST_AUDIO_PATH = os.path.join("assets", "audio", "benson.wav")
MOCK_AUDIO = FileAudioSource(os.path.join("assets", "audio", "benson.wav")).audio
MOCK_AUDIO2 = FileAudioSource(os.path.join("assets", "audio", "hackerino.wav")).audio


def test_track():
    track = Track(MOCK_AUDIO, 10, "pippo")
    assert MOCK_AUDIO == track.audio
    assert 10 == track.index
    assert "pippo" == track.slug
    assert "" == track.speech


def test_set_speech():
    track = Track(MOCK_AUDIO, 10, "pippo")
    track.speech = "hi"
    assert "hi" == track.speech


def test_set_audio():
    track = Track(MOCK_AUDIO, 10, "pippo")
    track.set_audio(MOCK_AUDIO2)
    assert MOCK_AUDIO2 == track.audio
