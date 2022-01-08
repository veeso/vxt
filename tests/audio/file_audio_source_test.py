from vxt.audio.file_audio_source import FileAudioSource, AudioSegment, AudioError
import os.path
import pytest

TEST_AUDIO_PATH = os.path.join("assets", "audio", "benson.wav")


def test_file_audio_source():
    source = FileAudioSource(TEST_AUDIO_PATH)
    assert TEST_AUDIO_PATH == source.slug
    assert isinstance(source.audio, AudioSegment)


def test_file_audio_source_with_bad_path():
    with pytest.raises(AudioError):
        FileAudioSource("omar.wav")
