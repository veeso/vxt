from vxt.audio.file_audio_source import FileAudioSource
from vxt.audio.playlist import Playlist
from vxt.audio.track import Track

import os.path
import pytest

TEST_AUDIO_PATH = os.path.join("assets", "audio", "benson.wav")
MOCK_AUDIO = FileAudioSource(os.path.join("assets", "audio", "benson.wav")).audio
TEST_PLAYLIST = Playlist(
    [
        Track(MOCK_AUDIO, 0, "foo"),
        Track(MOCK_AUDIO, 1, "bar"),
        Track(MOCK_AUDIO, 2, "omar"),
    ]
)


def test_playlist_length():
    assert 3 == TEST_PLAYLIST.length


def test_playlist_get():
    assert "bar" == TEST_PLAYLIST.get(1).slug


def test_playlist_get_fails_out_of_bounds():
    with pytest.raises(Exception):
        TEST_PLAYLIST.get(40)


def test_playlist_iter():
    assert ["foo", "bar", "omar"] == list(map(lambda x: x.slug, TEST_PLAYLIST.iter()))


def test_playlist_remove():
    playlist = Playlist(
        [
            Track(MOCK_AUDIO, 0, "foo"),
            Track(MOCK_AUDIO, 1, "bar"),
            Track(MOCK_AUDIO, 2, "omar"),
        ]
    )
    playlist.remove(1)
    assert 2 == playlist.length
    assert "foo" == playlist.get(0).slug
    assert "omar" == playlist.get(1).slug


def test_playlist_insert():
    playlist = Playlist(
        [
            Track(MOCK_AUDIO, 0, "foo"),
            Track(MOCK_AUDIO, 1, "bar"),
            Track(MOCK_AUDIO, 2, "omar"),
        ]
    )
    playlist.insert(Track(MOCK_AUDIO, 0, "pippo"), 1)
    assert ["foo", "pippo", "bar", "omar"] == list(
        map(lambda x: x.slug, playlist.iter())
    )
    assert [0, 1, 2, 3] == list(map(lambda x: x.index, playlist.iter()))


def test_playlist_replace():
    playlist = Playlist(
        [
            Track(MOCK_AUDIO, 0, "foo"),
            Track(MOCK_AUDIO, 1, "bar"),
            Track(MOCK_AUDIO, 2, "omar"),
        ]
    )
    playlist.replace(Track(MOCK_AUDIO, 0, "pippo"), 1)
    assert ["foo", "pippo", "omar"] == list(map(lambda x: x.slug, playlist.iter()))
    assert [0, 1, 2] == list(map(lambda x: x.index, playlist.iter()))


def test_playlist_rename():
    playlist = Playlist(
        [
            Track(MOCK_AUDIO, 0, "foo"),
            Track(MOCK_AUDIO, 1, "bar"),
            Track(MOCK_AUDIO, 2, "omar"),
        ]
    )
    playlist.rename_track("pippo", 1)
    assert ["foo", "pippo", "omar"] == list(map(lambda x: x.slug, playlist.iter()))


def test_playlist_set_speech():
    playlist = Playlist(
        [
            Track(MOCK_AUDIO, 0, "foo"),
            Track(MOCK_AUDIO, 1, "bar"),
            Track(MOCK_AUDIO, 2, "omar"),
        ]
    )
    playlist.set_track_speech("hello", 1)
    assert "hello" == playlist.get(1).speech
