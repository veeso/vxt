from vxt.view.context import Context, Config
from vxt.audio.file_audio_source import FileAudioSource
from vxt.audio.track import Track
from vxt.audio.playlist import Playlist

import os.path

MOCK_AUDIO = FileAudioSource(os.path.join("assets", "audio", "benson.wav")).audio


def test_new_context():
    audio = FileAudioSource(os.path.join("assets", "audio", "benson.wav"))
    context = Context(Config(), audio)
    assert isinstance(context.config, Config)
    assert audio == context.source
    assert 0 == context.playlist.length
    assert 0 == context.cursor


def test_context_setters():
    audio = FileAudioSource(os.path.join("assets", "audio", "benson.wav"))
    context = Context(Config(), audio)
    context.cursor = 5
    assert 5 == context.cursor
    context.playlist = Playlist(
        [
            Track(MOCK_AUDIO, 0, "foo"),
            Track(MOCK_AUDIO, 1, "bar"),
            Track(MOCK_AUDIO, 2, "omar"),
        ]
    )
    assert 3 == context.playlist.length
