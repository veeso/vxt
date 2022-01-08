from vxt.audio.file_audio_source import FileAudioSource
from vxt.audio.track import Track
from vxt.misc.track_fmt import TrackFmt

from datetime import datetime
import os.path

DEFAULT_TRACK = Track(
    FileAudioSource(os.path.join("assets", "audio", "benson.wav")).audio, 0, None
)


def test_percentage_symbol():
    fmt = TrackFmt("%%")
    assert "hello, %%" == fmt.fmt("hello, ", DEFAULT_TRACK)


def test_datetime_fmt():
    fmt = TrackFmt("%Y-%m-%d %H:%M:%S (%y) %I")
    assert datetime.now().astimezone().strftime(
        "%Y-%m-%d %H:%M:%S (%y) %Y-%m-%dT%H:%M:%S%z"
    ) == fmt.fmt("", DEFAULT_TRACK)


def test_name_fmt():
    fmt = TrackFmt("%s")
    track = DEFAULT_TRACK
    track.speech = "hello world!"
    assert "hello_world!" == fmt.fmt("", track)
    fmt = TrackFmt("%s.5")
    assert "hello" == fmt.fmt("", track)


def test_track_number_fmt():
    fmt = TrackFmt("%t")
    track = DEFAULT_TRACK
    track.index = 9  # NOTE: 0 to 1 index
    assert "10" == fmt.fmt("", track)
